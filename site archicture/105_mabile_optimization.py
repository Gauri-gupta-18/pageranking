"""
Factor 105: Mobile Optimization Check

Checks whether the website follows mobile optimization best practices.
"""

import requests
from bs4 import BeautifulSoup


def check_mobile_optimization(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "105 - Mobile Optimization Check",
        "viewport_meta": False,
        "responsive_css": False,
        "responsive_images": False,
        "mobile_navigation": False,
        "seo_score": 100,
        "status": "Failed"
    }

    try:

        # Fetch webpage
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

        # Check viewport meta tag
        viewport = soup.find(
            "meta",
            attrs={"name": "viewport"}
        )

        if viewport:

            result["viewport_meta"] = True

        else:

            result["seo_score"] -= 30

        # Check responsive CSS
        styles = soup.find_all("style")

        for style in styles:

            if style.string and "@media" in style.string:

                result["responsive_css"] = True

                break

        if not result["responsive_css"]:

            result["seo_score"] -= 25

        # Check responsive images
        images = soup.find_all("img")

        for image in images:

            if image.get("srcset"):

                result["responsive_images"] = True

                break

        if not result["responsive_images"]:

            result["seo_score"] -= 20

        # Check mobile navigation
        if soup.find(
            class_=lambda value:
            value and (
                "menu" in value.lower()
                or "mobile" in value.lower()
                or "hamburger" in value.lower()
            )
        ):

            result["mobile_navigation"] = True

        else:

            result["seo_score"] -= 25

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

    report = check_mobile_optimization(context)

    print(report)
    # nitin