"""
Factor 49: Linking Domain Age

Checks the creation date of the target domain using WHOIS records.
Older, established domains pass more trust and authority.
"""

from datetime import datetime
from urllib.parse import urlparse
import whois


def check_domain_age(context):
    # Get website URL
    url = context["url"]

    result = {
        "factor": "49 - Linking Domain Age",
        "domain_age_years": 0.0,
        "creation_date": None,
        "seo_score": 0,
        "status": "Failed",
    }

    try:
        # Clean the URL to extract just the root domain
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith("www."):
            domain = domain[4:]

        if not domain:
            result["error"] = "Invalid URL format"
            return result

        # Query public WHOIS registry
        try:
            if hasattr(whois, "whois"):
                domain_info = whois.whois(domain)
                creation_date = domain_info.creation_date
            elif hasattr(whois, "query"):
                domain_info = whois.query(domain)
                creation_date = getattr(domain_info, "creation_date", None)
            else:
                result["error"] = (
                    "Unsupported whois package API: neither whois() nor query() is available"
                )
                result["status"] = "Error"
                return result
        except FileNotFoundError as error:
            result["error"] = (
                "WHOIS lookup failed: system WHOIS command not found on this machine"
            )
            result["status"] = "Unavailable"
            return result
        except OSError as error:
            if error.winerror == 2:
                result["error"] = (
                    "WHOIS lookup failed: system WHOIS command not found on this machine"
                )
            else:
                result["error"] = str(error)
            result["status"] = "Unavailable"
            return result

        # WHOIS response can return a list or a single datetime object
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if not creation_date:
            result["error"] = "Could not parse domain creation date from registry"
            result["status"] = "Unknown"
            return result

        # Calculate exact age in years
        age_days = (datetime.now() - creation_date).days
        age_years = round(age_days / 365.25, 2)

        result["domain_age_years"] = age_years
        result["creation_date"] = str(creation_date.date())

        # Score assignment based on age bracket milestones
        if age_years >= 10:
            result["seo_score"] = 100
            result["status"] = "Excellent (Legacy Trust)"
        elif age_years >= 5:
            result["seo_score"] = 90
            result["status"] = "Excellent"
        elif age_years >= 2:
            result["seo_score"] = 75
            result["status"] = "Good"
        elif age_years >= 1:
            result["seo_score"] = 50
            result["status"] = "Average"
        else:
            result["seo_score"] = 20
            result["status"] = "Poor (Brand New Domain)"

    except Exception as error:
        result["error"] = str(error)
        result["status"] = "Error"

    return result


if __name__ == "__main__":
    context = {"url": "https://www.python.org"}

    report = check_domain_age(context)
    print(report)
    # nitin