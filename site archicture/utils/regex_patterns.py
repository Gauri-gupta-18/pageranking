"""
------------------------------------------------------------
Common Regular Expressions
------------------------------------------------------------
"""

NUMBER_PATTERN = r"\b\d+(?:,\d{3})*(?:\.\d+)?\b"

PERCENTAGE_PATTERN = r"\b\d+(?:\.\d+)?%"

YEAR_PATTERN = r"\b(19\d{2}|20\d{2}|21\d{2})\b"

DATE_PATTERN = (
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
)

URL_PATTERN = r"https?://[^\s]+"

EMAIL_PATTERN = (
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)

CURRENCY_PATTERN = (
    r"(?:₹|\$|€|£)\s?\d+(?:,\d{3})*(?:\.\d+)?"
)

MEASUREMENT_PATTERN = (
    r"\b\d+(?:\.\d+)?\s?"
    r"(GB|MB|TB|KB|kg|g|km|m|cm|mm|ms|s|hrs|hours|minutes)\b"
)