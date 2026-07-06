"""
Factor 75: Allow CCBot

Checks whether the website explicitly allows or blocks
CCBot (Common Crawl) in robots.txt.

Analyzes:
1. robots.txt availability
2. CCBot rule presence
3. Whether CCBot is allowed or blocked
"""

import requests
from urllib.parse import urljoin


def check_ccbot_permission(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "75 - Allow CCBot",
        "robots_txt_found": False,
        "ccbot_found": False,
        "permission": "Unknown",
        "recommendation": "",
        "status": "Failed"
    }

    try:

        robots_url = urljoin(
            url,
            "/robots.txt"
        )

        response = requests.get(
            robots_url,
            headers={
                "User-Agent": "Mozilla/5.0 SEO Analyzer Bot"
            },
            timeout=10
        )

        if response.status_code != 200:

            result["error"] = (
                f"robots.txt returned status code "
                f"{response.status_code}"
            )

            return result

        result["robots_txt_found"] = True

        lines = response.text.splitlines()

        current_agent = None
        permission = "Allowed"

        for line in lines:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.lower().startswith("user-agent:"):

                current_agent = (
                    line.split(":", 1)[1]
                    .strip()
                    .lower()
                )

                if current_agent == "ccbot":

                    result["ccbot_found"] = True

            elif (
                current_agent == "ccbot"
                and line.lower().startswith("disallow:")
            ):

                value = (
                    line.split(":", 1)[1]
                    .strip()
                )

                if value == "/":

                    permission = "Disallowed"

        result["permission"] = permission

        if result["ccbot_found"]:

            if permission == "Allowed":

                result["recommendation"] = (
                    "CCBot is explicitly allowed in robots.txt."
                )

            else:

                result["recommendation"] = (
                    "CCBot is explicitly blocked in robots.txt."
                )

        else:

            result["recommendation"] = (
                "No explicit CCBot rule found. "
                "The bot may follow the wildcard (*) rules."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result