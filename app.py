import streamlit as st

from components.ui import inject_css
from pages import about, home, recommendation, tutor, upload


st.set_page_config(
    page_title="AccessPrep AI",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

PAGES = {
    "Home": home.render,
    "Upload": upload.render,
    "AI Tutor": tutor.render,
    "Study Recommendation": recommendation.render,
    "About": about.render,
}

with st.sidebar:
    st.image("assets/logo.svg", width=96)
    st.markdown("## AccessPrep AI")
    st.caption("AI for Every Ability.")
    selected_page = st.radio("Navigation", list(PAGES.keys()))
    st.divider()
    st.markdown("### Accessibility")
    st.write("Large text, dark mode, keyboard-friendly controls, voice output, and screen-reader friendly content.")
    if st.session_state.get("ocr_source"):
        st.success(f"OCR: {st.session_state['ocr_source']}")

PAGES[selected_page]()
