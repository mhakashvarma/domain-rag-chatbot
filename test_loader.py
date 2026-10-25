
from document_loader import extract_text_from_pdf

pdf_path = "documents/sample.pdf"

pages = extract_text_from_pdf(pdf_path)

print("Total pages with extracted text:", len(pages))

for page in pages[:3]:
    print("\nSource:", page["source"])
    print("Page:", page["page"])
    print("Text:", page["text"][:300])
