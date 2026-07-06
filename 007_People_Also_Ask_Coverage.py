# Factor 7 - People Also Ask Coverage

import requests
from bs4 import BeautifulSoup

def check_paa_coverage(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'is', 'are', 'can', 'does']
        
        # find all subheadings — H2 and H3 only
        subheadings = soup.find_all(['h2', 'h3'])
        
        if not subheadings:
            return {
                "factor": "People Also Ask Coverage",
                "score": 0.0,
                "status": "No subheadings found"
            }
        
        # count question subheadings
        question_count = sum(1 for h in subheadings if any(h.get_text().lower().startswith(word) for word in question_words) or '?' in h.get_text())
        
        if question_count >= 5:
            return {
                "factor": "People Also Ask Coverage",
                "score": 1.0,
                "status": f"{question_count} related questions covered"
            }
        elif question_count >= 2:
            return {
                "factor": "People Also Ask Coverage",
                "score": 0.5,
                "status": f"{question_count} related questions covered"
            }
        
        return {
            "factor": "People Also Ask Coverage",
            "score": 0.0,
            "status": "Poor PAA coverage"
        }
    
    except Exception as e:
        return {
            "factor": "People Also Ask Coverage",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }