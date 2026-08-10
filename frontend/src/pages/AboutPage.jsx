function AboutPage() {
  return (
    <section className="page about-page">
      <div className="page-hero">
        <div className="hero-eyebrow">ABOUT</div>
        <h1>Academic Document Analyzer</h1>
        <p>
          A secure web application for OCR-based academic document analysis,
          classification, summary generation, and optional document comparison.
        </p>
      </div>

      <div className="about-grid">
        <div className="about-card">
          <h3>Features</h3>
          <ul>
            <li>OCR text extraction from academic documents</li>
            <li>Rule-based academic field extraction</li>
            <li>Document classification with confidence scoring</li>
            <li>Academic summary and performance statistics</li>
            <li>Optional compare workflow for two documents</li>
            <li>Temporary processing without persistent storage</li>
          </ul>
        </div>

        <div className="about-card">
          <h3>Technology</h3>
          <ul>
            <li>React + Vite frontend</li>
            <li>Python Flask backend</li>
            <li>Tesseract OCR and PyMuPDF</li>
            <li>Pillow image processing</li>
            <li>REST API design and secure upload handling</li>
          </ul>
        </div>

        <div className="about-card full-width">
          <h3>Important Limitation</h3>
          <p>
            This application performs OCR-based academic document analysis and
            comparison. It does not determine the legal authenticity or genuineness
            of academic documents.
          </p>
        </div>
      </div>
    </section>
  );
}

export default AboutPage;
