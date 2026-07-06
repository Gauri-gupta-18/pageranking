"""
Factor 71: Image Alt Text

Checks whether images on a webpage contain descriptive
alt attributes.

Analyzes:
1. Total number of images
2. Images with alt text
3. Images missing alt text
4. Percentage of images having alt text
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def check_image_alt_text(context):

    # Shared context
    url = context.get("url", "")
    keyword = context.get("keyword", "")
    keywords = context.get("keywords", [])
    competitor_url = context.get("competitor_url", "")

    result = {
        "factor": "71 - Image Alt Text",
        "total_images": 0,
        "images_with_alt": 0,
        "images_missing_alt": 0,
        "missing_alt_images": [],
        "alt_text_percentage": 0.0,
        "recommendation": "",
        "status": "Failed"
    }

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 SEO Analyzer Bot"
            },
            timeout=10
        )

        if response.status_code != 200:

            result["error"] = (
                f"Status code {response.status_code}"
            )

            return result

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        images = soup.find_all("img")

        total_images = len(images)

        images_with_alt = 0
        images_missing_alt = 0

        for image in images:

            alt = image.get("alt", "").strip()

            if alt:

                images_with_alt += 1

            else:

                images_missing_alt += 1

                image_src = image.get("src", "")

                if image_src:
                    result["missing_alt_images"].append(
                        urljoin(url, image_src)
                    )

        result["total_images"] = total_images
        result["images_with_alt"] = images_with_alt
        result["images_missing_alt"] = images_missing_alt

        if total_images > 0:

            result["alt_text_percentage"] = round(
                (images_with_alt / total_images) * 100,
                2
            )

        else:

            result["alt_text_percentage"] = 100.0

        if total_images == 0:

            result["recommendation"] = (
                "No images found on the page."
            )

        elif images_missing_alt == 0:

            result["recommendation"] = (
                "Excellent! Every image has descriptive alt text."
            )

        else:

            result["recommendation"] = (
                f"{images_missing_alt} of {total_images} image(s) "
                "are missing alt text. Add meaningful alt attributes "
                "to improve accessibility and SEO."
            )

        result["status"] = "Success"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result
