import streamlit as st
import sys
sys.path.insert(0, '.')
from utils.page_guard import require_data
from utils.data_loader import load_students
from agents.parent_agent import generate_parent_report

st.set_page_config(page_title="Parent Report · EduRisk AI", page_icon="📨", layout="wide")
require_data()

st.title("📨 Parent Communication Agent")

df       = load_students()
selected = st.selectbox("Select student", df["name"].tolist())

if selected:
    student = df[df["name"] == selected].iloc[0].to_dict()

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"📱 **Phone:** {student.get('parent_phone','N/A')}")
    with col2:
        st.write(f"📧 **Email:** {student.get('parent_email','N/A')}")

    teacher_name = st.text_input("Teacher Name", value="Class Teacher")
    school_name  = st.text_input("School Name",  value="EduRisk School")

    if st.button("📨 Generate Report", type="primary"):
        with st.spinner("Writing report..."):
            report = generate_parent_report(
                student=student,
                teacher_name=teacher_name,
                school_name=school_name
            )

        tab1, tab2 = st.tabs(["🇬🇧 English", "🇵🇰 Urdu"])
        with tab1:
            st.markdown(report["english"])
            st.download_button("📥 Download English",
                               data=report["english"],
                               file_name=f"report_{selected.replace(' ','_')}_EN.txt",
                               mime="text/plain")
        with tab2:
            st.markdown(report["urdu"])
            st.download_button("📥 Download Urdu",
                               data=report["urdu"],
                               file_name=f"report_{selected.replace(' ','_')}_UR.txt",
                               mime="text/plain")
