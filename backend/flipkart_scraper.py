import requests
from bs4 import BeautifulSoup

def get_flipkart_reviews(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers, timeout=20)

    soup = BeautifulSoup(response.text, "html.parser")

    reviews = []

    for review in soup.select("div.t-ZTKy"):
        reviews.append(review.get_text(strip=True))

    return reviews[:20]