import streamlit as st
from database.service import get_recent_analyses

# Premium Hero Section & Native Streamlit Element Styling
st.markdown("""
<style>
.hero-container {
    background: radial-gradient(circle at top right, rgba(139, 92, 246, 0.15), transparent 50%),
                radial-gradient(circle at bottom left, rgba(56, 189, 248, 0.15), transparent 50%);
    border-radius: 24px;
    padding: 5rem 2rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 3rem;
    box-shadow: inset 0 0 50px rgba(0,0,0,0.5);
}
.hero-title {
    font-size: 4.5rem !important;
    font-weight: 900 !important;
    margin-bottom: 1.5rem !important;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    letter-spacing: -0.03em;
}
.hero-subtitle {
    font-size: 1.3rem;
    color: #94A3B8;
    max-width: 750px;
    margin: 0 auto;
    line-height: 1.7;
    font-weight: 400;
}

/* Transform default Streamlit page_links into beautiful massive cards */
div[data-testid="stPageLink-NavLink"] {
    background: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    margin-bottom: 0.5rem;
}
div[data-testid="stPageLink-NavLink"]:hover {
    background: rgba(56, 189, 248, 0.1) !important;
    border-color: rgba(56, 189, 248, 0.5) !important;
    transform: translateY(-5px) !important;
    box-shadow: 0 15px 30px -10px rgba(56, 189, 248, 0.3) !important;
}
div[data-testid="stPageLink-NavLink"] p {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
}
</style>

<div class="hero-container">
    <h1 class="hero-title">CareerPilot AI</h1>
    <p class="hero-subtitle">
        Your ultimate AI-Powered Developer Career Assistant.<br/>
        Analyze your code, perfect your resume, and master your next interview with data-driven insights.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if "initialized" not in st.session_state:
    st.session_state.initialized = True

st.markdown("<h3 style='text-align: center; color: #F8FAFC; margin-bottom: 2.5rem; font-weight: 600; letter-spacing: -0.02em;'>Select a module to begin</h3>", unsafe_allow_html=True)

# Functional Navigation Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/3_📄_Resume_Review.py", label="Resume Review", icon="📄")
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.95rem; padding: 0 1rem;'>Instant ATS scoring & skill extraction.</p>", unsafe_allow_html=True)
with col2:
    st.page_link("pages/2_💻_GitHub_Review.py", label="GitHub Analysis", icon="💻")
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.95rem; padding: 0 1rem;'>Automated code quality & repo reviews.</p>", unsafe_allow_html=True)
with col3:
    st.page_link("pages/5_🎓_Interview_Readiness.py", label="Interview Prep", icon="🎓")
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.95rem; padding: 0 1rem;'>Get a week-by-week learning roadmap.</p>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.info("💡 **Pro Tip**: Start by uploading your Resume. The AI needs to learn your baseline skills before it can accurately map your Interview Readiness!")

st.markdown("<hr>", unsafe_allow_html=True)

st.subheader("Your Career Analytics")

try:
    df = get_recent_analyses(limit=50)
    total_analyses = len(df)
    
    github_reviews = len(df[df['type'] == 'GitHub Analysis']) if not df.empty else 0
    resume_reviews = len(df[df['type'] == 'Resume Analysis']) if not df.empty else 0
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total AI Analyses", total_analyses, delta="Active", delta_color="normal")
    m2.metric("GitHub Profiles Reviewed", github_reviews)
    m3.metric("Resumes Scanned", resume_reviews)
    
except Exception as e:
    st.write("Start running analyses to see your stats here!")
