"""
Factor 103: On-Site Duplicate Meta Info

Checks duplicate titles and meta descriptions across internal pages.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def check_duplicate_meta_info(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "103 - On-Site Duplicate Meta Info",
        "pages_crawled": 0,
        "duplicate_titles": [],
        "duplicate_meta_descriptions": [],
        "seo_score": 100,
        "status": "Success"
    }

    try:

        # Fetch homepage
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        if response.status_code != 200:
            result["error"] = f"Status Code {response.status_code}"
            result["status"] = "Failed"
            return result

        soup = BeautifulSoup(response.text, "html.parser")

        base_domain = urlparse(url).netloc

        internal_links = set()

        # Collect internal links
        for link in soup.find_all("a", href=True):

            full_url = urljoin(url, link["href"])

            if urlparse(full_url).netloc == base_domain:
                internal_links.add(full_url)

        # Limit crawl
        internal_links = list(internal_links)[:20]

        title_map = {}
        meta_map = {}

        # Crawl pages
        for page in internal_links:

            try:

                page_response = requests.get(
                    page,
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=10
                )

                if page_response.status_code != 200:
                    continue

                result["pages_crawled"] += 1

                page_soup = BeautifulSoup(
                    page_response.text,
                    "html.parser"
                )

                # Get title
                title = ""

                if page_soup.title:
                    title = page_soup.title.get_text(strip=True)

                if title:

                    title_map.setdefault(
                        title,
                        []
                    ).append(page)

                # Get meta description
                meta = page_soup.find(
                    "meta",
                    attrs={"name": "description"}
                )

                if meta:

                    description = meta.get(
                        "content",
                        ""
                    ).strip()

                    if description:

                        meta_map.setdefault(
                            description,
                            []
                        ).append(page)

            except Exception:
                continue

        # Find duplicate titles
        for title, pages in title_map.items():

            if len(pages) > 1:

                result["duplicate_titles"].append(
                    {
                        "title": title,
                        "pages": pages
                    }
                )

                result["seo_score"] -= 10

        # Find duplicate descriptions
        for description, pages in meta_map.items():

            if len(pages) > 1:

                result["duplicate_meta_descriptions"].append(
                    {
                        "description": description,
                        "pages": pages
                    }
                )

                result["seo_score"] -= 10

        # Minimum score
        if result["seo_score"] < 0:
            result["seo_score"] = 0

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

        result["status"] = "Failed"

    return result


if __name__ == "__main__":

    context = {
        "url": "https://www.python.org"
    }

    report = check_duplicate_meta_info(context)

    print(report)
    # nitin