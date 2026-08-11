import { useState } from "react";

const API_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

function AnalyzePage() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const allowedTypes = ["image/png", "image/jpeg", "image/jpg", "application/pdf"];

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    if (!allowedTypes.includes(selectedFile.type)) {
      setError("Unsupported file type. Please upload PNG, JPG, JPEG or PDF.");
      setFile(null);
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setError("File is too large. Maximum size is 10 MB.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setError("");
    setResult(null);
  };

  const analyzeDocument = async () => {
    if (!file) {
      setError("Please select an academic document first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const endpoint = API_URL ? `${API_URL}/api/analyze` : "/api/analyze";
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (!response.ok || !data.success) {
        throw new Error(data.error || "Unable to analyze document.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Unable to analyze the document. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setFile(null);
    setResult(null);
    setError("");
  };

  return (
    <section className="page analyze-page">
      <div className="page-hero">
        <div className="hero-eyebrow">ACADEMIC DOCUMENT ANALYZER</div>
        <h1>Extract, classify and summarize academic documents.</h1>
        <p>
          Upload a single academic document for OCR text extraction, field
          analysis, document classification, and a concise academic summary.
        </p>
      </div>

      <div className="analyze-grid">
        <div className="upload-panel">
          <div className={`drop-zone ${file ? "has-file" : ""}`}>
            <input
              id="analyze-upload"
              type="file"
              accept=".png,.jpg,.jpeg,.pdf"
              onChange={handleFileChange}
            />
            <label htmlFor="analyze-upload" className="upload-area">
              <div className="upload-icon">⭳</div>
              {file ? (
                <>
                  <h3>{file.name}</h3>
                  <p>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  <span className="upload-note">Click to change document</span>
                </>
              ) : (
                <>
                  <h3>Drag and drop or browse</h3>
                  <p>PNG, JPG, JPEG, PDF - maximum 10 MB</p>
                  <span className="upload-note">Upload academic document</span>
                </>
              )}
            </label>
          </div>

          {error && <div className="alert error">{error}</div>}

          <button
            className="primary-button"
            onClick={analyzeDocument}
            disabled={!file || loading}
          >
            {loading ? "Analyzing document..." : "Analyze Document"}
          </button>

          {result && (
            <button className="secondary-button" onClick={resetAnalysis}>
              New Analysis
            </button>
          )}

          <div className="privacy-banner">
            Your document is processed temporarily and is not permanently stored.
          </div>
        </div>

        {result && (
          <div className="result-panel">
            <div className="result-header">
              <span>ANALYSIS COMPLETE</span>
              <h2>{result.document_type}</h2>
              <p>Classification confidence: {result.confidence}%</p>
            </div>

            <div className="summary-card">
              <h3>Academic Summary</h3>
              <p>{result.summary}</p>
            </div>

            <div className="stats-row">
              <div className="stat-card">
                <span>{result.statistics.subjects_count}</span>
                <p>Subjects</p>
              </div>
              <div className="stat-card">
                <span>{result.statistics.average_marks ?? "-"}%</span>
                <p>Average</p>
              </div>
              <div className="stat-card">
                <span>{result.statistics.highest_marks ?? "-"}%</span>
                <p>Highest</p>
              </div>
              <div className="stat-card">
                <span>{result.statistics.lowest_marks ?? "-"}%</span>
                <p>Lowest</p>
              </div>
            </div>

            <div className="info-grid">
              <InfoCard label="Student Name" value={result.data.name} />
              <InfoCard
                label="Registration Number"
                value={result.data.registration_number}
              />
              <InfoCard label="Course" value={result.data.course} />
              <InfoCard label="Department" value={result.data.department} />
              <InfoCard label="Academic Year" value={result.data.academic_year} />
              <InfoCard label="Semester" value={result.data.semester} />
              <InfoCard label="Result" value={result.data.result} />
            </div>

            <div className="subjects-panel">
              <div className="section-title">Subject Performance</div>
              {result.data.subjects.length > 0 ? (
                <div className="subjects-table">
                  {result.data.subjects.map((subject, index) => (
                    <div key={index} className="subject-row">
                      <div>
                        <strong>{subject.subject}</strong>
                        <span>{subject.marks}%</span>
                      </div>
                      <div className="progress-bar">
                        <div
                          className="progress-fill"
                          style={{ width: `${subject.marks}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="empty-state">
                  No subject-level marks were detected in this document.
                </p>
              )}
            </div>

            <details className="ocr-details">
              <summary>View Extracted Text</summary>
              <pre>{result.ocr_text}</pre>
            </details>
          </div>
        )}
      </div>
    </section>
  );
}

function InfoCard({ label, value }) {
  return (
    <div className="info-card">
      <span>{label}</span>
      <strong>{value || "Not detected"}</strong>
    </div>
  );
}

export default AnalyzePage;
