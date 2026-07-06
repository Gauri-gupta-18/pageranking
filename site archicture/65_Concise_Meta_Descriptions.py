"""
Factor 65: Concise Meta Descriptions

Checks a website's meta description tag.

Analyzes:
1. Presence of meta description tag
2. Whether the description is empty
3. Description length
4. Whether the length is SEO-friendly (120–160 characters)
5. Recommendation for improvement
"""

import requests
from bs4 import BeautifulSoup


def check_concise_meta_descriptions(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "65 - Concise Meta Descriptions",
        "meta_description_found": False,
        "description": "",
        "description_length": 0,
        "seo_friendly": False,
        "recommendation": "",
        "status": "Failed"
    }

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 SEO Analyzer Bot"
            },
            timeout=10
        )

        if response.status_code != 200:

            result["error"] = (
                f"Status code {response.status_code}"
            )

            return result

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        meta_tag = soup.find(
            "meta",
            attrs={"name": lambda value: value and value.lower() == "description"}
        )

        if meta_tag is None:

            result["recommendation"] = (
                "Add a meta description tag to the page."
            )

            result["status"] = "Success"

            return result

        description = meta_tag.get(
            "content",
            ""
        ).strip()

        result["meta_description_found"] = True
        result["description"] = description

        description_length = len(description)

        result["description_length"] = description_length

        if description_length == 0:

            result["recommendation"] = (
                "Meta description is empty."
            )

        elif 120 <= description_length <= 160:

            result["seo_friendly"] = True

            result["recommendation"] = (
                "Meta description length is SEO-friendly."
            )

        elif description_length < 120:

            result["recommendation"] = (
                "Meta description is too short. "
                "Aim for 120–160 characters."
            )

        else:

            result["recommendation"] = (
                "Meta description is too long. "
                "Keep it between 120–160 characters."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result
