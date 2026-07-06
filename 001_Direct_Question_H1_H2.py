# Factor 1 - Direct Question in H1/H2

import requests
from bs4 import BeautifulSoup

def check_direct_question_heading(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'is', 'are', 'can', 'does']
        
        # Check H1 first
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            text = h1.get_text().lower()
            if any(text.startswith(word) for word in question_words) or '?' in text:
                return {
                    "factor": "Direct Question in H1/H2",
                    "score": 1.0,
                    "status": "Question found in H1"
                }
        
        # Check H2 next
        h2_tags = soup.find_all('h2')
        for h2 in h2_tags:
            text = h2.get_text().lower()
            if any(text.startswith(word) for word in question_words) or '?' in text:
                return {
                    "factor": "Direct Question in H1/H2",
                    "score": 0.5,
                    "status": "Question found in H2"
                }
        
        return {
            "factor": "Direct Question in H1/H2",
            "score": 0.0,
            "status": "No question heading found"
        }
    
    except Exception as e:
        return {
            "factor": "Direct Question in H1/H2",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }