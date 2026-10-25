# 📚 Domain-Specific RAG Chatbot

A Python-based AI chatbot that allows users to upload PDF documents, ask questions about their content, and receive contextual answers with source references. It also supports general conversation and follow-up questions.

**Built with:** Python · Streamlit · LangChain · FAISS · Sentence Transformers · Groq

## 🚀 Live Demo

**Try the application:** [Add your Streamlit Community Cloud URL here]

**GitHub Repository:** https://github.com/mhakashvarma/domain-rag-chatbot

> Replace the live demo placeholder with your deployed Streamlit URL before publishing this README.

## 📌 Project Overview

Large PDF documents can be difficult to search manually. Finding a particular answer may require reading many pages and understanding where the relevant information appears.

This project addresses that problem through **Retrieval-Augmented Generation (RAG)**. Users upload PDF documents, and the application extracts their text, divides it into smaller chunks, creates vector embeddings, and stores them in a FAISS vector index. When a document-related question is asked, the system retrieves relevant chunks and provides them to a language model to generate an answer.

The chatbot also supports general questions and uses recent conversation history to understand follow-up questions.

## 🎯 Problem Statement

Searching large documents manually is time-consuming and inefficient. Traditional keyword searches may also miss relevant information when the wording of a question differs from the wording in a document.

The proposed system provides a conversational interface for querying PDF documents using natural language, retrieving relevant content, and displaying source document and page information to help users verify answers.

## ✨ Features

- 📄 **PDF Upload:** Upload one or more PDF documents through the Streamlit interface.
- 📝 **Text Extraction:** Extract readable text from PDF pages using PyPDF.
- ✂️ **Text Chunking:** Split extracted text into smaller, overlapping chunks.
- 🧠 **Text Embeddings:** Convert text chunks into numerical vector representations.
- 🔎 **Semantic Retrieval:** Use FAISS to retrieve relevant document chunks.
- 🤖 **AI-Powered Answers:** Use the Groq API with the `openai/gpt-oss-20b` model to generate responses.
- 📚 **Source References:** Display source filenames and page numbers for cited document content.
- 💬 **General Conversation:** Answer general questions without requiring PDF retrieval.
- 🔄 **Follow-Up Questions:** Use recent chat history to understand conversational references.
- 🛡️ **Grounded Responses:** Instruct the model to avoid unsupported claims about uploaded documents.
- 🗂️ **Multiple PDF Support:** Process multiple PDFs together in one document index.
- 🧹 **Chat Controls:** Clear the chat or processed documents from the interface.
- ☁️ **Cloud Deployment:** Designed to run locally and deploy through Streamlit Community Cloud.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| PyPDF | PDF text extraction |
| LangChain | Text processing and language-model integration |
| Sentence Transformers | Text embedding generation |
| `all-MiniLM-L6-v2` | Embedding model |
| FAISS | Vector similarity search |
| Groq API | Language-model response generation |
| `openai/gpt-oss-20b` | Configured Groq model |
| python-dotenv | Loading local environment variables |
| Git and GitHub | Version control and source-code hosting |
| Streamlit Community Cloud | Online application deployment |

## 🏗️ System Architecture

The application follows a Retrieval-Augmented Generation workflow.

```text
                 USER
                  |
                  v
          Streamlit Interface
                  |
                  v
          Upload PDF Documents
                  |
                  v
          Extract PDF Text
                  |
                  v
          Split Text into Chunks
                  |
                  v
          Generate Embeddings
                  |
                  v
           FAISS Vector Index
                  |
                  v
           User Asks Question
                  |
                  v
       Question Routing and Retrieval
                  |
                  v
       Retrieve Relevant Text Chunks
                  |
                  v
        Construct Prompt with Context
                  |
                  v
             Groq LLM
                  |
                  v
        Generate Conversational Answer
                  |
                  v
       Display Answer and Source Details
```

General questions can follow a separate path without retrieving PDF content. The current implementation uses phrase-based routing to distinguish general questions from document-related questions.

