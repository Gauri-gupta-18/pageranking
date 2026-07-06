# Factor 8 - FAQ Section at Page Bottom

import requests
from bs4 import BeautifulSoup

def check_faq_section(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        faq_keywords = ['frequently asked questions', 'faq', 'common questions', 'people also ask']
        question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'is', 'are', 'can', 'does']
        
        # check if page has FAQ related keywords
        page_text = soup.get_text().lower()
        has_faq = any(keyword in page_text for keyword in faq_keywords)
        
        if not has_faq:
            return {
                "factor": "FAQ Section at Page Bottom",
                "score": 0.0,
                "status": "No FAQ section found"
            }
        
        # find FAQ heading
        headings = soup.find_all(['h2', 'h3'])
        faq_heading = next((h for h in headings if any(keyword in h.get_text().lower() for keyword in faq_keywords)), None)
        
        if not faq_heading:
            return {
                "factor": "FAQ Section at Page Bottom",
                "score": 0.3,
                "status": "FAQ keywords found but no dedicated heading"
            }
        
        # count question answer pairs after FAQ heading
        following_headings = faq_heading.find_all_next(['h2', 'h3'])
        qa_count = sum(1 for h in following_headings if any(h.get_text().lower().startswith(word) for word in question_words) or '?' in h.get_text())
        
        if qa_count >= 3:
            return {
                "factor": "FAQ Section at Page Bottom",
                "score": 1.0,
                "status": f"Well structured FAQ with {qa_count} question answer pairs"
            }
        elif qa_count >= 1:
            return {
                "factor": "FAQ Section at Page Bottom",
                "score": 0.5,
                "status": f"FAQ present with {qa_count} question answer pairs"
            }
        
        return {
            "factor": "FAQ Section at Page Bottom",
            "score": 0.3,
            "status": "FAQ heading found but no questions inside"
        }
    
    except Exception as e:
        return {
            "factor": "FAQ Section at Page Bottom",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }