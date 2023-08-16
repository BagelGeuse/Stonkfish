import requests
import os
from dotenv import load_dotenv
import sys

#handles any api requests and data processing

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")

def requestHistory(keyword):
    
    url = "https://stockyapiexchange.p.rapidapi.com/history"

    #Maybe make it go back one month to prevent too much unused data
    querystring = {"keyword":keyword, "startDate":"2023-07-21"}

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "stockyapiexchange.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if(response.status_code != 200):
        return "Error"
    else:
        return response.json()

if(__name__ == "__main__"):
    print(requestHistory(sys.argv[1]))