def summarize_academic_data(fields: dict, classification: dict, statistics: dict) -> str:
    parts = []
    name = fields.get("name")
    course = fields.get("course")
    department = fields.get("department")
    academic_year = fields.get("academic_year")
    semester = fields.get("semester")
    result = fields.get("result")
    subjects_count = statistics.get("subjects_count", 0)
    average = statistics.get("average_marks")
    highest = statistics.get("highest_marks")
    lowest = statistics.get("lowest_marks")

    if name or course or department or academic_year or semester:
        subject = name or "The student"
        details = []

        if course:
            details.append(course)
        if department:
            details.append(f"{department} department")
        if academic_year:
            details.append(f"for the {academic_year} academic year")
        if semester:
            details.append(f"in semester {semester}")

        if details:
            parts.append(f"{subject} is {' '.join(details)}.")
        else:
            parts.append(f"{subject} appears in the document.")

    if subjects_count:
        subject_word = "subject" if subjects_count == 1 else "subjects"
        parts.append(f"The document contains {subjects_count} {subject_word} with an average score of {average}%.")
        if highest is not None and lowest is not None:
            parts.append(f"The highest mark is {highest}% and the lowest mark is {lowest}%.")
    elif average is not None:
        parts.append(f"The extracted average score is {average}%.")

    if result:
        parts.append(f"The recorded result is {result}.")

    document_type = classification.get("document_type")
    if document_type:
        parts.append(f"This document is classified as {document_type}.")

    summary = " ".join(parts).strip()
    if not summary:
        return "The document was analyzed, but the academic details were not clearly detected."

    return summary
