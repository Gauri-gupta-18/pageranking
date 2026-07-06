"""
Brand & Sentiment Signals

Metric:
Active Customer Story Publishing
"""

from urllib.parse import urlparse


CUSTOMER_SIGNALS = {

    "case study": 20,

    "customer story": 20,

    "success story": 15,

    "testimonial": 10,

    "customer interview": 15,

    "client story": 10,

    "customer video": 10,

    "implementation": 15

}


def extract_brand_name(url):

    domain = urlparse(url).netloc

    domain = domain.replace("www.", "")

    return domain.split(".")[0].title()


def fetch_customer_content(brand):

    """
    Demo data.

    Replace later with:

    Google Search API
    SerpAPI
    Bing API
    News API
    """

    return [

        f"{brand} case study with Microsoft",

        f"{brand} customer story featuring Walmart",

        f"{brand} implementation success story",

        f"{brand} publishes customer testimonial",

        f"{brand} launches new AI feature"

    ]


def calculate_score(records):

    score = 0

    matched = []

    for record in records:

        text = record.lower()

        for keyword, weight in CUSTOMER_SIGNALS.items():

            if keyword in text:

                score += weight

                matched.append(record)

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


def check_active_customer_story_publishing(context):

    url = context.get("url", "")

    if not url:

        return {

            "factor": "Active Customer Story Publishing",

            "status": "Error",

            "reason": "Website URL missing"

        }

    brand = extract_brand_name(url)

    records = fetch_customer_content(brand)

    score, matched = calculate_score(records)

    return {

        "factor": "Active Customer Story Publishing",

        "status": get_rating(score),

        "score": score,

        "brand": brand,

        "customer_story_count": len(matched),

        "stories_found": matched,

        "recommendation":

            "Publish more case studies, customer success stories, testimonials, and implementation stories to improve AI visibility."

    }
#dev 