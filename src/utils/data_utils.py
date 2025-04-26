# src/utils/data_utils.py

import json
import pandas as pd
from pathlib import Path

def load_resumes(json_path):
    """
    Loads resumes from a JSON file.

    Args:
        json_path (str or Path): Path to the JSON file.

    Returns:
        list: List of resume dictionaries.
    """
    with open(json_path, 'r') as f:
        resumes = json.load(f)
    return resumes

def extract_features(resumes):
    """
    Extracts structured features from a list of resumes.

    Args:
        resumes (list): List of resume dictionaries.

    Returns:
        pd.DataFrame: DataFrame with extracted features.
    """
    feature_list = []

    for resume in resumes:
        total_experience = sum(exp['years'] for exp in resume.get('experience', []))
        num_skills = len(resume.get('skills', []))
        has_certifications = int(len(resume.get('certifications', [])) > 0)
        education_text = resume.get('education', '').lower()

        if 'ph.d' in education_text:
            education_level = 'PhD'
        elif 'm.s' in education_text or 'master' in education_text:
            education_level = 'MS'
        elif 'b.s' in education_text or 'bachelor' in education_text:
            education_level = 'BS'
        else:
            education_level = 'Unknown'

        feature_list.append({
            'name': resume.get('name', ''),
            'total_experience': total_experience,
            'num_skills': num_skills,
            'has_certifications': has_certifications,
            'education_level': education_level,
            'target_role': resume.get('target_role', '')
        })

    return pd.DataFrame(feature_list)

def save_features(df, output_path):
    """
    
    Saves the extracted features DataFrame to a CSV file.
    
    Args:
        df (pd.DataFrame): DataFrame of resume information
        output_path(str or Path): Destination path for the CSV.
    """
    
    df.to_csv(output_path, index = False)
    print("Saved extracted features to {output_path}")
