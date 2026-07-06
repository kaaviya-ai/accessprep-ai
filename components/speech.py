import html

import streamlit as st
import streamlit.components.v1 as components

from utils.tts import text_to_speech


def speech_controls(text: str, label: str, key: str) -> None:
    if not text.strip():
        return

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(label, key=f"{key}-gtts"):
            try:
                st.audio(text_to_speech(text))
            except Exception as exc:
                st.warning(f"Audio file generation is unavailable here: {exc}")
    with col2:
        safe_text = html.escape(text[:3500])
        components.html(
            f"""
            <button
              style="width:100%;min-height:42px;border-radius:8px;border:1px solid #8ab4f8;background:#1a73e8;color:white;font-size:16px;cursor:pointer;"
              onclick="const u=new SpeechSynthesisUtterance(document.getElementById('speech-{key}').textContent); u.rate=0.92; speechSynthesis.cancel(); speechSynthesis.speak(u);">
              Speak in browser
            </button>
            <span id="speech-{key}" style="display:none;">{safe_text}</span>
            """,
            height=54,
        )
