# Factor 11 - Comparison Tables for "vs." Queries

import requests
from bs4 import BeautifulSoup

def check_comparison_table(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # check if any heading contains "vs"
        headings = soup.find_all(['h1', 'h2', 'h3'])
        has_vs_heading = any('vs' in h.get_text().lower() for h in headings)
        
        # check if page has any HTML tables
        tables = soup.find_all('table')
        
        if has_vs_heading and tables:
            return {
                "factor": "Comparison Tables for vs Queries",
                "score": 1.0,
                "status": f"vs heading found and {len(tables)} table(s) present"
            }
        elif tables:
            return {
                "factor": "Comparison Tables for vs Queries",
                "score": 0.5,
                "status": f"{len(tables)} table(s) found but no vs heading"
            }
        
        return {
            "factor": "Comparison Tables for vs Queries",
            "score": 0.0,
            "status": "No comparison table found"
        }
    
    except Exception as e:
        return {
            "factor": "Comparison Tables for vs Queries",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }