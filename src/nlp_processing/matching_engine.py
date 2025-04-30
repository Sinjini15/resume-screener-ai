# src/nlp_processing/matching_engine.py

from sentence_transformers import SentenceTransformer, util

# Load a lightweight sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_resume_job_score(cleaned_resume_text, job_description_text):
    """
    Computes a semantic similarity score between the cleaned resume text and a job description.

    Args:
        cleaned_resume_text (str): Resume text cleaned and summarized by the LLM.
        job_description_text (str): Raw job description text.

    Returns:
        float: Cosine similarity score between 0 and 1.
    """
    # Encode both texts
    embeddings = model.encode([cleaned_resume_text, job_description_text])

    # Compute cosine similarity
    score = util.cos_sim(embeddings[0], embeddings[1]).item()

    return score
