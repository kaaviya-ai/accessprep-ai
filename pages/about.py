import streamlit as st


def render() -> None:
    st.title("About AccessPrep AI")
    st.markdown("AccessPrep AI helps visually impaired competitive exam aspirants convert inaccessible study material into explanations, quizzes, audio, and adaptive study decisions.")

    st.subheader("Architecture")
    st.image("architecture.png", caption="AccessPrep AI Google Cloud architecture", width="stretch")

    st.subheader("Technology")
    st.write("Python, Streamlit, Gemini API, Google Vision OCR or Gemini Vision, gTTS, Pillow, PyMuPDF, Docker, Cloud Run.")

    st.subheader("Team")
    st.write("Inclusive Intelligence Lab - AI for Every Ability.")

    st.subheader("Future Scope")
    st.write("Regional language voice support, speech input, Braille display integration, adaptive mock tests, classroom dashboards, and offline-first study packs.")

    st.subheader("GitHub")
    st.write("Ready to publish as a professional hackathon repository.")
