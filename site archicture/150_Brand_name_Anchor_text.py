'''
Brand Name Anchor Text:
Receiving backlinks containing your exact business name.
'''

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# Function to check whether a webpage contains brand-name anchor text
def check_brand_anchor_text(context):

    # Read website URL from the shared context
    page_url = context["url"]

    # Extract the domain from the website URL
    target_domain = urlparse(page_url).netloc.lower()

    # Try to get the brand name from the context
    brand_name = context.get("brand_name")

    # If brand name is not provided, derive it from the domain name
    
    if not brand_name:
        domain = target_domain.replace("www.", "")
        brand_name = domain.split(".")[0]

    # Initialize the result dictionary
    result = {
        "factor": "Brand Name Anchor Text",
        "status": "Bad",
        "total_links": 0,
        "brand_anchor_links": 0,
        "links": []
    }

    try:

        # Send a GET request to the webpage
        response = requests.get(
            page_url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        # Raise an exception if the request fails
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all anchor (<a>) tags containing href attributes
        for link in soup.find_all("a", href=True):

            # Extract the anchor text
            anchor = link.get_text(strip=True)

            # Convert relative URLs into absolute URLs
            href = urljoin(page_url, link["href"])

            # Check whether the link points to the same target domain
            if target_domain in urlparse(href).netloc.lower():

                # Count links pointing to the target domain
                result["total_links"] += 1

                # Check whether the anchor text contains the brand name
                if brand_name.lower() in anchor.lower():

                    # Count brand anchor links
                    result["brand_anchor_links"] += 1

                    # Store matching link information
                    result["links"].append({
                        "anchor": anchor,
                        "url": href
                    })

        # Update the status if any brand anchor links are found
        if result["brand_anchor_links"] > 0:
            result["status"] = "Good"

    except Exception as e:

        # Store error details if an exception occurs
        result["status"] = "Error"
        result["error"] = str(e)

    # Return the final result
    return result


# ---------------------------------------------------
# Individual Testing
# ---------------------------------------------------
if __name__ == "__main__":

    # Take website URL as input from the user
    url = input("Enter Website URL: ").strip()

    # Create the context dictionary
    context = {
        "url": url
    }

    # Execute the Brand Name Anchor Text checker
    result = check_brand_anchor_text(context)

    # Display the final result
    print("\n========== RESULT ==========")
    print(f"Factor              : {result['factor']}")
    print(f"Status              : {result['status']}")
    print(f"Target Domain Links : {result['total_links']}")
    print(f"Brand Anchor Links  : {result['brand_anchor_links']}")

    # Display matching links if found
    if result["links"]:

        print("\nMatching Links:")

        for i, link in enumerate(result["links"], 1):

            print(f"\n{i}. Anchor : {link['anchor']}")
            print(f"   URL      : {link['url']}")

    # Display the error message if any
    if "error" in result:

        print("\nError:", result["error"])