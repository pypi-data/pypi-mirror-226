import os
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple, Union

import numpy as np
import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms.functional_tensor as TFT
from numpy import ndarray
from torch import Tensor

from f2f.core.exceptions import FaceNotFoundError
from f2f.detection.s3fd.onnx import S3FDONNX
from f2f.detection.scrfd.onnx import SCRFDONNX
from f2f.utils import get_onnx_cache_dir
from f2f.utils.onnx_ops import OnnxExport

CHECKPOINT_PATH = (
    Path(__file__).parents[2]
    / "assets"
    / "landmark"
    / "synthetic_resnet50d.ckpt"
)


@OnnxExport()
def onnx_export() -> None:
    model = SyntheticLandmark2dInference()
    input = torch.randn(1, 3, 256, 256)
    print(f"Exporting {model._get_name()} ONNX...")
    print(f"Use Input: {input.size()}")
    torch.onnx.export(
        model,
        input,
        str(Path(get_onnx_cache_dir()) / "synthetic_resnet50d.onnx"),
        opset_version=13,
        input_names=["input"],
        output_names=["landmark"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "landmark": {0: "batch_size"},
        },
    )


class SyntheticLandmark2d(nn.Module):
    resolution: int = 256

    def __init__(self, checkpoint: Optional[str] = None) -> None:
        super().__init__()
        self.backbone = timm.create_model("resnet50d", num_classes=68 * 2)

        if checkpoint is not None:
            if not os.path.exists(checkpoint):
                raise FileNotFoundError(f"Checkpoint {checkpoint} not found")
            self.load_state_dict(
                torch.load(checkpoint, map_location="cpu")["state_dict"]
            )

    def assert_resolution(self, input: Tensor) -> None:
        if (
            input.size(-2) != self.resolution
            or input.size(-1) != self.resolution
        ):
            raise ValueError(
                f"Expected input size ({self.resolution}, {self.resolution}), "
                f"got {input.size(-2)}, {input.size(-1)}"
            )

    def forward(self, input: Tensor) -> Tensor:
        """
        Args:
            input: (N, 3, 256, 256) RGB image in range [-1, 1]
        """
        self.assert_resolution(input)
        return self.backbone(input).view(-1, 68, 2)


class SyntheticLandmark2dInference(SyntheticLandmark2d):
    # fmt: off
    flip_parts: Tuple[Tuple[int, int], ...] = (
        (0, 16), (1, 15), (2, 14), (3, 13), (4, 12), (5, 11), (6, 10), (7, 9),
        (17, 26), (18, 25), (19, 24), (20, 23), (21, 22),
        (31, 35), (32, 34),
        (36, 45), (37, 44), (38, 43), (39, 42), (40, 47), (41, 46),
        (48, 54), (49, 53), (50, 52), (61, 63), (60, 64), (67, 65), (58, 56), (59, 55)
    )
    # fmt: on

    def __init__(self) -> None:
        super().__init__(str(CHECKPOINT_PATH))
        self.eval()
        self.requires_grad_(False)

    def train(self, mode: bool = True) -> None:
        return super().train(False)

    @torch.no_grad()
    def flip_forward(self, input: Tensor) -> Tensor:
        output: Tensor = self.backbone(input.flip(dims=(-1,))).view(-1, 68, 2)
        output[..., 0] *= -1
        s, t = zip(*self.flip_parts)
        temp = output[:, t].clone()
        output[:, t] = output[:, s]
        output[:, s] = temp
        return output

    @torch.no_grad()
    def forward(self, input: Tensor, use_flip: bool = False) -> Tensor:
        """
        Args:
            input: (N, 3, 256, 256) bbox aligned RGB image in range [-1, 1]
            use_flip: whether to use flip augmentation
        Returns:
            (N, 68, 2) landmarks in range [-1, 1]
        """
        self.assert_resolution(input)
        output: Tensor = self.backbone(input).view(-1, 68, 2)
        if use_flip:
            output = (output + self.flip_forward(input)) / 2
        return output


