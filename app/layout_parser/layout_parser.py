"""
layout_parser.py

This module defines a parameterized layout parser for extracting custom
key-value pairs from OCR text using regular expressions.
"""

import re
from typing import Dict, List, Optional, Tuple


class LayoutParser:
    """
    Parameterized layout parser to extract structured information
    (like invoice number, date, total, etc.) using regex rules.
    """

    def __init__(self, field_patterns: Optional[Dict[str, List[str]]] = None):
        """
        Initialize the parser with optional field patterns.

        Args:
            field_patterns (dict): A dictionary where keys are field names
                                   and values are lists of regex patterns.
        """
        self.field_patterns = field_patterns or {
            "invoice_number": [
                r"Invoice\s*No[:\-]?\s*([A-Z0-9\-]+)",
                r"Inv\s*#[:\-]?\s*([A-Z0-9\-]+)"
            ],
            "date": [
                r"Date[:\-]?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
                r"(\d{2,4}[-/]\d{1,2}[-/]\d{1,4})"
            ],
            "total": [
                r"Total\s*Amount[:\-]?\s*\$?([\d,]+\.\d{2})",
                r"Grand\s*Total[:\-]?\s*\$?([\d,]+\.\d{2})",
                r"Total[:\-]?\s*\$?([\d,]+\.\d{2})"
            ]
        }

    def extract_fields(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract fields from OCR text based on configured regex patterns.

        Args:
            text (str): Raw OCR text.

        Returns:
            dict: Extracted key-value pairs.
        """
        results = {}
        for field_name, patterns in self.field_patterns.items():
            value = self._extract_by_patterns(text, patterns)
            results[field_name] = value
        return results

    def _extract_by_patterns(self, text: str, patterns: List[str]) -> Optional[str]:
        """
        Try multiple patterns to extract a single field.

        Args:
            text (str): The input text.
            patterns (List[str]): List of regex patterns.

        Returns:
            str or None: The first matched value or None.
        """
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:  # If two parts: e.g., "38" and "68"
                    return f"{match.group(1).replace(',', '').strip()}.{match.group(2).strip()}"
                return match.group(1).strip()
        return None

    def add_field(self, field_name: str, patterns: List[str]):
        """
        Dynamically add or update field extraction patterns.

        Args:
            field_name (str): Name of the field to extract.
            patterns (List[str]): List of regex patterns for this field.
        """
        self.field_patterns[field_name] = patterns
