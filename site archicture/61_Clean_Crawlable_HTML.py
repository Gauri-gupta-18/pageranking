"""
Factor 61: Clean Crawlable HTML

Checks whether a webpage provides clean, crawlable HTML.

Analyzes:
1. HTTP response status
2. HTML document presence
3. <body> tag presence
4. Visible text content
5. Crawlability status
"""

import requests
from bs4 import BeautifulSoup


def check_clean_crawlable_html(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "61 - Clean Crawlable HTML",
        "checked_url": url,
        "status_code": None,
        "html_found": False,
        "body_found": False,
        "text_length": 0,
        "crawlable": False,
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

        result["status_code"] = response.status_code

        if response.status_code != 200:
            result["error"] = (
                f"Website returned status code "
                f"{response.status_code}"
            )
            return result

        html = response.text

        if html.strip():
            result["html_found"] = True

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        body = soup.find("body")

        if body:

            result["body_found"] = True

            visible_text = body.get_text(
                separator=" ",
                strip=True
            )

            result["text_length"] = len(visible_text)

            if len(visible_text) >= 200:

                result["crawlable"] = True

                result["recommendation"] = (
                    "The page contains sufficient HTML content "
                    "for search engines and AI crawlers."
                )

            elif len(visible_text) > 0:

                result["recommendation"] = (
                    "The page contains limited HTML content. "
                    "Consider increasing server-rendered content."
                )

            else:

                result["recommendation"] = (
                    "No meaningful text found in the HTML body."
                )

        else:

            result["recommendation"] = (
                "No <body> tag found in the HTML document."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result