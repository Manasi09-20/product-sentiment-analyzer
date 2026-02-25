from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.sentiment import analyze_sentiment
from backend.flipkart_scraper import get_flipkart_reviews
import os

app = Flask(__name__)
CORS(app)

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "Product Sentiment Analyzer API Running!"

# ---------------- MANUAL REVIEWS ----------------
@app.route("/analyze", methods=["POST"])
def analyze_reviews():
    try:
        data = request.get_json()
        reviews = data.get("reviews", [])

        results = []
        summary = {"Positive": 0, "Negative": 0, "Neutral": 0}

        for review in reviews:
            sentiment = analyze_sentiment(review)
            results.append({
                "review": review,
                "sentiment": sentiment
            })
            summary[sentiment] += 1

        return jsonify({
            "summary": summary,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- URL REVIEWS ----------------
@app.route("/analyze-url", methods=["POST"])
def analyze_url():
    try:
        data = request.get_json()
        url = data.get("url")

        reviews = get_flipkart_reviews(url)

        results = []
        summary = {"Positive": 0, "Negative": 0, "Neutral": 0}

        for review in reviews:
            sentiment = analyze_sentiment(review)
            results.append({
                "review": review,
                "sentiment": sentiment
            })
            summary[sentiment] += 1

        return jsonify({
            "summary": summary,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- RENDER PORT BINDING ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)