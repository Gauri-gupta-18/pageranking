"""
Factor 97: Site Updates

Checks whether the site shows signs of regular updates.
"""

import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def check_site_updates(url):

    result = {
        "factor": "97 - Site Updates",
        "last_modified": None,
        "recent_dates_found": [],
        "seo_score": 0,
        "update_status": "Unknown",
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
            result["error"] = f"Status code {response.status_code}"
            return result

        # Read Last-Modified header
        last_modified = response.headers.get("Last-Modified")

        if last_modified:
            result["last_modified"] = last_modified

        # Parse HTML
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Get page text
        page_text = soup.get_text(
            " ",
            strip=True
        )

        # Find years
        years = re.findall(
            r"\b20\d{2}\b",
            page_text
        )

        # Remove duplicates
        years = sorted(
            set(years),
            reverse=True
        )

        # Save recent years
        result["recent_dates_found"] = years[:5]

        # Get current year
        current_year = datetime.now().year

        # Check freshness
        if str(current_year) in years:

            result["update_status"] = "Recently Updated"

            result["seo_score"] = 100

        elif str(current_year - 1) in years:

            result["update_status"] = "Possibly Updated"

            result["seo_score"] = 80

        elif str(current_year - 2) in years:

            result["update_status"] = "Updated Within Two Years"

            result["seo_score"] = 60

        elif years:

            result["update_status"] = "Old Content"

            result["seo_score"] = 40

        else:

            result["update_status"] = "No Recent Updates Found"

            result["seo_score"] = 20

        # Final Status
        score = result["seo_score"]

        if score >= 90:

            result["status"] = "Excellent"

        elif score >= 70:

            result["status"] = "Good"

        elif score >= 50:

            result["status"] = "Average"

        elif score > 0:

            result["status"] = "Poor"

        else:

            result["status"] = "Failed"

        return result

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

        result["status"] = "Error"

        return result


if __name__ == "__main__":

    website = "https://www.python.org"

    report = check_site_updates(
        website
    )

    print(report)
    # nitin