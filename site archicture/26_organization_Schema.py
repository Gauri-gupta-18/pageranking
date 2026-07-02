"""
Factor 26: Organization Schema with sameAs Checker

Checks whether a webpage contains Organization Schema.

It analyzes:
1. Organization Schema
2. Company Name
3. Logo
4. sameAs Links
"""

import requests
import json
from bs4 import BeautifulSoup


def check_organization_schema(context):

    url = context["url"]

    result = {
        "factor": "26 - Organization Schema",
        "organization_found": False,
        "organization_name": None,
        "logo": None,
        "sameAs_links": [],
        "status": "Failed"
    }

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )

        for script in scripts:

            if not script.string:
                continue

            try:
                data = json.loads(script.string)

            except json.JSONDecodeError:
                continue

            if not isinstance(data, list):
                data = [data]

            for item in data:

                if not isinstance(item, dict):
                    continue

                schema_type = item.get("@type")

                # Handle both string and list values
                if isinstance(schema_type, list):
                    is_organization = "Organization" in schema_type
                else:
                    is_organization = schema_type == "Organization"

                if is_organization:

                    result["organization_found"] = True
                    result["organization_name"] = item.get("name")
                    result["logo"] = item.get("logo")
                    result["sameAs_links"] = item.get("sameAs", [])

                    result["status"] = "Success"

                    return result

        return result

    except Exception as error:

        result["error"] = str(error)

        return result