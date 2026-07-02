from urllib.parse import urlparse


NEGATIVE_KEYWORDS = {

    "lawsuit": 20,
    "fraud": 25,
    "scam": 25,
    "hack": 20,
    "data breach": 30,
    "privacy": 15,
    "penalty": 15,
    "fine": 15,
    "investigation": 15,
    "recall": 20,
    "bankruptcy": 30,
    "layoffs": 10,
    "complaint": 10,
    "poor": 5,
    "negative": 5

}


def extract_brand_name(url):

    domain = urlparse(url).netloc

    domain = domain.replace("www.", "")

    return domain.split(".")[0].title()


def fetch_news(brand):
    """
    Replace this later with:
    Google Search API
    SerpAPI
    Bing API
    NewsAPI

    Returns article headlines.
    """

    return [

        f"{brand} launches new AI laptop",

        f"{brand} faces privacy investigation",

        f"{brand} receives positive customer reviews",

        f"{brand} announces record quarterly revenue",

        f"{brand} hit with lawsuit over warranty claims"

    ]


def analyze_negative_articles(headlines):

    matched_articles = []

    severity = 0

    for article in headlines:

        lower = article.lower()

        for keyword, weight in NEGATIVE_KEYWORDS.items():

            if keyword in lower:

                severity += weight

                matched_articles.append(article)

                break

    return severity, matched_articles


def calculate_score(severity):

    score = max(0, 100 - severity)

    return score


def get_rating(score):

    if score >= 90:

        return "Excellent"

    elif score >= 75:

        return "Good"

    elif score >= 60:

        return "Average"

    elif score >= 40:

        return "Poor"

    else:

        return "Critical"


def check_record_negative_coverage(context):

    url = context.get("url", "")

    if not url:

        return {

            "factor": "Record Negative Coverage",

            "status": "Error",

            "reason": "Website URL missing"

        }

    brand = extract_brand_name(url)

    headlines = fetch_news(brand)

    severity, negative_articles = analyze_negative_articles(headlines)

    score = calculate_score(severity)

    return {

        "factor": "Record Negative Coverage",

        "status": get_rating(score),

        "score": score,

        "brand": brand,

        "negative_article_count": len(negative_articles),

        "severity_score": severity,

        "negative_articles": negative_articles,

        "recommendation":

            "Publish authoritative positive content and address high-profile negative stories."

    }
#dev