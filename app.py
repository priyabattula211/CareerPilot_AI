import streamlit as st
from components.ui import load_css

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# Define Pages
home_page = st.Page("pages/1_🚀_Home.py", title="Dashboard", icon="📊", default=True)
github_page = st.Page("pages/2_💻_GitHub_Review.py", title="GitHub Analysis", icon="💻")
resume_page = st.Page("pages/3_📄_Resume_Review.py", title="Resume Review", icon="📄")
portfolio_page = st.Page("pages/4_🎯_Portfolio_Match.py", title="Portfolio Match", icon="🎯")
interview_page = st.Page("pages/5_🎓_Interview_Readiness.py", title="Interview Prep", icon="🎓")
settings_page = st.Page("pages/6_⚙️_Settings.py", title="Settings", icon="⚙️")

# Group pages in the sidebar
nav = st.navigation(
    {
        "Overview": [home_page],
        "AI Analysis Tools": [resume_page, github_page],
        "Career Strategy": [portfolio_page, interview_page],
        "Configuration": [settings_page],
    }
)

nav.run()
