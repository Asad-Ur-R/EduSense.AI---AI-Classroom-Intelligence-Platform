import os
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)


def _get_client():
    from groq import Groq
    return Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def generate_parent_report(student: dict,
                            teacher_name: str = "Class Teacher",
                            school_name: str  = "EduRisk School",
                            report_date: str  = "",
                            tone: str         = "Neutral") -> dict:
    """
    Generate parent communication in English and Urdu.
    Accepts the full 36-column CSV row as a dict.
    Returns {"english": str, "urdu": str}
    """
    context = f"""
Student:             {student.get('name')}
Grade:               {student.get('grade')} | Section: {student.get('section')}
Subject:             {student.get('subject')}
Overall Score:       {student.get('overall_score')}%
Attendance:          {student.get('attendance_pct')}%
Quiz Average:        {student.get('quiz_avg')}%
Late Submissions:    {student.get('late_submissions')}
Missing Assignments: {student.get('missing_assignments')}
Participation:       {student.get('participation_level')}
Weak Topics:         {student.get('weak_topic')}, {student.get('second_weak_topic')}
Risk Level:          {student.get('risk_level')}
School:              {school_name}
Teacher:             {teacher_name}
Date:                {report_date}
Tone:                {tone}
"""

    prompt_en = f"""
You are a school teacher in Pakistan writing a formal letter to parents.

{context}

Write a warm, professional parent message (4 short paragraphs):
1. Greeting with student name, school, and date
2. 1–2 genuine positives from the data above
3. 1–2 specific concerns with exact numbers from the data
4. 2 simple, practical actions parents can take at home
5. Warm closing signed by the teacher name

Adjust the tone to be {tone.lower()}.
Under 200 words. Caring but honest.
"""

    prompt_ur = f"""
آپ پاکستان میں ایک اسکول ٹیچر ہیں اور والدین کو باضابطہ خط لکھ رہے ہیں۔

{context}

مندرجہ ذیل نکات کے ساتھ مختصر، گرمجوش خط لکھیں (4 پیراگراف):
1. سلام اور طالب علم کے نام، اسکول اور تاریخ کے ساتھ آغاز
2. 1–2 مثبت پہلو (ڈیٹا سے)
3. 1–2 فکر کے شعبے اصل اعداد و شمار کے ساتھ
4. والدین کے لیے 2 عملی مشورے
5. گرمجوش اختتام اور ٹیچر کا نام

200 الفاظ سے کم۔ صرف اردو زبان میں لکھیں۔
"""

    client = _get_client()
    resp_en = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt_en}],
        max_tokens=500,
    )
    resp_ur = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt_ur}],
        max_tokens=700,
    )

    return {
        "english": resp_en.choices[0].message.content.strip(),
        "urdu":    resp_ur.choices[0].message.content.strip(),
    }
