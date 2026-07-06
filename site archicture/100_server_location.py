"""
Factor 100: Server Location

Checks the geographical location of the website server.
"""

import socket
import requests
from urllib.parse import urlparse


def check_server_location(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "100 - Server Location",
        "hostname": None,
        "ip_address": None,
        "country": None,
        "region": None,
        "city": None,
        "timezone": None,
        "isp": None,
        "status": "Failed"
    }

    try:

        # Extract hostname
        hostname = urlparse(url).netloc

        result["hostname"] = hostname

        # Resolve IP address
        ip_address = socket.gethostbyname(hostname)

        result["ip_address"] = ip_address

        # Query geolocation service
        response = requests.get(
            f"http://ip-api.com/json/{ip_address}",
            timeout=10
        )

        data = response.json()

        if data.get("status") == "success":

            result["country"] = data.get("country")
            result["region"] = data.get("regionName")
            result["city"] = data.get("city")
            result["timezone"] = data.get("timezone")
            result["isp"] = data.get("isp")
            result["status"] = "Success"

        else:

            result["error"] = "Unable to determine server location."

    except Exception as error:

        result["error"] = str(error)

    return result


if __name__ == "__main__":

    context = {
        "url": "https://www.python.org"
    }

    report = check_server_location(context)

    print(report)
    # nitin