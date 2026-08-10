# Academic Document Analyzer

Academic Document Analyzer is a modern full-stack project for OCR-based academic document intelligence. It uses Flask and Tesseract OCR on the backend to extract text, infer academic fields, classify document type, compute statistics, summarize academic content, and compare two documents side by side. The frontend is built with React and Vite.

## Features

- OCR-based academic document extraction from PNG, JPG, JPEG, and PDF
- Academic field extraction and structured data inference
- Document classification with confidence scoring
- Academic summary generation and statistics computation
- Optional document comparison mode for two uploaded documents
- Temporary processing with no database or permanent file storage
- Modern responsive React UI

## Technology Stack

- Python 3.x
- Flask
- Tesseract OCR (`pytesseract`)
- PyMuPDF for PDF rendering
- React + Vite
- JavaScript, HTML, CSS

## Project Structure

- `backend/` - Flask backend application and OCR analysis modules
- `frontend/` - React + Vite frontend application
- `ocr/` - OCR field extractor helpers
- `uploads/` - temporary uploads (ignored in Git)
- `processed/` - temporary processed files (ignored in Git)
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore configuration
- `README.md` - project documentation

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.
   - Windows: `python -m venv venv` and `venv\Scripts\Activate.ps1`
3. Install backend dependencies:
   - `python -m pip install -r requirements.txt`
4. Install frontend dependencies:
   - `cd frontend`
   - `npm install`

## Running the Backend

1. Activate the Python virtual environment.
2. Run the Flask server from the repository root:

```powershell
venv\Scripts\Activate.ps1
python backend\app.py
```

3. The backend listens on `http://127.0.0.1:5000` by default.
4. To change host or port, set environment variables before running:

```powershell
$env:HOST = '0.0.0.0'
$env:PORT = '5000'
python backend\app.py
```

## Running the Frontend

1. From the `frontend` directory:

```powershell
cd frontend
npm run dev
```

2. Open the Vite URL displayed in the terminal.
3. If the backend runs on a different URL, set `VITE_API_URL` in `.env` or your environment.

## OCR / Tesseract Requirement

This project requires Tesseract OCR installed on the host machine.

- Windows default Tesseract path is configured in `backend/analyzer.py` as:
  `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Override with the `TESSERACT_PATH` environment variable if needed.

## API Endpoints

- `GET /` - API health check
- `POST /api/analyze` - Analyze a single academic document
  - Form field: `file`
- `POST /api/compare` - Compare two academic documents
  - Form fields: `document1`, `document2`

## Testing

- Backend endpoints can be tested with `curl`, Postman, or any REST client.
- Frontend can be tested by uploading documents through the UI.
- Ensure the backend is running and the frontend points to the correct `VITE_API_URL` if not using the default.

## Deployment Overview

1. Deploy the backend to a Python-capable host with Tesseract installed.
2. Build the frontend with `npm run build`.
3. Serve the generated `frontend/dist` static app from a web server or static hosting provider.
4. Configure the frontend to call your deployed backend API.

## Important Limitation

This system performs OCR-based academic document analysis and comparison. It does NOT determine the legal authenticity of documents, verify official validity, or replace formal document verification processes.
