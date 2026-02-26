import React, { useState } from "react";
import axios from "axios";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

// 🔗 Your live backend URL
const API = "https://product-sentiment-analyzer-87ks.onrender.com";

function App() {

  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [details, setDetails] = useState([]);

  // ---------------- MANUAL REVIEW ANALYSIS ----------------
  const analyzeText = async () => {
    try {
      const reviewsArray = text
        .split("\n")
        .map(r => r.trim())
        .filter(r => r.length > 0);

      if (reviewsArray.length === 0) {
        alert("Enter at least one review");
        return;
      }

      const response = await axios({
        method: "post",
        url: `${API}/analyze`,
        headers: { "Content-Type": "application/json" },
        data: JSON.stringify({ reviews: reviewsArray })
      });

      setResult(response.data.summary);
      setDetails(response.data.results);

    } catch (error) {
      console.error(error);
      alert("Backend error (server waking up or invalid data)");
    }
  };

  // ---------------- URL ANALYSIS ----------------
  const analyzeURL = async () => {
    try {
      if (!url) {
        alert("Enter product URL");
        return;
      }

      const response = await axios({
        method: "post",
        url: `${API}/analyze-url`,
        headers: { "Content-Type": "application/json" },
        data: JSON.stringify({ url: url })
      });

      setResult(response.data.summary);
      setDetails(response.data.results);

    } catch (error) {
      console.error(error);
      alert("Could not fetch reviews (website may block server)");
    }
  };

  // ---------------- CHART DATA ----------------
  const chartData = result
    ? {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [
          {
            label: "Sentiment Distribution",
            data: [
              result.Positive,
              result.Negative,
              result.Neutral
            ],
            backgroundColor: ["#4CAF50", "#F44336", "#FFC107"],
            borderWidth: 1
          }
        ]
      }
    : null;

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>📊 Product Sentiment Analyzer Dashboard</h1>

      {/* URL Analysis */}
      <h2>Analyze using Product URL</h2>
      <input
        type="text"
        size="80"
        placeholder="Paste Flipkart product link here"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <br /><br />
      <button onClick={analyzeURL}>Analyze URL</button>

      <hr style={{ margin: "40px 0" }} />

      {/* Manual Reviews */}
      <h2>Or Enter Reviews Manually</h2>
      <textarea
        rows="8"
        cols="60"
        placeholder="Enter reviews (one per line)"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br /><br />
      <button onClick={analyzeText}>Analyze Reviews</button>

      {/* Chart */}
      {result && (
        <div style={{ marginTop: "40px", width: "400px" }}>
          <h2>Sentiment Chart</h2>
          <Pie data={chartData} />
        </div>
      )}

      {/* Details */}
      {details.length > 0 && (
        <div style={{ marginTop: "40px" }}>
          <h2>Review Analysis</h2>
          <ul>
            {details.map((item, index) => (
              <li key={index}>
                {item.review} → <b>{item.sentiment}</b>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;