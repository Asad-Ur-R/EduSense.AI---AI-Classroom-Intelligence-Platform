import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent

load_dotenv()


def _load_df() -> pd.DataFrame:
    base = os.path.dirname(__file__)
    path = os.path.join(base, "../sample_data/students.csv")
    return pd.read_csv(path)


def get_chatbot_agent():
    df = _load_df()

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        agent_type="tool-calling",
        verbose=False,
        allow_dangerous_code=True,
        prefix="""
You are EduSense AI, a helpful school analytics assistant for teachers in Pakistan.
You have access to a dataframe of 200 students with columns including:
- student_id, name, grade, section, subject, semester
- attendance_pct, participation_level, late_submissions, missing_assignments
- quiz_1 to quiz_5, quiz_avg, assignment_avg
- midterm_score, final_exam_score, overall_score
- weak_topic, second_weak_topic, days_since_login
- parent_phone, parent_email, risk_score, risk_level

risk_level values: 'High Risk', 'Medium Risk', 'Low Risk'
grades: 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'

Always answer in clear, teacher-friendly language.
Round numbers to 1 decimal place.
Format lists as bullet points.
Sort at-risk students by risk_score descending.
""",
    )
    return agent


def ask_chatbot(question: str, chat_history: list = []) -> str:
    try:
        agent = get_chatbot_agent()

        context = ""
        if chat_history:
            for msg in chat_history[-4:]:
                role = "Teacher" if msg["role"] == "user" else "EduSense AI"
                context += f"{role}: {msg['content']}\n"
            question = f"Previous conversation:\n{context}\nNew question: {question}"

        response = agent.invoke({"input": question})
        return response.get("output", "Sorry, I could not process that question.")

    except Exception as e:
        return f"Error: {str(e)}"
