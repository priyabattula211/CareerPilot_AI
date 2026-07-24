import streamlit as st
from components.ui import page_header, simulate_loading
from components.cards import skill_badge
from components.charts import draw_language_pie_chart
from github.client import GitHubClient
from ai.gemini import review_code_quality, analyze_repos_for_resume
from analysis.code_quality import clone_and_analyze
from database.service import add_analysis_record

st.set_page_config(page_title="GitHub Review | CareerPilot AI", layout="wide")
page_header("GitHub Review", "Analyze repositories, tech stack, and code quality", "💻")

st.markdown("Enter a **GitHub Username** (e.g. `octocat`) for a profile review, or a **full Repository URL** (e.g. `https://github.com/user/repo`) for a deep-dive repository review.")
repo_url = st.text_input("Username or Repository URL:", value="torvalds")

if st.button("Analyze GitHub", type="primary"):
    input_str = repo_url.strip()
    
    # URL parsing logic
    is_single_repo = False
    owner = ""
    repo_name = ""
    
    if "github.com/" in input_str:
        path = input_str.split("github.com/")[-1].strip("/")
        parts = path.split("/")
        if len(parts) >= 2:
            is_single_repo = True
            owner = parts[0]
            repo_name = parts[1]
        else:
            owner = parts[0]
    else:
        parts = input_str.split("/")
        if len(parts) == 2:
            is_single_repo = True
            owner = parts[0]
            repo_name = parts[1]
        else:
            owner = input_str
            
    with st.spinner("Fetching data from GitHub API..."):
        gh = GitHubClient()
        
        repos = []
        languages = {}
        
        if is_single_repo:
            repo_data = gh.get_repo(owner, repo_name)
            if not repo_data:
                st.error(f"Repository {owner}/{repo_name} not found.")
                st.stop()
            repos = [repo_data]
            langs = gh.get_repo_languages(owner, repo_name)
            languages = dict(sorted(langs.items(), key=lambda item: item[1], reverse=True)[:5])
        else:
            profile = gh.get_user_profile(owner)
            if not profile:
                st.error(f"User {owner} not found or API limit reached.")
                st.stop()
            repos = gh.get_user_repos(owner, limit=5)
            languages = gh.get_all_user_languages(owner)
        
    with st.spinner("Running AI and Static Code Analysis..."):
        readme = ""
        if repos:
            readme_owner = owner
            readme_repo = repos[0]['name']
            readme = gh.get_readme(readme_owner, readme_repo)
        
        repo_names = [r['name'] for r in repos]
        ai_reviews = review_code_quality(readme[:1000], list(languages.keys()), repo_names)
        
        # AI Resume Suggestions
        repo_info_list = [{'name': r['name'], 'description': r.get('description', ''), 'language': r.get('language', '')} for r in repos]
        repo_analysis_res = analyze_repos_for_resume(repo_info_list)
        repo_analysis_dict = {item.get('name'): item for item in repo_analysis_res.get('repo_analysis', []) if 'name' in item}

        # Static analysis
        static_analysis = []
        if repos:
            top_repo_url = repos[0].get('html_url', '')
            if top_repo_url:
                static_analysis = clone_and_analyze(top_repo_url)

    # Save to history
    record_type = "Single Repo Analysis" if is_single_repo else "GitHub Profile Analysis"
    add_analysis_record("GitHub Analysis", record_type, {"target": input_str})
    
    st.success("Analysis complete!")
    
    if is_single_repo:
        st.subheader(f"Repository Overview: {owner}/{repo_name}")
    else:
        st.subheader(f"Profile Overview: {owner}")
        
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"**{'Repository' if is_single_repo else 'Overall'} Language Distribution**")
        if languages:
            fig = draw_language_pie_chart(languages)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("**Tech Stack Found**")
            tech_html = " ".join([skill_badge(lang, "matched") for lang in languages.keys()])
            st.markdown(tech_html, unsafe_allow_html=True)
        else:
            st.write("No languages found.")
        
    with col2:
        st.markdown(f"**{'Repository Details' if is_single_repo else 'Top Repositories'}**")
        for repo in repos:
            with st.expander(f"{repo['name']} - ⭐ {repo.get('stargazers_count', 0)}", expanded=is_single_repo):
                ai_repo = repo_analysis_dict.get(repo['name'], {})
                desc = ai_repo.get('description') or repo.get('description') or 'None'
                
                st.write(f"**Description:** {desc}")
                st.write(f"**Main Language:** {repo.get('language', 'Unknown')}")
                
                if ai_repo.get('resume_suggestion'):
                    st.info(f"**Resume Value:** {ai_repo.get('resume_suggestion')}")
                
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.subheader(f"AI Code Quality & README Review ({repos[0]['name'] if repos else 'N/A'})")
    for review in ai_reviews:
        score_color = "green" if review.get("score", 0) >= 8 else "orange" if review.get("score", 0) >= 6 else "red"
        st.markdown(f"**{review.get('aspect', 'General')}** - <span style='color:{score_color}'>{review.get('score', 0)}/10</span>", unsafe_allow_html=True)
        st.write(review.get("feedback", ""))
        st.markdown("---")

    if static_analysis:
        st.subheader("Static Code Analysis Results")
        for sa in static_analysis:
            st.markdown(f"**{sa['aspect']}**: Score {sa['score']}/10 - {sa['feedback']}")
