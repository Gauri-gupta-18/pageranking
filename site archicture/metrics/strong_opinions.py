"""

Metric 04 : Strong Opinions & Hot Takes


Purpose:
--------
Evaluates whether a document contains strong,
clear and defensible opinions instead of generic
descriptions.

Author : Mayank

"""

from utils.base_metric import BaseMetric
from utils.keyword_library import (
    STRONG_OPINION_WORDS,
    COMPARISON_PHRASES,
    RECOMMENDATION_PHRASES
)
from utils.scoring import weighted_score, get_remark


class StrongOpinionsMetric(BaseMetric):

    def calculate(self, text: str, html: str = None) -> dict:

        
        # Step 1 : Normalize Text
        

        normalized_text = self.normalize(text)

        
        # Step 2 : Extract Features
        

        opinion_count = self.count_keywords(
            normalized_text,
            STRONG_OPINION_WORDS
        )

        comparison_count = self.count_keywords(
            normalized_text,
            COMPARISON_PHRASES
        )

        recommendation_count = self.count_keywords(
            normalized_text,
            RECOMMENDATION_PHRASES
        )

        
        # Step 3 : Calculate Score
        

        score = 0

        score += weighted_score(
            opinion_count,
            5,
            5
        )

        score += weighted_score(
            comparison_count,
            4,
            5
        )

        score += weighted_score(
            recommendation_count,
            4,
            5
        )

        # Bonus for balanced opinionated content
        if (
            opinion_count >= 3
            and comparison_count >= 1
        ):
            score += 15

        
        # Step 4 : Build Result
        

        details = {

            "opinion_words": opinion_count,

            "comparison_phrases": comparison_count,

            "recommendation_phrases": recommendation_count

        }

        remarks = get_remark(score)

        return self.build_result(

            metric_name="Strong Opinions & Hot Takes",

            score=score,

            details=details,

            remarks=remarks

        )


# 
# Standalone Testing
# 

if __name__ == "__main__":

    sample_text = """

    We strongly recommend using Infrastructure as Code.

    Kubernetes is better than manually managing containers.

    Every production application should have monitoring.

    Serverless should never be used for long-running workloads.

    """

    metric = StrongOpinionsMetric()

    result = metric.calculate(sample_text)

    print(result) 

from utils.webpage_parser import fetch_webpage_content


def check_strong_opinions(context):

    url = context.get("url", "")

    page = fetch_webpage_content(url)

    metric = StrongOpinionsMetric()

    return metric.calculate(
    text=page["text"],
    html=page["html"]
)