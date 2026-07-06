"""
Factor 64: Server-Side Rendered Content

Checks whether meaningful content is available in the
initial HTML response without requiring JavaScript.

Analyzes:
1. HTML availability
2. Visible text in initial HTML
3. Number of JavaScript files
4. Presence of <noscript> tag
5. Whether the page appears server-side rendered
"""

import requests
from bs4 import BeautifulSoup


def check_server_side_rendered_content(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "64 - Server-Side Rendered Content",
        "html_found": False,
        "visible_text_length": 0,
        "script_count": 0,
        "noscript_found": False,
        "ssr_detected": False,
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

        html = response.text

        if html.strip():

            result["html_found"] = True

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # Count JavaScript files
        scripts = soup.find_all("script")
        result["script_count"] = len(scripts)

        # Check for <noscript>
        if soup.find("noscript"):

            result["noscript_found"] = True

        # Extract visible text
        body = soup.find("body")

        if body:

            visible_text = body.get_text(
                " ",
                strip=True
            )

            result["visible_text_length"] = len(
                visible_text
            )

        # Simple SSR detection
        if result["visible_text_length"] >= 300:

            result["ssr_detected"] = True

            result["recommendation"] = (
                "The page contains sufficient server-rendered "
                "content for AI crawlers."
            )

        elif result["visible_text_length"] > 0:

            result["recommendation"] = (
                "Limited HTML content detected. "
                "The page may rely heavily on JavaScript."
            )

        else:

            result["recommendation"] = (
                "No meaningful HTML content found. "
                "AI crawlers may have difficulty accessing the page."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result