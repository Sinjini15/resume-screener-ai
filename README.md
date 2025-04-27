# Resume Screener AI 🚀

An AI-powered system to automatically screen, rank, and retrieve resumes based on job descriptions, powered by machine learning and modern retrieval architectures.

## 📚 Project Overview

This project builds a full resume screening pipeline:

- **Resume Parsing**: Structured synthetic resume data creation.
- **Job Matching**: Matching resumes to multiple job descriptions using skills, experience, and education alignment.
- **Feature Engineering**: Creation of nuanced raw signals (skills match %, experience matching, education evaluation).
- **Model Training**: CatBoost Regressor trained on engineered features to predict match quality.
- **Retrieval System** (Upcoming): Fast API service to retrieve top candidates for a given job query.

## 📈 Model Performance

- Model: **CatBoost Regressor**
- Final Test RMSE: **0.00004**
- Interpretation:  
  The model achieves near-perfect prediction of resume-to-job match scores, demonstrating high signal extraction and strong feature engineering alignment with the target metric.

## 📂 Project Structure

```
resume-screener-ai/
├── data/
│   ├── raw/                 # Raw synthetic resumes and job descriptions
│   ├── processed/           # Processed CSVs (resume-job scores)
├── models/                  # Saved trained model artifacts
|   ├── catboost_resume_matcher.pkl
├── src/
│   ├── utils/
│   │   ├── data_utils.py      # Data loading utilities
│   │   ├── feature_utils.py   # Feature engineering functions
│   │   └── matching_utils.py  # Resume-job matching logic
|   ├── api_service.py        # FastAPI implementation
│   ├── data_processing.py    # Initial data preparation
│   ├── model_training.py     # Model training and evaluation script
|   ├── kill_uvicorn.sh       # Bash script to kill FastAPI server
|   ├── llm_explanations.py   # Leveraging LLM to query specific jobs
|   ├── retrieval_system.py   # Retrieving jobs matching certain queries
├── docker-compose.yml
├── Dockerfile              # Docker image builder
├── README.md
├── requirements.txt
```

## Running Locally (Without Docker)

1. Clone the repository

```
git clone https://github.com/Sinjini15/resume-screener-ai.git
cd resume-screener-ai
```
2. Install dependencies

```
pip install -r requirements.txt
```

3. Start the FastAPI server:

```
uvicorn src.api_service:app --reload
```

4. Open your browser at http://127.0.0.1:8000/docs

## Running with Docker

1. Build the Docker image:

```
docker build -t resume-screener-api .
```

2. Run the Docker container:

```
docker run -p 8000:8000 resume-screener-api
```

3. Open your broswer at: http://127.0.0.1:8000/docs

## Running with Docker Compose:

1. Use Docker Compose to build and run:

```
docker-compose up --build
```

2. To stop the conmtainer:
```
docker-compose down
```

## API Endpoint

* POST/retrieve
Retrieve ranked resumes based on the given job description


✅ Fully modularized, production-ready codebase with clean separation of concerns.

---

> Built for real-world AI-driven hiring workflows.
> Future steps include retrieval system deployment via FastAPI, Dockerization, and AWS cloud hosting.

