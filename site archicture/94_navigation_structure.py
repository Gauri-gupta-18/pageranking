"""                                             #nitin
Factor 94: Website Architecture and Navigation Structure

This module checks a website's navigation structure.

It analyzes:
1. Presence of <nav> tag
2. Navigation links
3. Internal and external links
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def check_navigation_structure(url):

    # Dictionary to store final result
    result = {
        "factor": "94 - Website Architecture and Navigation",
        "navigation_found": False,
        "total_navigation_links": 0,
        "internal_links": [],
        "external_links": [],
        "seo_score": 0,
        "status": "Failed"
    }

    try:

        # Send HTTP request to website
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 SEO Analyzer Bot"
            },
            timeout=10
        )

        # Check if request is successful
        if response.status_code != 200:
            result["error"] = (
                f"Website returned status code {response.status_code}"
            )
            return result

        # Parse HTML content
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find navigation section
        nav = soup.find("nav")

        if nav:

            result["navigation_found"] = True

            # Extract all links inside navigation
            links = nav.find_all(
                "a",
                href=True
            )

            # Get current website domain
            base_domain = urlparse(url).netloc

            for link in links:

                # Convert relative URL to absolute URL
                full_url = urljoin(
                    url,
                    link["href"]
                )

                # Extract domain
                link_domain = urlparse(
                    full_url
                ).netloc

                # Check internal/external
                if link_domain == base_domain:

                    result["internal_links"].append(
                        full_url
                    )

                else:

                    result["external_links"].append(
                        full_url
                    )

            # Count links
            result["total_navigation_links"] = len(
                links
            )

        else:

            result["message"] = "No <nav> tag found"

        # ==========================
        # Calculate SEO Score
        # ==========================

        score = 0

        # Navigation exists
        if result["navigation_found"]:
            score += 40

        # Internal navigation links
        internal_count = len(result["internal_links"])

        if internal_count >= 10:
            score += 40

        elif internal_count >= 5:
            score += 30

        elif internal_count >= 2:
            score += 20

        elif internal_count >= 1:
            score += 10

        # External navigation links
        external_count = len(result["external_links"])

        if external_count <= 3:
            score += 20

        elif external_count <= 5:
            score += 10

        result["seo_score"] = score

        # Final Status
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

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

        result["status"] = "Error"

    return result


if __name__ == "__main__":

    website = "https://www.wikipedia.org"

    report = check_navigation_structure(
        website
    )

    print(report)