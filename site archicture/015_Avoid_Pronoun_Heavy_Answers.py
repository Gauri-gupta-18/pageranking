# Factor 15 - Avoid Pronoun Heavy Answers

import requests
from bs4 import BeautifulSoup

def check_pronoun_usage(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # extract plain text from page
        text = soup.get_text()
        words = text.lower().split()
        
        if len(words) == 0:
            return {
                "factor": "Avoid Pronoun Heavy Answers",
                "score": 0.0,
                "status": "No content found"
            }
        
        # list of pronouns that make snippets unclear
        pronouns = ['it', 'they', 'them', 'their', 'this', 'these', 'those', 'its']
        
        # count how many pronouns appear in the text
        pronoun_count = sum(1 for w in words if w in pronouns)
        
        # calculate ratio of pronouns to total words
        pronoun_ratio = pronoun_count / len(words)
        
        if pronoun_ratio < 0.02:
            return {
                "factor": "Avoid Pronoun Heavy Answers",
                "score": 1.0,
                "status": f"Very few pronouns detected — ratio: {pronoun_ratio:.3f}"
            }
        elif pronoun_ratio < 0.04:
            return {
                "factor": "Avoid Pronoun Heavy Answers",
                "score": 0.5,
                "status": f"Moderate pronoun usage — ratio: {pronoun_ratio:.3f}"
            }
        
        return {
            "factor": "Avoid Pronoun Heavy Answers",
            "score": 0.0,
            "status": f"Too many pronouns detected — ratio: {pronoun_ratio:.3f}"
        }
    
    except Exception as e:
        return {
            "factor": "Avoid Pronoun Heavy Answers",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }