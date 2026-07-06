
"""
Factor 104: Breadcrumb Navigation

Checks whether the website contains breadcrumb navigation.
Breadcrumbs help users understand their location in the site hierarchy.

Example:
Home > Category > Subcategory > Product
"""

import json
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}


def check_breadcrumb_navigation(url):
    """
    Check the availability of breadcrumb navigation.

    Args:
        url (str): Website URL

    Returns:
        dict: Breadcrumb analysis report
    """

    result = {
        "factor": "104 - Breadcrumb Navigation",
        "breadcrumb_found": False,
        "breadcrumb_text": [],
        "method": None,
        "status": "Failed"
    }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            result["error"] = (
                f"Website returned status code {response.status_code}"
            )
            return result

        soup = BeautifulSoup(response.text, "html.parser")

        # ====================================
        # Method 1: Check HTML breadcrumb tags
        # ====================================

        breadcrumb = (
            soup.find("nav", attrs={"aria-label": lambda x: x and "breadcrumb" in x.lower()})
            or soup.find(
                lambda tag:
                tag.get("class") and any(
                    "breadcrumb" in cls.lower()
                    for cls in tag.get("class")
                )
            )
            or soup.find(
                lambda tag:
                tag.get("id") and "breadcrumb" in tag.get("id").lower()
            )
        )

        if breadcrumb:
            items = breadcrumb.find_all(["a", "span", "li"])

            for item in items:
                text = item.get_text(strip=True)

                if text and text not in result["breadcrumb_text"]:
                    result["breadcrumb_text"].append(text)

            result["breadcrumb_found"] = True
            result["method"] = "HTML Breadcrumb"
            result["status"] = "Success"

            return result


        # ====================================
        # Method 2: Check JSON-LD Schema
        # ====================================

        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )

        for script in scripts:
            try:
                data = json.loads(script.string)

                if isinstance(data, dict):
                    data = [data]

                for item in data:
                    if item.get("@type") == "BreadcrumbList":

                        for element in item.get(
                            "itemListElement",
                            []
                        ):
                            name = element.get("name")

                            if name:
                                result["breadcrumb_text"].append(name)

                        result["breadcrumb_found"] = True
                        result["method"] = "Schema.org JSON-LD"
                        result["status"] = "Success"

                        return result

            except (json.JSONDecodeError, TypeError):
                continue


        result["message"] = "No breadcrumb navigation found"

    except requests.exceptions.RequestException as error:
        result["error"] = str(error)

    return result


# Test this module independently
if __name__ == "__main__":

    websites = [
        "https://vwo.com/glossary/breadcrumb-navigation/",
        "https://www.amazon.com",
        "https://www.apple.com"
    ]

    for website in websites:
        print("\nChecking:", website)
        print(check_breadcrumb_navigation(website))
        # nitin