import streamlit as st
import plotly.graph_objects as go
from components.ui import page_header
from components.cards import skill_badge
from resume.parser import extract_text_from_pdf
from ai.gemini import analyze_resume_text
from database.service import add_analysis_record
import json

st.set_page_config(page_title="Resume Review | CareerPilot AI", layout="wide")

page_header("Resume Review", "Upload your resume for AI-driven analysis and ATS scoring", "📄")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    if st.button("Analyze Resume", type="primary"):
        with st.spinner("Extracting text from PDF..."):
            pdf_bytes = uploaded_file.read()
            resume_text = extract_text_from_pdf(pdf_bytes)
            
        with st.spinner("Analyzing with Gemini AI..."):
            resume_data = analyze_resume_text(resume_text[:4000]) # limit text length for prompt
            
            if "error" in resume_data or not resume_data:
                err_msg = resume_data.get("error", "Unknown error")
                st.error(f"Failed to analyze resume. Error: {err_msg}")
                st.stop()
                
            # Store in session state for Portfolio Match page
            st.session_state['resume_skills'] = resume_data.get("extracted_skills", [])
            add_analysis_record("Resume Review", f"{resume_data.get('ats_score', 0)}/100")
            
        st.success("Resume parsed successfully!")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("ATS Match Score")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = resume_data.get("ats_score", 0),
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#4F46E5"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#334155",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                        {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.3)'},
                        {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.3)'}],
                }
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'), height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Extracted Skills")
            skills_html = " ".join([skill_badge(skill, "neutral") for skill in resume_data.get("extracted_skills", [])])
            st.markdown(skills_html, unsafe_allow_html=True)
            
        with col2:
            st.subheader("Experience")
            for exp in resume_data.get("experience", []):
                st.markdown(f"**{exp.get('title')}** at {exp.get('company')} *({exp.get('years')})*")
                st.write(exp.get("description"))
                
            st.subheader("Education")
            for edu in resume_data.get("education", []):
                st.markdown(f"**{edu.get('degree')}** - {edu.get('institution')} *({edu.get('year')})*")
                
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("### 💡 AI Suggestions for Improvement")
            suggestions = resume_data.get("suggestions", [])
            if suggestions:
                for idx, suggestion in enumerate(suggestions):
                    st.info(f"**Tip {idx+1}:** {suggestion}")
            else:
                st.success("Your resume looks great! No major improvements needed.")
