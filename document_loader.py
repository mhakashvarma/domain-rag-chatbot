
from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()

        if text:
            source = (
                pdf_file.name
                if hasattr(pdf_file, "name")
                else Path(pdf_file).name
            )

            documents.append({
                "text": text,
                "source": source,
                "page": page_number
            })

    return documents
