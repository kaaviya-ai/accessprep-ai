def rule_based_recommendation(exam: str, days_remaining: int, study_hours: float, current_score: int) -> dict[str, object]:
    score_gap = max(0, 75 - current_score)
    intensity = "High" if days_remaining <= 30 or score_gap >= 25 else "Moderate"
    weak_topics = ["Quantitative Aptitude", "Current Affairs", "Reasoning"] if current_score < 60 else ["Mock test speed", "Revision accuracy"]
    confidence = min(92, max(35, current_score + int(study_hours * 4) - (10 if days_remaining < 15 else 0)))
    return {
        "exam": exam,
        "intensity": intensity,
        "weak_topics": weak_topics,
        "next_chapter": weak_topics[0],
        "revision_topics": weak_topics[1:] + ["Previous year questions"],
        "confidence": confidence,
    }
