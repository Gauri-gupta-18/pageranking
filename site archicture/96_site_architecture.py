"""
Factor 96: Site Architecture

Checks the website hierarchy by analyzing internal links.
A good site should have a clear structure:
Homepage -> Category -> Subcategory
"""

from pathlib import Path

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def _load_html(source):
    """Load HTML from a web URL or a local file path."""

    if source.startswith(("http://", "https://")):
        response = requests.get(
            source,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )

        if response.status_code != 200:
            raise requests.RequestException(
                f"Website returned status {response.status_code}"
            )

        return response.text

    local_path = Path(source)
    if not local_path.is_file():
        raise FileNotFoundError(f"Local file not found: {source}")

    return local_path.read_text(encoding="utf-8")


def check_site_architecture(source):
    """
    Analyze website architecture.

    Args:
        source (str): Website URL or local HTML file path

    Returns:
        dict: Site architecture report
    """

    result = {
        "factor": "96 - Site Architecture",
        "homepage": source,
        "internal_pages": [],
        "total_internal_pages": 0,
        "architecture_status": "Poor"
    }

    try:
        html_content = _load_html(source)

        # Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Get current website domain
        base_domain = urlparse(source).netloc

        # Find all links
        links = soup.find_all("a", href=True)

        internal_links = set()

        for link in links:
            href = link["href"]

            # Convert relative URLs to complete URLs
            full_url = urljoin(source, href)

            # Check if the link belongs to the same website
            if urlparse(full_url).netloc == base_domain:
                internal_links.add(full_url)

        # Save internal links
        result["internal_pages"] = list(internal_links)
        result["total_internal_pages"] = len(internal_links)

        # Basic architecture evaluation
        if len(internal_links) >= 10:
            result["architecture_status"] = "Good"
        elif len(internal_links) >= 5:
            result["architecture_status"] = "Average"
        else:
            result["architecture_status"] = "Poor"

        return result

    except (requests.exceptions.RequestException, FileNotFoundError, OSError) as error:
        result["error"] = str(error)
        return result


# Test this file independently
if __name__ == "__main__":

    website = "https://random.tastemaker.design/"

    report = check_site_architecture(website)

    print(report)
    # nitin