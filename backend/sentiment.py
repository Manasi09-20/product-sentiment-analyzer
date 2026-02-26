def analyze_sentiment(text):
    text = text.lower()

    positive_words = ["good", "great", "excellent", "amazing", "love", "nice"]
    negative_words = ["bad", "worst", "poor", "hate", "terrible", "awful"]

    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"