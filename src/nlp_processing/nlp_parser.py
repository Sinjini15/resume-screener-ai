# src/nlp_processing/nlp_parser.py

import spacy
import re

# Load the small English model
nlp = spacy.load("en_core_web_sm")

# Example static list of skills to match (expand later)
SKILLS_DB = [
    "python", "machine learning", "data science", "deep learning", "nlp",
    "computer vision", "sql", "pytorch", "tensorflow", "docker",
    "aws", "azure", "spark", "hadoop", "java", "c++", "javascript"
]

def parse_resume_text(resume_text):
    parsed_data = {
        "name": None,
        "email": None,
        "phone": None,
        "skills": [],
        "education": [],
        "experience": []
    }

    doc = nlp(resume_text)

    # Extract name (first PERSON entity)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            parsed_data["name"] = ent.text
            break

    # Extract organizations as education or companies (for now just collect)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            parsed_data["education"].append(ent.text)

    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
    if email_match:
        parsed_data["email"] = email_match.group(0)

    # Extract phone number
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', resume_text)
    if phone_match:
        parsed_data["phone"] = phone_match.group(0)

    # Simple skill extraction (case insensitive match against skills DB)
    extracted_skills = []
    for token in doc:
        if token.text.lower() in SKILLS_DB:
            extracted_skills.append(token.text)
    parsed_data["skills"] = list(set(extracted_skills))  # deduplicate

    return parsed_data
