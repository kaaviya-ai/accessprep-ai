from __future__ import annotations

import io
import re
import zlib
from typing import Iterable

from PIL import Image

from utils.gemini_client import GeminiService


SAMPLE_STUDY_TEXT = """Sample Competitive Exam Study Page
Subject: Indian Polity | Topic: Fundamental Rights

Concept Summary
Fundamental Rights are basic rights guaranteed by the Constitution of India.
They protect individual liberty, equality, religious freedom, and constitutional remedies.
They are mainly listed in Part III, Articles 12 to 35.

Key Articles
Article 14: Equality before law and equal protection of laws.
Article 19: Freedom of speech, expression, movement, association, and profession.
Article 21: Protection of life and personal liberty.
Article 32: Right to constitutional remedies; called the heart and soul of the Constitution.

Exam Relevance
Questions often compare Fundamental Rights with Directive Principles.
Article 21 is important because courts have expanded its meaning over time.
Article 32 allows citizens to directly approach the Supreme Court.

Practice MCQ
Which Article is known as the heart and soul of the Indian Constitution?
A. Article 14
B. Article 19
C. Article 21
D. Article 32
Answer: D. Article 32"""


def load_pdf_pages(file_bytes: bytes, max_pages: int = 5) -> list[Image.Image]:
    try:
        import fitz
    except Exception as exc:
        raise RuntimeError("PDF visual preview renderer is unavailable in this local demo.") from exc

    document = fitz.open(stream=file_bytes, filetype="pdf")
    pages: list[Image.Image] = []
    for page_index in range(min(len(document), max_pages)):
        page = document.load_page(page_index)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        pages.append(Image.open(io.BytesIO(pix.tobytes("png"))))
    return pages


def pdf_preview_message() -> Image.Image:
    image = Image.new("RGB", (1100, 700), "#ffffff")
    try:
        from PIL import ImageDraw

        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((60, 60, 1040, 640), radius=24, outline="#1a73e8", width=5, fill="#f8fafc")
        draw.text((110, 140), "PDF preview renderer unavailable", fill="#202124")
        draw.text((110, 210), "AccessPrep AI will still extract selectable PDF text when available.", fill="#202124")
        draw.text((110, 280), "The extracted PDF text can still be used by AI Tutor and Study Recommendation.", fill="#5f6368")
    except Exception:
        pass
    return image


def extract_text_from_pdf(file_bytes: bytes) -> tuple[str, str]:
    try:
        import fitz

        document = fitz.open(stream=file_bytes, filetype="pdf")
        text = "\n".join(page.get_text("text") for page in document).strip()
        if text:
            return text, "Embedded PDF text"
    except Exception:
        pass

    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(file_bytes))
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        if text:
            return text, "Embedded PDF text"
    except Exception:
        pass

    text = _extract_simple_pdf_text(file_bytes)
    if text:
        return text, "Embedded PDF text"
    return "", ""


def _extract_simple_pdf_text(file_bytes: bytes) -> str:
    chunks = [file_bytes]
    for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", file_bytes, re.S):
        stream = match.group(1)
        try:
            chunks.append(zlib.decompress(stream))
        except Exception:
            chunks.append(stream)

    found: list[str] = []
    for chunk in chunks:
        for raw in re.findall(rb"\((.*?)\)\s*T[jJ]", chunk, re.S):
            value = raw.replace(rb"\\(", rb"(").replace(rb"\\)", rb")").replace(rb"\\n", rb"\n")
            try:
                found.append(value.decode("utf-8"))
            except UnicodeDecodeError:
                found.append(value.decode("latin-1", errors="ignore"))
    clean_lines = []
    for line in found:
        cleaned = line.strip()
        if not cleaned or cleaned.lower() in {"anonymous", "untitled"} or "reportlab" in cleaned.lower():
            continue
        if cleaned in {"http://www.reportlab.com", "opensource)"}:
            continue
        clean_lines.append(cleaned)
    text = "\n".join(clean_lines)
    start = text.find("Sample Competitive Exam Study Page")
    if start >= 0:
        text = text[start:]
    return text


def google_vision_ocr(image_bytes: bytes) -> str:
    try:
        from google.cloud import vision
    except Exception as exc:
        raise RuntimeError("Google Vision OCR requires google-cloud-vision and Google Cloud credentials.") from exc

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    if response.full_text_annotation and response.full_text_annotation.text:
        return response.full_text_annotation.text.strip()
    return ""


def image_to_png_bytes(image: Image.Image) -> bytes:
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="PNG")
    return buffer.getvalue()


def extract_text_from_images(images: Iterable[Image.Image], prefer_google_vision: bool = True) -> tuple[str, str]:
    gemini = GeminiService()
    extracted: list[str] = []
    source = "Gemini Vision"

    for image in images:
        text = str(image.info.get("accessprep_text") or image.info.get("Description") or "").strip()
        if text:
            source = "Embedded accessible text"
            extracted.append(text)
            continue
        if prefer_google_vision:
            try:
                text = google_vision_ocr(image_to_png_bytes(image))
                source = "Google Cloud Vision OCR"
            except Exception:
                text = ""
        if not text:
            result = gemini.vision_ocr(image)
            text = result.text if result.ok else ""
            source = result.source
        extracted.append(text)

    clean_text = "\n\n".join(part for part in extracted if part.strip()).strip()
    return clean_text, source


def offline_demo_text() -> tuple[str, str]:
    return SAMPLE_STUDY_TEXT, "Offline demo OCR fallback"
