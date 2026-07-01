'''
Official LinkedIn Company Page Checker:
Detects whether a website contains a link to a LinkedIn company page.
'''

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# Function: checks LinkedIn company page presence on a website
def check_linkedin_page(context):

    # Get website URL from shared context (from main.py)
    page_url = context["url"]

    try:
        # Send HTTP request to fetch website HTML content
        response = requests.get(
            page_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        # Raise error if request fails (404, 403, etc.)
        response.raise_for_status()

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Flag to track LinkedIn company page presence
        linkedin_found = False

        # Loop through all anchor tags (<a href="...">)
        for link in soup.find_all("a", href=True):

            # Convert relative URLs to absolute URLs
            href = urljoin(page_url, link["href"])

            # Detect LinkedIn company page links
            if "linkedin.com/company" in href.lower():
                linkedin_found = True
                break

        # Decide final status based on detection
        if linkedin_found:
            status = "Found"
        else:
            status = "Not Found"

    except Exception as e:
        # Handle errors like network issues or invalid URL
        return {
            "factor": "Official LinkedIn Company Page",
            "status": "Error",
            "error": str(e)
        }

    # Return final structured result
    return {
        "factor": "Official LinkedIn Company Page",
        "status": status
    }


# ---------------------------------------------------
# Individual Testing (run file directly)
# ---------------------------------------------------
if __name__ == "__main__":

    print("\n===== LINKEDIN COMPANY PAGE CHECKER =====\n")

    # Take website URL input from user
    url = input("Enter Website URL: ").strip()

    # Create context for plugin system
    context = {
        "url": url
    }

    # Run the checker function
    result = check_linkedin_page(context)

    # Print clean output
    print("\n========== RESULT ==========")
    print(f"Factor : {result['factor']}")
    print(f"Status : {result['status']}")

    # Show error only if something went wrong
    if "error" in result:
        print("\nError:", result["error"])