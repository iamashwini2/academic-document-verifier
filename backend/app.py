import os
import sys
import tempfile
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from analyzer import analyze_document
from comparison import compare_documents
from security import is_allowed_file

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["JSON_SORT_KEYS"] = False
CORS(app)

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

    if not is_allowed_file(file.filename):
        return error_response("Unsupported file type. Please upload PNG, JPG, JPEG or PDF.")

    suffix = Path(file.filename).suffix.lower()
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

    if not is_allowed_file(document1.filename) or not is_allowed_file(document2.filename):
        return error_response("Unsupported file type. Please upload PNG, JPG, JPEG or PDF.")

    temp_files = []
    try:
        for document in (document1, document2):
            suffix = Path(document.filename).suffix.lower()
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
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "1") != "0",
    )