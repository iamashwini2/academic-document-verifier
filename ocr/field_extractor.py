import re


def extract_fields(text):

    fields = {
        "name": None,
        "registration_number": None,
        "course": None,
        "department": None,
        "academic_year": None,
        "semester": None,
        "result": None,
        "subjects": [],
        "average_marks": None
    }

    patterns = {
        "name": r"Name\s*[:\-]\s*(.+)",
        "registration_number": r"(?:Registration Number|Register Number|Reg No|USN)\s*[:\-]\s*([A-Za-z0-9]+)",
        "course": r"Course\s*[:\-]\s*(.+)",
        "department": r"Department\s*[:\-]\s*(.+)",
        "academic_year": r"Academic Year\s*[:\-]\s*(\d{4}\s*-\s*\d{4})",
        "semester": r"Semester\s*[:\-]\s*(.+)",
        "result": r"Result\s*[:\-]\s*(.+)"
    }

    for field, pattern in patterns.items():

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            fields[field] = match.group(1).strip()

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        match = re.match(
            r"^([A-Za-z][A-Za-z ]+?)\s+(\d{1,3})$",
            line
        )

        if match:

            subject = match.group(1).strip()
            marks = int(match.group(2))

            if 0 <= marks <= 100:

                fields["subjects"].append({
                    "subject": subject,
                    "marks": marks
                })

    if fields["subjects"]:

        total = sum(
            item["marks"]
            for item in fields["subjects"]
        )

        fields["average_marks"] = round(
            total / len(fields["subjects"]),
            2
        )

    return fields