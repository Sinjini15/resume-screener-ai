# utils/pdf_extractor_utils.py

import pdfplumber
import spacy
import re
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n"
    return extracted_text


def split_into_sections(text):
    sections = {
        "skills": "",
        "education": "",
        "experience": ""
    }
    current_section = None
    lines = text.split("\n")

    for line in lines:
        line_lower = line.strip().lower()

        if "skill" in line_lower:
            current_section = "skills"
            continue
        if "education" in line_lower:
            current_section = "education"
            continue
        if "experience" in line_lower or "professional experience" in line_lower:
            current_section = "experience"
            continue

        if current_section:
            sections[current_section] += line + " "

    return sections

# Load pretrained NER model
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
nlp_ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


def extract_entities(text):
    entities = nlp_ner(text)
    return [ent['word'] for ent in entities if ent['entity_group'] in ['ORG', 'MISC', 'PER']]

def parse_resume_nlp(pdf_path):
    full_text = extract_text_from_pdf(pdf_path)
    sections = split_into_sections(full_text)

    parsed_resume = {
        "skills": [],
        "education": [],
        "experience": []
    }

    if sections["skills"]:
        parsed_resume["skills"] = extract_entities(sections["skills"])

    if sections["education"]:
        parsed_resume["education"] = extract_entities(sections["education"])

    if sections["experience"]:
        parsed_resume["experience"] = extract_entities(sections["experience"])

    return parsed_resume
