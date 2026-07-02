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
        "seo_score": 0,
        "architecture_status": "Poor",
        "status": "Failed"
    }

    try:

        html_content = _load_html(source)

        # Parse HTML
        soup = BeautifulSoup(
            html_content,
            "html.parser"
        )

        # Get current website domain
        base_domain = urlparse(source).netloc

        # Find all links
        links = soup.find_all(
            "a",
            href=True
        )

        internal_links = set()

        for link in links:

            href = link["href"]

            # Convert relative URLs to complete URLs
            full_url = urljoin(
                source,
                href
            )

            # Check if link belongs to same domain
            if urlparse(full_url).netloc == base_domain:

                internal_links.add(full_url)

        # Save internal links
        result["internal_pages"] = list(internal_links)

        result["total_internal_pages"] = len(
            internal_links
        )

        # -----------------------------
        # Architecture Evaluation
        # -----------------------------
        if len(internal_links) >= 20:

            result["architecture_status"] = "Excellent"

            result["seo_score"] = 100

        elif len(internal_links) >= 15:

            result["architecture_status"] = "Good"

            result["seo_score"] = 80

        elif len(internal_links) >= 10:

            result["architecture_status"] = "Average"

            result["seo_score"] = 60

        elif len(internal_links) >= 5:

            result["architecture_status"] = "Poor"

            result["seo_score"] = 40

        else:

            result["architecture_status"] = "Very Poor"

            result["seo_score"] = 20

        # -----------------------------
        # Final Status
        # -----------------------------
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

    except (
        requests.exceptions.RequestException,
        FileNotFoundError,
        OSError
    ) as error:

        result["error"] = str(error)

        result["status"] = "Error"

        return result


# Test this file independently
if __name__ == "__main__":

    website = "https://random.tastemaker.design/"

    report = check_site_architecture(
        website
    )

    print(report)
    # nitin