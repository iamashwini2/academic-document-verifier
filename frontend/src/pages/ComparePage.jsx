import { useState } from "react";

const API_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

function ComparePage() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const allowedTypes = ["image/png", "image/jpeg", "image/jpg", "application/pdf"];

  const handleFileChange = (event, setFile) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!allowedTypes.includes(file.type)) {
      setError("Unsupported file type. Please upload PNG, JPG, JPEG or PDF.");
      setFile(null);
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("File is too large. Maximum size is 10 MB.");
      setFile(null);
      return;
    }

    setError("");
    setFile(file);
  };

  const compareDocuments = async () => {
    if (!file1 || !file2) {
      setError("Please upload both documents before comparing.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("document1", file1);
    formData.append("document2", file2);

    try {
      const endpoint = API_URL ? `${API_URL}/api/compare` : "/api/compare";
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (!response.ok || !data.success) {
        throw new Error(data.error || "Unable to compare documents.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Unable to compare the documents. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="page compare-page">
      <div className="page-hero">
        <div className="hero-eyebrow">COMPARE ACADEMIC DOCUMENTS</div>
        <h1>Compare two academic records side by side.</h1>
        <p>
          Upload two documents to compare key academic fields, subject marks,
          and matching status without storing your files permanently.
        </p>
      </div>

      <div className="compare-grid">
        <div className="compare-panel">
          <div className="upload-pair">
            <div className="drop-zone has-file">
              <input
                id="compare-upload-1"
                type="file"
                accept=".png,.jpg,.jpeg,.pdf"
                onChange={(e) => handleFileChange(e, setFile1)}
              />
              <label htmlFor="compare-upload-1" className="upload-area">
                <h3>Document 1</h3>
                {file1 ? (
                  <p>{file1.name}</p>
                ) : (
                  <p>Upload PNG, JPG, JPEG or PDF</p>
                )}
              </label>
            </div>

            <div className="drop-zone has-file">
              <input
                id="compare-upload-2"
                type="file"
                accept=".png,.jpg,.jpeg,.pdf"
                onChange={(e) => handleFileChange(e, setFile2)}
              />
              <label htmlFor="compare-upload-2" className="upload-area">
                <h3>Document 2</h3>
                {file2 ? (
                  <p>{file2.name}</p>
                ) : (
                  <p>Upload PNG, JPG, JPEG or PDF</p>
                )}
              </label>
            </div>
          </div>

          {error && <div className="alert error">{error}</div>}

          <button
            className="primary-button"
            onClick={compareDocuments}
            disabled={!file1 || !file2 || loading}
          >
            {loading ? "Comparing documents..." : "Compare Documents"}
          </button>
        </div>

        {result && (
          <div className="compare-result-panel">
            <div className="result-header">
              <span>COMPARISON RESULT</span>
              <h2>Document Comparison</h2>
              <p>{result.comparison.summary}</p>
            </div>

            <div className="comparison-table">
              <div className="table-head">
                <span>Field</span>
                <span>Document 1</span>
                <span>Document 2</span>
                <span>Status</span>
              </div>
              {result.comparison.fields.map((item) => (
                <div key={item.field} className="table-row">
                  <span>{formatFieldName(item.field)}</span>
                  <span>{item.document1 || "-"}</span>
                  <span>{item.document2 || "-"}</span>
                  <span className={`status-badge ${item.status.toLowerCase()}`}>
                    {item.status}
                  </span>
                </div>
              ))}
            </div>

            <div className="comparison-table">
              <div className="table-head">
                <span>Subject</span>
                <span>Document 1</span>
                <span>Document 2</span>
                <span>Status</span>
              </div>
              {result.comparison.subjects.map((subject) => (
                <div key={subject.subject} className="table-row">
                  <span>{subject.subject}</span>
                  <span>{subject.document1 ?? "-"}</span>
                  <span>{subject.document2 ?? "-"}</span>
                  <span className={`status-badge ${subject.status.toLowerCase()}`}>
                    {subject.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

function formatFieldName(field) {
  return field.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

export default ComparePage;
