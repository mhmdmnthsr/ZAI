import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.pdf_loader import load_and_split_pdfs
from utils.vector_store import save_to_chroma

PDF_DIR = "pdfs"
router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Save uploaded PDF to the pdfs folder
        if not os.path.exists(PDF_DIR):
            os.makedirs(PDF_DIR)

        file_name = file.filename or "uploaded_file.pdf"  # Fallback filename if None
        file_path = os.path.join(PDF_DIR, file_name)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract and store embeddings
        documents = load_and_split_pdfs([file_path])
        if not documents:
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF.")

        save_to_chroma(documents)

        return {"message": f"✅ Successfully uploaded and processed {file.filename}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
