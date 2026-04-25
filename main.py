from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os

from pdf_reader import read_pdf
from rag import rag

app = FastAPI()

UPLOAD_FOLDER = "uploads"

@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = read_pdf(file_path)
    rag.build_index(text)

    return {"message": "PDF uploaded and processed"}


@app.post("/ask")
async def ask_question(q: dict):
    question = q["question"]
    answer = rag.query(question)
    return {"answer": answer}