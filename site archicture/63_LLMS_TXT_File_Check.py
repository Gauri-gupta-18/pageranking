"""
Factor 63: llms.txt File Check

Checks whether a website has an llms.txt file
at its root directory.
"""

import requests
from urllib.parse import urljoin


def check_llms_txt(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "63 - llms.txt File Check",
        "llms_txt_found": False,
        "llms_txt_url": None,
        "line_count": 0,
        "character_count": 0,
        "preview": "",
        "status": "Failed"
    }

    try:

        llms_url = urljoin(
            url,
            "/llms.txt"
        )

        result["llms_txt_url"] = llms_url

        response = requests.get(
            llms_url,
            headers={
                "User-Agent": "Mozilla/5.0 SEO Analyzer Bot"
            },
            timeout=10
        )

        if response.status_code != 200:

            result["error"] = (
                f"llms.txt returned status code "
                f"{response.status_code}"
            )

            return result

        content = response.text

        result["llms_txt_found"] = True

        result["line_count"] = len(
            content.splitlines()
        )

        result["character_count"] = len(
            content
        )

        result["preview"] = content[:300]

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result