class FDSyntheticLandmark2dInference(SyntheticLandmark2dInference):
    def __init__(
        self,
        detect_model_name: str = "scrfd",
        detect_threshold: float = 0.5,
        detect_max_faces: int = 10,
        device: Optional[Union[str, int, torch.device]] = None,
    ) -> None:
        super().__init__()
        self.detect_model_name = detect_model_name
        self.detect_threshold = detect_threshold
        self.detect_max_faces = detect_max_faces
        self.device = torch.device(device or "cpu")

        if self.detect_model_name == "s3fd":
            self.detect_model = S3FDONNX(threshold=self.detect_threshold)
        elif self.detect_model_name == "scrfd":
            self.detect_model = SCRFDONNX(threshold=self.detect_threshold)

    def _apply(
        self, fn: Callable[..., Any]
    ) -> "FDSyntheticLandmark2dInference":
        if "t" in fn.__code__.co_varnames:
            with torch.no_grad():
                null_tensor = torch.empty(0).to(device=self.device)
                device = getattr(fn(null_tensor), "device", "cpu")
            self.device = torch.device(device)
            self.scrfd.to(str(self.device))
        return super()._apply(fn)

    @torch.no_grad()
    def forward(
        self, input: Tensor, use_flip: bool = False
    ) -> Tuple[List[ndarray], List[Tensor]]:
        """
        Args:
            input: (N, 3, H, W) RGB image in range [-1, 1]
            use_flip: whether to use flip augmentation
        Returns:
            bboxes: list of (F, 5) bboxes in range [0, 1] where F is the number of faces of each image
            landmarks: list of (F, 68, 2) landmarks in range [-1, 1] where F is the number of faces of each image
        """
        N = input.size(0)
        np_input = input.cpu().permute(0, 2, 3, 1).mul(127.5).add(127.5).numpy()
        batch_bboxes = []
        batch_landmarks = []
        for i in range(N):
            try:
                if self.detect_model_name == "scrfd":
                    bboxes, lm5s = self.scrfd_detect(np_input[i])
                elif self.detect_model_name == "s3fd":
                    bboxes = self.s3fd_detect(np_input[i])
            except FaceNotFoundError as e:
                raise FaceNotFoundError(
                    f"Failed to detect face in image {i}"
                ) from e
            batch_bboxes.append(bboxes)
            batch_landmarks.append(
                self.single_landmarks(input[i], bboxes, use_flip)
            )
        return batch_bboxes, batch_landmarks

    def scrfd_detect(self, input: ndarray) -> Tuple[ndarray, ndarray]:
        """
        Args:
            input: (H, W, 3) RGB image in range [0, 255]
        Returns:
            bboxes: (F, 5) bounding boxes where F is the number of faces
            keypoints: (F, 5, 2) 5 landmarks where F is the number of faces
        """
        bboxes, lm5s = self.detect_model(input)
        matched_bboxes = []
        matched_lm5s = []
        for bbox, lm5 in zip(bboxes, lm5s):
            if bbox[-1] > self.detect_threshold:
                matched_bboxes.append(bbox)
                matched_lm5s.append(lm5)
            if len(matched_bboxes) >= self.detect_max_faces:
                break
        if len(matched_bboxes) == 0:
            if self.detect_at_least_one:
                matched_bboxes = bboxes[:1]
                matched_lm5s = lm5s[:1]
            else:
                raise FaceNotFoundError(f"Face not found in image")
        matched_bboxes = np.array(matched_bboxes, dtype=np.float32)
        matched_lm5s = np.array(matched_lm5s, dtype=np.float32)
        return matched_bboxes, matched_lm5s

    def s3fd_detect(self, input: ndarray) -> ndarray:
        """
        Args:
            input: (H, W, 3) RGB image in range [0, 255]
        Rreturns:
           bboxes: (F, 5) bounding boxes where F is the number of faces
        """
        bboxes = self.detect_model(input)
        if bboxes is None:
            raise FaceNotFoundError(f"Face not found in image")
        return bboxes

    def single_landmarks(
        self, input: Tensor, bboxes: ndarray, use_flip: bool = False
    ) -> Tensor:
        """
        Args:
            input: (3, H, W) RGB image in range [-1, 1]
            bboxes: (F, 5) bounding boxes where F is the number of faces
            use_flip: whether to use flip augmentation
        Returns:
            (F, 68, 2) landmarks in range [-1, 1] where F is the number of faces
        """
        H, W = input.size(-2), input.size(-1)

        landmarks = []
        for bbox in bboxes:
            L, T, R, B, score = bbox
            bbox_W = R - L
            bbox_H = B - T

            W_center = (L + R) / 2
            H_center = (T + B) / 2
            crop_size = max(bbox_W, bbox_H) * 1.5

            L_crop = int(W_center - crop_size / 2)
            T_crop = int(H_center - crop_size / 2)
            R_crop = int(W_center + crop_size / 2)
            B_crop = int(H_center + crop_size / 2)
            crop = F.pad(input, (-L_crop, R_crop - W, -T_crop, B_crop - H))
            # This use torch resize not PIL, the result is slightly different with onnx version
            resized = TFT.resize(
                crop.unsqueeze(0),
                (self.resolution, self.resolution),
                antialias=True,
            )
            face_landmarks = self.backbone(resized).view(-1, 68, 2)
            if use_flip:
                face_landmarks = (
                    face_landmarks + self.flip_forward(resized)
                ) / 2
            face_landmarks = (face_landmarks + 1) * crop_size / 2
            face_landmarks[..., 0] = face_landmarks[..., 0] + L_crop
            face_landmarks[..., 1] = face_landmarks[..., 1] + T_crop
            landmarks.append(face_landmarks)
        return torch.cat(landmarks, dim=0)
