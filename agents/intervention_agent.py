import os
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)


def _get_client():
    from groq import Groq
    return Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def get_intervention_plan(student: dict) -> str:
    """
    Generate a personalised intervention plan for an at-risk student.
    Accepts the full 36-column CSV row as a dict.
    Returns markdown-formatted text.
    """
    prompt = f"""
You are an experienced school teacher creating an intervention plan for a struggling student.

Student Profile:
- Name:              {student.get('name')}
- Grade:             {student.get('grade')} | Section: {student.get('section')}
- Subject:           {student.get('subject')} | Semester: {student.get('semester')}
- Attendance:        {student.get('attendance_pct')}%
- Quiz Average:      {student.get('quiz_avg')}%
- Assignment Avg:    {student.get('assignment_avg', 'N/A')}%
- Midterm Score:     {student.get('midterm_score')} | Final Exam: {student.get('final_exam_score')}
- Overall Score:     {student.get('overall_score')}%
- Late Submissions:  {student.get('late_submissions')} | Missing: {student.get('missing_assignments')}
- Participation:     {student.get('participation_level')}
- Days Since Login:  {student.get('days_since_login')}
- Weak Topics:       {student.get('weak_topic')}, {student.get('second_weak_topic')}
- Risk Level:        {student.get('risk_level')} (Score: {student.get('risk_score')})

Write a 2-week intervention plan with exactly 5 sections:

## Student Summary
One paragraph summarising the key problems from the data.

## Week 1 Actions (Days 1–7)
- 3 specific, actionable daily tasks for the student

## Week 2 Actions (Days 8–14)
- 3 follow-up tasks building on Week 1

## Parent Involvement
- 2 things the parent should do at home this fortnight

## Success Metrics
- 3 measurable targets to check after 2 weeks (e.g. "attendance above 80%")

Use markdown formatting. Keep total under 300 words. Supportive, constructive tone.
"""
    client = _get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
    )
    return response.choices[0].message.content.strip()
