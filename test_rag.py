
from document_loader import extract_text_from_pdf
from chunker import split_documents
from vector_store import create_vector_store
from rag_pipeline import answer_question

pages = extract_text_from_pdf("documents/sample.pdf")
chunks = split_documents(pages)

vector_store = create_vector_store(chunks)

question = "What is the purpose of Hackfest?"

result = answer_question(vector_store, question)

print("\nQuestion:", question)
print("\nAnswer:", result["answer"])
print("\nSources:")

for source in result["sources"]:
    print(f'{source["source"]}, Page {source["page"]}')
