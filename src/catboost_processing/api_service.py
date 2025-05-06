# src/api_service.py

from fastapi import FastAPI
from pydantic import BaseModel
from src.retrieval_system import retrieve_top_n_resumes

app = FastAPI(title="Resume Screener API", version="0.1")

class JobQuery(BaseModel):
    job_role: str
    top_n: int = 5

@app.post("/retrieve")
def retrieve_resumes(query: JobQuery):
    results = retrieve_top_n_resumes(query.job_role, top_n=query.top_n)
    # Convert to JSON-friendly output
    return {
        "job_role": query.job_role,
        "top_matches": results.to_dict(orient="records")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
