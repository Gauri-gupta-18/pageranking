"""
Factor 109: User Reviews / Site Reputation

Checks whether the website references trusted review platforms
and contains review schema.
"""

import requests
from bs4 import BeautifulSoup


def check_site_reputation(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "109 - User Reviews / Site Reputation",
        "trustpilot_found": False,
        "bbb_found": False,
        "google_reviews_found": False,
        "facebook_reviews_found": False,
        "yelp_found": False,
        "review_schema_found": False,
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

        # Check Trustpilot
        if "trustpilot.com" in html:

            result["trustpilot_found"] = True

            result["seo_score"] += 20

        # Check BBB
        if "bbb.org" in html:

            result["bbb_found"] = True

            result["seo_score"] += 20

        # Check Google Reviews
        if (
            "google.com/maps"
            in html
            or "g.page" in html
        ):

            result["google_reviews_found"] = True

            result["seo_score"] += 20

        # Check Facebook Reviews
        if "facebook.com" in html:

            result["facebook_reviews_found"] = True

            result["seo_score"] += 20

        # Check Yelp
        if "yelp.com" in html:

            result["yelp_found"] = True

            result["seo_score"] += 20

        # Check Review Schema
        if (
            "aggregaterating" in html
            or "\"review\"" in html
        ):

            result["review_schema_found"] = True

        # Final status
        if result["seo_score"] >= 80:

            result["status"] = "Excellent"

        elif result["seo_score"] >= 60:

            result["status"] = "Good"

        elif result["seo_score"] >= 40:

            result["status"] = "Average"

        elif result["seo_score"] > 0:

            result["status"] = "Poor"

        else:

            result["status"] = "No Reputation Signals"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result


if __name__ == "__main__":

    context = {
        "url": "https://www.python.org"
    }

    report = check_site_reputation(context)

    print(report)
    # nitin