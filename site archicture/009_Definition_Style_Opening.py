# Factor 9 - Definition Style Opening Sentences

import requests
from bs4 import BeautifulSoup

def check_definition_style(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # definition patterns to look for
        definition_patterns = [' is ', ' is a ', ' is an ', ' refers to ', ' can be defined as ', ' is defined as ']
        
        # find all paragraphs
        paragraphs = soup.find_all('p')
        
        if not paragraphs:
            return {
                "factor": "Definition Style Opening Sentences",
                "score": 0.0,
                "status": "No paragraphs found"
            }
        
        # check first 3 paragraphs for definition pattern
        for i, para in enumerate(paragraphs[:3]):
            text = para.get_text()
            if any(pattern in text for pattern in definition_patterns):
                if i == 0:
                    return {
                        "factor": "Definition Style Opening Sentences",
                        "score": 1.0,
                        "status": "Definition found in first paragraph"
                    }
                else:
                    return {
                        "factor": "Definition Style Opening Sentences",
                        "score": 0.5,
                        "status": f"Definition found in paragraph {i + 1}"
                    }
        
        return {
            "factor": "Definition Style Opening Sentences",
            "score": 0.0,
            "status": "No definition pattern found"
        }
    
    except Exception as e:
        return {
            "factor": "Definition Style Opening Sentences",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }