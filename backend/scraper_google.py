import requests
from database import insert_review
from config import GOOGLE_API_KEY

def get_google_reviews(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews&key={AIzaSyBkIAZJwSbbDokzP3lpvfU2Ya2qKOjX_Oo}"
    response = requests.get(url).json()
    reviews = response.get("result", {}).get("reviews", [])
    for rev in reviews:
        data = {
            "source": "google",
            "author": rev.get("author_name"),
            "rating": rev.get("rating"),
            "text": rev.get("text"),
            "time": rev.get("time")
        }
        insert_review(data)

