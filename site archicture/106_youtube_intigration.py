"""
Factor 106: YouTube Integration

Checks whether the website integrates YouTube content.
"""

import requests
from bs4 import BeautifulSoup


def check_youtube_integration(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "106 - YouTube Integration",
        "youtube_embed_found": False,
        "youtube_link_found": False,
        "youtube_links": [],
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

        # Check iframe embeds
        iframes = soup.find_all("iframe")

        for iframe in iframes:

            src = iframe.get("src", "").lower()

            if (
                "youtube.com" in src
                or "youtu.be" in src
            ):

                result["youtube_embed_found"] = True

                result["youtube_links"].append(src)

        # Check anchor links
        links = soup.find_all(
            "a",
            href=True
        )

        for link in links:

            href = link["href"].lower()

            if (
                "youtube.com" in href
                or "youtu.be" in href
            ):

                result["youtube_link_found"] = True

                result["youtube_links"].append(href)

        # Remove duplicates
        result["youtube_links"] = list(
            set(result["youtube_links"])
        )

        # Calculate SEO score
        if result["youtube_embed_found"]:

            result["seo_score"] += 70

        if result["youtube_link_found"]:

            result["seo_score"] += 30

        # Final status
        if result["seo_score"] == 100:

            result["status"] = "Excellent"

        elif result["seo_score"] >= 70:

            result["status"] = "Good"

        elif result["seo_score"] > 0:

            result["status"] = "Average"

        else:

            result["status"] = "Poor"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result


if __name__ == "__main__":

    context = {
        "url": "https://www.python.org"
    }

    report = check_youtube_integration(context)

    print(report)
    # nitin