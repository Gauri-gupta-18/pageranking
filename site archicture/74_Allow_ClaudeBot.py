"""
Factor 74: Allow ClaudeBot / anthropic-ai

Checks whether the website explicitly allows or blocks
ClaudeBot (Anthropic) in robots.txt.

Analyzes:
1. robots.txt availability
2. ClaudeBot rule
3. anthropic-ai rule
4. Whether access is Allowed or Disallowed
"""

import requests
from urllib.parse import urljoin


def check_claudebot_permission(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "74 - Allow ClaudeBot / anthropic-ai",
        "robots_txt_found": False,
        "claudebot_found": False,
        "anthropic_ai_found": False,
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

                if current_agent == "claudebot":

                    result["claudebot_found"] = True

                elif current_agent == "anthropic-ai":

                    result["anthropic_ai_found"] = True

            elif (
                current_agent in [
                    "claudebot",
                    "anthropic-ai"
                ]
                and line.lower().startswith("disallow:")
            ):

                value = (
                    line.split(":", 1)[1]
                    .strip()
                )

                if value == "/":

                    permission = "Disallowed"

        result["permission"] = permission

        if permission == "Allowed":

            result["recommendation"] = (
                "ClaudeBot / anthropic-ai is allowed "
                "to access the website."
            )

        else:

            result["recommendation"] = (
                "ClaudeBot / anthropic-ai is blocked "
                "in robots.txt."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result