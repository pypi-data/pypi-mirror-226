from pathlib import Path
from typing import Tuple, Union

import numpy as np
from numpy import ndarray
from PIL import Image

from f2f.core.exceptions import FaceNotFoundError
from f2f.core.onnx import BaseONNX
from f2f.detection.s3fd.onnx import S3FDONNX
from f2f.detection.scrfd.onnx import SCRFDONNX
from f2f.utils import get_onnx_cache_dir

ONNX_PATH = Path(get_onnx_cache_dir()) / "synthetic_resnet50d.onnx"


class FDSyntheticLandmark2dONNX(BaseONNX):
    # fmt: off
    flip_parts: Tuple[Tuple[int, int], ...] = (
        (0, 16), (1, 15), (2, 14), (3, 13), (4, 12), (5, 11), (6, 10), (7, 9),
        (17, 26), (18, 25), (19, 24), (20, 23), (21, 22),
        (31, 35), (32, 34),
        (36, 45), (37, 44), (38, 43), (39, 42), (40, 47), (41, 46),
        (48, 54), (49, 53), (50, 52), (61, 63), (60, 64), (67, 65), (58, 56), (59, 55)
    )
    # fmt: on
    resolution: int = 256

    def __init__(
        self,
        detect_model_name: str = "scrfd",
        detect_threshold: float = 0.5,
        detect_max_faces: int = 10,
        detect_at_least_one: bool = False,
        min_face_size: int = 50,
        onnx_path: str = str(ONNX_PATH),
        device: Union[str, int] = "cpu",
    ) -> None:
        self.detect_model_name = detect_model_name.lower()
        self.detect_threshold = detect_threshold
        self.detect_max_faces = detect_max_faces
        self.detect_at_least_one = detect_at_least_one
        if self.detect_model_name == "s3fd":
            if self.detect_at_least_one:
                threshold = 0.0
            else:
                threshold = self.detect_threshold
            self.detect_model = S3FDONNX(threshold=threshold, device=device)
        elif self.detect_model_name == "scrfd":
            self.detect_model = SCRFDONNX(
                min_face_size=min_face_size, device=device
            )
        super().__init__(onnx_path, device)

    def to(self, device: Union[str, int]) -> "FDSyntheticLandmark2dONNX":
        super().to(device)
        self.detect_model.to(device)
        return self

    def scrfd_detect(
        self, input: Union[ndarray, Image.Image]
    ) -> Tuple[ndarray, ndarray]:
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

    def s3fd_detect(self, input: Union[ndarray, Image.Image]) -> ndarray:
        """
        Args:
            input: (H, W, 3) RGB image in range [0, 255]
        Rreturns:
           bboxes: (F, 5) bounding boxes where F is the number of faces
        """
        bboxes = self.detect_model(input)
        if bboxes is None:
            raise FaceNotFoundError(f"Face not found in image")
        return bboxes[: self.detect_max_faces]

    def single_landmarks(
        self,
        input: Union[ndarray, Image.Image],
        bboxes: ndarray,
        use_flip: bool = False,
    ) -> ndarray:
        """
        Args:
            input: (H, W, 3) RGB image in range [0, 255]
            bboxes: (F, 5) bounding boxes where F is the number of faces
            use_flip: whether to use flip augmentation
        Returns:
            (F, 68, 2) landmarks in range [-1, 1] where F is the number of faces
        """
        if isinstance(input, ndarray):
            input = Image.fromarray(input.astype(np.uint8))

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
            crop = input.crop((L_crop, T_crop, R_crop, B_crop))
            # This use PIL resize not torch, the result is slightly different with torch version
            resized = crop.resize(
                (self.resolution, self.resolution), Image.Resampling.LANCZOS
            ).convert("RGB")
            session_input = (
                np.array(resized, dtype=np.float32).transpose(2, 0, 1)[None]
                / 255.0
            )
            face_landmarks = self.session_run(session_input)[0].reshape(
                -1, 68, 2
            )
            if use_flip:
                flip_input = np.flip(session_input, axis=-1)
                flip_landmarks = self.session_run(flip_input)[0].reshape(
                    -1, 68, 2
                )
                face_landmarks = (
                    face_landmarks + self.flip_landmark(flip_landmarks)
                ) / 2
            face_landmarks = (face_landmarks + 1) * crop_size / 2
            face_landmarks[..., 0] = face_landmarks[..., 0] + L_crop
            face_landmarks[..., 1] = face_landmarks[..., 1] + T_crop
            landmarks.append(face_landmarks)
        return np.concatenate(landmarks, axis=0)

    def flip_landmark(self, landmark: ndarray) -> ndarray:
        """
        Args:
            landmark: (N, 68, 2) landmarks in range [-1, 1]
        Returns:
            (N, 68, 2) landmarks in range [-1, 1]
        """
        landmark[..., 0] *= -1
        s, t = zip(*self.flip_parts)
        temp = landmark[:, t].copy()
        landmark[:, t] = landmark[:, s]
        landmark[:, s] = temp
        return landmark

    def __call__(
        self, input: Union[ndarray, Image.Image], use_flip: bool = False
    ) -> Tuple[ndarray, ndarray]:
        """
        Args:
            input: (H, W, 3), RGB image in range [0, 255] or PIL.Image
            use_flip: whether to use flip augmentation
        Returns:
            bboxes: (F, 5) bounding boxes where F is the number of faces
            landmarks: (F, 68, 2) landmarks where F is the number of faces
        """
        if self.detect_model_name == "s3fd":
            bboxes = self.s3fd_detect(input)
        elif self.detect_model_name == "scrfd":
            bboxes, lm5s = self.scrfd_detect(input)
        landmarks = self.single_landmarks(input, bboxes, use_flip)
        return bboxes, landmarks
