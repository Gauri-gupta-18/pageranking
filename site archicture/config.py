"""
------------------------------------------------------------
Configuration File
------------------------------------------------------------

Purpose:
--------
Stores all configurable values used across the Content
Evaluation Framework.

Changing values here automatically affects all metrics.

Author : Mayank
------------------------------------------------------------
"""

# ==========================================================
# General Configuration
# ==========================================================

MAX_METRIC_SCORE = 100

# ==========================================================
# Default Weights
# ==========================================================

DEFAULT_WEIGHTS = {

    "number": 2,

    "percentage": 5,

    "currency": 5,

    "year": 5,

    "measurement": 5,

    "keyword": 3,

    "organization": 5,

    "citation": 5,

    "quotable_sentence": 15

}

# ==========================================================
# Maximum Count Considered
# (Prevents documents with excessive matches
# from getting unfairly high scores.)
# ==========================================================

MAX_COUNTS = {

    "numbers": 10,

    "percentages": 3,

    "currency": 3,

    "years": 3,

    "measurements": 4,

    "keywords": 5,

    "organizations": 6,

    "citations": 4,

    "quotable_sentences": 5

}

# ==========================================================
# Score Thresholds
# ==========================================================

EXCELLENT_SCORE = 80
GOOD_SCORE = 60
AVERAGE_SCORE = 40