def classify_document(text: str) -> dict:
    text = text or ""
    lower_text = text.lower()

    if all(token in lower_text for token in ["subject", "marks", "semester", "result"]):
        return {"document_type": "Academic Mark Sheet", "confidence": 90}

    if all(token in lower_text for token in ["certificate", "awarded", "completed"]):
        return {"document_type": "Academic Certificate", "confidence": 94}

    if any(token in lower_text for token in ["transcript", "credits", "gpa", "grade point"]):
        return {"document_type": "Transcript", "confidence": 88}

    if any(token in lower_text for token in ["academic record", "student record", "academic history"]):
        return {"document_type": "Academic Record", "confidence": 86}

    if any(token in lower_text for token in ["grade report", "grade sheet", "marksheet"]):
        return {"document_type": "Grade Report", "confidence": 84}

    if any(token in lower_text for token in ["result", "semester", "marks", "percentage"]):
        return {"document_type": "Student Result", "confidence": 80}

    rules = {
        "Academic Mark Sheet": ["subject", "marks", "semester", "result", "grade", "percentage"],
        "Academic Certificate": ["certificate", "awarded", "completed", "congratulations", "this is to certify"],
        "Transcript": ["transcript", "credits", "course", "gpa", "credit hours", "grade point"],
        "Academic Record": ["academic record", "student record", "academic history", "programme", "program"],
        "Grade Report": ["grade report", "grade", "marks", "percentage"],
        "Student Result": ["result", "semester", "marks", "average", "percentage"]
    }

    best_type = "Unknown Academic Document"
    best_score = 0
    best_confidence = 0

    for document_type, indicators in rules.items():
        score = sum(1 for token in indicators if token in lower_text)
        if score > best_score:
            best_score = score
            best_type = document_type
            best_confidence = min(100, max(35, round((score / len(indicators)) * 100)))

    if best_score == 0:
        return {"document_type": "Unknown Academic Document", "confidence": 0}

    return {"document_type": best_type, "confidence": best_confidence}
