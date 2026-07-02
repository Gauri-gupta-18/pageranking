"""
------------------------------------------------------------
Base Metric Class
------------------------------------------------------------

Purpose:
--------
Provides common helper methods that every metric can reuse.

Author : Mayank
------------------------------------------------------------
"""

import re

from utils.text_utils import normalize_text
from utils.scoring import clamp_score


class BaseMetric:
    """
    Parent class for every evaluation metric.
    """

    def normalize(self, text: str) -> str:
        """
        Returns normalized lowercase text.
        """

        return normalize_text(text)

    def count_keywords(
        self,
        text: str,
        keywords: list
    ) -> int:
        """
        Counts occurrences of keywords.
        """

        text = self.normalize(text)

        total = 0

        for keyword in keywords:
            total += text.count(keyword.lower())

        return total

    def count_regex_matches(
        self,
        pattern: str,
        text: str
    ) -> int:
        """
        Counts regex matches.
        """

        return len(re.findall(pattern, text))

    def build_result(
        self,
        metric_name: str,
        score: int,
        details: dict,
        remarks: str
    ) -> dict:
        """
        Returns a standardized metric response.
        """

        return {

            "factor": metric_name,

            "metric": metric_name,

            "score": clamp_score(score),

            "max_score": 100,

            "details": details,

            "remarks": remarks

        }