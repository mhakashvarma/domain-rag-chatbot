
import streamlit as st

from document_loader import extract_text_from_pdf
from chunker import split_documents
from vector_store import create_vector_store
from rag_pipeline import answer_question


st.set_page_config(
    page_title="Domain-Specific RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Domain-Specific RAG Chatbot")
st.caption(
    "Ask questions about your PDFs or have a general conversation."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []


with st.sidebar:
    st.header("📄 Document Upload")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process Documents", type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            try:
                all_pages = []

                for uploaded_file in uploaded_files:
                    uploaded_file.seek(0)
                    pages = extract_text_from_pdf(uploaded_file)

                    if not pages:
                        st.warning(
                            f"No extractable text found in "
                            f"{uploaded_file.name}."
                        )

                    all_pages.extend(pages)

                if not all_pages:
                    st.error(
                        "No readable text was found in the uploaded PDFs."
                    )
                else:
                    chunks = split_documents(all_pages)

                    with st.spinner(
                        "Creating embeddings and indexing documents..."
                    ):
                        new_vector_store = create_vector_store(chunks)

                    st.session_state.vector_store = new_vector_store
                    st.session_state.processed_files = [
                        file.name for file in uploaded_files
                    ]
                    st.session_state.messages = []

                    st.success(
                        f"Processed {len(uploaded_files)} PDF file(s) "
                        f"into {len(chunks)} chunks."
                    )

            except Exception as error:
                st.error(f"Document processing failed: {error}")

    if st.session_state.processed_files:
        st.subheader("Processed Documents")

        for filename in st.session_state.processed_files:
            st.write(f"📄 {filename}")

    st.divider()

    st.caption(
        "General questions can be answered without uploading a PDF. "
        "For PDF-specific answers, upload and process your documents."
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("Clear Processed Documents"):
        st.session_state.vector_store = None
        st.session_state.processed_files = []
        st.session_state.messages = []
        st.rerun()


# Display previous conversation.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("mode"):
            st.caption(message["mode"])

        if message.get("sources"):
            with st.expander("📚 View Sources"):
                for source in message["sources"]:
                    st.write(
                        f'{source["source"]} — Page {source["page"]}'
                    )


question = st.chat_input(
    "Ask anything, or ask about your uploaded PDFs..."
)

if question:
    # Display and save the user's question.
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Use earlier messages, excluding the current question.
    chat_history = st.session_state.messages[:-1]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = answer_question(
                    st.session_state.vector_store,
                    question,
                    chat_history=chat_history
                )

                st.markdown(result["answer"])
                st.caption(result["mode"])

                if result["sources"]:
                    with st.expander(
                        "📚 View Sources",
                        expanded=True
                    ):
                        for source in result["sources"]:
                            st.write(
                                f'{source["source"]} — '
                                f'Page {source["page"]}'
                            )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                    "mode": result["mode"]
                })

            except Exception as error:
                error_message = (
                    f"Could not generate an answer: {error}"
                )
                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                    "mode": "Error"
                })
