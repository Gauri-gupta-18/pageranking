"""

Metric 05 : Expert Quotes


Purpose:
--------
Detects whether the document contains quotes or
statements attributed to named experts.

Author : Mayank

"""

import re

from utils.base_metric import BaseMetric

from utils.keyword_library import (
    EXPERT_TITLES,
    QUOTE_INDICATORS
)

from utils.scoring import (
    weighted_score,
    get_remark
)


class ExpertQuotesMetric(BaseMetric):

    def calculate(self, text: str, html: str = None) -> dict:

        
        # Step 1 : Normalize
        

        normalized_text = self.normalize(text)

        
        # Step 2 : Extract Features
        

        title_count = self.count_keywords(
            normalized_text,
            EXPERT_TITLES
        )

        quote_indicator_count = self.count_keywords(
            normalized_text,
            QUOTE_INDICATORS
        )

        quotation_marks = len(
            re.findall(r'"(.*?)"', text)
        )

        
        # Step 3 : Score
        

        score = 0

        score += weighted_score(
            title_count,
            4,
            10
        )

        score += weighted_score(
            quote_indicator_count,
            4,
            10
        )

        score += weighted_score(
            quotation_marks,
            3,
            20
        )

        # Bonus
        if (
            quotation_marks > 0
            and quote_indicator_count > 0
        ):
            score += 20

        
        # Step 4 : Result
        

        details = {

            "expert_titles": title_count,

            "quote_indicators": quote_indicator_count,

            "quoted_statements": quotation_marks

        }

        remarks = get_remark(score)

        return self.build_result(

            metric_name="Expert Quotes",

            score=score,

            details=details,

            remarks=remarks

        )


if __name__ == "__main__":

    sample_text = """

    According to Dr. Andrew Ng,

    "AI is the new electricity."

    Gartner states that cloud adoption
    continues to grow.

    """

    metric = ExpertQuotesMetric()

    print(metric.calculate(sample_text))

from utils.webpage_parser import fetch_webpage_content


def check_expert_quotes(context):

    url = context.get("url", "")

    page = fetch_webpage_content(url)

    metric = ExpertQuotesMetric()

    return metric.calculate(
    text=page["text"],
    html=page["html"]
)