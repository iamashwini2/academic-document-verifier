import pytesseract
from PIL import Image
from field_extractor import extract_fields


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


image = Image.open("processed/academic_processed.png")


text = pytesseract.image_to_string(image)


print("\n===== OCR OUTPUT =====\n")
print(text)


fields = extract_fields(text)


print("\n===== EXTRACTED ACADEMIC INFORMATION =====\n")

print("Name:", fields["name"])
print("Registration Number:", fields["registration_number"])
print("Course:", fields["course"])
print("Department:", fields["department"])
print("Academic Year:", fields["academic_year"])
print("Semester:", fields["semester"])
print("Result:", fields["result"])
print("Average Marks:", fields["average_marks"])


print("\n===== SUBJECT MARKS =====\n")

for item in fields["subjects"]:

    print(
        item["subject"],
        ":",
        item["marks"]
    )