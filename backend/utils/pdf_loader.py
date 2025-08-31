import os
import PyPDF2
from typing import List, Optional
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

PDF_DIR = "pdfs"

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a given PDF using PyPDF2.
    """
    text = ""
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
    return text


def load_and_split_pdfs(file_paths: Optional[List[str]] = None):
    """
    Loads PDFs, extracts text, and splits them into smaller chunks.
    If no file_paths are provided, loads everything from the pdfs/ folder.
    """
    all_docs = []

    if file_paths is None:  # Default to all PDFs in the folder
        if not os.path.isdir(PDF_DIR):
            print(f"⚠️ Folder '{PDF_DIR}' not found.")
            return all_docs

        file_paths = [
            os.path.join(PDF_DIR, f)
            for f in os.listdir(PDF_DIR)
            if f.lower().endswith(".pdf")
        ]

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for path in file_paths:
        file_name = os.path.basename(path)
        print(f"📄 Extracting: {file_name}")
        text = extract_text_from_pdf(path)

        if text.strip():
            doc = Document(page_content=text, metadata={"source": file_name})
            split_docs = splitter.split_documents([doc])
            all_docs.extend(split_docs)

    print(f"✅ Loaded and split {len(all_docs)} chunks")
    return all_docs
