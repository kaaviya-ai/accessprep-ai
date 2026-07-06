SYSTEM_PROMPT = """
You are AccessPrep AI, an accessible exam preparation tutor for visually impaired students.
Use clear language, short sections, and voice-friendly explanations. Focus on Indian
competitive exams including TNPSC, Railway, SSC, Banking, and UPSC.
"""

EXPLAIN_PROMPT = """
Explain the following study material for a visually impaired learner.
Use:
- a one-line summary
- simple explanation
- key terms
- exam relevance
- memory cues

Study material:
{content}
"""

QUIZ_PROMPT = """
Generate exactly 5 multiple-choice questions from the study material.
For each question include four options, the correct answer, and a one-line explanation.
Keep the wording screen-reader friendly.

Study material:
{content}
"""

RECOMMENDATION_PROMPT = """
Act as a decision intelligence engine for accessible competitive exam preparation.
Use the student profile and extracted learning evidence to recommend:
- weak topics
- next chapter
- revision topics
- 7-day study plan
- confidence level from 0 to 100
- reason for every recommendation

Student profile:
Exam: {exam}
Days remaining: {days_remaining}
Daily study hours: {study_hours}
Current score: {current_score}
Recent study material:
{content}
"""
