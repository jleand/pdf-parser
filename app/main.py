import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

try:
    from pdf_parser import parse_pdf
except ModuleNotFoundError:
    from app.pdf_parser import parse_pdf

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("pdf_parser")

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", str(20 * 1024 * 1024)))
MAX_CONCURRENT = int(os.getenv("MAX_CONCURRENT", "4"))

_semaphore = asyncio.Semaphore(MAX_CONCURRENT)


class ParseResponse(BaseModel):
    status: str
    data: str | None = None
    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    data: str
    error: None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("PDF Parser service starting")
    yield
    logger.info("PDF Parser service shutting down")


app = FastAPI(
    title="PDF Parser",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", data="healthy")


@app.post("/parse", response_model=ParseResponse)
async def parse(file: UploadFile = File(...), lang: str = "eng"):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB",
        )

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="File is not a valid PDF")

    try:
        async with _semaphore:
            text = await asyncio.to_thread(parse_pdf, content, lang)
        logger.info("Parsed %s (%d bytes, %d chars extracted)", file.filename, len(content), len(text))
        return ParseResponse(status="ok", data=text)
    except Exception as e:
        logger.exception("Failed to parse %s", file.filename)
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ParseResponse(status="error", error=exc.detail).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content=ParseResponse(status="error", error="Internal server error").model_dump(),
    )
