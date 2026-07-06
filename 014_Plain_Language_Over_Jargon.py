# Factor 14 - Plain Language Over Jargon

import requests
from bs4 import BeautifulSoup

def check_plain_language(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # extract plain text from page
        text = soup.get_text()
        words = text.split()
        
        if len(words) == 0:
            return {
                "factor": "Plain Language Over Jargon",
                "score": 0.0,
                "status": "No content found"
            }
        
        # check average word length
        # longer words usually mean more jargon
        avg_word_length = sum(len(w) for w in words) / len(words)
        
        # check average sentence length
        # shorter sentences = simpler language
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        if avg_word_length < 5 and avg_sentence_length < 15:
            return {
                "factor": "Plain Language Over Jargon",
                "score": 1.0,
                "status": f"Simple language detected — avg word length: {avg_word_length:.1f}, avg sentence length: {avg_sentence_length:.1f}"
            }
        elif avg_word_length < 6 and avg_sentence_length < 20:
            return {
                "factor": "Plain Language Over Jargon",
                "score": 0.5,
                "status": f"Moderate complexity — avg word length: {avg_word_length:.1f}, avg sentence length: {avg_sentence_length:.1f}"
            }
        
        return {
            "factor": "Plain Language Over Jargon",
            "score": 0.0,
            "status": f"Complex language detected — avg word length: {avg_word_length:.1f}, avg sentence length: {avg_sentence_length:.1f}"
        }
    
    except Exception as e:
        return {
            "factor": "Plain Language Over Jargon",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }