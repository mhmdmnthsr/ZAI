# PDF AI Assistant

A simple web-based PDF Question & Answer system using **FastAPI**, **React**, and **LangChain**. Upload PDFs and ask questions about their content.

---

## Features

- Upload PDF files to the backend
- Search and list uploaded PDFs
- Ask questions about the PDFs using a RAG (Retrieval-Augmented Generation) chain
- Minimal and responsive React frontend

---

## Project Structure

```
backend/        # FastAPI backend
frontend/       # React frontend
utils/          # Helper scripts (PDF loader, vector store, RAG chain)
routers/        # API routes
pdfs/           # Uploaded PDFs
```

---

## Requirements

- Python 3.13+
- Node.js 18+
- OpenAI API key (for embeddings & chat)
- Virtual environment for Python packages

---

## Setup

### Backend

1. Navigate to `backend/`:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

2. Set environment variable:
   ```bash
   export OPENAI_API_KEY="your_openai_key"
   ```

3. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend

1. Navigate to `frontend/`:
   ```bash
   cd frontend
   npm install
   npm start
   ```

2. Open browser at `http://localhost:3000`

---

## Usage

1. Upload PDFs via the left panel.
2. Ask questions in the right panel.
3. View the answers and source PDFs.
red.

