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

    def _topic(self, content: str) -> str:
        lowered = content.lower()
        if "fundamental rights" in lowered:
            return "Fundamental Rights"
        if "time and work" in lowered:
            return "Time and Work"
        first_line = next((line.strip() for line in content.splitlines() if line.strip()), "")
        return first_line[:70] or "the uploaded study material"

    def _offline_explanation(self, content: str) -> AIResult:
        topic = self._topic(content)
        text = (
            f"Offline demo explanation for {topic}.\n\n"
            "One-line summary: This topic is important because it is frequently tested and connects basic facts with exam-style reasoning.\n\n"
            "Simple explanation:\n"
            "Fundamental Rights are protections given by the Constitution to every citizen and, in some cases, every person. "
            "They protect equality, liberty, religious freedom, cultural rights, and the right to approach courts when rights are violated.\n\n"
            "Key terms:\n"
            "- Article 14: equality before law.\n"
            "- Article 19: major freedoms such as speech, movement, and profession.\n"
            "- Article 21: life and personal liberty.\n"
            "- Article 32: constitutional remedies.\n\n"
            "Exam relevance: Questions often ask article numbers, comparisons with Directive Principles, and why Article 32 is called the heart and soul of the Constitution."
        )
        return AIResult(True, text, "Offline demo AI")

    def _offline_summary(self, content: str) -> AIResult:
        topic = self._topic(content)
        text = (
            f"Offline demo summary for {topic}.\n\n"
            "Key points:\n"
            "1. Fundamental Rights are listed mainly in Part III of the Constitution.\n"
            "2. They protect equality, freedom, religion, culture, education, and legal remedies.\n"
            "3. Article 21 is broad because courts have expanded its meaning over time.\n"
            "4. Article 32 lets citizens directly approach the Supreme Court.\n"
            "5. For exams, revise article numbers and landmark interpretations first."
        )
        return AIResult(True, text, "Offline demo AI")

    def _offline_quiz(self, content: str) -> AIResult:
        text = (
            "Offline demo quiz: 5 MCQs\n\n"
            "1. Fundamental Rights are mainly found in which part of the Constitution?\n"
            "A. Part I\nB. Part II\nC. Part III\nD. Part IV\nAnswer: C. Part III\n\n"
            "2. Which article provides equality before law?\n"
            "A. Article 14\nB. Article 19\nC. Article 21\nD. Article 32\nAnswer: A. Article 14\n\n"
            "3. Which article protects life and personal liberty?\n"
            "A. Article 15\nB. Article 18\nC. Article 21\nD. Article 25\nAnswer: C. Article 21\n\n"
            "4. Which article is called the heart and soul of the Constitution?\n"
            "A. Article 12\nB. Article 32\nC. Article 44\nD. Article 51\nAnswer: B. Article 32\n\n"
            "5. What does Article 32 help citizens do?\n"
            "A. Vote in elections\nB. Approach the Supreme Court for rights protection\nC. Create a state law\nD. Join public service\nAnswer: B. Approach the Supreme Court for rights protection"
        )
        return AIResult(True, text, "Offline demo AI")

    def _offline_answer(self, question: str, content: str) -> AIResult:
        text = (
            f"Offline demo answer for your question: {question}\n\n"
            "Based on the study material, focus on the article, its meaning, and why it matters in exams. "
            "For Fundamental Rights, remember that Article 32 is important because it gives a direct remedy through the Supreme Court. "
            "A good exam answer should include the article number, the right protected, and one practical example."
        )
        return AIResult(True, text, "Offline demo AI")

    def _offline_recommendation(self, exam: str, days_remaining: int, study_hours: float, current_score: int, content: str) -> AIResult:
        confidence = min(90, max(35, current_score + int(study_hours * 5) - (8 if days_remaining < 20 else 0)))
        text = (
            f"Offline demo decision intelligence plan for {exam}.\n\n"
            "Weak topics:\n"
            "- Article number recall\n- Difference between Fundamental Rights and Directive Principles\n- Application-based polity questions\n\n"
            "Next chapter: Directive Principles of State Policy, because it is commonly compared with Fundamental Rights.\n\n"
            "Revision topics:\n"
            "- Articles 14, 19, 21, and 32\n- Writs and constitutional remedies\n- Previous year polity questions\n\n"
            f"7-day plan with {study_hours} hours per day:\n"
            "Day 1: Revise key articles and make audio notes.\n"
            "Day 2: Study Directive Principles comparison.\n"
            "Day 3: Practice 25 MCQs on rights.\n"
            "Day 4: Review wrong answers.\n"
            "Day 5: Take a mini mock test.\n"
            "Day 6: Revise high-error topics.\n"
            "Day 7: Final recall and speed practice.\n\n"
            f"Confidence level: {confidence}%.\nReason: The plan prioritizes high-frequency topics and converts weak areas into daily revision actions."
        )
        return AIResult(True, text, "Offline demo AI")

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
        if not self.available:
            return self._offline_explanation(content)
        return self.generate(EXPLAIN_PROMPT.format(content=content), content)

    def summarize(self, content: str) -> AIResult:
        if not self.available:
            return self._offline_summary(content)
        prompt = (
            "Summarize the study material into a voice-friendly exam revision note. "
            "Include a short summary and 5 key points.\n\n"
            f"Study material:\n{content}"
        )
        return self.generate(prompt, content)

    def quiz(self, content: str) -> AIResult:
        if not self.available:
            return self._offline_quiz(content)
        return self.generate(QUIZ_PROMPT.format(content=content), content)

    def answer_question(self, question: str, content: str) -> AIResult:
        if not self.available:
            return self._offline_answer(question, content)
        prompt = (
            f"{SYSTEM_PROMPT}\n\nStudy material:\n{content}\n\n"
            f"Student question: {question}\n\n"
            "Answer clearly, include examples, and keep it voice-friendly."
        )
        return self.generate(prompt, content)

    def recommend(self, exam: str, days_remaining: int, study_hours: float, current_score: int, content: str) -> AIResult:
        if not self.available:
            return self._offline_recommendation(exam, days_remaining, study_hours, current_score, content)
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
