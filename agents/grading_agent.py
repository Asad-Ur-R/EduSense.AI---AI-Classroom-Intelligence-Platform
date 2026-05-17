import os
import re
import json
import base64
from pathlib import Path
from dotenv import load_dotenv

# Always load .env from project root (two levels up from this file)
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TEXT_MODEL   = "llama-3.3-70b-versatile"


def _get_client():
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(f".env not found or GROQ_API_KEY missing. Looked at: {_ENV_PATH}")
    return Groq(api_key=api_key)


# OCR via Groq Vision
def ocr_image_to_text(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    client = _get_client()
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{b64}"},
                    },
                    {
                        "type": "text",
                        "text": (
                            "Extract ALL text from this student answer sheet exactly as written. "
                            "Preserve question numbers and answers. Output plain text only."
                        ),
                    },
                ],
            }
        ],
        max_tokens=1500,
    )
    return response.choices[0].message.content.strip()


# Grading Logic
def grade_answers(student_text: str, marking_scheme: str, total_marks: int = 100) -> dict:
    client = _get_client()
    prompt = f"""
You are an expert teacher grading a student's exam paper.

MARKING SCHEME (correct answers):
{marking_scheme}

STUDENT'S ANSWERS:
{student_text}

Total marks available: {total_marks}

Grade the student's answers strictly against the marking scheme.
Return your response as valid JSON with this EXACT structure — no markdown, no extra text:
{{
  "score": <integer marks awarded>,
  "percentage": <float 0-100>,
  "grade_letter": "<A/B/C/D/F>",
  "question_breakdown": [
    {{"question": "Q1", "marks_awarded": 0, "marks_available": 0, "status": "Correct|Partial|Incorrect", "comment": "..."}}
  ],
  "missed_points": ["point 1", "point 2"],
  "weak_topics": ["topic1", "topic2"],
  "feedback": "<2-3 sentence constructive feedback for the student>"
}}
"""
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)


# Public API
def grade_from_image(image_bytes: bytes, marking_scheme: str,
                     mime_type: str = "image/jpeg", total_marks: int = 100,
                     student_name: str = "", grade: str = "") -> dict:
    student_text = ocr_image_to_text(image_bytes, mime_type)
    result = grade_answers(student_text, marking_scheme, total_marks)
    result["ocr_text"] = student_text
    return result


def grade_from_pdf_text(pdf_bytes: bytes, marking_scheme: str,
                        total_marks: int = 100,
                        student_name: str = "", grade: str = "") -> dict:
    from utils.pdf_parser import extract_text_from_bytes
    pdf_text = extract_text_from_bytes(pdf_bytes)
    result = grade_answers(pdf_text, marking_scheme, total_marks)
    result["ocr_text"] = pdf_text
    return result
