# src/nlp_processing/test_candidate_ranking.py

from src.nlp_processing.pdf_parser import extract_text_from_pdf
from src.nlp_processing.llm_text_cleaner import clean_resume_text_with_openai
from src.nlp_processing.matching_engine import compute_resume_job_score  
from dotenv import load_dotenv
import os


# Test job description
job_description = """
We are looking for a machine learning engineer with experience in Python, PyTorch, deep learning, model deployment, and cloud infrastructure. Knowledge of large language models and generative AI is a strong plus.
"""

# Test resume PDF paths
resume_paths = [
    "data/raw/test_resume_1.pdf",
    "data/raw/test_resume_2.pdf",
    "data/raw/test_resume_3.pdf"
]

ranked_candidates = []

print("==> Now parsing resumes")

for path in resume_paths:
    raw_text = extract_text_from_pdf(path)
    cleaned = clean_resume_text_with_openai(raw_text)
    score = compute_resume_job_score(cleaned, job_description)
    ranked_candidates.append((path, score))

# Sort candidates by score (descending)
ranked_candidates.sort(key=lambda x: x[1], reverse=True)

print("==> Displaying ranked candidates")
# Print results
for i, (path, score) in enumerate(ranked_candidates, 1):
    print(f"{i}. {path} — Match Score: {score:.4f}")


