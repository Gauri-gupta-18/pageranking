"""
Factor 22: FAQPage Schema Checker

This module checks whether a webpage contains FAQPage schema.

It analyzes:
1. FAQPage Schema
2. Total Questions
3. Questions List
"""

import requests
import json
from bs4 import BeautifulSoup


def check_faq_schema(context):

    url = context["url"]

    result = {
        "factor": "22 - FAQPage Schema",
        "faq_found": False,
        "total_questions": 0,
        "questions": [],
        "status": "Failed"
    }

    try:

        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 SEO Analyzer Bot"},
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

            items = []

            # Handle list
            if isinstance(data, list):
                items = data

            # Handle dictionary
            elif isinstance(data, dict):

                # Handle @graph
                if "@graph" in data:
                    items = data["@graph"]
                else:
                    items = [data]

            # Check every schema object
            for item in items:

                if not isinstance(item, dict):
                    continue

                if item.get("@type") == "FAQPage":

                    result["faq_found"] = True

                    questions = item.get("mainEntity", [])

                    for question in questions:

                        if isinstance(question, dict):
                            result["questions"].append(
                                question.get("name")
                            )

                    result["total_questions"] = len(
                        result["questions"]
                    )

                    result["status"] = "Success"

                    return result

    except Exception as error:

        result["error"] = str(error)

    return result