from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import tempfile
import os
import logging

from src.nlp_processing.pdf_parser import extract_text_from_pdf
from src.nlp_processing.llm_text_cleaner import clean_resume_text_with_openai
from src.nlp_processing.matching_engine import compute_resume_job_score

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.post("/match")
async def match_resumes(
    files: list[UploadFile] = File(...),
    job_description: str = Form(...)
):
    ranked_candidates = []

    for file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        try:
            raw_text = extract_text_from_pdf(tmp_path)
            cleaned = clean_resume_text_with_openai(raw_text)
            score = compute_resume_job_score(cleaned, job_description)
            ranked_candidates.append({
                "resume_file": file.filename,
                "match_score": round(score, 4)
            })
            logging.info(f"{file.filename}: Score {score:.4f}")
        finally:
            os.remove(tmp_path)  # always clean up

    # Sort by match score (descending)
    ranked_candidates.sort(key=lambda x: x["match_score"], reverse=True)

    return JSONResponse({
        "job_description_snippet": job_description[:100],
        "ranked_candidates": ranked_candidates
    })
