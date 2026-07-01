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

        elif str(current_year - 1) in years:
            result["update_status"] = "Possibly Updated"

        else:
            result["update_status"] = "No Recent Updates Found"

        # Mark success
        result["status"] = "Success"

        return result

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

        return result


if __name__ == "__main__":

    website = "https://www.python.org"

    report = check_site_updates(
        website
    )

    print(report)
    # nitin