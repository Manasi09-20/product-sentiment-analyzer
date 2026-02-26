import requests
from bs4 import BeautifulSoup

def get_flipkart_reviews(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-IN,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive"
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        reviews = []

        # Flipkart review containers
        review_blocks = soup.find_all("div", {"class": "t-ZTKy"})

        for block in review_blocks:
            text = block.get_text(strip=True)
            if text:
                reviews.append(text)

        return reviews[:20]

    except Exception as e:
        print("Scraper error:", e)
        return []