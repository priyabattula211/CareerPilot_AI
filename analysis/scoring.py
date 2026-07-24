def calculate_portfolio_match(resume_skills, github_skills):
    """Calculates match percentage and identifies missing skills."""
    res_set = set([s.lower() for s in resume_skills])
    gh_set = set([s.lower() for s in github_skills])
    
    if not res_set:
        return {"match_percentage": 0, "matched": [], "missing_in_github": [], "missing_in_resume": list(gh_set)}
        
    matched = res_set.intersection(gh_set)
    missing_gh = res_set - gh_set
    missing_res = gh_set - res_set
    
    match_percentage = int((len(matched) / len(res_set)) * 100)
    
    return {
        "match_percentage": match_percentage,
        "matched": list(matched),
        "missing_in_github": list(missing_gh),
        "missing_in_resume": list(missing_res),
        "action_plan": [
            f"Consider building a project on GitHub using {', '.join(list(missing_gh)[:3])} to back up your resume." if missing_gh else "Great alignment between resume and GitHub!",
            f"You seem to know {', '.join(list(missing_res)[:3])} based on GitHub. Add them to your resume!" if missing_res else "Your resume captures your GitHub skills well."
        ]
    }
