from pypdf import PdfReader

pdf_path = "data/college-dataset.pdf"

reader = PdfReader(pdf_path)

college_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        college_text += text + "\n"

print("PDF loaded successfully.")
print("Number of characters:", len(college_text))