## 🔄 How the RAG Workflow Works

### 1. Document Upload

The user uploads one or more PDF files through the Streamlit sidebar.

### 2. Text Extraction

The application extracts readable text from each PDF page and records metadata such as the filename and page number.

### 3. Chunking

The extracted text is divided into smaller chunks to make retrieval more efficient.

The current configuration uses a chunk size of 800 characters and an overlap of 120 characters.

### 4. Embedding Generation

Each chunk is converted into a vector representation using the Sentence Transformers model `sentence-transformers/all-MiniLM-L6-v2`.

### 5. Vector Storage

The vectors are stored in a FAISS index, enabling similarity-based retrieval of relevant document content.

### 6. Question Processing

The chatbot determines whether a question appears to require PDF information or is a general conversational question.

For document-related questions, it searches the vector index for relevant chunks.

### 7. Answer Generation

The retrieved text is included in the prompt sent to the Groq language model. The model is instructed to answer document-specific questions using the supplied context and cite supporting source IDs.

For general questions, the chatbot can generate an answer without retrieving PDF content.

### 8. Source Display

When the generated answer cites retrieved chunks, the interface displays the corresponding source filenames and page numbers.

## 📁 Project Structure

```text
domain-rag-chatbot/
│
├── .vscode/
│   └── settings.json
│
├── documents/
│   └── sample.pdf
│
├── tests/
│   └── test_questions.csv
│
├── app.py
├── document_loader.py
├── chunker.py
├── vector_store.py
├── rag_pipeline.py
├── prompt.py
│
├── test_loader.py
├── test_chunker.py
├── test_vector_store.py
├── test_rag.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

### File Descriptions

| File | Description |
|---|---|
| `app.py` | Streamlit user interface, PDF uploads, chat history, and source display |
| `document_loader.py` | Extracts text and page metadata from PDF files |
| `chunker.py` | Splits extracted text into overlapping chunks |
| `vector_store.py` | Creates the embedding model and FAISS vector index and performs retrieval |
| `rag_pipeline.py` | Handles question routing, conversation history, retrieval, Groq calls, and source citations |
| `prompt.py` | Defines the assistant's behavior and document-grounding instructions |
| `test_loader.py` | Tests PDF text extraction |
| `test_chunker.py` | Tests document chunking |
| `test_vector_store.py` | Tests embedding generation and vector retrieval |
| `test_rag.py` | Tests the end-to-end question-answering pipeline |
| `tests/test_questions.csv` | Contains planned questions and expected testing behavior |
| `requirements.txt` | Lists the Python dependencies |
| `.gitignore` | Excludes sensitive files and generated artifacts from Git |

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11 recommended
- Git
- A Groq API key
- Internet access for downloading dependencies and accessing the Groq API

### 1. Clone the Repository

```bash
git clone https://github.com/mhakashvarma/domain-rag-chatbot.git
cd domain-rag-chatbot
```

### 2. Create a Virtual Environment

Using Conda:

```bash
conda create -n domain_rag python=3.11
conda activate domain_rag
```

If the environment already exists, activate it instead of creating it again.

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Groq API Key

Create a `.env` file in the project root directory:

```text
GROQ_API_KEY=your_actual_groq_api_key
```

Replace the placeholder with your own key.

Obtain an API key from [Groq Console](https://console.groq.com/keys).

**Security:** Never commit `.env` or expose your API key in source code, screenshots, or public repositories. The `.env` file should remain excluded through `.gitignore`.

### 5. Run the Application

```bash
streamlit run app.py --server.fileWatcherType none
```

The application should open in your browser. If it does not, open:

```text
http://localhost:8501
```

## ☁️ Cloud Deployment

The application can be deployed using [Streamlit Community Cloud](https://share.streamlit.io/).

1. Push the project to GitHub.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Create an app using the `main` branch and `app.py` as the main file.
4. Configure the application secret:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
```

5. Deploy the application and test PDF upload, document processing, chat responses, and source display.

