
from document_loader import extract_text_from_pdf
from chunker import split_documents

pages = extract_text_from_pdf("documents/sample.pdf")
chunks = split_documents(pages)

print("Total pages:", len(pages))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3], start=1):
    print("\nChunk:", i)
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("Text:", chunk["text"][:200])
