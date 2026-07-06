# Factor 2 - Immediate Answer Below Heading

import requests
from bs4 import BeautifulSoup

def check_immediate_answer(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'is', 'are', 'can', 'does']
        
        # find all H1 and H2 headings
        headings = soup.find_all(['h1', 'h2'])
        
        for heading in headings:
            text = heading.get_text().lower()
            
            # check if heading is a question
            if any(text.startswith(word) for word in question_words) or '?' in text:
                
                # find next paragraph after this heading
                next_paragraph = heading.find_next('p')
                
                if next_paragraph:
                    word_count = len(next_paragraph.get_text().split())
                    
                    # ideal answer is 40-60 words
                    if 40 <= word_count <= 60:
                        return {
                            "factor": "Immediate Answer Below Heading",
                            "score": 1.0,
                            "status": f"Perfect answer length: {word_count} words"
                        }
                    elif word_count > 0:
                        return {
                            "factor": "Immediate Answer Below Heading",
                            "score": 0.5,
                            "status": f"Answer present but not ideal length: {word_count} words"
                        }
        
        return {
            "factor": "Immediate Answer Below Heading",
            "score": 0.0,
            "status": "No immediate answer found below heading"
        }
    
    except Exception as e:
        return {
            "factor": "Immediate Answer Below Heading",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }