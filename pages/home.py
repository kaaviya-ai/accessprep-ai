import streamlit as st

from components.ui import info_card, logo_header


def render() -> None:
    st.image("assets/logo.svg", width=120)
    logo_header("AccessPrep AI", "AI-powered Decision Intelligence for Accessible Competitive Exam Preparation.")
    st.markdown("### Built by Inclusive Intelligence Lab")
    st.markdown("**Team tagline:** AI for Every Ability.")

    col1, col2, col3 = st.columns(3)
    with col1:
        info_card("Problem", "Visually impaired aspirants often struggle with image/PDF study material, inaccessible explanations, and fragmented revision planning.", "!")
    with col2:
        info_card("Solution", "OCR, Gemini tutoring, voice output, quizzes, and decision intelligence come together in one accessible study workflow.", "+")
    with col3:
        info_card("Hackathon Fit", "Demonstrates Computer Vision, OCR, Conversational AI, Gemini, accessibility, and personalized recommendations.", "*")

    st.markdown("## Team")
    st.markdown(
        "Inclusive Intelligence Lab is a multidisciplinary team of AI researchers, engineers, and innovators "
        "building accessible, inclusive, human-centered technologies with Computer Vision, Generative AI, "
        "Decision Intelligence, and Multimodal AI."
    )

    st.markdown("## Supported Exams")
    st.write("TNPSC, Railway, SSC, Banking, UPSC, and other competitive examinations.")
