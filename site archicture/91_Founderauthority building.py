"""
Brand & Sentiment Signals

Metric:
Founder Authority Building
"""

from urllib.parse import urlparse


AUTHORITY_SIGNALS = {

    "podcast": 20,

    "interview": 15,

    "conference": 20,

    "speaker": 20,

    "quote": 10,

    "guest blog": 10,

    "linkedin": 5,

    "forbes": 15,

    "techcrunch": 15,

    "youtube": 10

}


def extract_brand_name(url):

    domain = urlparse(url).netloc

    domain = domain.replace("www.", "")

    return domain.split(".")[0].title()


def fetch_founder_content(brand):

    """
    Demo Data

    Replace later using:

    Google Search API

    Bing Search API

    SerpAPI

    News API

    YouTube API

    LinkedIn API
    """

    return [

        f"{brand} founder interviewed on popular podcast",

        f"{brand} founder keynote conference speaker",

        f"{brand} founder quoted by Forbes",

        f"{brand} founder shares insights on LinkedIn",

        f"{brand} launches new AI product"

    ]


def calculate_authority(records):

    score = 0

    matched = []

    for item in records:

        text = item.lower()

        for keyword, weight in AUTHORITY_SIGNALS.items():

            if keyword in text:

                score += weight

                matched.append(item)

                break

    return min(score, 100), matched


def get_rating(score):

    if score >= 90:

        return "Excellent"

    elif score >= 75:

        return "Very Good"

    elif score >= 60:

        return "Good"

    elif score >= 40:

        return "Average"

    elif score >= 20:

        return "Poor"

    return "Critical"


def check_founder_authority_building(context):

    url = context.get("url", "")

    if not url:

        return {

            "factor": "Founder Authority Building",

            "status": "Error",

            "reason": "Website URL missing"

        }

    brand = extract_brand_name(url)

    records = fetch_founder_content(brand)

    score, matched = calculate_authority(records)

    return {

        "factor": "Founder Authority Building",

        "status": get_rating(score),

        "score": score,

        "brand": brand,

        "authority_signals_found": len(matched),

        "signals": matched,

        "recommendation":

            "Increase founder visibility through podcasts, interviews, keynote talks, guest articles, and media quotes."

    }
#dev