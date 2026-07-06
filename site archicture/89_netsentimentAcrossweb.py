"""
Brand Sentiment Signal

Metric:
Net Sentiment Across Web
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()


def extract_brand_name(url):

    domain = urlparse(url).netloc

    domain = domain.replace("www.", "")

    return domain.split(".")[0].title()


def search_brand_mentions(brand):

    """
    Dummy implementation.

    Replace this function later using:

    Google Custom Search API
    SerpAPI
    NewsAPI
    Reddit API
    Bing Search API

    Returns list of text snippets.
    """

    snippets = [

        f"{brand} provides excellent customer service.",

        f"I love using {brand}.",

        f"{brand} has good pricing.",

        f"{brand} website loads slowly.",

        f"{brand} support is poor.",

        f"{brand} is reliable.",

        f"{brand} is recommended by users.",

        f"{brand} quality is amazing."

    ]

    return snippets


def analyze_sentiment(snippets):

    positive = 0

    neutral = 0

    negative = 0


    for text in snippets:

        score = analyzer.polarity_scores(text)["compound"]

        if score >= 0.05:

            positive += 1

        elif score <= -0.05:

            negative += 1

        else:

            neutral += 1


    total = positive + neutral + negative

    if total == 0:

        return positive, neutral, negative, 0


    net_score = (

        (positive - negative)

        / total

    ) * 100

    return (

        positive,

        neutral,

        negative,

        round(net_score, 2)

    )


def get_status(score):

    if score >= 70:

        return "Excellent"

    elif score >= 40:

        return "Good"

    elif score >= 10:

        return "Average"

    elif score >= 0:

        return "Weak"

    return "Negative"


def check_net_sentiment_across_web(context):

    url = context.get("url", "")

    if not url:

        return {

            "factor": "Net Sentiment Across Web",

            "status": "Error",

            "reason": "Website URL missing"

        }


    brand = extract_brand_name(url)

    snippets = search_brand_mentions(brand)

    positive, neutral, negative, score = analyze_sentiment(snippets)


    return {

        "factor": "Net Sentiment Across Web",

        "status": get_status(score),

        "brand": brand,

        "positive_mentions": positive,

        "neutral_mentions": neutral,

        "negative_mentions": negative,

        "net_sentiment_score": score,

        "total_mentions": len(snippets),

        "details": snippets

    }
#dev