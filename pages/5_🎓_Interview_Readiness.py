import streamlit as st
import pandas as pd
from components.ui import page_header
from components.charts import draw_readiness_radar_chart
from ai.gemini import get_interview_readiness_plan, analyze_resume_text
from resume.parser import extract_text_from_pdf
from github.client import GitHubClient

st.set_page_config(page_title="Interview Readiness | CareerPilot AI", layout="wide")
page_header("Interview Readiness", "Evaluate your skills and get a personalized learning roadmap", "🎓")

st.markdown("Provide both your **Resume** and your **GitHub Username** so the AI can build a comprehensive learning roadmap based on your combined skill profile.")

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("1. Upload Resume (PDF)", type=["pdf"])
    if st.session_state.get('resume_skills') and not uploaded_file:
        st.success("✅ Previously parsed resume skills are loaded in your session!")

with col2:
    repo_url = st.text_input("2. Enter GitHub Username:", value="torvalds")

if st.button("Generate Readiness Plan", type="primary"):
    
    # Handle Resume
    resume_skills = st.session_state.get('resume_skills', [])
    if uploaded_file:
        with st.spinner("Extracting and parsing new Resume..."):
            pdf_bytes = uploaded_file.read()
            resume_text = extract_text_from_pdf(pdf_bytes)
            resume_data = analyze_resume_text(resume_text[:4000])
            resume_skills = resume_data.get("extracted_skills", [])
            st.session_state['resume_skills'] = resume_skills
            
    if not resume_skills:
        st.error("No resume skills found. Please upload a PDF resume.")
        st.stop()

    # Handle GitHub
    username = repo_url.strip()
    if "github.com/" in username:
        username = username.split("github.com/")[-1].strip("/")
        
    with st.spinner("Analyzing GitHub profile and generating AI roadmap..."):
        gh = GitHubClient()
        languages = gh.get_all_user_languages(username)
        gh_skills = list(languages.keys())
        
        readiness_data = get_interview_readiness_plan(resume_skills, gh_skills)
        
        if not readiness_data:
            st.error("Failed to generate plan. Check API limits.")
            st.stop()

    st.success("Analysis complete!")
    st.markdown("<hr>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])

    with c1:
        st.subheader("Skill Radar")
        if "categories" in readiness_data:
            fig = draw_readiness_radar_chart(readiness_data["categories"])
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader(f"Overall Readiness Score: {readiness_data.get('overall_score', 0)}/100")
        
        st.markdown("### Strengths")
        for strength in readiness_data.get("strengths", []):
            st.markdown(f"- ✅ {strength}")
            
        st.markdown("### Areas for Improvement")
        for weakness in readiness_data.get("weaknesses", []):
            st.markdown(f"- ⚠️ {weakness}")

    with c2:
        st.subheader("Learning Roadmap")
        if "learning_roadmap" in readiness_data:
            df_roadmap = pd.DataFrame(readiness_data["learning_roadmap"])
            st.dataframe(df_roadmap, use_container_width=True, hide_index=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.subheader("Recommended Projects")
        for project in readiness_data.get("recommended_projects", []):
            st.info(f"🛠️ {project}")
            
        st.subheader("Practice Questions")
        for idx, question in enumerate(readiness_data.get("recommended_questions", []), 1):
            with st.expander(f"Question {idx}"):
                st.write(f"**{question}**")
