from flask import Flask, request, jsonify
from flipkart_scraper import get_flipkart_reviews

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.json.get("url")
    reviews = get_flipkart_reviews(url)
    return jsonify({"reviews": reviews})

app.run(port=5050)