import streamlit as st
import pandas as pd
import plotly.express as px
import sys
sys.path.insert(0, '.')
from utils.page_guard import require_data
from utils.data_loader import load_students, summary_stats

st.set_page_config(page_title="Dashboard · EduRisk AI", page_icon="📊", layout="wide")
require_data()

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    header { visibility: hidden; }
    .page-title  { font-size: 30px; font-weight: 800; color: #e2e8f0; margin-bottom: 4px; }
    .page-sub    { font-size: 14px; color: #718096; margin-bottom: 28px; }
    .risk-card   { border-radius: 10px; padding: 18px 16px; text-align: center; }
    .risk-high   { background: rgba(154,44,44,0.25); border: 1px solid #fc8181; }
    .risk-medium { background: rgba(116,66,16,0.25); border: 1px solid #f6ad55; }
    .risk-low    { background: rgba(26,71,49,0.25);  border: 1px solid #68d391; }
    .risk-val    { font-size: 36px; font-weight: 800; color: #fff; }
    .risk-lbl    { font-size: 12px; color: rgba(255,255,255,0.6); font-weight:600;
                   text-transform:uppercase; letter-spacing:0.8px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">📊 Class Dashboard</div>', unsafe_allow_html=True)

df = load_students()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")
    grades   = ["All"] + sorted(df["grade"].unique().tolist())
    subjects = ["All"] + sorted(df["subject"].unique().tolist())
    risks    = ["All", "High Risk", "Medium Risk", "Low Risk"]
    sections = ["All"] + sorted(df["section"].unique().tolist())

    sel_grade   = st.selectbox("Grade",      grades)
    sel_subject = st.selectbox("Subject",    subjects)
    sel_risk    = st.selectbox("Risk Level", risks)
    sel_section = st.selectbox("Section",    sections)
    st.markdown("---")
    st.markdown(f"**Total loaded:** {len(df)} students")

# ── Apply Filters ─────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_grade   != "All": fdf = fdf[fdf["grade"]      == sel_grade]
if sel_subject != "All": fdf = fdf[fdf["subject"]    == sel_subject]
if sel_risk    != "All": fdf = fdf[fdf["risk_level"] == sel_risk]
if sel_section != "All": fdf = fdf[fdf["section"]    == sel_section]

st.markdown(f'<div class="page-sub">Showing {len(fdf)} students after filters</div>', unsafe_allow_html=True)

# ── Risk Cards ────────────────────────────────────────────────────────────────
high   = len(fdf[fdf["risk_level"] == "High Risk"])
medium = len(fdf[fdf["risk_level"] == "Medium Risk"])
low    = len(fdf[fdf["risk_level"] == "Low Risk"])

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="risk-card risk-high"><div class="risk-val">🔴 {high}</div><div class="risk-lbl">High Risk</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="risk-card risk-medium"><div class="risk-val">🟡 {medium}</div><div class="risk-lbl">Medium Risk</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="risk-card risk-low"><div class="risk-val">🟢 {low}</div><div class="risk-lbl">Low Risk</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ── Student Table ─────────────────────────────────────────────────────────────
st.markdown("### 📋 Student Records")
display_cols = [c for c in ["name","grade","section","subject","risk_score","risk_level",
                              "attendance_pct","quiz_avg","overall_score","weak_topic"] if c in fdf.columns]

def color_risk(val):
    return {"High Risk": "background-color:#5c1f1f;color:#fc8181",
            "Medium Risk": "background-color:#5c3a0d;color:#f6ad55",
            "Low Risk": "background-color:#1a3d2a;color:#68d391"}.get(val, "")

styled = fdf[display_cols].reset_index(drop=True).style.map(color_risk, subset=["risk_level"]) \
    .format({c: "{:.1f}" for c in ["risk_score","attendance_pct","quiz_avg","overall_score"] if c in display_cols})
st.dataframe(styled, use_container_width=True, height=350)

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────────────────────
col_l, col_r = st.columns(2)
color_map = {"High Risk": "#fc8181", "Medium Risk": "#f6ad55", "Low Risk": "#68d391"}

with col_l:
    st.markdown("### 📈 Risk Score per Student")
    chart_df = fdf[["name","risk_score","risk_level"]].sort_values("risk_score", ascending=False).head(30)
    fig = px.bar(chart_df, x="name", y="risk_score", color="risk_level",
                 color_discrete_map=color_map, template="plotly_dark")
    fig.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117",
                      xaxis_tickangle=-45, height=380, margin=dict(t=20,b=80))
    fig.add_hline(y=65, line_dash="dash", line_color="#fc8181", annotation_text="High Risk")
    fig.add_hline(y=35, line_dash="dash", line_color="#f6ad55", annotation_text="Medium Risk")
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.markdown("### 🥧 Risk Distribution")
    risk_counts = fdf["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level","count"]
    fig2 = px.pie(risk_counts, names="risk_level", values="count",
                  color="risk_level", color_discrete_map=color_map,
                  template="plotly_dark", hole=0.45)
    fig2.update_layout(paper_bgcolor="#0e1117", height=380, margin=dict(t=20))
    st.plotly_chart(fig2, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("### 📉 Attendance vs Overall Score")
    fig3 = px.scatter(fdf, x="attendance_pct", y="overall_score", color="risk_level",
                      hover_name="name", color_discrete_map=color_map, template="plotly_dark")
    fig3.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", height=380)
    st.plotly_chart(fig3, use_container_width=True)

with col_b:
    st.markdown("### 📚 Risk by Subject")
    subj_risk = fdf.groupby(["subject","risk_level"]).size().reset_index(name="count")
    fig4 = px.bar(subj_risk, x="subject", y="count", color="risk_level",
                  color_discrete_map=color_map, barmode="stack", template="plotly_dark")
    fig4.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117",
                       xaxis_tickangle=-30, height=380, margin=dict(b=60))
    st.plotly_chart(fig4, use_container_width=True)
