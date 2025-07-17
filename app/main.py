"""
main.py

FastAPI backend to extract structured information from scanned documents or receipts.
"""

import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from typing import Dict

from ocr_engine import OCREngine
from preprocess import ImagePreprocessor
from layout_parser import LayoutParser

import cv2
from pdf2image import convert_from_bytes
import numpy as np


# Initialize components
ocr_engine = OCREngine()
preprocessor = ImagePreprocessor(resize_width=800)

receipt_patterns = {
    "id": [
        r"#(\d+)",                        # Matches #12345
        r"Receipt\s*[:\-]?\s*#?(\d+)"     # Matches "Receipt: #9876"
    ],
    "date": [
        r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",         # Matches 15/07/2025 or 07-15-25
        r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})"            # Matches 2025-07-15
    ],
    "total": [
        r"TOTAL\s*[:\-]?\s*\$?\s*([\d,]+)\s*[.,]\s*(\d{2})",
        r"total\s*[:\-]?\s*\$?\s*([\d,]+)\s*[.,]\s*(\d{2})",
        r"Total\s*Amount\s*[:\-]?\s*\$?\s*([\d,]+)\s*[.,]\s*(\d{2})",
        r"Total.*?\$?\s*([\d,]+)[.,]\s*(\d{2})"
    ],
    "change": [
        r"Change\s*Due\s*[:\-]?\s*\$?([\d,]+\.\d{2})",
        r"Change\s*[:\-]?\s*\$?([\d,]+\.\d{2})",
        r"change\s*[:\-]?\s*\$?([\d,]+\.\d{2})"
    ]
}
parser = LayoutParser(field_patterns=receipt_patterns)

# FastAPI App
app = FastAPI(
    title="Smart Document OCR API",
    description="Extract structured fields from uploaded receipts or documents.",
    version="1.0.1"
)

def read_image(file: UploadFile) -> np.ndarray:
    """
    Reads uploaded file (image or PDF) and returns a numpy image array.

    Args:
        file (UploadFile): Uploaded file

    Returns:
        np.ndarray: OpenCV image
    """
    try:
        if file.filename.lower().endswith(".pdf"):
            # Convert first page of PDF to image
            pages = convert_from_bytes(file.file.read(), dpi=300)
            if not pages:
                raise ValueError("PDF is empty or unreadable")
            img = np.array(pages[0])
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            # Save temp file and read with OpenCV
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                shutil.copyfileobj(file.file, temp_file)
                img = cv2.imread(temp_file.name)
            if img is None:
                raise ValueError("Invalid image format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return img


@app.post("/extract")
async def extract(file: UploadFile = File(...)) -> Dict:
    """
    Endpoint to extract structured fields from a document/receipt image.

    Request:
        - UploadFile (.jpg/.png/.pdf)

    Response:
        - JSON with extracted fields
    """
    try:
        image = read_image(file)
        preprocessed = preprocessor.preprocess(image)
        text = ocr_engine.extract_text(preprocessed)
        fields = parser.extract_fields(text)

        return JSONResponse(content={
            "filename": file.filename,
            "fields": fields,
            "raw_text": text
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {e}")
