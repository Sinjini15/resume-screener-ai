import pandas as pd
from pathlib import Path

def load_training_data():
    """
    Loads the resume-job matching dataset.
    """
    processed_dir = Path(__file__).resolve().parents[2] / 'data' / 'processed'
    input_path = processed_dir / 'resume_job_scores.csv'
    
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} resume-job match entries.")
    
    return df

def engineer_features(df):
    """
    Engineers features for model training.
    Returns X (features) and y (target).
    """

    # Feature 1: total_experience (simulate from job_level)
    job_level_map = {
        'Entry-level': 1,
        'Mid-level': 3,
        'PhD/Early Career': 2,  # Special handling possible later
    }
    df['job_level_num'] = df['job_level'].map(job_level_map).fillna(2)

    # Feature 2: resume seniority (simulate from resume_name if needed)
    
    df['resume_seniority'] = df['resume_name'].apply(lambda x: 2 if 'Dr.' in x else 1)

    # Feature 3: interaction term — job_level vs resume seniority (optional)
    df['level_match'] = (df['resume_seniority'] == df['job_level_num']).astype(int)
    
    #Feature 4: Add the new features and scale them for balance with other features 
    df['skills_match_pct'] = df['skills_match_pct'] * 0.01
    df['experience_score'] = df['experience_score'] * 0.01
    df['education_score'] = df['education_score'] * 0.01   

    # Select final features
    X = df[['skills_match_pct', 'experience_score', 'education_score', 'job_level_num', 'resume_seniority', 'level_match']]
    y = df['match_score']

    return X, y