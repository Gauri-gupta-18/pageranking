"""
Factor 76: Allow Bytespider, Applebot-Extended, MetaExternalAgent

Checks whether the website explicitly allows or blocks
Bytespider, Applebot-Extended and MetaExternalAgent
in robots.txt.
"""

import requests
from urllib.parse import urljoin


AI_BOTS = [
    "Bytespider",
    "Applebot-Extended",
    "MetaExternalAgent"
]


def check_additional_ai_bots(context):

    url = context.get("url", "")

    result = {
        "factor": "76 - Allow Bytespider, Applebot-Extended, MetaExternalAgent",
        "robots_txt_found": False,
        "allowed_bots": [],
        "disallowed_bots": [],
        "not_found": [],
        "status": "Failed"
    }

    try:

        robots_url = urljoin(url, "/robots.txt")

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

        bot_status = {
            bot: "Allowed"
            for bot in AI_BOTS
        }

        found = set()

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

                        found.add(bot)

                        if value == "/":

                            bot_status[bot] = "Disallowed"

        for bot in AI_BOTS:

            if bot not in found:

                result["not_found"].append(bot)

            elif bot_status[bot] == "Allowed":

                result["allowed_bots"].append(bot)

            else:

                result["disallowed_bots"].append(bot)

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result