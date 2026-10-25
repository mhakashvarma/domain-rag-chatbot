
# Domain-Specific RAG Chatbot for PDF Question Answering

## 1. Project Overview

The Domain-Specific RAG Chatbot is an AI-powered application that allows users to upload PDF documents and ask questions in natural language. It retrieves relevant information from the uploaded documents and generates answers grounded in the retrieved text.

The application also displays source document names and page numbers to help users verify answers.

## 2. Problem Statement

Searching lengthy documents manually is time-consuming. This project simplifies document search by providing a chatbot that retrieves relevant passages and answers questions based on uploaded PDFs.

## 3. Objectives

- Extract text from PDF documents.
- Split extracted text into manageable chunks.
- Generate text embeddings using a pretrained model.
- Store and retrieve embeddings using FAISS.
- Generate answers using a language model.
- Display source document names and page numbers.
- Refuse to answer when information is unavailable.
- Provide an interactive Streamlit interface.

## 4. Technologies Used

- Programming Language: Python
- PDF Processing: pypdf
- Text Splitting: LangChain Text Splitters
- Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
- Vector Store: FAISS
- Language Model: Groq API
- User Interface: Streamlit
- Environment Variables: python-dotenv
- Version Control: Git and GitHub

## 5. Project Workflow

1. Upload PDF documents.
2. Extract text and preserve page metadata.
3. Split the extracted text into overlapping chunks.
4. Generate embeddings for each chunk.
5. Store embeddings in the FAISS vector index.
6. Retrieve relevant chunks for each question.
7. Generate an answer using the retrieved context.
8. Display the answer and available source references.

## 6. Project Structure

```text
domain_rag_chatbot/
├── app.py
├── document_loader.py
├── chunker.py
├── vector_store.py
├── rag_pipeline.py
├── prompt.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── documents/
├── tests/
│   └── test_questions.csv
└── test_rag.py
```

## 7. Installation and Setup

### Prerequisites

- Python 3.11
- pip
- A Groq API key

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_actual_api_key
```

Never commit your `.env` file or share your API key.

### Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, upload PDF documents, click Process Documents, and ask questions.

## 8. Main Features

- Multiple PDF uploads
- Page-wise PDF text extraction
- Text chunking with overlap
- Semantic retrieval using embeddings and FAISS
- AI-generated answers grounded in retrieved context
- Source document and page references
- Fallback response for unavailable information
- Chat history
- Document and chat clearing controls

## 9. Testing and Evaluation

The project includes a CSV file containing 15 planned test questions.

Evaluation criteria include:
- Retrieval relevance
- Answer correctness
- Groundedness
- Refusal quality
- Source citation quality
- Response time

Test results should be recorded after running the questions against the actual documents.

## 10. Limitations

- Scanned PDFs may require OCR.
- Answers depend on document quality and retrieval relevance.
- The language model may still generate unsupported claims.
- Internet access and a valid API key are required for Groq inference.
- High-stakes information should always be verified against the original document.

## 11. Future Enhancements

- OCR for scanned documents
- Conversation memory
- Document category filters
- User authentication and access control
- Feedback on answer quality
- Automated retrieval evaluation
- Cloud deployment

## 12. Responsible AI

The chatbot is designed to answer using retrieved document context and provide source references. Users should verify important information against the original documents. API keys and confidential documents must be handled securely.

## 13. Conclusion

This project demonstrates how Retrieval-Augmented Generation combines document processing, embeddings, vector search, and a language model to create an interactive PDF question-answering application.
