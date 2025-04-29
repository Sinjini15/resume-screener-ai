# test_full_flow.py

from src.nlp_processing.pdf_extractor import extract_text_from_pdf
from src.nlp_processing.nlp_parser import parse_resume_text
from src.nlp_processing.matching_engine import compute_resume_job_score

# Step 1: Extract text from a sample PDF
pdf_path = "data/raw/Sinjini_resume_LinkedIn.pdf"  # replace with an actual PDF path
extracted_text = extract_text_from_pdf(pdf_path)

# Step 2: Parse the extracted text into structured resume fields
parsed_resume = parse_resume_text(extracted_text)

# Step 3: Define a sample job description
job_description = """
We are looking for a Machine Learning Engineer skilled in Python, deep learning, and data science.
The ideal candidate should have experience with large-scale model training and cloud deployments.
"""

# Step 4: Compute match score
score = compute_resume_job_score(parsed_resume, job_description)

# Step 5: Print outputs
print("\nParsed Resume:")
for key, value in parsed_resume.items():
    print(f"{key}: {value}")

print(f"\nResume-JD Match Score: {score:.4f}")
