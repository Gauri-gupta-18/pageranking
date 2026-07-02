"""
Factor 24: Dataset Schema Checker

Checks whether a webpage contains Dataset Schema.

It analyzes:
1. Presence of Dataset Schema
2. Dataset Name
3. Description
4. Creator
5. License
"""

import requests
import json
from bs4 import BeautifulSoup


def check_dataset_schema(context):

    url = context["url"]

    result = {
        "factor": "24 - Dataset Schema",
        "dataset_found": False,
        "dataset_name": None,
        "description": None,
        "creator": None,
        "license": None,
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
                    is_dataset = "Dataset" in schema_type
                else:
                    is_dataset = schema_type == "Dataset"

                if is_dataset:

                    result["dataset_found"] = True
                    result["dataset_name"] = item.get("name")
                    result["description"] = item.get("description")

                    creator = item.get("creator")

                    if isinstance(creator, dict):
                        result["creator"] = creator.get("name")
                    else:
                        result["creator"] = creator

                    result["license"] = item.get("license")

                    result["status"] = "Success"

                    return result

        return result

    except Exception as error:

        result["error"] = str(error)

        return result