import streamlit as st

def require_data():
    """
    Call at the top of every page.
    If no CSV has been uploaded yet, shows a friendly message and stops the page.
    """
    if "df" not in st.session_state or st.session_state["df"] is None:
        st.markdown("""
        <style>
            header { visibility: hidden; }
            .guard-box {
                background: #1a2332; border: 1px solid #2d4a6e;
                border-radius: 16px; padding: 48px 32px;
                text-align: center; margin-top: 60px;
            }
            .guard-icon  { font-size: 56px; margin-bottom: 16px; }
            .guard-title { font-size: 22px; font-weight: 800; color: #e2e8f0; margin-bottom: 8px; }
            .guard-sub   { font-size: 15px; color: #718096; margin-bottom: 24px; }
        </style>
        <div class="guard-box">
            <div class="guard-icon">📂</div>
            <div class="guard-title">No Data Uploaded Yet</div>
            <div class="guard-sub">
                Please go to the <strong>Home page</strong> and upload your students CSV file first.
                All agents will unlock instantly after upload.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link("main.py", label="⬅️ Go to Home & Upload CSV", icon="🏠")
        st.stop()
