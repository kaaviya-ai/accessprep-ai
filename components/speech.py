import html

import streamlit as st
import streamlit.components.v1 as components

def speech_controls(text: str, label: str, key: str) -> None:
    if not text.strip():
        return

    st.caption("Speech output")
    col1, col2 = st.columns([1, 1])
    with col1:
        safe_text = html.escape(text[:3500])
        components.html(
            f"""
            <button
              style="width:100%;min-height:42px;border-radius:8px;border:1px solid #8ab4f8;background:#1a73e8;color:white;font-size:16px;cursor:pointer;"
              onclick="
                const text = document.getElementById('speech-{key}').textContent;
                if (!('speechSynthesis' in window)) {{
                  document.getElementById('speech-status-{key}').textContent = 'Browser speech is not supported here.';
                  return;
                }}
                const u = new SpeechSynthesisUtterance(text);
                u.rate = 0.92;
                u.pitch = 1;
                u.lang = 'en-IN';
                speechSynthesis.cancel();
                speechSynthesis.speak(u);
                document.getElementById('speech-status-{key}').textContent = 'Speaking now...';
              ">
              Speak aloud now
            </button>
            <button
              style="width:100%;min-height:36px;margin-top:6px;border-radius:8px;border:1px solid #dadce0;background:#202124;color:white;font-size:14px;cursor:pointer;"
              onclick="speechSynthesis.cancel(); document.getElementById('speech-status-{key}').textContent = 'Speech stopped.';">
              Stop speech
            </button>
            <div id="speech-status-{key}" style="font-size:13px;color:#d9e2f1;margin-top:6px;"></div>
            <span id="speech-{key}" style="display:none;">{safe_text}</span>
            """,
            height=112,
        )
    with col2:
        if st.button("Generate MP3 audio (optional)", key=f"{key}-gtts", help=label):
            try:
                from utils.tts import text_to_speech

                st.audio(text_to_speech(text))
            except Exception as exc:
                st.warning(f"MP3 generation needs network access for gTTS. Use 'Speak aloud now' instead. Details: {exc}")
