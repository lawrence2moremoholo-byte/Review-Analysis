import requests
from bs4 import BeautifulSoup
from database import insert_review

def scrape_hellopeter(business_url):
    response = requests.get(business_url)
    soup = BeautifulSoup(response.text, "html.parser")
    reviews = soup.find_all("div", class_="review")
    for r in reviews:
        text = r.find("p").text.strip()
        rating = int(r.find("span", class_="stars")["data-rating"])
        author = r.find("span", class_="review-author").text.strip()
        insert_review({
            "source":"hellopeter",
            "author":author,
            "rating":rating,
            "text":text
        })

