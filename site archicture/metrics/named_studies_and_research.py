"""

Metric 02 : Named Studies & Research


Purpose:
--------
Checks whether the document references named studies,
research papers, surveys, reports, universities or
well-known organizations.

Author : Mayank

"""

import re
from utils.base_metric import BaseMetric


class NamedStudiesResearchMetric(BaseMetric):

    def __init__(self):

        # Keywords representing studies or reports
        self.study_keywords = [
            "study",
            "survey",
            "report",
            "research",
            "whitepaper",
            "paper",
            "analysis",
            "benchmark",
            "case study"
        ]

        # Citation phrases
        self.citation_phrases = [
            "according to",
            "published by",
            "conducted by",
            "reported by",
            "research from",
            "study by",
            "survey by"
        ]

        # Common trusted organizations
        self.organizations = [

            "google",
            "microsoft",
            "amazon",
            "aws",
            "gartner",
            "forrester",
            "stanford",
            "harvard",
            "mit",
            "ibm",
            "oracle",
            "openai",
            "meta",
            "accenture",
            "deloitte",
            "mckinsey",
            "world bank",
            "who",
            "unesco",
            "nasa"

        ]

        self.year_pattern = r"\b(19\d{2}|20\d{2}|21\d{2})\b"

    

    def calculate(self, text: str, html: str = None) -> dict:

        lower_text = text.lower()

        study_count = 0
        citation_count = 0
        organization_count = 0

        # Count study keywords
        for word in self.study_keywords:
            study_count += lower_text.count(word)

        # Count citation phrases
        for phrase in self.citation_phrases:
            citation_count += lower_text.count(phrase)

        # Count organizations
        for org in self.organizations:
            organization_count += lower_text.count(org)

        # Detect publication years
        years = re.findall(self.year_pattern, text)

        
        # Score Calculation
        

        score = 0

        score += min(study_count, 6) * 5

        score += min(organization_count, 6) * 5

        score += min(citation_count, 4) * 5

        score += min(len(years), 4) * 5

        score = min(score, 100)

        

        if score >= 80:

            remarks = "Excellent use of credible studies."

        elif score >= 60:

            remarks = "Good research references."

        elif score >= 40:

            remarks = "Average supporting references."

        else:

            remarks = "Very few named studies found."

        details = {
    "study_keywords": study_count,
    "citation_phrases": citation_count,
    "organizations": organization_count,
    "publication_years": len(years),
}

        return self.build_result(
    metric_name="Named Studies & Research",
    score=score,
    details=details,
    remarks=remarks,
)



# Standalone Testing


if __name__ == "__main__":

    sample_text = """
    According to the 2025 Gartner Report,
    Microsoft Research found that cloud adoption
    increased significantly.

    A Stanford University study also supports
    these findings.

    The survey was conducted by Deloitte.
    """

    metric = NamedStudiesResearchMetric()

    result = metric.calculate(sample_text)

    print(result)

from utils.webpage_parser import fetch_webpage_content


def check_named_studies_and_research(context):

    url = context.get("url", "")

    page = fetch_webpage_content(url)

    metric = NamedStudiesResearchMetric()

    return metric.calculate(
    text=page["text"],
    html=page["html"]
)