# src/nlp_processing/matching_engine.py

from sentence_transformers import SentenceTransformer, util

# Load a lightweight sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_list(items):
    return list(set([item.strip() for item in items if item]))

def compute_resume_job_score(parsed_resume, job_description_text):
    """
    Computes a matching score between a parsed resume and a job description.
    
    Args:
        parsed_resume (dict): Structured resume data from NLP parser.
        job_description_text (str): Job description text.

    Returns:
        float: Similarity score between 0 and 1.
    """
    
    

    # Create a text representation of the resume
    resume_text_parts = []
    if parsed_resume.get("name"):
        resume_text_parts.append(parsed_resume["name"])
    if parsed_resume.get("skills"):
        resume_text_parts.append(" ".join(clean_list(parsed_resume["skills"])))
    if parsed_resume.get("education"):
        resume_text_parts.append(" ".join(clean_list(parsed_resume["education"])))
    if parsed_resume.get("experience"):
        resume_text_parts.append(" ".join(clean_list(parsed_resume["experience"])))

    full_resume_text = " ".join(resume_text_parts)

    # Encode both texts
    embeddings = model.encode([full_resume_text, job_description_text])

    # Compute cosine similarity
    score = util.cos_sim(embeddings[0], embeddings[1]).item()

    return score
