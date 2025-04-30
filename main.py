from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ResumeRequest(BaseModel):
    resume_text: str

@app.post("/match")
def match_resume(request: ResumeRequest):
    # Placeholder response
    return {"matched_jobs": ["Job A", "Job B"], "input_snippet": request.resume_text[:100]}
