"""
Factor 94: Contact Us Page Availability

Checks whether a website provides contact information.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def check_contact_page(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "94 - Contact Us Page Availability",
        "contact_page_found": False,
        "contact_page_url": None,
        "email_found": False,
        "phone_found": False,
        "contact_form_found": False,
        "address_found": False,
        "status": "Failed"
    }

    try:

        # Download webpage
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
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

        # Common contact keywords
        keywords = [
            "contact",
            "contact us",
            "support",
            "help",
            "reach us",
            "get in touch"
        ]

        # Search contact page
        for link in links:

            text = link.get_text(
                strip=True
            ).lower()

            href = link["href"].lower()

            if any(
                keyword in text or keyword in href
                for keyword in keywords
            ):

                result["contact_page_found"] = True
                result["contact_page_url"] = urljoin(
                    url,
                    link["href"]
                )
                break

        # Search email
        page_text = soup.get_text(" ")

        email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        if re.search(email_pattern, page_text):
            result["email_found"] = True

        # Search phone number
        phone_pattern = (
            r"(\+?\d[\d\s\-\(\)]{7,}\d)"
        )

        if re.search(phone_pattern, page_text):
            result["phone_found"] = True

        # Search contact form
        if soup.find("form"):
            result["contact_form_found"] = True

        # Search address keywords
        address_keywords = [
            "address",
            "office",
            "location",
            "head office"
        ]

        if any(
            keyword in page_text.lower()
            for keyword in address_keywords
        ):
            result["address_found"] = True

        # Final status
        if (
            result["contact_page_found"]
            or result["email_found"]
            or result["phone_found"]
        ):
            result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result


if __name__ == "__main__":

    context = {
        "url": "https://www.python.org"
    }

    report = check_contact_page(context)

    print(report)
    # nitin