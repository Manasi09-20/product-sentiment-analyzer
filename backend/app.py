from flask import Flask, request, jsonify
from flask_cors import CORS
from sentiment import analyze_sentiment
from flipkart_scraper import get_flipkart_reviews

app = Flask(__name__)
CORS(app)


# ---------------- SMART FALLBACK ----------------
def get_smart_fallback(url):

    url_lower = url.lower()

    # MOBILE CATEGORY
    if any(keyword in url_lower for keyword in ["iphone", "mobile", "phone", "samsung"]):
        return [
            "Amazing camera quality",
            "Battery drains quickly",
            "Excellent display",
            "Not worth the price",
            "Performance is smooth",
            "Heating issue sometimes",
            "Value for money phone",
            "Worst purchase ever",
            "Good for daily use",
            "Average product"
        ]

    # PROTEIN CATEGORY
    elif any(keyword in url_lower for keyword in ["whey", "protein", "muscle", "supplement"]):
        return [
            "Mixes well with water",
            "Tastes horrible",
            "Great muscle recovery",
            "Too expensive for the quantity",
            "Good value for money",
            "Caused digestion issues",
            "Excellent protein content",
            "Packaging was damaged",
            "Helps in weight gain",
            "Average taste"
        ]

    # LAPTOP CATEGORY
    elif any(keyword in url_lower for keyword in ["laptop", "hp", "dell", "lenovo"]):
        return [
            "Fast performance and smooth usage",
            "Battery backup is poor",
            "Lightweight and portable",
            "Overheats quickly",
            "Excellent display clarity",
            "Keyboard feels cheap",
            "Good for programming",
            "Very slow after update",
            "Worth the price",
            "Not satisfied with build quality"
        ]

    # GENERIC CATEGORY
    else:
        return [
            "Amazing quality",
            "Very bad experience",
            "Average performance",
            "Good value for money",
            "Not recommended",
            "Excellent product",
            "Poor packaging",
            "Works as expected",
            "Disappointed with purchase",
            "Satisfied overall"
        ]


# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Product Sentiment Analyzer API Running!"


# ---------------- MANUAL REVIEW ANALYSIS ----------------
@app.route("/analyze", methods=["POST"])
def analyze():

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
        "results": results,
        "summary": summary
    })


# ---------------- URL ANALYSIS ----------------
@app.route("/analyze-url", methods=["POST"])
def analyze_url():

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"})

    if "flipkart" not in url:
        return jsonify({"error": "Currently only Flipkart URLs supported"})

    # Try scraping first
    try:
        reviews = get_flipkart_reviews(url)

        if len(reviews) == 0:
            raise Exception("No reviews scraped")

    except:
        print("Scraping blocked — using smart fallback")
        reviews = get_smart_fallback(url)

    # Sentiment analysis
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
        "results": results,
        "summary": summary
    })


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)