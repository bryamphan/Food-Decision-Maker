# yelp_client.py
import os
import requests
from dotenv import load_dotenv

# loads .env and grab the key
load_dotenv()
API_KEY = os.getenv("YELP_API_KEY")
if not API_KEY:
    raise RuntimeError("Sets YELP_API_KEY in .env file")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def search_spots(term, location, limit=5, radius=2000):
    """
    Calls Yelp and returns a list of business dicts for `term` near `location`.
    """
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        "term":     term,
        "location": location,
        "limit":    limit,
        "radius":   radius
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json().get("businesses", [])
