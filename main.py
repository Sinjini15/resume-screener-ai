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
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            raw_text = extract_text_from_pdf(tmp_path)
            cleaned = clean_resume_text_with_openai(raw_text)
            score = compute_resume_job_score(cleaned, job_description)

            ranked_candidates.append({
                "resume_file": file.filename,
                "match_score": round(score, 4)
            })
            logging.info(f"{file.filename}: Score {score:.4f}")
        except Exception as e:
            logging.error(f"Failed to process {file.filename}: {e}")
            ranked_candidates.append({
                "resume_file": file.filename,
                "match_score": None,
                "error": str(e)
            })
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # Sort valid scores to the top
    ranked_candidates.sort(key=lambda x: x["match_score"] if x["match_score"] is not None else -1, reverse=True)

    return JSONResponse({
        "job_description_snippet": job_description[:100],
        "ranked_candidates": ranked_candidates
    })
