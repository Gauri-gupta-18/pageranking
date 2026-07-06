"""
Factor 66: Title Tag Check

Checks the title tag of a webpage.

Analyzes:
1. Presence of the title tag
2. Title text
3. Title length
4. Whether the title length is SEO-friendly (50–60 characters)
"""

import requests
from bs4 import BeautifulSoup


def check_title_tag(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "66 - Title Tag Check",
        "checked_url": url,
        "title_found": False,
        "title_text": "",
        "title_length": 0,
        "is_length_optimal": False,
        "metric_passed": False,
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

        title = soup.title

        if title and title.string:

            title_text = title.string.strip()

            result["title_found"] = True
            result["title_text"] = title_text

            title_length = len(title_text)

            result["title_length"] = title_length

            if 50 <= title_length <= 60:

                result["is_length_optimal"] = True
                result["metric_passed"] = True

                result["recommendation"] = (
                    "Title length is SEO-friendly."
                )

            elif title_length < 50:

                result["recommendation"] = (
                    "Title is too short. "
                    "Aim for 50–60 characters."
                )

            else:

                result["recommendation"] = (
                    "Title is too long. "
                    "Keep it between 50–60 characters."
                )

        else:

            result["recommendation"] = (
                "No title tag found."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result
