# Factor 12 - Bulleted Lists for "Best of" Queries

import requests
from bs4 import BeautifulSoup

def check_bulleted_list(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # check if any heading contains "best" or "top"
        headings = soup.find_all(['h1', 'h2', 'h3'])
        has_best_heading = any(
            'best' in h.get_text().lower() or 'top' in h.get_text().lower()
            for h in headings
        )
        
        # check if page has unordered list with at least 3 items
        ul_tags = soup.find_all('ul')
        has_good_list = any(len(ul.find_all('li')) >= 3 for ul in ul_tags)
        
        if has_best_heading and has_good_list:
            return {
                "factor": "Bulleted Lists for Best of Queries",
                "score": 1.0,
                "status": "Best of heading and bullet list both found"
            }
        elif has_good_list:
            return {
                "factor": "Bulleted Lists for Best of Queries",
                "score": 0.5,
                "status": "Bullet list found but no best of heading"
            }
        
        return {
            "factor": "Bulleted Lists for Best of Queries",
            "score": 0.0,
            "status": "No bullet list found"
        }
    
    except Exception as e:
        return {
            "factor": "Bulleted Lists for Best of Queries",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        } 
