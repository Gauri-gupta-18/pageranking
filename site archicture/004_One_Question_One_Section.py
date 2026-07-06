# Factor 4 - One Question One Section

import requests
from bs4 import BeautifulSoup

def check_one_question_one_section(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'is', 'are', 'can', 'does']
        
        # find all headings
        headings = soup.find_all(['h1', 'h2', 'h3'])
        
        if not headings:
            return {
                "factor": "One Question One Section",
                "score": 0.0,
                "status": "No headings found"
            }
        
        # find question headings
        question_headings = [h for h in headings if any(h.get_text().lower().startswith(word) for word in question_words) or '?' in h.get_text()]
        
        if not question_headings:
            return {
                "factor": "One Question One Section",
                "score": 0.0,
                "status": "No question headings found"
            }
        
        # check if each question heading has dedicated content
        well_separated = 0
        for heading in question_headings:
            next_p = heading.find_next('p')
            if next_p and len(next_p.get_text().split()) > 20:
                well_separated += 1
        
        ratio = well_separated / len(question_headings)
        
        if ratio >= 0.8:
            return {
                "factor": "One Question One Section",
                "score": 1.0,
                "status": "Each question has its own dedicated section"
            }
        elif ratio >= 0.5:
            return {
                "factor": "One Question One Section",
                "score": 0.5,
                "status": "Some questions have dedicated sections"
            }
        
        return {
            "factor": "One Question One Section",
            "score": 0.0,
            "status": "Questions are mixed together"
        }
    
    except Exception as e:
        return {
            "factor": "One Question One Section",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }