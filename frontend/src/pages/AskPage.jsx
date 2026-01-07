import { useState } from "react";
import axios from "axios";
import NavBar from "../components/NavBar";

const AskPage = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const reportId = localStorage.getItem("report_id");

    if (!reportId) {
      setError("No report context found. Please upload a report again.");
      return;
    }

    setLoading(true);
    setError(null);
    setAnswer("");

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/ask",
        {
          question,
          report_id: reportId
        }
      );

      setAnswer(response.data.answer);
    } catch (err) {
      setError("Failed to get response");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuestion("");
    setAnswer("");
    setError(null);
  };

  return (
    <div>
      <NavBar />

      <div className="ask-page">
        <h2 className="ask-title">
          Ask Questions About Your Report
        </h2>

        <div className="ask-container">
          {/* Input */}
          <textarea
            className="ask-textarea"
            placeholder="Ask something like: What does low PCV mean?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            rows={3}
          />

          {/* Buttons */}
          <div className="ask-button-group">
            <button
              onClick={handleAsk}
              disabled={loading}
              className="ask-button"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>

            <button
              onClick={handleClear}
              disabled={loading}
              className="ask-clear-button"
            >
              Clear
            </button>
          </div>

          {/* Error */}
          {error && <p className="ask-error">{error}</p>}

          {/* Answer */}
          {answer && (
            <div className="ask-answer">
              <strong>Answer</strong>
              <p>{answer}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AskPage;
