"""
Factor 99: Site Uptime

Checks the current availability of the website.
"""

import time
import requests


def check_site_uptime(context):

    # Get website URL
    url = context["url"]

    result = {
        "factor": "99 - Site Uptime",
        "website_available": False,
        "status_code": None,
        "response_time_ms": None,
        "uptime_status": "Unknown",
        "status": "Failed"
    }

    try:

        # Record start time
        start_time = time.time()

        # Send request
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        # Record end time
        end_time = time.time()

        # Calculate response time
        response_time = round(
            (end_time - start_time) * 1000,
            2
        )

        result["status_code"] = response.status_code
        result["response_time_ms"] = response_time

        # Check availability
        if response.status_code == 200:

            result["website_available"] = True

            if response_time < 1000:
                result["uptime_status"] = "Excellent"

            elif response_time < 3000:
                result["uptime_status"] = "Good"

            else:
                result["uptime_status"] = "Slow"

            result["status"] = "Success"

        else:

            result["uptime_status"] = "Website Down"

    except requests.exceptions.Timeout:

        result["uptime_status"] = "Request Timeout"

    except requests.exceptions.ConnectionError:

        result["uptime_status"] = "Connection Failed"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    return result


if __name__ == "__main__":

    context = {
        "url": "https://www.python.org"
    }

    report = check_site_uptime(context)

    print(report)
    # nitin