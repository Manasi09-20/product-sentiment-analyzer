from sentiment import analyze_sentiment

reviews = [
    "Camera quality is amazing",
    "Battery drains very fast",
    "Average performance",
    "Excellent phone and smooth display",
    "Waste of money"
]

print("\nSentiment Test:\n")

for r in reviews:
    print(r, "->", analyze_sentiment(r))