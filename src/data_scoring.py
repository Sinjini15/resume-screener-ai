import json
import pandas as pd
from pathlib import Path
from utils.data_utils import load_resumes  # You already have this
from utils.matching_utils import match_resume_to_job

# === CONFIG ===
data_dir = Path(__file__).resolve().parents[1] / 'data' / 'raw'
resumes_path = data_dir / 'synthetic_resumes.json'
jobs_path = data_dir / 'job_descriptions.json'

# === Load Resumes and Job Descriptions ===
with open(resumes_path, 'r') as f:
    resumes = json.load(f)

with open(jobs_path, 'r') as f:
    jobs = json.load(f)

# === Matching ===
results = []

for resume in resumes:
    for job in jobs:
        match_score, skills_match_pct, experience_score, education_score = match_resume_to_job(resume, job)
        results.append({
            'resume_name': resume.get('name', ''),
            'job_role': job.get('role', ''),
            'job_level': job.get('level', ''),
            'match_score': match_score,
            'skills_match_pct': skills_match_pct,
            'experience_score': experience_score,
            'education_score': education_score
        })

# === Save to DataFrame ===
match_df = pd.DataFrame(results)

# Print a preview
print(match_df.head())

# Save
processed_dir = Path(__file__).resolve().parents[1] / 'data' / 'processed'
processed_dir.mkdir(parents=True, exist_ok=True)
output_path = processed_dir / 'resume_job_scores.csv'
match_df.to_csv(output_path, index=False)

print(f"Saved resume-job match scores to {output_path}")
