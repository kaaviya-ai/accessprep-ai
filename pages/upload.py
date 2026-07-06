import streamlit as st
from PIL import Image

from utils.analytics import log_learning_event
from utils.ocr import extract_text_from_images, extract_text_from_pdf, load_pdf_pages, offline_demo_text, pdf_preview_message


def render() -> None:
    st.title("Upload Study Material")
    st.markdown('<div class="access-note">Upload an image or PDF. AccessPrep AI extracts readable text for tutoring, quizzes, and recommendations.</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload image or PDF", type=["png", "jpg", "jpeg", "webp", "pdf"])
    prefer_google = st.toggle("Use Google Vision OCR first when credentials are available", value=True)

    if not uploaded:
        st.info("Choose a file to begin.")
        return

    file_bytes = uploaded.getvalue()
    images = []
    embedded_pdf_text = ""
    embedded_pdf_source = ""
    if uploaded.type == "application/pdf" or uploaded.name.lower().endswith(".pdf"):
        embedded_pdf_text, embedded_pdf_source = extract_text_from_pdf(file_bytes)
        try:
            images = load_pdf_pages(file_bytes)
        except Exception as exc:
            images = [pdf_preview_message()]
            if embedded_pdf_text:
                st.info("PDF text was detected and is ready for extraction.")
            else:
                st.info("PDF uploaded. Visual preview is limited in this local demo, but text extraction will still run when selectable text or OCR credentials are available.")
        if len(images) > 0:
            st.success(f"Loaded {len(images)} PDF page preview(s).")
    else:
        source_image = Image.open(uploaded)
        image = source_image.convert("RGB")
        image.info.update(source_image.info)
        images = [image]

    st.subheader("Preview")
    for idx, image in enumerate(images[:3], start=1):
        st.image(image, caption=f"Page {idx}", width="stretch")

    if st.button("Extract OCR Text", type="primary"):
        with st.spinner("Extracting accessible text..."):
            if embedded_pdf_text:
                text, source = embedded_pdf_text, embedded_pdf_source
            else:
                text, source = extract_text_from_images(images, prefer_google_vision=prefer_google)
        if text:
            st.session_state["extracted_text"] = text
            st.session_state["ocr_source"] = source
            log_learning_event("ocr_completed", {"source": source, "characters": len(text)})
            st.success(f"OCR complete using {source}.")
        else:
            text, source = offline_demo_text()
            st.session_state["extracted_text"] = text
            st.session_state["ocr_source"] = source
            log_learning_event("ocr_demo_fallback_used", {"source": source, "characters": len(text)})
            st.warning("Live OCR is not configured in this local run, so AccessPrep AI loaded a sample extraction for the demo flow.")

    text = st.session_state.get("extracted_text", "")
    if text:
        st.subheader("Extracted Text")
        st.text_area("OCR result", value=text, height=320)
