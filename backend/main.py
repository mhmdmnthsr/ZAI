from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.pdf_loader import load_and_split_pdfs  # Extract and split PDFs
from utils.vector_store import save_to_chroma
from utils.rag_chain import get_rag_chain
from routers import upload
from pydantic import BaseModel
import os

app = FastAPI()

# Include the upload router if needed elsewhere
app.include_router(upload.router)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev; restrict later in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Folder to store uploaded PDFs
PDF_DIR = "pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# ----------------------------
# ✅ Upload PDF Endpoint
# ----------------------------

class Question(BaseModel):
    question: str
    chat_history: list = []

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    print("📥 Upload endpoint hit!")  # Debug log
    try:
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded!")

        file_path = os.path.join(PDF_DIR, file.filename)

        # Save uploaded PDF
        with open(file_path, "wb") as f:
            f.write(await file.read())
        print(f"✅ Saved file to: {file_path}")

        # Process PDFs & update ChromaDB
        documents = load_and_split_pdfs()
        print(f"✅ Loaded {len(documents)} document chunks")
        save_to_chroma(documents)

        return {"message": f"✅ Successfully uploaded {file.filename}"}

    except Exception as e:
        print(f"❌ Upload Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
# ✅ List Uploaded PDFs
# ----------------------------
@app.get("/list_pdfs")
async def list_pdfs():
    try:
        files = os.listdir(PDF_DIR)
        return {"pdfs": files}
    except Exception as e:
        print(f"❌ List PDFs Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
# ✅ Ask a Question Endpoint
# ----------------------------

@app.post("/ask")
async def ask_question(data: Question):
    question = data.question
    print(f"🤔 Incoming question: {question}")

    try:
        # Build the RAG chain
        rag_chain = get_rag_chain()
        print("✅ RAG chain created successfully")

        # Invoke the chain
        result = rag_chain.invoke({"query": question})
        print(f"🧠 RAG Result: {result}")

        if isinstance(result, dict) and "result" in result:
            return {"answer": result["result"]}
        elif isinstance(result, str):
            return {"answer": result}
        else:
            return {"answer": "⚠️ No answer generated. Check embeddings or RAG chain."}

    except Exception as e:
        import traceback
        print("❌ Ask Question Error:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


#@app.post("/ask/")
#async def ask_question(data: Question):
#    try:
#        # Pass the question + history to LangChain
#        response = qa_chain({
#            "question": data.question,
#            "chat_history": data.chat_history
#        })
#
#        return {
#            "answer": response["answer"],
#            "sources": [doc.metadata.get("source", "") for doc in response["source_documents"]],
#            "chat_history": response.get("chat_history", [])
#        }
#
#    except Exception as e:
#        return {"error": str(e)}



# ----------------------------
# ✅ Root Endpoint (For Testing)
# ----------------------------
@app.get("/")
def root():
    return {"message": "PDF Q&A API is running 🚀"}
