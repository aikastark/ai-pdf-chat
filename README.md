# AI PDF Chat

A small FastAPI app for chatting with a PDF using OpenAI embeddings, FAISS search, and a lightweight retrieval-augmented generation flow.

## What It Does

- Upload a PDF from the browser.
- Extract text from the PDF with `pypdf`.
- Build an in-memory FAISS vector index with OpenAI embeddings.
- Ask questions about the uploaded document.
- Answer only from the retrieved document context.

## Project Structure

```text
.
+-- index.html      # Browser UI
+-- main.py         # FastAPI app and routes
+-- pdf_reader.py   # PDF text extraction
+-- rag.py          # Embeddings, FAISS index, and chat query logic
+-- uploads/        # Uploaded PDFs, ignored by git
`-- .env            # Local environment variables, ignored by git
```

## Requirements

- Python 3.10+
- An OpenAI API key

Install the Python packages:

```bash
pip install fastapi uvicorn python-multipart pypdf openai faiss-cpu numpy python-dotenv
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

Make sure the upload directory exists:

```bash
mkdir uploads
```

## Run The App

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Open the app:

```text
http://127.0.0.1:8000
```

## API

### `GET /`

Serves the browser UI from `index.html`.

### `POST /upload`

Uploads and processes a PDF.

Form field:

- `file`: the PDF file to index

Response:

```json
{
  "message": "PDF uploaded and processed"
}
```

### `POST /ask`

Asks a question about the current uploaded PDF.

Body:

```json
{
  "question": "What is this document about?"
}
```

Response:

```json
{
  "answer": "..."
}
```

## Notes

- The FAISS index is stored in memory, so it resets when the server restarts.
- Uploading a new PDF replaces the current in-memory document index.
- If no PDF has been uploaded yet, the app returns `No document uploaded yet.`
