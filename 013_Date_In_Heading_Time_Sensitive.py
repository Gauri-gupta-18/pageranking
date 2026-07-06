# Factor 13 - Date in Heading for Time-Sensitive Answers

import requests
import datetime
from bs4 import BeautifulSoup

def check_date_in_heading(context):
    url = context.get("url")  # get URL from context
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # get current and last year
        current_year = str(datetime.datetime.now().year)
        last_year = str(datetime.datetime.now().year - 1)
        
        # check all headings for year
        headings = soup.find_all(['h1', 'h2', 'h3'])
        
        for heading in headings:
            text = heading.get_text()
            
            # current year in heading = fresh content
            if current_year in text:
                return {
                    "factor": "Date in Heading for Time Sensitive Answers",
                    "score": 1.0,
                    "status": f"Current year {current_year} found in heading"
                }
            
            # last year in heading = slightly outdated
            elif last_year in text:
                return {
                    "factor": "Date in Heading for Time Sensitive Answers",
                    "score": 0.5,
                    "status": f"Last year {last_year} found in heading — slightly outdated"
                }
        
        return {
            "factor": "Date in Heading for Time Sensitive Answers",
            "score": 0.0,
            "status": "No year found in any heading"
        }
    
    except Exception as e:
        return {
            "factor": "Date in Heading for Time Sensitive Answers",
            "score": 0.0,
            "status": f"Error: {str(e)}"
        }