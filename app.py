# app.py
import random
from flask import Flask, render_template, request
from yelp_client import search_spots
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

DEFAULT_CATEGORIES = [
    "Pizza", "Sushi", "Burgers",
    "Tacos", "Thai Food", "Korean Food",
    "Salads", "BBQ", "Coffee"
]

def pick_random_craving():
    return random.choice(DEFAULT_CATEGORIES)

# Page 1 (Landing Page)
@app.route("/", methods=["GET"])
def landing():
    return render_template("landing.html")

# Page 2 (Search Page)
@app.route("/search", methods=["GET", "POST"])
def search():
    spots = None
    craving = ""
    location = ""
    if request.method == "POST":
        craving = request.form.get("craving", "").strip() or pick_random_craving()
        location = request.form.get("location", "").strip() or "San Francisco, CA"
        spots = search_spots(craving, location, limit=20)
    return render_template(
        "search.html",
        spots=spots,
        craving=craving,
        location=location
    )

if __name__ == "__main__":
    app.run(debug=True)
