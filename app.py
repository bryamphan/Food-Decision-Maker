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

@app.route("/", methods=["GET", "POST"])
def index():
    spots = None
    craving = ""
    location = ""
    if request.method == "POST":
        craving = request.form.get("craving", "").strip()
        location = request.form.get("location", "").strip()

        # fallback if they left craving blank
        if not craving:
            craving = pick_random_craving()

        # fallback if they left location blank
        if not location:
            location = "San Francisco, CA"

        # fetch up to 20 and we'll show top 5
        spots = search_spots(craving, location, limit=20)

    return render_template(
        "index.html",
        spots=spots,
        craving=craving,
        location=location
    )

if __name__ == "__main__":
    app.run(debug=True)
