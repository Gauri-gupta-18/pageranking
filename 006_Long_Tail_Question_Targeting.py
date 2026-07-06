# Factor 6 - Long Tail Question Targeting

import requests
from bs4 import BeautifulSoup

def check_long_tail_questions(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # extract all headings
        headings = soup.find_all(['h1', 'h2', 'h3'])
        
        if not headings:
            return {
                "factor": "Long Tail Question Targeting",
                "score": 0.0,
                "status": "No headings found"
            }
        
        # count headings that are 5-10 words long
        long_tail_count = sum(1 for h in headings if 5 <= len(h.get_text().strip().split()) <= 10)
        ratio = long_tail_count / len(headings)
        
        if ratio >= 0.5:
            return {
                "factor": "Long Tail Question Targeting",
                "score": 1.0,
                "status": f"{long_tail_count} long tail headings found"
            }
        elif ratio >= 0.2:
            return {
                "factor": "Long Tail Question Targeting",
                "score": 0.5,
                "status": f"{long_tail_count} long tail headings found"
            }
        
        return {
            "factor": "Long Tail Question Targeting",
            "score": 0.0,
            "status": "Mostly short head keywords found"
        }
    
    except Exception as e:
        return {
            "factor": "Long Tail Question Targeting",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }