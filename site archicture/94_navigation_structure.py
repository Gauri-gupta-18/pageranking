"""
Factor 94: Website Architecture and Navigation Structure:-This module checks a website's navigation structure.
It analyzes:
1. Presence of <nav> tag
2. Navigation links
3. Internal and external links
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def check_navigation_structure(url):

   # Fetch website HTML and analyze navigation structure.  Args: url (str): Website URL Returns: dict: Navigation analysis report

# Dictionary to store final result
    result = {
        "factor": "94 - Website Architecture and Navigation",
        "navigation_found": False,
        "total_navigation_links": 0,
        "internal_links": [],
        "external_links": [],
        "status": "Failed"
    }

    try:
        # Send HTTP request to website
        response = requests.get(url,headers={"User-Agent": "Mozilla/5.0 SEO Analyzer Bot"},timeout=10)

        # Check if request is successful
        if response.status_code != 200:
            result["error"] = (f"Website returned status code {response.status_code}")
            return result

        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        # Find navigation section
        nav = soup.find("nav")

        if nav:
            result["navigation_found"] = True
            # Extract all links inside navigation
            links = nav.find_all("a", href=True)
            # Get current website domain
            base_domain = urlparse(url).netloc

            for link in links:
                # Convert relative URL to absolute URL
                full_url = urljoin(url, link["href"])
                # Extract domain from link
                link_domain = urlparse(full_url).netloc
                # Check whether link is internal or external
                if link_domain == base_domain:
                    result["internal_links"].append(full_url)
                else:
                    result["external_links"].append(full_url)

            # Count total navigation links
            result["total_navigation_links"] = len(links)

            result["status"] = "Success"

        else:
            result["message"] = "No <nav> tag found"

    except requests.exceptions.RequestException as error:

        # Handle connection, timeout, and other request errors
        result["error"] = str(error)

    return result


if __name__ == "__main__":

    website = "https://www.wikipedia.org"

    report = check_navigation_structure(website)

    print(report)