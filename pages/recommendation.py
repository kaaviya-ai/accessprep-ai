import streamlit as st

from utils.analytics import log_learning_event
from utils.gemini_client import GeminiService
from utils.study_logic import rule_based_recommendation
from utils.tts import text_to_speech


def render() -> None:
    st.title("Decision Intelligence")
    st.markdown("Build a personalized plan using student profile, exam urgency, score, study time, and recent learning evidence.")

    col1, col2 = st.columns(2)
    with col1:
        exam = st.selectbox("Target exam", ["TNPSC", "Railway", "SSC", "Banking", "UPSC", "Other"])
        days_remaining = st.number_input("Days remaining", min_value=1, max_value=730, value=60)
    with col2:
        study_hours = st.number_input("Daily study hours", min_value=0.5, max_value=16.0, value=3.0, step=0.5)
        current_score = st.slider("Current mock test score", min_value=0, max_value=100, value=55)

    content = st.text_area("Recent study material or notes", value=st.session_state.get("extracted_text", ""), height=180)

    if st.button("Generate Study Recommendation", type="primary"):
        baseline = rule_based_recommendation(exam, int(days_remaining), float(study_hours), int(current_score))
        service = GeminiService()
        with st.spinner("Building recommendation..."):
            result = service.recommend(exam, int(days_remaining), float(study_hours), int(current_score), content)
        log_learning_event(
            "study_recommendation_generated",
            {"exam": exam, "days_remaining": int(days_remaining), "study_hours": float(study_hours), "score": int(current_score)},
        )

        st.subheader("Decision Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Confidence", f"{baseline['confidence']}%")
        c2.metric("Intensity", str(baseline["intensity"]))
        c3.metric("Next Chapter", str(baseline["next_chapter"]))

        st.subheader("AI Recommendation")
        st.markdown(result.text)
        if st.button("Convert plan to speech"):
            try:
                st.audio(text_to_speech(result.text))
            except Exception as exc:
                st.warning(f"Text-to-speech could not run in this environment: {exc}")
