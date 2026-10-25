
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "vector_store/saved_index"


def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    documents = [
        Document(
            page_content=chunk["text"],
            metadata={
                "source": chunk["source"],
                "page": chunk["page"]
            }
        )
        for chunk in chunks
    ]

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    Path(INDEX_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    vector_store.save_local(INDEX_PATH)

    return vector_store


def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    if not Path(INDEX_PATH).exists():
        raise FileNotFoundError(
            "Vector index not found. Process the PDFs first."
        )

    return FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=False
    )


def search_documents(vector_store, question, k=3):
    return vector_store.similarity_search(
        question,
        k=k
    )
