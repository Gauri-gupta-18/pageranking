"""
Factor 108: Google Analytics & Search Console

Checks Google Analytics, Google Tag Manager,
and Google Search Console verification.
"""

import requests
from bs4 import BeautifulSoup


def check_google_integration(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "108 - Google Analytics & Search Console",
        "google_analytics_found": False,
        "google_tag_manager_found": False,
        "search_console_verification_found": False,
        "seo_score": 0,
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

        html = response.text.lower()

        # Check Google Analytics
        analytics_patterns = [
            "gtag(",
            "google-analytics.com",
            "googletagmanager.com/gtag",
            "ga(",
            "gtag/js"
        ]

        if any(
            pattern in html
            for pattern in analytics_patterns
        ):

            result["google_analytics_found"] = True

            result["seo_score"] += 40

        # Check Google Tag Manager
        if (
            "googletagmanager.com"
            in html
        ):

            result["google_tag_manager_found"] = True

            result["seo_score"] += 30

        # Check Search Console verification
        verification = soup.find(
            "meta",
            attrs={
                "name": "google-site-verification"
            }
        )

        if verification:

            result["search_console_verification_found"] = True

            result["seo_score"] += 30

        # Final status
        if result["seo_score"] == 100:

            result["status"] = "Excellent"

        elif result["seo_score"] >= 70:

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

    report = check_google_integration(context)

    print(report)
    # nitin