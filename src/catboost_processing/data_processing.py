# src/data_processing.py

from pathlib import Path
from utils.data_utils import load_resumes, extract_features, save_features


if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parents[1] / 'data' / 'raw'
    processed_dir = Path(__file__).resolve().parents[1] / 'data' / 'processed'
    processed_dir.mkdir(parents=True, exist_ok=True)  # Create processed/ if it doesn't exist
    
    json_path = data_dir / 'synthetic_resumes.json'
    csv_path = processed_dir/'processed_resumes.csv'
    
    resumes = load_resumes(json_path)
    print(f"Loaded {len(resumes)} resumes successfully.")

    # Extract features
    df_features = extract_features(resumes)
    
    # Save to a CSV
    
    save_features(df_features, csv_path)
    print("Saved resume csv to {csv_path}")
    
