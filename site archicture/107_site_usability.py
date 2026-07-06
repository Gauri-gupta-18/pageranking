"""
Factor 107: Site Usability

Checks whether the website provides a good user experience.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def check_site_usability(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "107 - Site Usability",
        "navigation_found": False,
        "search_box_found": False,
        "broken_links": 0,
        "images_without_alt": 0,
        "buttons_found": 0,
        "seo_score": 100,
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

        # Check navigation
        if (
            soup.find("nav")
            or soup.find(class_="navbar")
            or soup.find(id="menu")
        ):

            result["navigation_found"] = True

        else:

            result["seo_score"] -= 20

        # Check search box
        if soup.find(
            "input",
            attrs={"type": "search"}
        ):

            result["search_box_found"] = True

        elif soup.find(
            "input",
            attrs={"name": "q"}
        ):

            result["search_box_found"] = True

        else:

            result["seo_score"] -= 10

        # Count buttons
        buttons = soup.find_all("button")

        result["buttons_found"] = len(buttons)

        # Check image alt text
        images = soup.find_all("img")

        for image in images:

            if not image.get("alt"):

                result["images_without_alt"] += 1

        result["seo_score"] -= min(
            result["images_without_alt"] * 2,
            20
        )

        # Check first 10 internal links
        checked = 0

        for link in soup.find_all(
            "a",
            href=True
        ):

            if checked >= 10:
                break

            href = urljoin(
                url,
                link["href"]
            )

            try:

                link_response = requests.get(
                    href,
                    timeout=5
                )

                if link_response.status_code >= 400:

                    result["broken_links"] += 1

            except requests.RequestException:

                result["broken_links"] += 1

            checked += 1

        result["seo_score"] -= min(
            result["broken_links"] * 5,
            30
        )

        # Prevent negative score
        if result["seo_score"] < 0:

            result["seo_score"] = 0

        # Final status
        if result["seo_score"] >= 80:

            result["status"] = "Excellent"

        elif result["seo_score"] >= 60:

            result["status"] = "Good"

        elif result["seo_score"] >= 40:

            result["status"] = "Average"

        else:

            result["status"] = "Poor"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result


if __name__ == "__main__":

    context = {
        "url": "https://www.python.org"
    }

    report = check_site_usability(context)

    print(report)
    # nitin