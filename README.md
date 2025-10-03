# 📄 SkillMatch Resume

A Flask-based web application that helps job seekers match their resumes with job descriptions, calculates an ATS (Applicant Tracking System) score, and provides skill gap analysis. The platform also allows users to register, log in, upload resumes, and give feedback.

---
## 📌 Table of Contents
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Proposed Solution](#proposed-solution)
- [Architecture](#architecture)
- [Tech Stack Used](#tech-stack-used)
- [Installation Steps](#installation-steps)
- [How to Run](#how-to-run)
- [Features](#features)
- [Sample Use-Case](#sample-use-case)
- [Future Scope](#future-scope)
- [Acknowledgements](#acknowledgements)

---
## 🛑 Problem Statement

In today’s competitive job market, candidates often fail to pass ATS systems because their resumes don’t align well with the job description. Recruiters, on the other hand, spend a lot of time manually filtering resumes. There’s a need for an intelligent system that:

Analyzes resumes,

Matches them with job descriptions,

Calculates ATS scores, and

Suggests improvements.

---

## 🎯 Objectives

- Allow job seekers to upload resumes or paste resume text.

- Extract skills from resumes and job descriptions.

- Calculate a match score (ATS score).

- Provide an updated resume highlighting missing skills.

- Allow users to register, log in, and manage their resumes.

- Enable feedback submission for continuous improvement.

---

## ✅ Proposed Solution

- Preprocess uploaded resumes (PDF/TXT/DOCX).

- Extract skills from resumes and job descriptions using text processing.

- Match both sets of skills to generate an ATS score.

- Provide feedback on missing skills and generate an updated resume.

- Implement user authentication (Register/Login).

- Store user resumes in a database for future use.

---

## 🏗 Architecture

1.Frontend (UI): HTML, CSS, Bootstrap for a clean interface.

2.Backend (Flask): Handles authentication, resume parsing, skill extraction, and score calculation.

3.Database (SQLite/MySQL): Stores user credentials, resumes, and feedback.

4.Resume Parser: Extracts text from uploaded resumes.

5.Skill Extractor: Identifies relevant skills from text.

6.Match Engine: Compares resume skills with job description skills to calculate ATS score.

---

## 🛠 Tech Stack Used
| Component       | Technology               |
|---------------- |---------------------------|
|Programming	    |  Python                   |
|Backend Framework|	Flask                     |
|Database        	|SQLite / SQLAlchemy ORM      |
|Frontend        	|HTML, CSS, Bootstrap          |
|File Handling	  |PyPDF2 / docx / Text extraction|
|Authentication	 |Flask-Login                  |
|Environment	   |Virtualenv (optional)          |

---

## ⚙️ Installation Steps

1.Clone the repository
```bash
git clone https://github.com/Mahalakshmi100/SkillMatch-Resume.git
cd SkillMatch-Resume
```

2.Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Linux/Mac
```

3.Install required dependencies
```bash
pip install -r requirements.txt

```
4.Set up database (if needed)
```bash
flask db init
flask db migrate
flask db upgrade
```
## ▶️ How to Run
### Flask API:
```bash
python app.py

```

---

## 🌟 Features

- User Registration & Login (Flask-Login authentication).

- Upload Resume (PDF/DOCX/TXT) or paste resume text.

- Skill Extraction from resumes and job descriptions.

- ATS Score Calculation based on skill matching.

- Updated Resume PDF generation with highlighted skills.

- Feedback Module where users can submit their experience.

- Secure storage of resumes and user details in DB.

---
## 🔍 Sample Use-Case

**Step 1:** User registers and logs in.

**Step 2:** Uploads resume or pastes resume text.

**Step 3:** Pastes job description.

**Step 4:** System extracts skills from both documents.

**Step 5:** ATS Score is displayed with missing skills.

**Step 6:** User downloads an updated resume with improvements.

**Step 7:** User submits feedback.

---

## 🚀 Future Scope

- Integrate AI-powered resume scoring using NLP models.

- Suggest course recommendations for missing skills.

- Employer module to post jobs and view candidate matches.

- Deploy on cloud (Heroku/AWS) for global accessibility.

- Provide email notifications with resume reports.

---

## 🙏 Acknowledgements

**Flask Documentation**

**SQLAlchemy ORM**

**PyPDF2 & python-docx libraries**

**Bootstrap for frontend design**

**Open-source community**
