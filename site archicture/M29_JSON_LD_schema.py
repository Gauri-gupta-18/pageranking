"""
Factor 29: JSON-LD Schema Validation

Checks whether a webpage contains JSON-LD Schema.

It analyzes:
1. Presence of JSON-LD
2. Total JSON-LD Blocks
3. Schema Types
"""

import requests
import json
from bs4 import BeautifulSoup


def check_jsonld(context):

    url = context["url"]

    result = {
        "factor": "29 - JSON-LD Schema Validation",
        "jsonld_found": False,
        "total_blocks": 0,
        "schema_types": [],
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

        if scripts:

            result["jsonld_found"] = True
            result["total_blocks"] = len(scripts)

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

                    if not schema_type:
                        continue

                    if isinstance(schema_type, list):
                        result["schema_types"].extend(schema_type)
                    else:
                        result["schema_types"].append(schema_type)

            # Remove duplicate schema types
            result["schema_types"] = list(set(result["schema_types"]))

            result["status"] = "Success"

        return result

    except Exception as error:

        result["error"] = str(error)

        return result
