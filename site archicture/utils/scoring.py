"""
------------------------------------------------------------
Scoring Utility Functions
------------------------------------------------------------

Purpose:
--------
Provides common scoring methods shared by all metrics.

Author : Mayank
------------------------------------------------------------
"""

from config import MAX_METRIC_SCORE


def weighted_score(
    count: int,
    max_count: int,
    weight: int
) -> int:
    """
    Calculates weighted score with a maximum cap.
    """

    return min(count, max_count) * weight


def clamp_score(score: int) -> int:
    """
    Ensures score stays between 0 and MAX_METRIC_SCORE.
    """

    return max(0, min(score, MAX_METRIC_SCORE))


def get_remark(score: int) -> str:
    """
    Converts numeric score into qualitative feedback.
    """

    if score >= 80:
        return "Excellent"

    if score >= 60:
        return "Good"

    if score >= 40:
        return "Average"

    return "Needs Improvement"