Do not store the actual API key in the GitHub repository. Configure it only in the deployment platform's Secrets settings.

## 💬 How to Use the Chatbot

### Step 1: Open the Application

Open the local application or the deployed Streamlit URL.

### Step 2: Upload PDF Documents

Use the sidebar to upload one or more PDF files.

### Step 3: Process Documents

Click **Process Documents** and wait for text extraction, chunking, embedding generation, and vector indexing to finish.

### Step 4: Ask Questions

Enter a question in the chat input.

Examples:

- According to the uploaded PDF, what is the purpose of Hackfest?
- Summarize the main points in the document.
- Explain Python functions with an example.
- What does the second point mean?

### Step 5: View Sources

For document-grounded answers, expand **View Sources** to inspect the source filename and page number associated with cited content.

### Step 6: Continue the Conversation

Ask follow-up questions to build on earlier answers. The application passes recent chat messages to the language model.

## 🧪 Testing

The project includes individual test scripts for the main components.

Run the tests from the project root using:

```bash
python test_loader.py
python test_chunker.py
python test_vector_store.py
python test_rag.py
```

The `tests/test_questions.csv` file provides a collection of planned test questions, including document-related, general, and unsupported questions.

### Recommended Test Cases

| Test | Expected Behavior |
|---|---|
| Upload a readable PDF | Text is extracted |
| Process a PDF | Chunks and a FAISS index are created |
| Ask a question answered in the PDF | A context-based answer is generated |
| Inspect source references | Cited sources show filename and page |
| Ask about unavailable PDF information | The document fallback is returned |
| Ask a general programming question | A general answer is generated |
| Ask a follow-up question | Recent conversation history is used |
| Upload multiple PDFs | Documents are indexed together |
| Omit the API key | A clear configuration error is reported |

These are recommended checks; results should be recorded from actual test runs.

## 🔐 Security and Responsible AI

- Store API credentials in environment variables or deployment secrets.
- Keep `.env` out of GitHub.
- Treat uploaded document text as untrusted input.
- Use retrieved context to ground document-specific answers.
- Display source information to help users verify responses.
- Do not assume every generated answer is correct simply because it includes a citation.

## ⚠️ Limitations

- The current implementation supports PDF files rather than every document format.
- Scanned PDFs may require OCR if they do not contain extractable text.
- Retrieval quality depends on document quality, chunking, embeddings, and question wording.
- Question routing uses phrase-based rules and may occasionally classify ambiguous questions incorrectly.
- Source display is based on source IDs cited by the model; citations should still be checked for relevance and correctness.
- Conversation history is limited to recent messages in the active Streamlit session and is not permanent cross-session memory.
- Uploaded documents and the FAISS index are not managed as persistent, user-specific knowledge bases.
- The application depends on access to the Groq API for answer generation.
- Cloud deployment is subject to the hosting platform's resource limits.

## 🔮 Future Enhancements

Possible improvements include:

- Improved AI-based question classification
- Follow-up question rewriting for more reliable retrieval
- Retrieval relevance thresholds and reranking
- OCR support for scanned PDFs
- Support for DOCX and TXT files
- Persistent conversation history
- User authentication and document access controls
- Automated retrieval and answer-quality evaluation
- Streaming responses
- Downloadable conversation history
- Better logging and error reporting

## 📝 Conclusion

The Domain-Specific RAG Chatbot demonstrates how PDF processing, semantic search, vector databases, and large language models can be combined to create a conversational question-answering application.

By retrieving relevant document chunks before generating answers, the system aims to provide useful document-grounded responses while retaining the flexibility of general conversation.

The project provides a foundation for more advanced knowledge assistants with improved retrieval, persistent memory, document management, and evaluation capabilities.

## 👨‍💻 Author

**Project:** Domain-Specific RAG Chatbot  
**GitHub:** [mhakashvarma/domain-rag-chatbot](https://github.com/mhakashvarma/domain-rag-chatbot)

Developed as an academic project exploring Retrieval-Augmented Generation, semantic search, and conversational AI.
