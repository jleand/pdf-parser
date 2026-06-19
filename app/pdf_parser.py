import logging

from pdf2image import convert_from_bytes
from pypdf import PdfReader

logger = logging.getLogger("pdf_parser")

MAX_OCR_PAGES = 50
OCR_DPI = 200


def _extract_text(content: bytes) -> str:
    with PdfReader(content) as reader:
        text_parts: list[str] = []
        for i, page in enumerate(reader.pages):
            t = page.extract_text()
            if t:
                text_parts.append(t.strip())
            if i > 0 and i % 50 == 0:
                logger.debug("Extracted text from %d pages", i)
    return "\n\n".join(text_parts)


def _ocr_text(content: bytes, lang: str) -> str:
    from pytesseract import image_to_string

    with PdfReader(content) as reader:
        total_pages = len(reader.pages)

    limit = min(total_pages, MAX_OCR_PAGES)
    if total_pages > MAX_OCR_PAGES:
        logger.warning("PDF has %d pages, limiting OCR to %d", total_pages, MAX_OCR_PAGES)

    text_parts: list[str] = []
    for page_num in range(1, limit + 1):
        images = convert_from_bytes(content, dpi=OCR_DPI, first_page=page_num, last_page=page_num)
        text = image_to_string(images[0], lang=lang)
        stripped = text.strip()
        if stripped:
            text_parts.append(stripped)
        if page_num % 10 == 0:
            logger.debug("OCR'd %d/%d pages", page_num, limit)
    return "\n\n".join(text_parts)


def parse_pdf(content: bytes, lang: str = "eng") -> str:
    text = _extract_text(content)
    if text.strip():
        return text
    return _ocr_text(content, lang)
