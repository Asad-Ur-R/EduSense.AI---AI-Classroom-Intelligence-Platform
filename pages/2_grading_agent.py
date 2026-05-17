import streamlit as st
import sys
sys.path.insert(0, '.')
from utils.page_guard import require_data
from agents.grading_agent import grade_from_image, grade_from_pdf_text

st.set_page_config(page_title="Grading · EduRisk AI", page_icon="📝", layout="wide")
require_data()

st.title("📝 AI Grading Agent")

uploaded = st.file_uploader("Upload answer sheet", type=["jpg","jpeg","png","pdf"])
scheme   = st.text_area("Paste marking scheme here", height=200)
total    = st.number_input("Total marks", min_value=1, value=100)

if st.button("Grade Now") and uploaded and scheme:
    with st.spinner("Grading..."):
        raw_bytes = uploaded.read()
        if uploaded.type == "application/pdf":
            result = grade_from_pdf_text(raw_bytes, scheme, total)
        else:
            result = grade_from_image(raw_bytes, scheme, uploaded.type, total)

    c1, c2 = st.columns(2)
    c1.metric("Score",      f"{result['score']} / {total}")
    c2.metric("Percentage", f"{result['percentage']}%")

    st.subheader("Feedback")
    st.write(result.get("feedback", result.get("overall_feedback", "No feedback generated.")))

    st.subheader("Question Breakdown")
    st.dataframe(result["question_breakdown"])

    if result.get("missed_points"):
        st.subheader("Missed Points")
        for p in result["missed_points"]:
            st.write(f"- {p}")

    if result.get("weak_topics"):
        st.subheader("Weak Topics")
        for t in result["weak_topics"]:
            st.write(f"- {t}")
