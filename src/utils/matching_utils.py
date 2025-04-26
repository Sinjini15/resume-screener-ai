# src/utils/matching_utils.py

import math

def education_level_order(level):
    """Assigns a numeric ranking to education levels."""
    mapping = {'PhD': 3, 'MS': 2, 'BS': 1, 'Unknown': 0}
    return mapping.get(level, 0)

def calculate_skills_match(resume_skills, job_skills):
    """Calculates skill overlap percentage."""
    resume_skills_set = set(resume_skills)
    job_skills_set = set(job_skills)
    if not job_skills_set:
        return 0.0
    return len(resume_skills_set & job_skills_set) / len(job_skills_set) * 100

def meets_experience_threshold(resume_experience, min_experience, multiplier):
    """Checks if resume experience meets a scaled threshold."""
    min_years = max(min_experience, 1)  # Apply floor to avoid 0 experience multipliers
    return resume_experience >= (min_years * multiplier)

def evaluate_education_match(resume_education, job_education, skills_match, resume_experience, min_experience):
    """
    Evaluates education match with nuanced logic.
    Returns a score between 0 and 100.
    """
    resume_level = education_level_order(resume_education)
    job_level = education_level_order(job_education)

    # Case 1: Education matches or exceeds
    if resume_level >= job_level:
        return 100

    # Case 2: No Degree
    if resume_level == 0:
        if skills_match > 90 and meets_experience_threshold(resume_experience, min_experience, 5):
            return 100
        else:
            return 50

    # Case 3: Lower Degree
    if job_level == 3 and resume_level == 1:  # BS vs PhD
        if skills_match > 85 and resume_experience >= (min_experience + 6):
            return 100
        else:
            return 50
    elif job_level == 3 and resume_level == 2:  # MS vs PhD
        if skills_match > 75 and resume_experience >= (min_experience + 4):
            return 100
        else:
            return 50
    else:
        # Other lower degree cases
        if skills_match > 80 and resume_experience >= (min_experience + 5):
            return 80
        else:
            return 50

def match_resume_to_job(resume, job):
    """
    Matches a single resume to a single job description.
    Returns an overall score (0-100).
    """
    resume_skills = resume.get('skills', [])
    resume_experience = sum(exp.get('years', 0) for exp in resume.get('experience', []))
    resume_education = resume.get('education_level', 'Unknown')

    job_skills = job.get('required_skills', [])
    job_min_experience = job.get('min_experience_years', 0)
    job_education = job.get('education_requirement', 'Unknown')

    skills_score = calculate_skills_match(resume_skills, job_skills)

    # Experience score: normally full if meets requirement, otherwise check skills exception
    if resume_experience >= job_min_experience or skills_score > 50:
        experience_score = 100
    else:
        experience_score = 50

    education_score = evaluate_education_match(
        resume_education,
        job_education,
        skills_score,
        resume_experience,
        job_min_experience
    )

    # Weighted scoring
    final_score = (skills_score * 0.7) + (experience_score * 0.2) + (education_score * 0.1)

    return round(final_score, 2), round(skills_score, 2), experience_score, education_score
