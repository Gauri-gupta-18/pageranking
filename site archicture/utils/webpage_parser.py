"""

Webpage Parser Utility


Purpose:
--------
Downloads a webpage and extracts clean visible text
for all content evaluation metrics.

Author : Mayank

"""

import requests
from bs4 import BeautifulSoup


def fetch_webpage_content(url: str):

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "noscript",
            "svg",
            "header",
            "footer"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

      
        return {
            "html": response.text,
            "text": text
        }

    except Exception:

        return {
            "html": "",
            "text": ""
        }