"""
Factor 67: Sitemap Freshness

Checks whether the website sitemap is present
and whether it appears to be recently updated.

Analyzes:
1. Presence of sitemap.xml
2. Number of URLs in sitemap
3. Latest <lastmod> date
4. Sitemap freshness
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime


def check_sitemap_freshness(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "67 - Sitemap Freshness",
        "sitemap_found": False,
        "sitemap_url": "",
        "total_urls": 0,
        "latest_lastmod": None,
        "fresh": False,
        "recommendation": "",
        "status": "Failed"
    }

    try:

        sitemap_url = urljoin(url, "/sitemap.xml")
        result["sitemap_url"] = sitemap_url

        response = requests.get(
            sitemap_url,
            headers={
                "User-Agent": "Mozilla/5.0 SEO Analyzer Bot"
            },
            timeout=10
        )

        if response.status_code != 200:

            result["error"] = (
                f"Sitemap returned status code "
                f"{response.status_code}"
            )

            return result

        result["sitemap_found"] = True

        soup = BeautifulSoup(
            response.text,
            "xml"
        )

        urls = soup.find_all("url")
        result["total_urls"] = len(urls)

        lastmod_dates = []

        for url_tag in urls:

            lastmod = url_tag.find("lastmod")

            if lastmod and lastmod.text.strip():

                date_text = lastmod.text.strip()

                try:

                    # Handle ISO timestamps
                    date = datetime.fromisoformat(
                        date_text.replace("Z", "+00:00")
                    )

                    lastmod_dates.append(date)

                except Exception:
                    pass

        if lastmod_dates:

            latest = max(lastmod_dates)

            result["latest_lastmod"] = (
                latest.strftime("%Y-%m-%d")
            )

            days_old = (
                datetime.now(latest.tzinfo) - latest
            ).days

            if days_old <= 30:

                result["fresh"] = True

                result["recommendation"] = (
                    "Sitemap appears to be recently updated."
                )

            else:

                result["recommendation"] = (
                    f"Sitemap was last updated "
                    f"{days_old} days ago."
                )

        else:

            result["recommendation"] = (
                "No <lastmod> dates found in sitemap."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result