import streamlit as st
from components.ui import page_header
from components.cards import kpi_card
from database.service import get_recent_analyses

st.set_page_config(page_title="Dashboard | CareerPilot AI", layout="wide")

page_header("Dashboard", "Your career metrics overview", "📊")

# We no longer hardcode profile data here, we could fetch from DB if we cached the user
# For now, let's keep the dashboard focused on history
recent = get_recent_analyses()

# KPI Cards - Derived from history if possible, or static for now
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("Analyses Run", str(len(recent)), "+1 this week")
with col2:
    kpi_card("Avg Resume Score", "78", "+5")
with col3:
    kpi_card("Avg Github Score", "A-", "Steady")
with col4:
    kpi_card("Interview Readiness", "75%", "+10%")

st.markdown("<br>", unsafe_allow_html=True)

# Main Dashboard Content
col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("Recent Activity / Analyses")
    if not recent.empty:
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.info("No analyses run yet. Go to GitHub or Resume review to get started!")
    
    st.subheader("Quick Actions")
    qa_col1, qa_col2, qa_col3 = st.columns(3)
    with qa_col1:
        if st.button("Run New GitHub Review", use_container_width=True):
            st.switch_page("pages/2_💻_GitHub_Review.py")
    with qa_col2:
        if st.button("Analyze Resume", use_container_width=True):
            st.switch_page("pages/3_📄_Resume_Review.py")
    with qa_col3:
        if st.button("Check Readiness", use_container_width=True):
            st.switch_page("pages/5_🎓_Interview_Readiness.py")

with col_side:
    st.subheader("Welcome Back")
    st.markdown("Use the navigation menu to analyze your developer profile.")
    st.info("Live data is now connected to SQLite and Gemini AI.")
