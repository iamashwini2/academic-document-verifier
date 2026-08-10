from field_extractor import extract_fields

text = """
ABC COLLEGE

STUDENT ACADEMIC RECORD

Name: Ashwini
Registration Number: MCA2026001
Course: MCA
Department: Computer Applications
Academic Year: 2025-2026
Semester: IV
Result: PASS
"""

fields = extract_fields(text)

print("\n===== EXTRACTED ACADEMIC INFORMATION =====\n")

for key, value in fields.items():
    print(f"{key}: {value}")