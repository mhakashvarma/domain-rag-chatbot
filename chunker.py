
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for document in documents:
        text_chunks = splitter.split_text(document["text"])

        for chunk in text_chunks:
            chunks.append({
                "text": chunk,
                "source": document["source"],
                "page": document["page"]
            })

    return chunks
