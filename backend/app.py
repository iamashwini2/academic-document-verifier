import os
import sys
import tempfile
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.analyzer import analyze_document
from backend.comparison import compare_documents
from backend.security import is_allowed_file


def get_cors_origins():
    configured = os.environ.get("CORS_ORIGINS", "").strip()
    origins = [origin.strip() for origin in configured.split(",") if origin.strip()]
    if not origins:
        origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    return origins


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["JSON_SORT_KEYS"] = False
CORS(app, resources={r"/api/*": {"origins": get_cors_origins()}})

def error_response(message, status_code=400):
    return jsonify({"success": False, "error": message}), status_code


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(_error):
    return error_response("File is too large. Maximum size is 10 MB."), 413


@app.route("/")
def home():

    return jsonify({
        "success": True,
        "message": "Academic Document Intelligence API is running"
    })


@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return error_response("No document uploaded.")

    file = request.files["file"]
    if not file or file.filename == "":
        return error_response("No file selected.")

    safe_name = secure_filename(file.filename)
    if not safe_name:
        return error_response("Invalid file name.")

    if not is_allowed_file(safe_name):
        return error_response("Unsupported file type. Please upload PNG, JPG, JPEG or PDF.")

    suffix = Path(safe_name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        file.save(temp_file)
        temp_path = temp_file.name

    try:
        result = analyze_document(temp_path)
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass

    if result.get("error"):
        return error_response(result["error"])

    return jsonify({
        "success": True,
        "filename": file.filename,
        "document_type": result.get("document_type"),
        "confidence": result.get("confidence"),
        "ocr_text": result.get("ocr_text"),
        "data": result.get("data"),
        "summary": result.get("summary"),
        "statistics": result.get("statistics"),
    })


@app.route("/api/compare", methods=["POST"])
def compare():
    document1 = request.files.get("document1")
    document2 = request.files.get("document2")

    if not document1 or not document2:
        return error_response("Please upload two academic documents for comparison.")

    safe_name_1 = secure_filename(document1.filename)
    safe_name_2 = secure_filename(document2.filename)
    if not safe_name_1 or not safe_name_2:
        return error_response("Invalid file name.")

    if not is_allowed_file(safe_name_1) or not is_allowed_file(safe_name_2):
        return error_response("Unsupported file type. Please upload PNG, JPG, JPEG or PDF.")

    temp_files = []
    try:
        for document, safe_name in ((document1, safe_name_1), (document2, safe_name_2)):
            suffix = Path(safe_name).suffix.lower()
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            document.save(temp)
            temp.close()
            temp_files.append(temp.name)

        result = compare_documents(temp_files[0], temp_files[1])
    finally:
        for path in temp_files:
            try:
                os.remove(path)
            except OSError:
                pass

    if result.get("error"):
        return error_response(result["error"])

    return jsonify({
        "success": True,
        "document1": document1.filename,
        "document2": document2.filename,
        "document1_data": result["document1"],
        "document2_data": result["document2"],
        "comparison": result["comparison"],
    })


if __name__ == "__main__":

    print()
    print("======================================")
    print(" Academic Document Analyzer API")
    print("======================================")
    print()

    app.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "0") != "0",
    )