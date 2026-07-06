"""
Factor 73: Allow PerplexityBot

Checks whether the website explicitly allows or blocks
PerplexityBot in robots.txt.

Analyzes:
1. Presence of robots.txt
2. Presence of PerplexityBot rule
3. Whether PerplexityBot is allowed or blocked
"""

import requests
from urllib.parse import urljoin


def check_perplexitybot_permission(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "73 - Allow PerplexityBot",
        "robots_txt_found": False,
        "perplexitybot_found": False,
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

                if current_agent == "perplexitybot":

                    result["perplexitybot_found"] = True

            elif (
                current_agent == "perplexitybot"
                and line.lower().startswith("disallow:")
            ):

                value = (
                    line.split(":", 1)[1]
                    .strip()
                )

                if value == "/":

                    permission = "Disallowed"

        result["permission"] = permission

        if result["perplexitybot_found"]:

            if permission == "Allowed":

                result["recommendation"] = (
                    "PerplexityBot is explicitly allowed in robots.txt."
                )

            else:

                result["recommendation"] = (
                    "PerplexityBot is explicitly blocked in robots.txt."
                )

        else:

            result["recommendation"] = (
                "No explicit PerplexityBot rule found. "
                "The bot may follow the wildcard (*) rules."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result