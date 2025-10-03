# matcher.py
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import extract_skills_from_text

# TF-IDF vectorizer (use unigrams and bigrams)
vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)

# --- Helper functions ---

def clean_text(text):
    """Lowercase, remove extra spaces and special chars for better similarity"""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # collapse whitespace
    text = re.sub(r'[^a-z0-9\s\+\-]', '', text)  # remove special chars except +, -
    return text.strip()

def tfidf_similarity(a, b):
    """Compute TF-IDF cosine similarity between two texts"""
    if not a.strip() or not b.strip():
        return 0.0
    a_clean = clean_text(a)
    b_clean = clean_text(b)
    X = vectorizer.fit_transform([a_clean, b_clean])
    return float(cosine_similarity(X[0], X[1])[0][0])

def compute_final_score(text_sim, skill_cov, w_text=0.6, w_skill=0.4):
    """Weighted final score based on text similarity and skill coverage"""
    return round((w_text * text_sim + w_skill * skill_cov) * 100, 1)

def ats_score(resume_text, jd_skills):
    """Simple ATS-friendliness score: fraction of JD skills found in resume"""
    if not jd_skills or not resume_text.strip():
        return 100.0
    resume_text_lower = resume_text.lower()
    matched = sum(1 for s in jd_skills if s.lower() in resume_text_lower)
    return round((matched / len(jd_skills)) * 100, 1)

# --- Main match function ---

def match(resume_text, jd_text, resume_skills, jd_skills):
    """
    Returns a dictionary with matching details between resume and JD.
    """
    # Text similarity
    text_sim = tfidf_similarity(resume_text, jd_text)

    # Skill coverage and matched/missing skills
    resume_skills_set = set([s.lower() for s in resume_skills])
    jd_skills_set = set([s.lower() for s in jd_skills])
    matched_skills = sorted(list(resume_skills_set & jd_skills_set))
    missing_skills = sorted(list(jd_skills_set - resume_skills_set))
    skill_cov = (len(matched_skills) / len(jd_skills_set)) if jd_skills_set else 0.0

    # Weighted final score
    final_score = compute_final_score(text_sim, skill_cov)

    # ATS-friendly score
    ats = ats_score(resume_text, jd_skills)

    return {
        "match_score": final_score,
        "text_similarity": round(text_sim * 100, 1),
        "skill_coverage": round(skill_cov * 100, 1),
        "ats_score": ats,
        "matched_skills": matched_skills if matched_skills else None,
        "missing_skills": missing_skills if missing_skills else None
    }

def get_jd_keywords(jd_text):
    """Return list of skills/keywords from JD text"""
    return extract_skills_from_text(jd_text)
