"""
------------------------------------------------------------
Text Utility Functions
------------------------------------------------------------

Purpose:
--------
Provides reusable text processing functions used across
multiple evaluation metrics.

Author : Mayank
------------------------------------------------------------
"""

import re
from typing import List


def clean_text(text: str) -> str:
    """
    Removes extra spaces and trims leading/trailing whitespace.
    """
    return re.sub(r"\s+", " ", text).strip()


def normalize_text(text: str) -> str:
    """
    Converts text to lowercase after cleaning.
    """
    return clean_text(text).lower()


def split_sentences(text: str) -> List[str]:
    """
    Splits text into individual sentences.
    """
    sentences = re.split(r"[.!?]+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def tokenize(text: str) -> List[str]:
    """
    Splits text into words.
    """
    return re.findall(r"\b[\w'-]+\b", text.lower())


def count_words(text: str) -> int:
    """
    Returns total number of words.
    """
    return len(tokenize(text))