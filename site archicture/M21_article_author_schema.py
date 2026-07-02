"""
Factor 21: Article + Author Schema Checker

Checks whether a webpage contains Article schema
and whether Author information is present.
"""

import json
import requests
from bs4 import BeautifulSoup


def check_article_author_schema(context):
    """
    Plugin function called by main.py
    """

    url = context["url"]

    result = {
        "factor": "21 - Article + Author Schema",
        "article_schema_found": False,
        "author_found": False,
        "author_name": None,
        "headline": None,
        "date_published": None,
        "article_type": None,
        "status": "Failed"
    }

    article_types = [
        "Article",
        "NewsArticle",
        "BlogPosting",
        "TechArticle",
        "LiveBlogPosting"
    ]

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

            except Exception:
                continue

            items = []

            # Case 1 : JSON Array
            if isinstance(data, list):
                items.extend(data)

            # Case 2 : JSON Object
            elif isinstance(data, dict):

                # Handle @graph
                if "@graph" in data and isinstance(data["@graph"], list):
                    items.extend(data["@graph"])

                else:
                    items.append(data)

            for item in items:

                if not isinstance(item, dict):
                    continue

                schema_type = item.get("@type")

                if isinstance(schema_type, list):
                    is_article = any(
                        t in article_types
                        for t in schema_type
                    )
                else:
                    is_article = schema_type in article_types

                if not is_article:
                    continue

                result["article_schema_found"] = True
                result["article_type"] = schema_type
                result["headline"] = item.get("headline")
                result["date_published"] = item.get("datePublished")

                author = item.get("author")

                if author:

                    result["author_found"] = True

                    # Single Author Object
                    if isinstance(author, dict):
                        result["author_name"] = author.get("name")

                    # Multiple Authors
                    elif isinstance(author, list):

                        names = []

                        for person in author:

                            if isinstance(person, dict):
                                if person.get("name"):
                                    names.append(person.get("name"))

                            elif isinstance(person, str):
                                names.append(person)

                        result["author_name"] = ", ".join(names)

                    # Author is plain string
                    elif isinstance(author, str):
                        result["author_name"] = author

                result["status"] = "Success"

                return result

    except Exception as error:

        result["error"] = str(error)

    return result