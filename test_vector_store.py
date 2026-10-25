
from document_loader import extract_text_from_pdf
from chunker import split_documents
from vector_store import create_vector_store, search_documents

pdf_path = "documents/sample.pdf"

pages = extract_text_from_pdf(pdf_path)
chunks = split_documents(pages)

print("Creating embeddings and FAISS index...")

vector_store = create_vector_store(chunks)

question = "What is the purpose of Hackfest?"

results = search_documents(
    vector_store,
    question,
    k=3
)

print("\nQuestion:", question)

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("Source:", result.metadata["source"])
    print("Page:", result.metadata["page"])
    print("Text:", result.page_content[:300])
