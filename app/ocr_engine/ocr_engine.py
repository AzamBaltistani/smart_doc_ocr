"""
ocr_engine.py

This module defines a class-based OCR engine for extracting text from images.
Currently supports Tesseract-based OCR with optional bounding box extraction.

Dependencies:
- pytesseract
- PIL or OpenCV image as input (numpy array or path)
"""

import pytesseract
import cv2
import numpy as np
from typing import Union, List, Dict, Optional

class OCREngine:
    """
    Optical Character Recognition (OCR) engine using Tesseract.
    Supports plain text extraction and structured text with bounding boxes.
    """

    def __init__(self, lang: str = "eng", config: Optional[str] = None):
        """
        Initialize the OCR engine.

        Args:
            lang (str): Language for OCR (default: 'eng').
            config (str): Optional Tesseract configuration string.
        """
        self.lang = lang
        self.config = config if config else "--oem 3 --psm 6"

    def _load_image(self, image: Union[str, np.ndarray]) -> np.ndarray:
        """
        Load and convert the image if a path is given.

        Args:
            image (Union[str, np.ndarray]): Image path or OpenCV image.

        Returns:
            np.ndarray: Loaded OpenCV image in BGR format.
        """
        if isinstance(image, str):
            image = cv2.imread(image)
            if image is None:
                raise FileNotFoundError(f"Image not found: {image}")
        return image

    def extract_text(self, image: Union[str, np.ndarray]) -> str:
        """
        Perform OCR and return the raw extracted text.

        Args:
            image (str or np.ndarray): Path or image array.

        Returns:
            str: Extracted text as a string.
        """
        image = self._load_image(image)
        text = pytesseract.image_to_string(image, lang=self.lang, config=self.config)
        return text

    def extract_with_boxes(self, image: Union[str, np.ndarray]) -> List[Dict]:
        """
        Perform OCR and return text with bounding box information.

        Args:
            image (str or np.ndarray): Path or image array.

        Returns:
            List[Dict]: List of dictionaries containing text and bounding box.
        """
        image = self._load_image(image)
        data = pytesseract.image_to_data(image, lang=self.lang, config=self.config, output_type=pytesseract.Output.DICT)

        results = []
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            if data['text'][i].strip():
                results.append({
                    "text": data['text'][i],
                    "conf": int(data['conf'][i]),
                    "box": {
                        "x": int(data['left'][i]),
                        "y": int(data['top'][i]),
                        "w": int(data['width'][i]),
                        "h": int(data['height'][i]),
                    }
                })
        return results
