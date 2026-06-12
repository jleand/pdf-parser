from fastapi import FastAPI, UploadFile, File

from pdf_parser import parse_pdf

app = FastAPI(title="PDF Parser", version="1.0.0")


@app.post("/parse")
async def parse(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return {"status": "error", "data": None, "error": "Only PDF files are accepted"}

    try:
        content = await file.read()
        if not content.startswith(b"%PDF"):
            return {"status": "error", "data": None, "error": "File is not a valid PDF"}
        text = parse_pdf(content)
        return {"status": "ok", "data": text, "error": None}
    except Exception as e:
        return {"status": "error", "data": None, "error": str(e)}


@app.get("/health")
async def health():
    return {"status": "ok", "data": "healthy", "error": None}
