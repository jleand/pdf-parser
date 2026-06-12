import logging
from io import BytesIO

from pdf2image import convert_from_bytes
from pypdf import PdfReader

logger = logging.getLogger("pdf_parser")

MAX_OCR_PAGES = 50
OCR_DPI = 200


def _has_text_layer(content: bytes) -> bool:
    reader = PdfReader(BytesIO(content))
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            return True
    return False


def _extract_text(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    text_parts: list[str] = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text()
        if t:
            text_parts.append(t.strip())
        if i > 0 and i % 50 == 0:
            logger.debug("Extracted text from %d pages", i)
    return "\n\n".join(text_parts)


def _ocr_text(content: bytes) -> str:
    from pytesseract import image_to_string

    reader = PdfReader(BytesIO(content))
    total_pages = len(reader.pages)

    if total_pages > MAX_OCR_PAGES:
        logger.warning("PDF has %d pages, limiting OCR to %d", total_pages, MAX_OCR_PAGES)

    images = convert_from_bytes(
        content,
        dpi=OCR_DPI,
        first_page=1,
        last_page=min(total_pages, MAX_OCR_PAGES),
    )
    text_parts: list[str] = []
    try:
        for i, img in enumerate(images):
            text = image_to_string(img, lang="eng")
            stripped = text.strip()
            if stripped:
                text_parts.append(stripped)
            if i > 0 and i % 10 == 0:
                logger.debug("OCR'd %d/%d pages", i + 1, len(images))
    finally:
        del images
    return "\n\n".join(text_parts)


def parse_pdf(content: bytes) -> str:
    if _has_text_layer(content):
        return _extract_text(content)
    return _ocr_text(content)
