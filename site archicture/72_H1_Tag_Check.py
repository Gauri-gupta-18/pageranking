"""
Factor 72: H1 Tag Check

Checks the H1 tags present on a webpage.

Analyzes:
1. Presence of H1 tag
2. Number of H1 tags
3. H1 text
4. Whether exactly one H1 tag exists
"""

import requests
from bs4 import BeautifulSoup


def check_h1_tag(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "72 - H1 Tag Check",
        "checked_url": url,
        "h1_found": False,
        "h1_count": 0,
        "h1_text": [],
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
                f"Website returned status code "
                f"{response.status_code}"
            )

            return result

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        h1_tags = soup.find_all("h1")

        result["h1_count"] = len(h1_tags)

        if h1_tags:

            result["h1_found"] = True

            result["h1_text"] = [
                tag.get_text(strip=True)
                for tag in h1_tags
            ]

            if len(h1_tags) == 1:

                result["metric_passed"] = True

                result["recommendation"] = (
                    "Exactly one H1 tag found. "
                    "This follows SEO best practices."
                )

            else:

                result["recommendation"] = (
                    f"{len(h1_tags)} H1 tags found. "
                    "Ideally, a page should contain exactly one H1 tag."
                )

        else:

            result["recommendation"] = (
                "No H1 tag found. Add one descriptive H1 heading."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result
