# Factor 3 - Inverted Pyramid Writing

import requests
from bs4 import BeautifulSoup

def check_inverted_pyramid(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # extract all paragraphs
        paragraphs = soup.find_all('p')
        paragraphs = [p.get_text() for p in paragraphs if len(p.get_text().split()) > 10]
        
        if len(paragraphs) < 3:
            return {
                "factor": "Inverted Pyramid Writing",
                "score": 0.0,
                "status": "Not enough content to evaluate"
            }
        
        # compare word density of first paragraph vs rest
        first_para_words = set(paragraphs[0].lower().split())
        rest_para_words = set(' '.join(paragraphs[1:]).lower().split())
        
        unique_to_first = len(first_para_words) / len(rest_para_words) if rest_para_words else 0
        
        if unique_to_first > 0.3:
            return {
                "factor": "Inverted Pyramid Writing",
                "score": 1.0,
                "status": "Answer is front loaded — good inverted pyramid"
            }
        elif unique_to_first > 0.15:
            return {
                "factor": "Inverted Pyramid Writing",
                "score": 0.5,
                "status": "Moderate front loading detected"
            }
        
        return {
            "factor": "Inverted Pyramid Writing",
            "score": 0.0,
            "status": "Answer is buried — poor inverted pyramid"
        }
    
    except Exception as e:
        return {
            "factor": "Inverted Pyramid Writing",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }