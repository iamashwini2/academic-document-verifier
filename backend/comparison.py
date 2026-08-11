from backend.analyzer import analyze_document

COMPARE_FIELDS = [
    "name",
    "registration_number",
    "course",
    "department",
    "academic_year",
    "semester",
    "result",
    "average_marks"
]


def normalize_value(value):
    if value is None:
        return None
    return str(value).strip().lower()


def build_subject_map(subjects):
    subject_map = {}
    for subject in subjects:
        name = subject.get("subject")
        marks = subject.get("marks")
        if not name:
            continue
        key = name.strip().lower()
        if key:
            subject_map[key] = {
                "subject": subject["subject"].strip(),
                "marks": marks
            }
    return subject_map


def compare_documents(file1: str, file2: str) -> dict:
    document1 = analyze_document(file1)
    document2 = analyze_document(file2)

    data1 = document1["data"]
    data2 = document2["data"]

    fields = []
    for field in COMPARE_FIELDS:
        value1 = data1.get(field)
        value2 = data2.get(field)
        normalized1 = normalize_value(value1)
        normalized2 = normalize_value(value2)

        if normalized1 and normalized2:
            status = "MATCH" if normalized1 == normalized2 else "DIFFERENT"
        else:
            status = "MISSING"

        fields.append({
            "field": field,
            "document1": value1 or None,
            "document2": value2 or None,
            "status": status
        })

    subjects1 = build_subject_map(data1.get("subjects", []))
    subjects2 = build_subject_map(data2.get("subjects", []))
    subject_keys = sorted(set(subjects1.keys()) | set(subjects2.keys()))

    subjects = []
    for key in subject_keys:
        entry1 = subjects1.get(key)
        entry2 = subjects2.get(key)
        if entry1 and entry2:
            status = "MATCH" if entry1["marks"] == entry2["marks"] else "DIFFERENT"
        else:
            status = "MISSING"

        subjects.append({
            "subject": entry1["subject"] if entry1 else entry2["subject"],
            "document1": entry1["marks"] if entry1 else None,
            "document2": entry2["marks"] if entry2 else None,
            "status": status
        })

    matched_fields = sum(1 for field in fields if field["status"] == "MATCH")
    matched_subjects = sum(1 for subject in subjects if subject["status"] == "MATCH")
    total_subjects = len(subjects)
    total_fields = len(fields)

    summary_parts = [
        f"{matched_fields} of {total_fields} academic fields match."
    ]

    if total_subjects:
        summary_parts.append(f"{matched_subjects} of {total_subjects} subjects match.")
    else:
        summary_parts.append("No subject records were available for comparison.")

    summary = " ".join(summary_parts)

    return {
        "document1": document1,
        "document2": document2,
        "comparison": {
            "fields": fields,
            "subjects": subjects,
            "summary": summary
        }
    }
