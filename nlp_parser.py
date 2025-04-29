# src/nlp_processing/nlp_parser.py

from src.nlp_processing.pdf_parser import parse_resume_nlp
from src.nlp_processing.matching_engine import compute_resume_job_score


job_description_text = """
    We are looking for a Machine Learning Engineer with strong skills in Python, deep learning frameworks like PyTorch and TensorFlow, and experience deploying models in production environments.
    """

parsed_resume = parse_resume_nlp("data/raw/Sinjini_resume_LinkedIn.pdf")
print("\nParsed Resume Output:\n")

for section, items in parsed_resume.items():
        print(f"{section.capitalize()}: {items}")
        
match_score = compute_resume_job_score(parsed_resume, job_description_text)

print(f"\nResume-JD Match Score: {match_score:.4f}")