import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)


def _get_client():
    from groq import Groq
    return Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def generate_worksheet(topic: str,
                        grade_level: str    = "Grade 10",
                        n: int              = 5,
                        subject: str        = "General",
                        difficulty: str     = "Mixed",
                        question_types: list = None,
                        second_topic: str   = "") -> dict:
    """
    Generate a worksheet for a given topic.
    Returns:
      {
        "title": str,
        "total_marks": int,
        "questions": [
          {
            "type": "MCQ|Short Answer|True/False|Fill in the Blank",
            "question": str,
            "options": [str, str, str, str],   # only for MCQ
            "answer": str,
            "marks": int,
            "explanation": str
          }
        ]
      }
    """
    if question_types is None:
        question_types = ["Multiple Choice (MCQ)", "Short Answer"]

    second_note = f"\nAlso include 1–2 questions on the related topic: {second_topic}." if second_topic else ""

    prompt = f"""
You are a Pakistan curriculum teacher creating a quiz worksheet.

Topic:          {topic}
Grade Level:    {grade_level}
Subject:        {subject}
Difficulty:     {difficulty}
Total Questions:{n}
Question Types: {', '.join(question_types)}{second_note}

Create exactly {n} questions mixing the requested question types.

Rules:
- MCQ must have 4 options as a plain list (not a dict)
- Answer field: for MCQ write the full correct option text, for True/False write "True" or "False"
- Marks: MCQ=2, Short Answer=3, True/False=1, Fill in the Blank=2
- Align content with Pakistan national curriculum for {grade_level}

Return ONLY valid JSON — no markdown, no extra text — in this exact structure:
{{
  "title": "Worksheet: {topic} – {grade_level}",
  "total_marks": <sum of all marks>,
  "questions": [
    {{
      "type": "MCQ",
      "question": "Question text?",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "answer": "Option A text",
      "marks": 2,
      "explanation": "One sentence reason."
    }},
    {{
      "type": "Short Answer",
      "question": "Question text?",
      "options": [],
      "answer": "Model answer here.",
      "marks": 3,
      "explanation": "Key points to look for."
    }}
  ]
}}
"""
    client = _get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1800,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)
