"""
Factor 77: Decide on Training vs Retrieval Separately

Checks whether different AI crawlers have different
robots.txt permissions, indicating separate treatment
for AI retrieval/training bots.
"""

import requests
from urllib.parse import urljoin


AI_BOTS = [
    "GPTBot",
    "ClaudeBot",
    "PerplexityBot",
    "Google-Extended",
    "CCBot",
    "Bytespider",
    "Applebot-Extended",
    "MetaExternalAgent"
]


def check_training_vs_retrieval_policy(context):

    url = context.get("url", "")

    result = {
        "factor": "77 - Training vs Retrieval Separately",
        "robots_txt_found": False,
        "different_rules_detected": False,
        "bot_permissions": {},
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

        permissions = {}

        for line in lines:

            line = line.split("#", 1)[0].strip()

            if not line:
                continue

            if line.lower().startswith("user-agent:"):

                current_agent = (
                    line.split(":", 1)[1]
                    .strip()
                    .lower()
                )

            elif (
                current_agent
                and line.lower().startswith("disallow:")
            ):

                value = (
                    line.split(":", 1)[1]
                    .strip()
                )

                for bot in AI_BOTS:

                    if current_agent == bot.lower():

                        permissions[bot] = (
                            "Disallowed"
                            if value == "/"
                            else "Allowed"
                        )

        for bot in AI_BOTS:

            permissions.setdefault(
                bot,
                "Not Explicitly Mentioned"
            )

        result["bot_permissions"] = permissions

        unique_permissions = set(
            permissions.values()
        )

        if len(unique_permissions) > 1:

            result["different_rules_detected"] = True

            result["recommendation"] = (
                "Different AI crawlers have different "
                "robots.txt permissions."
            )

        else:

            result["recommendation"] = (
                "All AI crawlers appear to have "
                "similar robots.txt permissions."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result