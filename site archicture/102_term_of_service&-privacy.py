"""
Factor 102: Terms of Service & Privacy Pages

Checks whether the website contains legal pages.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def check_legal_pages(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "102 - Terms of Service & Privacy Pages",
        "privacy_policy_found": False,
        "privacy_policy_url": None,
        "terms_of_service_found": False,
        "terms_of_service_url": None,
        "status": "Failed"
    }

    try:

        # Fetch webpage
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        # Check response
        if response.status_code != 200:
            result["error"] = f"Status Code {response.status_code}"
            return result

        # Parse HTML
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find all links
        links = soup.find_all(
            "a",
            href=True
        )

        # Privacy keywords
        privacy_keywords = [
            "privacy",
            "privacy policy"
        ]

        # Terms keywords
        terms_keywords = [
            "terms",
            "terms of service",
            "terms and conditions",
            "conditions"
        ]

        # Check all links
        for link in links:

            text = link.get_text(
                strip=True
            ).lower()

            href = link["href"].lower()

            # Check Privacy Page
            if (
                not result["privacy_policy_found"]
                and any(
                    keyword in text or keyword in href
                    for keyword in privacy_keywords
                )
            ):

                result["privacy_policy_found"] = True

                result["privacy_policy_url"] = urljoin(
                    url,
                    link["href"]
                )

            # Check Terms Page
            if (
                not result["terms_of_service_found"]
                and any(
                    keyword in text or keyword in href
                    for keyword in terms_keywords
                )
            ):

                result["terms_of_service_found"] = True

                result["terms_of_service_url"] = urljoin(
                    url,
                    link["href"]
                )

        # Final status
        if (
            result["privacy_policy_found"]
            and result["terms_of_service_found"]
        ):

            result["status"] = "Success"

        elif (
            result["privacy_policy_found"]
            or result["terms_of_service_found"]
        ):

            result["status"] = "Partial Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result


if __name__ == "__main__":

    context = {
        "url": "https://www.python.org"
    }

    report = check_legal_pages(context)

    print(report)
    # nitin