
import os
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

from prompt import SYSTEM_PROMPT
from vector_store import search_documents

load_dotenv()

FALLBACK = (
    "I could not find this information in the uploaded documents."
)

MODEL_NAME = "openai/gpt-oss-20b"
MAX_HISTORY_MESSAGES = 10


def is_document_question(question):
    """
    Identify questions that probably need information from PDFs.
    Follow-up questions are treated as document questions when a
    previous conversation exists.
    """
    text = question.lower().strip()

    document_phrases = [
        "uploaded document",
        "uploaded pdf",
        "in the document",
        "in this document",
        "in the pdf",
        "according to the pdf",
        "according to the document",
        "from the document",
        "from the pdf",
        "based on the document",
        "based on the pdf",
        "what does the document say",
        "what does the pdf say",
        "summarize this document",
        "summarize the pdf",
        "this file",
        "these documents",
        "these pdfs",
    ]

    if any(phrase in text for phrase in document_phrases):
        return True

    # Follow-up phrases often refer to a previous PDF question.
    follow_up_phrases = [
        "explain more",
        "explain it",
        "tell me more",
        "elaborate",
        "the second point",
        "the first point",
        "that point",
        "what about",
        "why is that",
        "how about that",
        "give an example of that",
        "can you explain that",
    ]

    if any(phrase in text for phrase in follow_up_phrases):
        return True

    return False


def answer_question(vector_store, question, chat_history=None):
    """
    Answer document-specific or general questions.
    chat_history should contain earlier user/assistant message
    dictionaries from Streamlit session state.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )

    chat_history = chat_history or []
    recent_history = chat_history[-MAX_HISTORY_MESSAGES:]

    document_question = is_document_question(question)
    retrieved_docs = []

    # Retrieve PDF content only when the question needs it.
    if vector_store is not None and document_question:
        retrieved_docs = search_documents(
            vector_store,
            question,
            k=3
        )

    context_parts = []
    source_map = {}

    for index, doc in enumerate(retrieved_docs, start=1):
        source_id = f"S{index}"
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "Unknown")

        source_map[source_id] = {
            "source": source,
            "page": page
        }

        context_parts.append(
            f"[{source_id} | Source: {source} | Page: {page}]\n"
            f"{doc.page_content}"
        )

    if context_parts:
        context = "\n\n".join(context_parts)
        document_instructions = (
            "The user is asking about uploaded documents. Use only "
            "the supplied document context to answer document-specific "
            "claims. Cite supporting source IDs such as [S1]. If the "
            "answer is not supported by the context, reply exactly: "
            f"{FALLBACK}\n\n"
            f"Document context:\n{context}"
        )
    elif document_question:
        document_instructions = (
            "The user appears to be asking about uploaded documents, "
            "but no relevant document context was retrieved. Do not "
            "invent document contents. Reply exactly: "
            f"{FALLBACK}"
        )
    else:
        document_instructions = (
            "This appears to be general conversation, not a request "
            "for information from an uploaded PDF. Answer naturally "
            "using general knowledge. Do not claim that your answer "
            "comes from an uploaded document. Do not invent citations."
        )

    llm = ChatGroq(
        model=MODEL_NAME,
        temperature=0
    )

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT + "\n\n" + document_instructions
        )
    ]

    # Restore recent conversation history.
    for item in recent_history:
        role = item.get("role")
        content = item.get("content", "")

        if not content:
            continue

        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=question))

    response = llm.invoke(messages)
    answer = response.content.strip()

    # Keep the document fallback behavior.
    if document_question and FALLBACK.lower() in answer.lower():
        return {
            "answer": FALLBACK,
            "sources": [],
            "mode": "Document search"
        }

    # Only show sources that the model actually cited.
    cited_ids = set(re.findall(r"\[(S\d+)\]", answer))

    sources = [
        source_map[source_id]
        for source_id in source_map
        if source_id in cited_ids
    ]

    return {
        "answer": answer,
        "sources": sources,
        "mode": (
            "Document-grounded answer"
            if document_question
            else "General conversation"
        )
    }
