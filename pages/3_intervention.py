import streamlit as st
import sys
sys.path.insert(0, '.')
from utils.page_guard import require_data
from utils.data_loader import get_at_risk_students
from agents.intervention_agent import get_intervention_plan

st.set_page_config(page_title="Intervention · EduRisk AI", page_icon="🚨", layout="wide")
require_data()

st.title("🚨 Intervention Plans")

df = get_at_risk_students(35)

if df.empty:
    st.success("🎉 No at-risk students found in your dataset!")
    st.stop()

names    = df["name"].tolist()
selected = st.selectbox("Select at-risk student", names)

if selected:
    student = df[df["name"] == selected].iloc[0].to_dict()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk Score",  f"{student['risk_score']:.1f}")
    c2.metric("Attendance",  f"{student['attendance_pct']}%")
    c3.metric("Quiz Avg",    f"{student['quiz_avg']}%")
    c4.metric("Overall",     f"{student['overall_score']}%")

    st.info(f"⚠️ Weak Topics: **{student.get('weak_topic','N/A')}** | **{student.get('second_weak_topic','N/A')}**")

    if st.button("🤖 Generate Intervention Plan", type="primary"):
        with st.spinner("Creating plan..."):
            plan = get_intervention_plan(student)
        st.subheader("Intervention Plan")
        st.markdown(plan)
        st.download_button("📥 Download Plan", data=plan,
                           file_name=f"plan_{selected.replace(' ','_')}.txt",
                           mime="text/plain")
