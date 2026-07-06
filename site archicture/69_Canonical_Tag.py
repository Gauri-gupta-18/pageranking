"""
Factor 69: Canonical Tags

Checks a website's canonical tag.

Analyzes:
1. Presence of <link rel="canonical"> tag
2. Canonical URL value
3. Whether the canonical URL is self-canonical
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def check_canonical_tags(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "69 - Canonical Tags",
        "canonical_found": False,
        "canonical_url": "",
        "self_canonical": False,
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

        canonical = soup.find(
            "link",
            attrs={
                "rel": lambda value: value and "canonical" in value
            }
        )

        if canonical and canonical.get("href"):

            canonical_url = canonical["href"].strip()

            result["canonical_found"] = True
            result["canonical_url"] = canonical_url

            page = urlparse(url)
            canonical_page = urlparse(canonical_url)

            page_url = (
                page.scheme,
                page.netloc,
                page.path.rstrip("/")
            )

            canonical_url_tuple = (
                canonical_page.scheme,
                canonical_page.netloc,
                canonical_page.path.rstrip("/")
            )

            if page_url == canonical_url_tuple:

                result["self_canonical"] = True

                result["recommendation"] = (
                    "Page has a valid self-canonical tag."
                )

            else:

                result["recommendation"] = (
                    "Canonical tag points to a different URL."
                )

        else:

            result["recommendation"] = (
                "Canonical tag not found."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result
