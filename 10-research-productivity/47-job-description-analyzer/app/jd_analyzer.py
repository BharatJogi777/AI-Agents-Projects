"""Analyze a job description against a user-provided skill inventory."""
import re

def analyze_job_description(description: str, candidate_skills: list[str]) -> dict:
    if not description.strip():
        raise ValueError("job description is required")
    if any(not skill.strip() for skill in candidate_skills):
        raise ValueError("candidate skills cannot be empty")
    normalized = description.casefold()
    unique = {s.casefold().strip(): s.strip() for s in candidate_skills}
    matched = [original for key, original in unique.items() if re.search(r"(?<![\w])" + re.escape(key) + r"(?![\w])", normalized)]
    missing = [original for key, original in unique.items() if original not in matched]
    headings = [line.strip(" #:-") for line in description.splitlines() if line.strip().casefold().startswith(("responsibilities", "requirements", "qualifications", "what you will do"))]
    return {"matched_candidate_skills": matched, "not_found_in_description": missing, "detected_section_headings": headings, "match_ratio": round(len(matched) / len(unique), 3) if unique else 0.0, "note": "Lexical matching only; absence from text does not prove a skill is irrelevant."}
