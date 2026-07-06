"""
Factor 70: Hreflang for Multilingual Sites

Checks whether the webpage uses hreflang tags for
multilingual or multi-regional SEO.

Analyzes:
1. Presence of hreflang tags
2. Number of hreflang tags
3. Languages declared
4. Presence of x-default
5. Recommendation
"""

import requests
from bs4 import BeautifulSoup


def check_hreflang_multilingual(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "70 - Hreflang for Multilingual Sites",
        "hreflang_found": False,
        "hreflang_count": 0,
        "languages": [],
        "x_default_found": False,
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

        hreflang_tags = soup.find_all(
            "link",
            attrs={
                "rel": lambda value: value and "alternate" in value,
                "hreflang": True
            }
        )

        result["hreflang_count"] = len(hreflang_tags)

        if hreflang_tags:

            result["hreflang_found"] = True

            languages = []

            for tag in hreflang_tags:

                language = tag.get(
                    "hreflang",
                    ""
                ).strip()

                if language:

                    languages.append(language)

                    if language.lower() == "x-default":
                        result["x_default_found"] = True

            result["languages"] = sorted(
                list(set(languages))
            )

            if result["x_default_found"]:

                result["recommendation"] = (
                    "Hreflang implementation looks good "
                    "and includes x-default."
                )

            else:

                result["recommendation"] = (
                    "Hreflang tags found. Consider adding "
                    "an x-default hreflang if appropriate."
                )

        else:

            result["recommendation"] = (
                "No hreflang tags found. "
                "If the website targets multiple languages "
                "or regions, implement hreflang tags."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result