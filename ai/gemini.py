import google.generativeai as genai
from utils.config import GEMINI_API_KEY
from utils.logger import get_logger
from database.service import get_setting
import json

logger = get_logger(__name__)

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.warning("No API key loaded on startup.")

def generate_json_response(prompt):
    model_name = get_setting("GEMINI_MODEL", "gemini-2.5-flash")
    if not GEMINI_API_KEY:
        logger.warning("Gemini model not initialized. Missing API key.")
        return {"error": "Gemini model not initialized. Missing API key."}
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        return json.loads(raw_text.strip())
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return {"error": str(e)}

def analyze_resume_text(resume_text):
    prompt = f"""
    Analyze the following resume text and extract key information. 
    Return the result strictly as JSON with this schema:
    {{
        "ats_score": (int from 0 to 100),
        "extracted_skills": ["skill1", "skill2"],
        "experience": [
            {{"title": "Role", "company": "Company", "years": "Duration", "description": "Short summary"}}
        ],
        "education": [
            {{"degree": "Degree", "institution": "School", "year": "Year"}}
        ],
        "suggestions": ["suggestion1", "suggestion2"]
    }}
    
    Resume Text:
    {resume_text}
    """
    return generate_json_response(prompt)

def review_code_quality(readme_text, languages, repos):
    prompt = f"""
    You are an expert software engineer reviewing a developer's GitHub profile.
    Based on their README, Languages: {languages}, and Repos: {repos}, provide a code quality and architecture review.
    Return JSON:
    {{
        "reviews": [
            {{"aspect": "Modularity", "score": (0-10), "feedback": "reasoning"}},
            {{"aspect": "Documentation", "score": (0-10), "feedback": "reasoning"}},
            {{"aspect": "Testing", "score": (0-10), "feedback": "reasoning"}},
            {{"aspect": "Best Practices", "score": (0-10), "feedback": "reasoning"}}
        ]
    }}
    """
    res = generate_json_response(prompt)
    return res.get("reviews", [])

def get_interview_readiness_plan(resume_skills, github_skills):
    prompt = f"""
    Analyze a developer's readiness for a software engineering interview based on their resume skills ({resume_skills}) and GitHub skills ({github_skills}).
    Return JSON:
    {{
        "overall_score": (0-100),
        "categories": {{
            "Algorithms": (0-100),
            "System Design": (0-100),
            "Language Mastery": (0-100),
            "Behavioral": (0-100)
        }},
        "strengths": ["strength1"],
        "weaknesses": ["weakness1"],
        "learning_roadmap": [
            {{"week": "Week 1", "topic": "topic", "status": "Pending"}}
        ],
        "recommended_projects": ["project1"],
        "recommended_questions": ["q1", "q2", "q3"]
    }}
    """
    return generate_json_response(prompt)

def analyze_repos_for_resume(repos_info):
    prompt = f"""
    You are an expert technical recruiter and software engineer.
    Analyze the following list of GitHub repositories belonging to a candidate.
    For each repository, provide a brief, professional description (inferring from the name and language if the original description is missing) and a specific suggestion on how this project adds value to their resume and what talking points they should use in an interview.

    Repositories: {json.dumps(repos_info)}

    Return the result strictly as JSON with this schema:
    {{
        "repo_analysis": [
            {{
                "name": "repository-name",
                "description": "A brief, clear description of the project.",
                "resume_suggestion": "Why this is useful on a resume and what skills/concepts to highlight in an interview."
            }}
        ]
    }}
    """
    return generate_json_response(prompt)
