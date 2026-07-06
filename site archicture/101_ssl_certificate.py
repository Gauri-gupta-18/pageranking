"""
Factor 101: SSL Certificate (HTTPS)

Checks whether the website uses HTTPS and has a valid SSL certificate.
"""

import ssl
import socket
from urllib.parse import urlparse


def check_ssl_certificate(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "101 - SSL Certificate (HTTPS)",
        "https_enabled": False,
        "ssl_certificate_found": False,
        "certificate_issuer": None,
        "certificate_expiry": None,
        "status": "Failed"
    }

    try:

        # Parse URL
        parsed_url = urlparse(url)

        # Extract hostname
        hostname = parsed_url.netloc

        # Check HTTPS
        if parsed_url.scheme == "https":
            result["https_enabled"] = True

        # Create SSL context
        context_ssl = ssl.create_default_context()

        # Connect to server
        with socket.create_connection(
            (hostname, 443),
            timeout=5
        ) as sock:

            # Wrap socket with SSL
            with context_ssl.wrap_socket(
                sock,
                server_hostname=hostname
            ) as secure_socket:

                # Get certificate
                certificate = secure_socket.getpeercert()

                if certificate:

                    result["ssl_certificate_found"] = True

                    # Get certificate issuer
                    issuer = certificate.get("issuer", [])

                    issuer_name = []

                    for item in issuer:
                        for key, value in item:
                            issuer_name.append(value)

                    result["certificate_issuer"] = ", ".join(issuer_name)

                    # Get expiry date
                    result["certificate_expiry"] = certificate.get("notAfter")

                    result["status"] = "Success"

    except Exception as error:

        result["error"] = str(error)

    return result


if __name__ == "__main__":

    context = {
        "url": "https://www.python.org"
    }

    report = check_ssl_certificate(context)

    print(report)
    # nitin