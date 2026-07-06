# AccessPrep AI - Final Submission

## Deployment Link


Recommended deployment platform:

```text
Streamlit Community Cloud connected to GitHub
```

Local development URL:

```text
http://localhost:8501/
```

Localhost is not publicly accessible and should not be used as the final submission deployment link.

## GitHub Repository Link

https://github.com/kaaviya-ai/accessprep-ai

## Final Project PPT

## Demo Video Link


```text
(https://wilpbitspilaniacin0-my.sharepoint.com/:v:/g/personal/kaaviya_a_wilp_bits-pilani_ac_in/IQCFde5KAN2IQZx9gnNcA2UmAe4AaAPc-Vo6tqCEPF_85c4?e=XJiiEG)
```

## Brief Description

AccessPrep AI is an AI-powered Decision Intelligence platform for visually impaired students preparing for competitive exams such as TNPSC, Railway, SSC, Banking, and UPSC. The application lets a student upload an image or PDF, extract study text, receive Gemini-powered explanations, ask follow-up questions, generate MCQs, get personalized weak-topic and revision recommendations, and access voice-first speech output for learning.

The project demonstrates Computer Vision, OCR, Conversational AI, Gemini, decision intelligence, accessibility-first UI design, and personalized study planning. It is built with Python, Streamlit, Gemini API, Google Vision OCR or Gemini Vision, gTTS, Pillow, PyMuPDF, python-dotenv, Docker, and Google Cloud Run-ready configuration.

## Streamlit Community Cloud Deployment

GitHub Pages cannot run this project because AccessPrep AI is a Python Streamlit application, not a static website. Use Streamlit Community Cloud with the GitHub repository.

1. Open https://share.streamlit.io/
2. Sign in with GitHub.
3. Click **New app**.
4. Select repository:

```text
kaaviya-ai/accessprep-ai
```

5. Select branch:

```text
main
```

6. Main file path:

```text
app.py
```

7. In app secrets, add:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
```

8. Deploy the app and copy the public URL.

