"""
Factor 62: Robots.txt AI Crawler Permissions

Checks a website's robots.txt file for AI crawler permissions.

Analyzes:
1. Presence of robots.txt
2. Explicit allow/disallow rules for well-known AI crawlers
3. Wildcard (*) inherited permissions
4. Summary of AI crawler accessibility
"""

import requests
from urllib.parse import urljoin


# List of well-known AI crawler user-agents
AI_BOTS = [
    "GPTBot",
    "ClaudeBot",
    "anthropic-ai",
    "PerplexityBot",
    "Google-Extended",
    "CCBot",
    "Bytespider",
    "Applebot-Extended",
    "MetaExternalAgent"
]


def _parse_robots_txt(robots_text):
    """
    Parse robots.txt according to RFC 9309.

    Consecutive User-agent lines share the same Allow/Disallow rules.
    """

    agent_rules = {}
    current_group_agents = []
    group_is_open = True

    for line in robots_text.splitlines():

        # Remove comments and whitespace
        stripped_line = line.split("#", 1)[0].strip()

        if not stripped_line:
            continue

        if stripped_line.lower().startswith("user-agent:"):

            agent_name = stripped_line.split(
                ":",
                1
            )[1].strip().lower()

            if not group_is_open:
                current_group_agents = []
                group_is_open = True

            current_group_agents.append(agent_name)

            agent_rules.setdefault(
                agent_name,
                {
                    "allow": [],
                    "disallow": []
                }
            )

            continue

        if stripped_line.lower().startswith("disallow:"):

            path = stripped_line.split(
                ":",
                1
            )[1].strip()

            if current_group_agents and path:

                for agent in current_group_agents:
                    agent_rules[agent]["disallow"].append(path)

            group_is_open = False

        elif stripped_line.lower().startswith("allow:"):

            path = stripped_line.split(
                ":",
                1
            )[1].strip()

            if current_group_agents and path:

                for agent in current_group_agents:
                    agent_rules[agent]["allow"].append(path)

            group_is_open = False

        elif current_group_agents and ":" in stripped_line:
            group_is_open = False

    return agent_rules


def _classify_rules(
    allow_paths,
    disallow_paths
):
    """
    Determine crawler access status.
    """

    site_wide_disallow = "/" in disallow_paths
    site_wide_allow = "/" in allow_paths

    if site_wide_disallow and not site_wide_allow:
        return "disallowed"

    if site_wide_allow:
        return "allowed"

    if disallow_paths:
        return "partially_disallowed"

    return "allowed"


def check_robots_ai_permissions(context):
    """
    Factor 62
    """

    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "62 - Robots.txt AI Crawler Permissions",
        "robots_txt_found": False,
        "allowed_bots": [],
        "disallowed_bots": [],
        "partially_disallowed_bots": {},
        "implicitly_allowed_bots": [],
        "implicitly_disallowed_bots": [],
        "not_mentioned_bots": [],
        "summary": {},
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

        agent_rules = _parse_robots_txt(
            response.text
        )

        wildcard_rules = agent_rules.get("*")

        wildcard_verdict = None

        if wildcard_rules:

            wildcard_verdict = _classify_rules(
                wildcard_rules["allow"],
                wildcard_rules["disallow"]
            )

        for bot in AI_BOTS:

            bot_rules = agent_rules.get(
                bot.lower()
            )

            # Explicit block exists
            if bot_rules is not None:

                verdict = _classify_rules(
                    bot_rules["allow"],
                    bot_rules["disallow"]
                )

                if verdict == "allowed":

                    result["allowed_bots"].append(bot)

                elif verdict == "disallowed":

                    result["disallowed_bots"].append(bot)

                else:

                    result["partially_disallowed_bots"][bot] = (
                        bot_rules["disallow"]
                    )

            # Wildcard inheritance
            elif wildcard_rules is not None:

                if wildcard_verdict == "disallowed":

                    result["implicitly_disallowed_bots"].append(bot)

                else:

                    result["implicitly_allowed_bots"].append(bot)

            # No rule at all
            else:

                result["not_mentioned_bots"].append(bot)

        result["summary"] = {
            "allowed": len(
                result["allowed_bots"]
            ),
            "disallowed": len(
                result["disallowed_bots"]
            ),
            "partially_disallowed": len(
                result["partially_disallowed_bots"]
            ),
            "implicitly_allowed": len(
                result["implicitly_allowed_bots"]
            ),
            "implicitly_disallowed": len(
                result["implicitly_disallowed_bots"]
            ),
            "not_mentioned": len(
                result["not_mentioned_bots"]
            )
        }

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result
