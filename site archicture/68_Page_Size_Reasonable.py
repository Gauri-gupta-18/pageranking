"""
Factor 68: Page Size Reasonable

Checks whether the webpage size is within a
reasonable range for fast loading and crawling.

Analyzes:
1. HTML page size
2. Page size in KB
3. Size category
4. Whether the page size is SEO-friendly
"""

import requests


def check_page_size_reasonable(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "68 - Page Size Reasonable",
        "page_size_bytes": 0,
        "page_size_kb": 0.0,
        "size_category": "",
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
                f"Website returned status code "
                f"{response.status_code}"
            )

            return result

        page_size = len(response.content)
        page_size_kb = round(page_size / 1024, 2)

        result["page_size_bytes"] = page_size
        result["page_size_kb"] = page_size_kb

        # Categorize page size
        if page_size_kb <= 100:

            result["size_category"] = "Excellent"
            result["seo_friendly"] = True

            result["recommendation"] = (
                "Excellent page size for SEO and AI crawlers."
            )

        elif page_size_kb <= 500:

            result["size_category"] = "Good"
            result["seo_friendly"] = True

            result["recommendation"] = (
                "Page size is within the recommended range."
            )

        elif page_size_kb <= 1024:

            result["size_category"] = "Large"

            result["recommendation"] = (
                "Page size is larger than recommended. "
                "Consider reducing HTML, CSS, or JavaScript."
            )

        else:

            result["size_category"] = "Very Large"

            result["recommendation"] = (
                "Page size is too large. "
                "Compress resources and optimize the page."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result