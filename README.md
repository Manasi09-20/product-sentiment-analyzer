# Product Sentiment Analyzer

An AI-powered web application that analyzes customer sentiment from product reviews or product URLs and visualizes the results using an interactive dashboard.

---

## Features

- Manual review sentiment analysis
- Product URL-based analysis
- Smart fallback system when scraping is blocked
- Category-aware sentiment datasets
- Interactive charts dashboard using Chart.js

---

## Technologies Used

Frontend:
- React.js
- Chart.js
- Axios

Backend:
- Flask (Python)
- Flask-CORS
- Selenium (for scraping)
- TextBlob (NLP)

---

## How It Works

1. User enters reviews manually OR provides a product URL.
2. The system attempts to fetch product reviews.
3. If scraping is blocked by anti-bot protection, the smart fallback dataset activates.
4. The NLP engine classifies reviews into Positive, Negative, and Neutral.
5. Results are visualized through an interactive dashboard.

---

## Project Structure

Product-Sentiment-Analyzer  
│  
├── backend  
├── frontend  
├── dataset  
├── models  
└── README.md  

---

## Run Locally

### Backend

cd backend  
venv\Scripts\activate  
python app.py  

### Frontend

cd frontend  
npm start  

---

## Deployment

Frontend: Netlify  
Backend: Render  

---

## Author

Manasi T
