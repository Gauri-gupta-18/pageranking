# 
"""
Factor 98: Presence of Sitemap

Checks XML and HTML sitemaps.
Sitemaps help search engines crawl website pages efficiently.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}


def check_sitemap_availability(url):
    """
    Check whether a website has XML or HTML sitemap.
    """

    result = {
        "factor": "98 - Presence of Sitemap",
        "xml_sitemap_found": False,
        "html_sitemap_found": False,
        "xml_sitemap_url": None,
        "html_sitemap_url": None,
        "status": "Failed"
    }

    try:
        # Remove extra slash problems
        base_url = url.rstrip("/")

        # -----------------------------
        # Check common XML sitemap URLs
        # -----------------------------
        xml_locations = [
            "/sitemap.xml",
            "/sitemap_index.xml",
            "/sitemap-index.xml"
        ]

        for location in xml_locations:

            sitemap_url = base_url + location

            response = requests.get(
                sitemap_url,
                headers=HEADERS,
                timeout=10
            )

            if response.status_code == 200:
                if "xml" in response.text.lower() or "urlset" in response.text.lower():
                    result["xml_sitemap_found"] = True
                    result["xml_sitemap_url"] = sitemap_url
                    break


        # -----------------------------
        # Check robots.txt for sitemap
        # -----------------------------
        if not result["xml_sitemap_found"]:

            robots_url = base_url + "/robots.txt"

            response = requests.get(
                robots_url,
                headers=HEADERS,
                timeout=10
            )

            if response.status_code == 200:

                lines = response.text.splitlines()

                for line in lines:

                    if line.lower().startswith("sitemap:"):

                        sitemap_url = line.split(":", 1)[1].strip()

                        result["xml_sitemap_found"] = True
                        result["xml_sitemap_url"] = sitemap_url
                        break


        # -----------------------------
        # Check HTML sitemap
        # -----------------------------
        response = requests.get(
            base_url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            links = soup.find_all("a", href=True)

            for link in links:

                text = link.get_text(strip=True).lower()
                href = link["href"].lower()

                if "sitemap" in text or "sitemap" in href or "site map" in text:

                    result["html_sitemap_found"] = True

                    result["html_sitemap_url"] = urljoin(
                        base_url,
                        link["href"]
                    )

                    break


        # Final result
        if result["xml_sitemap_found"] or result["html_sitemap_found"]:

            result["status"] = "Success"

        else:

            result["message"] = "No sitemap found"


    except requests.exceptions.RequestException as error:

        result["error"] = str(error)


    return result


# Independent testing
if __name__ == "__main__":

    websites = [
        "https://www.python.org",
        "https://www.wikipedia.org",
        "https://www.microsoft.com",
        "https://github.com"
    ]

    for website in websites:

        print("\nChecking:", website)

        report = check_sitemap_availability(website)

        print(report)
        # nitin