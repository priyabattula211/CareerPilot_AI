import streamlit as st
import plotly.graph_objects as go
from components.ui import page_header
from components.cards import skill_badge
from analysis.scoring import calculate_portfolio_match
from github.client import GitHubClient

st.set_page_config(page_title="Portfolio Match | CareerPilot AI", layout="wide")
page_header("Portfolio Match", "Bridge the gap between your resume claims and GitHub evidence", "🎯")

# Ensure skills are present in session state or fetch them
if 'resume_skills' not in st.session_state:
    st.warning("Please run a Resume Review first to extract your skills.")
else:
    repo_url = st.text_input("Enter GitHub Username to compare against:", value="torvalds")
    
    if st.button("Calculate Match"):
        username = repo_url.strip()
        if "github.com/" in username:
            username = username.split("github.com/")[-1].strip("/")
            
        with st.spinner("Fetching GitHub skills..."):
            gh = GitHubClient()
            languages = gh.get_all_user_languages(username)
            gh_skills = list(languages.keys())
            
        match_data = calculate_portfolio_match(st.session_state['resume_skills'], gh_skills)

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Match Score")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = match_data["match_percentage"],
                title = {'text': "Resume vs GitHub Alignment"},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#10B981"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [
                        {'range': [0, 60], 'color': 'rgba(239, 68, 68, 0.3)'},
                        {'range': [60, 80], 'color': 'rgba(245, 158, 11, 0.3)'},
                        {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.3)'}],
                }
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'), height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Skills Analysis")
            
            st.markdown("**✅ Verified Skills (On Resume & GitHub)**")
            matched_html = " ".join([skill_badge(skill, "matched") for skill in match_data["matched"]])
            st.markdown(matched_html if matched_html else "None found", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("**⚠️ Missing Evidence (On Resume, NOT on GitHub)**")
            missing_gh_html = " ".join([skill_badge(skill, "missing") for skill in match_data["missing_in_github"]])
            st.markdown(missing_gh_html if missing_gh_html else "None found", unsafe_allow_html=True)
            st.caption("You claim these skills, but we couldn't find public repositories using them.")

            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("**💡 Hidden Strengths (On GitHub, NOT on Resume)**")
            missing_res_html = " ".join([skill_badge(skill, "neutral") for skill in match_data["missing_in_resume"]])
            st.markdown(missing_res_html if missing_res_html else "None found", unsafe_allow_html=True)
            st.caption("You use these regularly on GitHub. Consider adding them to your resume!")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Action Plan")
        for action in match_data["action_plan"]:
            st.info(action)
