"""
--
Metric 03 : Quotable Insights
--

Purpose:
--------
Detects short, standalone and meaningful sentences that
can easily be quoted by LLMs.

Author : Mayank
--
"""

import re

from utils.base_metric import BaseMetric


class QuotableInsightsMetric(BaseMetric):

    def __init__(self):

        # Words that generally make a sentence stronger
        self.strong_words = [

            "always",
            "never",
            "best",
            "worst",
            "important",
            "critical",
            "essential",
            "key",
            "must",
            "should",
            "avoid",
            "improve",
            "increase",
            "reduce",
            "optimize",
            "security",
            "performance",
            "quality",
            "automation",
            "scalable"

        ]

  

    def calculate(self, text: str, html: str = None) -> dict:

        # Split document into sentences
        sentences = re.split(r'[.!?]+', text)

        quotable_sentences = []

        strong_word_count = 0

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            words = sentence.split()

            # Only consider short sentences
            if len(words) <= 25:

                # Check if sentence contains at least one strong word
                contains_strong = False

                for word in self.strong_words:

                    if word.lower() in sentence.lower():

                        contains_strong = True
                        strong_word_count += 1
                        break

                if contains_strong:
                    quotable_sentences.append(sentence)

        
        # Score Calculation
        

        score = 0

        score += min(len(quotable_sentences), 5) * 15

        score += min(strong_word_count, 5) * 5

        if len(quotable_sentences) >= 3:
            score += 25

        score = min(score, 100)

        

        if score >= 80:

            remarks = "Excellent quotable content."

        elif score >= 60:

            remarks = "Good number of quotable insights."

        elif score >= 40:

            remarks = "Average quotable content."

        else:

            remarks = "Very few quotable insights."

        #Return Result

        details = {

    "quotable_sentences": len(quotable_sentences),

    "strong_word_matches": strong_word_count

}

        return self.build_result(

    metric_name="Quotable Insights",

    score=score,

    details=details,

    remarks=remarks,

)



# Standalone Testing


if __name__ == "__main__":

    sample_text = """

    Quality is better than quantity.

    Security should never be optional.

    Every API must fail gracefully.

    Automation improves developer productivity.

    Cloud-native applications are scalable.

    """

    metric = QuotableInsightsMetric()

    result = metric.calculate(sample_text)

    print(result) 

from utils.webpage_parser import fetch_webpage_content


def check_quotable_insights(context):

    url = context.get("url", "")

    page = fetch_webpage_content(url)

    metric = QuotableInsightsMetric()

    return metric.calculate(
    text=page["text"],
    html=page["html"]
)