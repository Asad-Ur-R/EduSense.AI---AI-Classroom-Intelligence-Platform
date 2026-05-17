import streamlit as st
import sys
sys.path.insert(0, '.')
from utils.page_guard import require_data
from utils.data_loader import load_students
from agents.worksheet_agent import generate_worksheet

st.set_page_config(page_title="Worksheet · EduRisk AI", page_icon="📋", layout="wide")
require_data()

st.title("📋 Auto Worksheet Generator")

df       = load_students()
selected = st.selectbox("Select student (auto-fills weak topic)",
                        ["Manual input"] + df["name"].tolist())

if selected != "Manual input":
    student = df[df["name"] == selected].iloc[0]
    topic   = st.text_input("Topic", value=student.get("weak_topic", ""))
    grade   = student.get("grade", "Grade 10")
    st.caption(f"Grade auto-set to: **{grade}**")
else:
    topic = st.text_input("Topic", placeholder="e.g. Fractions, Photosynthesis...")
    grade = st.selectbox("Grade", ["Grade 8","Grade 9","Grade 10","Grade 11","Grade 12"])

num_q = st.slider("Number of questions", 3, 10, 5)

if st.button("📄 Generate Worksheet", type="primary") and topic:
    with st.spinner("Generating questions..."):
        result = generate_worksheet(topic, grade, num_q)

    # Handle both dict return {title, total_marks, questions:[]} and plain list
    if isinstance(result, dict):
        questions   = result.get("questions", [])
        title       = result.get("title", f"Worksheet: {topic}")
        total_marks = result.get("total_marks", "")
    else:
        questions   = result
        title       = f"Worksheet: {topic}"
        total_marks = ""

    st.subheader(f"{title}  |  Total Marks: {total_marks}")

    for i, q in enumerate(questions, 1):
        q_text  = q.get("question", "")
        options = q.get("options", [])
        answer  = q.get("answer", "")
        explain = q.get("explanation", "")
        marks   = q.get("marks", "")
        q_type  = q.get("type", "MCQ")

        with st.expander(f"Q{i} [{q_type}] — {q_text}"):
            if isinstance(options, dict):
                for key, val in options.items():
                    st.write(f"{key}) {val}")
            elif isinstance(options, list) and options:
                for j, val in enumerate(options):
                    st.write(f"{chr(65+j)}) {val}")
            if marks:
                st.caption(f"Marks: {marks}")
            st.success(f"✅ Answer: {answer}")
            if explain:
                st.info(f"💡 {explain}")
