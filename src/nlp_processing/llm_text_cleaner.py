import requests
import openai
import os
from dotenv import load_dotenv

def clean_resume_text_with_huggingface(resume_text):
    
    prompt = f"""
    You are a helpful assistant. Summarize the following resume, focusing on:

    - Key technical and professional skills
    - Education (degrees and institutions)
    - Work experience (roles, companies, durations)

    Return a clean, readable plain text summary with no formatting or extra commentary.

    Resume:
    \"\"\"
    {resume_text}
    \"\"\"
    """
    


    
    with open("/home/smitra16/resume-screener-ai/src/nlp_processing/hf_token.txt", "r") as f: hf_token = f.read().strip()


    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

    headers = {
        "Authorization": f"Bearer {hf_token}"
    }

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        raise RuntimeError(f"Hugging Face API error: {response.status_code} - {response.text}")



def clean_resume_text_with_openai(resume_text):
    
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    openai.api_key = openai_api_key

    prompt = f"""
    You are an assistant tasked with extracting detailed, structured information from a resume.

    Parse the following resume text and extract the following:

    1. **Skills** — List each individual tool, technology, or domain mentioned under any skill heading. Include:
    - Programming languages
    - Libraries and frameworks
    - ML techniques (e.g., GNNs, CNNs, diffusion models)
    - Deployment tools, visualization libraries, data processing tools

    Do NOT just list high-level categories like "Programming". Parse all details after colons.

    2. **Education** — Include all degrees and institutions mentioned.

    3. **Experience** — For each job:
    - Include the title, employer, and time range (if available)
    - Write a concise 1–2 sentence summary of what the candidate actually did
    - Emphasize technical responsibilities, tools used, research/work impact, or team contributions
    - **Do not copy or reformat bullet points**. Instead, rewrite in clean, natural English.

    ---

    Example:

    Skills:
    Python, PyTorch, TensorFlow, Scikit-learn, Docker, GitHub Actions, Databricks, CUDA, CNNs, GNNs, VAEs, diffusion models, Hugging Face Transformers, pandas, matplotlib, seaborn

    Education:
    M.S. in Computer Science, Stanford University

    Experience:
    - Machine Learning Engineer, Acme Corp (2021–2022): Built and deployed deep learning models for document classification. Led model optimization and collaborated with engineers to improve accuracy and latency in production pipelines.

    ---

    Now follow the same format for the resume below.

    Return the output in this exact structure:

    Skills:
    <list>

    Education:
    <list>

    Experience:
    - Title, Org (Years): Summary

    Resume:
    \"\"\"
    {resume_text}
    \"\"\"
    """

    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that extracts structured resume content."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
    )

    return response["choices"][0]["message"]["content"].strip()
