"""
preprocess.py

Provides preprocessing utilities for OCR input images.
Includes grayscale conversion, noise removal, thresholding, and resizing.

Dependencies:
- OpenCV (cv2)
- numpy
"""

import cv2
import numpy as np
from typing import Union, Optional

class ImagePreprocessor:
    """
    Class for preprocessing images before OCR.
    """

    def __init__(self, resize_width: Optional[int] = None):
        """
        Args:
            resize_width (int or None): Resize image to a fixed width (optional).
        """
        self.resize_width = resize_width

    def load_image(self, image_input: Union[str, np.ndarray]) -> np.ndarray:
        """
        Load image from path or return array directly.

        Args:
            image_input (str or np.ndarray): Path to image or image array.

        Returns:
            np.ndarray: Loaded image in BGR format.
        """
        if isinstance(image_input, str):
            img = cv2.imread(image_input)
            if img is None:
                raise FileNotFoundError(f"Image not found: {image_input}")
            return img
        return image_input

    def preprocess(self, image_input: Union[str, np.ndarray]) -> np.ndarray:
        """
        Apply full preprocessing pipeline: grayscale, denoise, threshold, resize.

        Args:
            image_input (str or np.ndarray): Image path or image array.

        Returns:
            np.ndarray: Preprocessed binary image ready for OCR.
        """
        img = self.load_image(image_input)

        # Optional resize
        if self.resize_width:
            img = self._resize(img, width=self.resize_width)

        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Denoising
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive Thresholding (better for variable lighting)
        binary = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )

        return binary

    def _resize(self, image: np.ndarray, width: int) -> np.ndarray:
        """
        Resize image to fixed width while keeping aspect ratio.

        Args:
            image (np.ndarray): Input image
            width (int): Target width

        Returns:
            np.ndarray: Resized image
        """
        h, w = image.shape[:2]
        ratio = width / w
        new_height = int(h * ratio)
        return cv2.resize(image, (width, new_height), interpolation=cv2.INTER_AREA)
