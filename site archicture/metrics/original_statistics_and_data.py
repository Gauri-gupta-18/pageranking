"""

Metric 01 : Original Statistics & Data


Purpose:
--------
Detects whether a document contains numerical and statistical
information that makes it more valuable for AI retrieval,
citation and RAG systems.

Author : Mayank

"""

import re

from utils.base_metric import BaseMetric


class OriginalStatisticsMetric(BaseMetric):
    """
    Evaluates statistical richness of a document.
    """

    def __init__(self):

        # Regular expressions used throughout the metric

        self.number_pattern = r"\b\d+(?:,\d{3})*(?:\.\d+)?\b"

        self.percentage_pattern = r"\b\d+(?:\.\d+)?%"

        self.currency_pattern = (
            r"(?:₹|\$|€|£)\s?\d+(?:,\d{3})*(?:\.\d+)?"
        )

        self.year_pattern = r"\b(19\d{2}|20\d{2}|21\d{2})\b"

        self.measurement_pattern = (
            r"\b\d+(?:\.\d+)?\s?"
            r"(GB|MB|TB|KB|kg|g|mg|km|m|cm|mm|ms|s|hrs|hours|minutes|%)\b"
        )

        self.statistical_keywords = [
            "average",
            "median",
            "mean",
            "growth",
            "increase",
            "decrease",
            "variance",
            "distribution",
            "sample",
            "survey",
            "dataset",
            "statistics",
            "ratio",
            "percentage"
        ]

   

    def calculate(self, text: str, html: str = None) -> dict:
        """
        Calculates the Original Statistics score.

        Parameters
        ----------
        text : str
            Input document.

        Returns
        -------
        dict
            Metric result.
        """

        # Convert to lowercase for keyword search

        lower_text = text.lower()

        
        # Find all patterns
        

        numbers = re.findall(self.number_pattern, text)

        percentages = re.findall(self.percentage_pattern, text)

        currency = re.findall(self.currency_pattern, text)

        years = re.findall(self.year_pattern, text)

        measurements = re.findall(self.measurement_pattern, text)

        keyword_count = 0

        for word in self.statistical_keywords:

            keyword_count += lower_text.count(word)

        
        # Score Calculation
        

        score = 0

        score += min(len(numbers), 10) * 2

        score += min(len(percentages), 3) * 5

        score += min(len(currency), 3) * 5

        score += min(len(years), 3) * 5

        score += min(len(measurements), 4) * 5

        score += min(keyword_count, 5) * 3

        score = min(score, 100)

        
        # Remarks
        

        if score >= 80:

            remarks = "Excellent statistical content."

        elif score >= 60:

            remarks = "Good use of numerical information."

        elif score >= 40:

            remarks = "Average statistical evidence."

        else:

            remarks = "Very little statistical information."

        
        # Return Result
        

        details = {
            "numbers": len(numbers),
            "percentages": len(percentages),
            "currency": len(currency),
            "years": len(years),
            "measurements": len(measurements),
            "statistical_keywords": keyword_count,
        }

        return self.build_result(
            metric_name="Original Statistics & Data",
            score=score,
            details=details,
            remarks=remarks,
        )


# Standalone Testing

if __name__ == "__main__":

    sample_text = """
    Microsoft reported a 25% increase in cloud revenue during 2025.

    Azure Storage reached 512 GB capacity.

    Average latency was 23 ms.

    The service cost was $450.

    According to the survey,
    the dataset contained 15,000 records.
    """

    metric = OriginalStatisticsMetric()

    result = metric.calculate(sample_text)

    print(result)
  
from utils.webpage_parser import fetch_webpage_content


def check_original_statistics(context):

    url = context.get("url", "")

    page = fetch_webpage_content(url)

    metric = OriginalStatisticsMetric()

    return metric.calculate(
    text=page["text"],
    html=page["html"]
)