import { useEffect, useState } from "react";
import axios from "axios";
import NavBar from "../components/NavBar";
import { useNavigate } from "react-router";

const ReportPage = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showOnlyAbnormal, setShowOnlyAbnormal] = useState(false);

  const navigate = useNavigate();
  const reportId = localStorage.getItem("report_id");

  useEffect(() => {
    if (!reportId) {
      navigate("/upload");
      return;
    }

    const fetchAnalysis = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/analyze?report_id=${reportId}`
        );
        setResults(response.data.results || []);
      } catch (err) {
        setError(
          err.response?.data?.error ||
          "Unable to analyze the uploaded report."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [reportId, navigate]);

  const displayedResults = showOnlyAbnormal
    ? results.filter(
        (item) => !item.status?.toLowerCase().includes("normal")
      )
    : results;

  return (
    <div className="p-6">
      {/* NavBar ALWAYS visible */}
      <NavBar />

      <div className="report-page">
        {/* Loading */}
        {loading && (
          <div className="spinner-container">
            <div className="spinner"></div>
            <p>Analyzing report...</p>
          </div>
        )}

        {/* Error */}
        {!loading && error && (
          <p className="report-error">{error}</p>
        )}

        {/* Results */}
        {!loading && !error && (
          <>
            <h2>Report Analysis</h2>

            {/* Toggle */}
            <div className="toggle-container">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={showOnlyAbnormal}
                  onChange={() =>
                    setShowOnlyAbnormal(!showOnlyAbnormal)
                  }
                />
                Show only out-of-range values
              </label>
            </div>

            <table className="report-table">
              <thead>
                <tr>
                  <th>Test</th>
                  <th>Value</th>
                  <th>Normal Range</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {displayedResults.map((item, index) => (
                  <tr key={index}>
                    <td>{item.test}</td>
                    <td>{item.value}</td>
                    <td>{item.range}</td>
                    <td
                      className={
                        item.status?.toLowerCase().includes("normal")
                          ? "status-normal"
                          : "status-abnormal"
                      }
                    >
                      {item.status}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="ask-link-container">
              <button
                onClick={() => navigate("/ask")}
                className="ask-link-button"
              >
                Ask questions about this report →
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ReportPage;
