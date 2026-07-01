"""
Factor 95: Domain Trust (TrustRank)

Checks basic trust signals of a domain:
- HTTPS enabled
- SSL certificate validity
- Security headers
"""

import ssl
import socket
import requests
from urllib.parse import urlparse


def check_domain_trust(source):
    """
    Analyze domain trust signals.

    Args:
        source (str): Website URL

    Returns:
        dict: Domain trust report
    """

    result = {
        "factor": "95 - Domain Trust (TrustRank)",
        "https_enabled": False,
        "ssl_valid": False,
        "security_headers": {},
        "trust_score": 0,
        "status": "Failed"
    }

    try:

        parsed_url = urlparse(source)

        hostname = parsed_url.netloc

        # -----------------------------
        # HTTPS Check
        # -----------------------------
        if parsed_url.scheme == "https":

            result["https_enabled"] = True

            result["trust_score"] += 30

        # -----------------------------
        # SSL Certificate Check
        # -----------------------------
        try:

            context = ssl.create_default_context()

            with socket.create_connection(
                (hostname, 443),
                timeout=5
            ) as sock:

                with context.wrap_socket(
                    sock,
                    server_hostname=hostname
                ) as secure_socket:

                    certificate = secure_socket.getpeercert()

                    if certificate:

                        result["ssl_valid"] = True

                        result["trust_score"] += 30

        except Exception:

            result["ssl_valid"] = False

        # -----------------------------
        # Security Headers Check
        # -----------------------------
        response = requests.get(
            source,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options"
        ]

        for header in security_headers:

            if header in response.headers:

                result["security_headers"][header] = True

                result["trust_score"] += 10

            else:

                result["security_headers"][header] = False

        # -----------------------------
        # Trust Evaluation
        # -----------------------------
        if result["trust_score"] >= 80:

            result["status"] = "High Trust"

        elif result["trust_score"] >= 50:

            result["status"] = "Medium Trust"

        else:

            result["status"] = "Low Trust"

        return result

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

        return result


# Test this file independently
if __name__ == "__main__":

    website = "https://www.python.org"

    report = check_domain_trust(website)

    print(report)
    # nitin