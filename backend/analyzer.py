import os
import sys
import tempfile
from pathlib import Path

import pytesseract
from PIL import Image
import fitz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ocr.field_extractor import extract_fields
from classifier import classify_document
from summarizer import summarize_academic_data

pytesseract.pytesseract.tesseract_cmd = os.environ.get(
    "TESSERACT_PATH",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def image_to_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def pdf_to_text(pdf_path):
    document = fitz.open(pdf_path)
    text_pages = []

    for page in document:
        pix = page.get_pixmap(dpi=200)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
            temp_img.write(pix.tobytes("png"))
            temp_img.flush()
            text_pages.append(image_to_text(temp_img.name))
        try:
            os.remove(temp_img.name)
        except OSError:
            pass

    return "\n".join(text_pages)


def compute_statistics(fields):
    subjects = fields.get("subjects", [])
    if not subjects:
        return {
            "subjects_count": 0,
            "average_marks": None,
            "highest_marks": None,
            "lowest_marks": None,
            "total_marks": None,
        }

    marks = [item.get("marks") for item in subjects if isinstance(item.get("marks"), (int, float))]
    marks = [m for m in marks if m is not None]

    if not marks:
        return {
            "subjects_count": len(subjects),
            "average_marks": None,
            "highest_marks": None,
            "lowest_marks": None,
            "total_marks": None,
        }

    total = sum(marks)
    average = round(total / len(marks), 2)

    return {
        "subjects_count": len(marks),
        "average_marks": average,
        "highest_marks": max(marks),
        "lowest_marks": min(marks),
        "total_marks": total,
    }


def analyze_document(file_path):
    suffix = Path(file_path).suffix.lower()

    try:
        if suffix == ".pdf":
            ocr_text = pdf_to_text(file_path)
        else:
            ocr_text = image_to_text(file_path)
    except Exception as exc:
        return {"error": f"Unable to process the document: {exc}"}

    if not ocr_text or not ocr_text.strip():
        return {"error": "We could not extract readable text from this document."}

    fields = extract_fields(ocr_text)
    statistics = compute_statistics(fields)
    classification = classify_document(ocr_text)
    summary = summarize_academic_data(fields, classification, statistics)

    return {
        "ocr_text": ocr_text,
        "data": fields,
        "statistics": statistics,
        "document_type": classification["document_type"],
        "confidence": classification["confidence"],
        "summary": summary,
    }