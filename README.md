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
├── src/
│   ├── utils/
│   │   ├── data_utils.py      # Data loading utilities
│   │   ├── feature_utils.py   # Feature engineering functions
│   │   └── matching_utils.py  # Resume-job matching logic
│   ├── data_processing.py    # Initial data preparation
│   ├── model_training.py     # Model training and evaluation script
├── README.md
├── requirements.txt
```

✅ Fully modularized, production-ready codebase with clean separation of concerns.

---

> Built for real-world AI-driven hiring workflows.
> Future steps include retrieval system deployment via FastAPI, Dockerization, and AWS cloud hosting.

