from __future__ import annotations

from dataclasses import dataclass
from importlib.util import find_spec

from PIL import Image

from prompts import EXPLAIN_PROMPT, QUIZ_PROMPT, RECOMMENDATION_PROMPT, SYSTEM_PROMPT
from utils.config import gcp_location, gcp_project_id, get_gemini_api_key, use_vertex_ai


@dataclass
class AIResult:
    ok: bool
    text: str
    source: str = "Gemini"


class GeminiService:
    def __init__(self) -> None:
        self.api_key = get_gemini_api_key()
        self.model_name = "gemini-1.5-flash"
        self.vertex_enabled = use_vertex_ai()
        if self.vertex_enabled and gcp_project_id():
            try:
                import vertexai

                vertexai.init(project=gcp_project_id(), location=gcp_location())
            except Exception:
                self.vertex_enabled = False
        elif self.api_key:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)

    @property
    def available(self) -> bool:
        direct_gemini = bool(self.api_key) and find_spec("google.generativeai") is not None
        vertex_gemini = self.vertex_enabled and bool(gcp_project_id()) and find_spec("vertexai") is not None
        return direct_gemini or vertex_gemini

    def _offline(self, task: str, content: str = "") -> AIResult:
        preview = " ".join(content.split())[:380]
        text = (
            f"Offline demo mode: add GEMINI_API_KEY in .env for live Gemini responses.\n\n"
            f"{task}\n\n"
            f"Detected study material preview: {preview or 'No extracted text yet.'}\n\n"
            "Suggested response:\n"
            "- Read the concept once with audio.\n"
            "- Mark unfamiliar terms.\n"
            "- Revise the highest-weight topics first.\n"
            "- Attempt five MCQs and review every wrong answer."
        )
        return AIResult(ok=True, text=text, source="Offline demo mode")

    def generate(self, prompt: str, content: str = "") -> AIResult:
        if not self.available:
            return self._offline("AI generation requested", content)
        try:
            if self.vertex_enabled and gcp_project_id():
                from vertexai.generative_models import GenerativeModel

                model = GenerativeModel(self.model_name, system_instruction=[SYSTEM_PROMPT])
                response = model.generate_content(prompt)
                return AIResult(ok=True, text=(response.text or "").strip(), source=f"Vertex AI {self.model_name}")
            import google.generativeai as genai

            model = genai.GenerativeModel(self.model_name, system_instruction=SYSTEM_PROMPT)
            response = model.generate_content(prompt)
            return AIResult(ok=True, text=(response.text or "").strip(), source=f"Gemini API {self.model_name}")
        except Exception as exc:
            return AIResult(ok=False, text=f"Gemini error: {exc}", source=self.model_name)

    def explain(self, content: str) -> AIResult:
        return self.generate(EXPLAIN_PROMPT.format(content=content), content)

    def quiz(self, content: str) -> AIResult:
        return self.generate(QUIZ_PROMPT.format(content=content), content)

    def answer_question(self, question: str, content: str) -> AIResult:
        prompt = (
            f"{SYSTEM_PROMPT}\n\nStudy material:\n{content}\n\n"
            f"Student question: {question}\n\n"
            "Answer clearly, include examples, and keep it voice-friendly."
        )
        return self.generate(prompt, content)

    def recommend(self, exam: str, days_remaining: int, study_hours: float, current_score: int, content: str) -> AIResult:
        prompt = RECOMMENDATION_PROMPT.format(
            exam=exam,
            days_remaining=days_remaining,
            study_hours=study_hours,
            current_score=current_score,
            content=content,
        )
        return self.generate(prompt, content)

    def vision_ocr(self, image: Image.Image) -> AIResult:
        if not self.available:
            return AIResult(False, "Gemini Vision unavailable without GEMINI_API_KEY.", "Offline demo mode")
        try:
            if self.vertex_enabled and gcp_project_id():
                return AIResult(False, "Image OCR uses Google Vision OCR or direct Gemini API in this prototype.", "Vertex AI")
            import google.generativeai as genai

            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content([
                "Extract all readable text from this exam preparation image. Preserve headings and lists.",
                image,
            ])
            return AIResult(True, (response.text or "").strip(), self.model_name)
        except Exception as exc:
            return AIResult(False, f"Gemini Vision OCR error: {exc}", self.model_name)
