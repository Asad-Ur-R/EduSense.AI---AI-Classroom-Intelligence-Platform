import streamlit as st
import pandas as pd
from utils.data_loader import validate_and_prepare, summary_stats

st.set_page_config(
    page_title="EduRisk AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    header { visibility: hidden; }
    .stDeployButton { display: none; }

    .hero-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px; padding: 48px 40px; margin-bottom: 32px;
        text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .hero-badge {
        display: inline-block; background: rgba(99,179,237,0.15); color: #63b3ed;
        border: 1px solid rgba(99,179,237,0.3); border-radius: 20px;
        padding: 4px 16px; font-size: 13px; font-weight: 600;
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 16px;
    }
    .hero-title { font-size: 48px; font-weight: 800; color: #fff; line-height: 1.2; margin-bottom: 12px; }
    .hero-title span { color: #63b3ed; }
    .hero-subtitle { font-size: 18px; color: #a0aec0; max-width: 620px;
                     margin: 0 auto 28px auto; line-height: 1.7; }
    .hero-pills { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
    .pill { background: rgba(255,255,255,0.08); color: #e2e8f0; border-radius: 20px;
            padding: 6px 16px; font-size: 13px; border: 1px solid rgba(255,255,255,0.12); }

    .upload-box { background: #1a2332; border: 2px dashed #2d4a6e; border-radius: 16px;
                  padding: 36px 32px; text-align: center; margin: 24px 0; }
    .upload-title { font-size: 20px; font-weight: 700; color: #e2e8f0; margin-bottom: 8px; }
    .upload-sub   { font-size: 14px; color: #718096; margin-bottom: 20px; }

    .metric-card { border-radius: 12px; padding: 24px 20px; text-align: center; }
    .metric-card-total  { background: linear-gradient(135deg,#2d3748,#4a5568); border:1px solid #718096; }
    .metric-card-high   { background: linear-gradient(135deg,#742a2a,#9b2c2c); border:1px solid #fc8181; }
    .metric-card-medium { background: linear-gradient(135deg,#744210,#975a16); border:1px solid #f6ad55; }
    .metric-card-low    { background: linear-gradient(135deg,#1a4731,#276749); border:1px solid #68d391; }
    .metric-card-avg    { background: linear-gradient(135deg,#1a365d,#2a4a7f); border:1px solid #63b3ed; }
    .metric-icon  { font-size: 32px; margin-bottom: 8px; }
    .metric-label { font-size: 13px; color: rgba(255,255,255,0.7); font-weight:600;
                    text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px; }
    .metric-value { font-size: 40px; font-weight: 800; color: #fff; line-height: 1; }
    .metric-sub   { font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 4px; }

    .agent-card { background:#1e2a3a; border:1px solid #2d3f55; border-radius:12px;
                  padding:20px; margin-bottom:12px; }
    .agent-card:hover { border-color:#63b3ed; }
    .agent-title { font-size:15px; font-weight:700; color:#e2e8f0; margin-bottom:4px; }
    .agent-desc  { font-size:13px; color:#718096; }

    .section-header { font-size:22px; font-weight:700; color:#e2e8f0;
                      margin:32px 0 16px 0; padding-bottom:8px; border-bottom:2px solid #2d3748; }
    .success-banner { background:#1a3d2a; border:1px solid #68d391; border-radius:10px;
                      padding:14px 20px; display:flex; align-items:center; gap:12px;
                      margin-bottom:20px; }
    .col-pill { display:inline-block; background:#0d1b2a; border:1px solid #2d4a6e;
                border-radius:6px; padding:3px 10px; font-size:12px; color:#63b3ed;
                margin:3px; }
    .missing-pill { display:inline-block; background:#3d1515; border:1px solid #fc8181;
                    border-radius:6px; padding:3px 10px; font-size:12px; color:#fc8181;
                    margin:3px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">🤖 AI-Powered</div>
    <div class="hero-title">EduSense <span>AI</span> Platform</div>
    <div class="hero-subtitle">
        Upload your class data and instantly get AI-powered risk detection,
        assignment grading, personalized interventions, and parent reports.
    </div>
    <div class="hero-pills">
        <span class="pill">📊 Risk Detection</span>
        <span class="pill">📝 Assignment Grading</span>
        <span class="pill">🎯 Interventions</span>
        <span class="pill">📨 Parent Reports</span>
        <span class="pill">📄 Worksheets</span>
        <span class="pill">🤖 AI Chatbot</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── CSV Upload Section ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📂 Step 1 · Upload Your Class Data</div>', unsafe_allow_html=True)

# Template download
with open("sample_data/students.csv", "rb") as f:
    template_bytes = f.read()

col_up, col_dl = st.columns([3, 1], gap="large")

with col_dl:
    st.markdown("**Don't have a file yet?**")
    st.download_button(
        label="📥 Download Template CSV",
        data=template_bytes,
        file_name="students_template.csv",
        mime="text/csv",
        use_container_width=True,
        help="Download our sample CSV, fill it with your students, then upload it here"
    )
    st.caption("Fill in your own students and re-upload")

with col_up:
    uploaded_file = st.file_uploader(
        "Upload your students CSV file",
        type=["csv"],
        help="Must include: name, grade, subject, attendance_pct, quiz_avg, overall_score"
    )

# ── Process Upload ─────────────────────────────────────────────────────────────
if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        df, warnings, missing_cols = validate_and_prepare(raw_df)

        if missing_cols:
            st.error(f"❌ **Cannot load file.** These required columns are missing:")
            for col in missing_cols:
                st.markdown(f'<span class="missing-pill">✗ {col}</span>', unsafe_allow_html=True)
            st.info("💡 Download the template above to see the correct column names.")
            st.stop()

        # Store in session state — all pages read from here
        st.session_state["df"]        = df
        st.session_state["file_name"] = uploaded_file.name

        # Show warnings for auto-computed columns
        if warnings:
            with st.expander("⚠️ Some columns were auto-computed (click to see)", expanded=False):
                for w in warnings:
                    st.caption(f"• {w}")

        # Success banner
        st.markdown(f"""
        <div class="success-banner">
            <span style="font-size:24px;">✅</span>
            <div>
                <div style="font-weight:700; color:#68d391; font-size:15px;">
                    {uploaded_file.name} loaded successfully
                </div>
                <div style="color:#a0aec0; font-size:13px;">
                    {len(df)} students · {len(df.columns)} columns · All agents ready
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Show detected columns
        with st.expander("📋 Detected columns in your file", expanded=False):
            for col in df.columns:
                st.markdown(f'<span class="col-pill">{col}</span>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to read file: {str(e)}")
        st.stop()

elif "df" in st.session_state:
    # File was uploaded in a previous interaction — still active
    st.success(f"✅ Using previously uploaded: **{st.session_state.get('file_name', 'your file')}** — {len(st.session_state['df'])} students loaded")

else:
    st.markdown("""
    <div class="upload-box">
        <div class="upload-title">👆 Upload your class CSV to get started</div>
        <div class="upload-sub">Or download the template, fill it in, and upload it here</div>
    </div>""", unsafe_allow_html=True)
    st.info("All pages will be unlocked once you upload your data.")
    st.stop()

# ── Stats Cards ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Class Overview</div>', unsafe_allow_html=True)
stats = summary_stats()

c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    ("c1", "metric-card-total",  "👥", "Total Students", stats["total_students"],   "enrolled"),
    ("c2", "metric-card-high",   "🔴", "High Risk",      stats["high_risk"],        "need urgent help"),
    ("c3", "metric-card-medium", "🟡", "Medium Risk",    stats["medium_risk"],      "need monitoring"),
    ("c4", "metric-card-low",    "🟢", "Low Risk",       stats["low_risk"],         "on track"),
    ("c5", "metric-card-avg",    "📊", "Avg Score",      stats["avg_overall_score"],"class average"),
]
for col, cls, icon, label, value, sub in zip([c1,c2,c3,c4,c5], *zip(*[(c,i,l,v,s) for _,c,i,l,v,s in cards])):
    with col:
        st.markdown(f"""
        <div class="metric-card {cls}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ── Agent Cards ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🤖 Available AI Agents</div>', unsafe_allow_html=True)

agents = [
    ("📊", "1 · Dashboard & Risk Analytics",
     "Filter and explore your students. View risk scores, attendance charts, and subject breakdowns."),
    ("📝", "2 · Assignment Grading Agent",
     "Upload a student's answer image + marking scheme. AI grades via OCR and returns score and feedback."),
    ("🎯", "3 · Intervention Planning Agent",
     "Select any at-risk student and generate a personalized 2-week improvement plan using Groq AI."),
    ("📨", "4 · Parent Communication Agent",
     "Auto-generate formal parent reports in English or Urdu for any student with one click."),
    ("📄", "5 · Worksheet Generator",
     "Choose a topic and grade level. AI creates a custom quiz with MCQ and short-answer questions instantly."),
    ("🤖", "6 · EduSense AI Chatbot",
     "Ask anything about your students in plain English. Powered by LangChain + LLaMA 3.3."),
]

col_a, col_b = st.columns(2)
for idx, (icon, title, desc) in enumerate(agents):
    col = col_a if idx % 2 == 0 else col_b
    with col:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-title">{icon} {title}</div>
            <div class="agent-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#4a5568; font-size:13px;'>"
    "EduRisk AI · Built for AI Hackathon 2025 · Powered by Groq API</p>",
    unsafe_allow_html=True
)
