# src/retrieval_system.py

import pandas as pd
from pathlib import Path

def load_score_data():
    """
    Loads the resume-job match scores.
    """
    processed_dir = Path(__file__).resolve().parents[1] / 'data' / 'processed'
    input_path = processed_dir / 'resume_job_scores.csv'
    df = pd.read_csv(input_path)
    return df

def retrieve_top_n_resumes(job_role, top_n=5):
    """
    Given a job_role, retrieves Top N resumes sorted by match_score.
    """
    df = load_score_data()
    
    # Filter for the specific job role
    df_filtered = df[df['job_role'].str.lower() == job_role.lower()]
    
    # Sort by match_score descending
    df_sorted = df_filtered.sort_values(by='match_score', ascending=False)
    
    # Return top N results
    return df_sorted[['resume_name', 'match_score']].head(top_n)
   


if __name__ == "__main__":
    top_resumes = retrieve_top_n_resumes('Doctor', top_n=3)
    
    #Check if there are any  matches
    
    if len(top_resumes) > 0:
        print(top_resumes)
    else:
        print("No candidates match queired job role")
