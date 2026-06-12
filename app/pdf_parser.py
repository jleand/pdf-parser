from io import BytesIO

from pdf2image import convert_from_bytes
from pypdf import PdfReader
from pytesseract import image_to_string


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
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text_parts.append(t.strip())
    return "\n\n".join(text_parts)


def _ocr_text(content: bytes) -> str:
    images = convert_from_bytes(content, dpi=300)
    text_parts: list[str] = []
    for img in images:
        text = image_to_string(img, lang="eng")
        text_parts.append(text.strip())
    return "\n\n".join(text_parts)


def parse_pdf(content: bytes) -> str:
    if _has_text_layer(content):
        return _extract_text(content)
    return _ocr_text(content)
