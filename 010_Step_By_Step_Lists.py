# Factor 10 - Step by Step Lists for How Queries

import requests
from bs4 import BeautifulSoup

def check_step_by_step(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        how_to_patterns = ['how to', 'how do', 'steps to', 'guide to', 'how can']
        
        # check H1 and title for how-to patterns
        headings = soup.find_all('h1')
        title = soup.find('title')
        check_text = ' '.join([h.get_text().lower() for h in headings])
        if title:
            check_text += ' ' + title.get_text().lower()
        
        # check if page is a how-to page
        is_how_to = any(pattern in check_text for pattern in how_to_patterns)
        
        if not is_how_to:
            return {
                "factor": "Step by Step Lists for How Queries",
                "score": 0.0,
                "status": "Not a how-to page"
            }
        
        # check for ordered list with 3+ steps
        ol_tags = soup.find_all('ol')
        has_ordered_list = any(len(ol.find_all('li')) >= 3 for ol in ol_tags)
        
        if has_ordered_list:
            return {
                "factor": "Step by Step Lists for How Queries",
                "score": 1.0,
                "status": "How-to page with proper numbered list found"
            }
        
        # check for bullet list as fallback
        ul_tags = soup.find_all('ul')
        has_bullet_list = any(len(ul.find_all('li')) >= 3 for ul in ul_tags)
        
        if has_bullet_list:
            return {
                "factor": "Step by Step Lists for How Queries",
                "score": 0.5,
                "status": "How-to page with bullet list instead of numbered list"
            }
        
        return {
            "factor": "Step by Step Lists for How Queries",
            "score": 0.0,
            "status": "How-to page but no list structure found"
        }
    
    except Exception as e:
        return {
            "factor": "Step by Step Lists for How Queries",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }