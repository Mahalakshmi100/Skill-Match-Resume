# extractor.py
import re
from pdfminer.high_level import extract_text as pdf_extract
import docx
import os

# Load skills list
SKILLS_FILE = os.path.join("data", "skills_seed.txt")
with open(SKILLS_FILE, encoding="utf8") as f:
    SKILLS = [s.strip().lower() for s in f if s.strip()]

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_from_pdf(path):
    return pdf_extract(path)

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_file(path):
    path = path.lower()
    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.endswith(".docx") or path.endswith(".doc"):
        return extract_text_from_docx(path)
    elif path.endswith(".txt"):
        with open(path, encoding="utf8") as f: return f.read()
    else:
        raise ValueError("Unsupported file type")

def extract_skills_from_text(text):
    text_l = text.lower()
    found = set()
    for skill in SKILLS:
        if skill in text_l:
            found.add(skill)
    return sorted(found)
