import React, { useState } from "react";
import axios from "axios";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {

  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [details, setDetails] = useState([]);

  // Manual review analysis
  const analyzeText = async () => {
    try {
      const reviews = text.split("\n");

      const response = await axios.post("http://127.0.0.1:5000/analyze", {
        reviews: reviews
      });

      setResult(null);
      setDetails([]);

      setTimeout(() => {
        setResult(response.data.summary);
        setDetails(response.data.results);
      }, 100);

    } catch (error) {
      alert("Backend error");
    }
  };

  // URL analysis
  const analyzeURL = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze-url", {
        url: url
      });

      setResult(null);
      setDetails([]);

      setTimeout(() => {
        setResult(response.data.summary);
        setDetails(response.data.results);
      }, 100);

    } catch (error) {
      alert("Invalid URL or backend not running");
    }
  };

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

      {result && (
        <div style={{ marginTop: "40px", width: "400px" }}>
          <h2>Sentiment Chart</h2>
          <Pie data={chartData} />
        </div>
      )}

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