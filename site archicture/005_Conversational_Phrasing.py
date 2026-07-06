# Factor 5 - Conversational Phrasing

import requests
from bs4 import BeautifulSoup

def check_conversational_phrasing(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # conversational phrases to look for
        conversational_phrases = [
            'how do i', 'how do you', 'what is', 'what are',
            'why does', 'why is', 'when should', 'when do',
            'can i', 'can you', 'is it', 'are there'
        ]
        
        # extract all headings
        headings = soup.find_all(['h1', 'h2', 'h3'])
        heading_texts = [h.get_text().lower() for h in headings]
        
        if not heading_texts:
            return {
                "factor": "Conversational Phrasing",
                "score": 0.0,
                "status": "No headings found"
            }
        
        # count conversational headings
        conversational_count = sum(1 for text in heading_texts if any(phrase in text for phrase in conversational_phrases))
        ratio = conversational_count / len(heading_texts)
        
        if ratio >= 0.5:
            return {
                "factor": "Conversational Phrasing",
                "score": 1.0,
                "status": f"{conversational_count} conversational headings found"
            }
        elif ratio >= 0.2:
            return {
                "factor": "Conversational Phrasing",
                "score": 0.5,
                "status": f"{conversational_count} conversational headings found"
            }
        
        return {
            "factor": "Conversational Phrasing",
            "score": 0.0,
            "status": "No conversational phrasing found"
        }
    
    except Exception as e:
        return {
            "factor": "Conversational Phrasing",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }