# utils.py
from fpdf import FPDF
import os
import re

def create_updated_resume_pdf(original_text, matched_skills, jd_keywords, filename):
    """
    Create a new PDF resume including original text, matched skills, and JD keywords.
    Supports Unicode characters.
    """
    pdf = FPDF()
    pdf.add_page()

    # Absolute path to font file (relative to this utils.py file)
    # Absolute path to font file (relative to this utils.py file)
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'dejavu-sans', 'DejaVuSans.ttf')
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"TTF Font file not found: {font_path}")

    # Add and set font
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Title
    pdf.cell(0, 10, "Updated Resume", ln=True, align='C')
    pdf.ln(10)

    # Original resume text
    pdf.multi_cell(0, 8, "Original Resume:\n" + original_text)
    pdf.ln(10)

    # Matched skills from JD
    pdf.multi_cell(0, 8, "Matched Keywords (from JD):\n" + ", ".join(matched_skills))
    pdf.ln(10)

    # All JD keywords suggested
    pdf.multi_cell(0, 8, "Suggested Keywords to Include:\n" + ", ".join(jd_keywords))
    
    # Output PDF
    pdf.output(filename)
    return filename

def extract_skills_from_text(text):
    skills_db = [
        "python", "java", "c++", "javascript", "html", "css", "sql",
        "flask", "fastapi", "machine learning", "deep learning",
        "pytorch", "tensorflow", "excel", "git", "github", "nlp", "pandas",
        "numpy", "keras", "scikit-learn", "react", "docker", "linux"
    ]
    text_lower = text.lower()
    # Split text into words, handle punctuation
    text_words = set(re.findall(r'\b\w[\w\+\-]*\b', text_lower))
    # Only include skills present in the text
    found_skills = [skill for skill in skills_db if skill.lower() in text_words]
    return found_skills
