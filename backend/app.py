from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from sentiment import analyze_sentiment
from flipkart_scraper import get_flipkart_reviews
import os

app = Flask(__name__)

# ✅ Proper CORS for production (Vercel frontend)
CORS(app, resources={r"/*": {"origins": "*"}})


# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "Product Sentiment Analyzer API Running!"


# ---------------- MANUAL REVIEWS ----------------
@app.route("/analyze", methods=["POST"])
@cross_origin()
def analyze_reviews():
    try:
        data = request.get_json()
        reviews = data.get("reviews", [])

        if not reviews:
            return jsonify({"error": "No reviews provided"}), 400

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


# ---------------- URL ANALYSIS ----------------
@app.route("/analyze-url", methods=["POST"])
@cross_origin()
def analyze_url():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        reviews = get_flipkart_reviews(url)

        if not reviews:
            return jsonify({
                "error": "Unable to fetch reviews. Website may block automated requests."
            }), 400

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


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)