import streamlit as st

from utils.analytics import log_learning_event
from utils.gemini_client import GeminiService
from utils.tts import text_to_speech


def _speak_button(label: str, text: str, key: str) -> None:
    if st.button(label, key=key):
        try:
            path = text_to_speech(text)
            st.audio(path)
        except Exception as exc:
            st.warning(f"Text-to-speech could not run in this environment: {exc}")


def render() -> None:
    st.title("AI Tutor")
    service = GeminiService()
    content = st.text_area(
        "Study material",
        value=st.session_state.get("extracted_text", ""),
        height=220,
        help="Paste text or use the Upload page to extract OCR first.",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        explain = st.button("Explain", type="primary")
    with col2:
        summarize = st.button("Summarize and Key Points")
    with col3:
        quiz = st.button("Generate 5 MCQs")

    if explain or summarize:
        with st.spinner("Gemini is preparing an accessible explanation..."):
            result = service.explain(content)
        log_learning_event("tutor_explanation_generated", {"characters": len(content), "source": result.source})
        st.session_state["last_ai_response"] = result.text
        st.markdown(result.text)
        _speak_button("Convert explanation to speech", result.text, "speak-explain")

    if quiz:
        with st.spinner("Generating quiz questions..."):
            result = service.quiz(content)
        log_learning_event("quiz_generated", {"characters": len(content), "source": result.source})
        st.session_state["last_ai_response"] = result.text
        st.markdown(result.text)
        _speak_button("Convert quiz to speech", result.text, "speak-quiz")

    st.divider()
    st.subheader("Ask a Follow-up Question")
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []
    for message in st.session_state["chat_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask about the uploaded study material")
    if question:
        st.session_state["chat_messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = service.answer_question(question, content)
            st.markdown(result.text)
        st.session_state["chat_messages"].append({"role": "assistant", "content": result.text})
