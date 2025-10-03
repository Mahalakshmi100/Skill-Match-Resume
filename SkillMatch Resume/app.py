import os
import secrets
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user, current_user
)
from forms import DashboardForm
from utils import create_updated_resume_pdf, extract_skills_from_text
from matcher import match as match_resume, extract_skills_from_text as matcher_extract_skills

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


# --- Config ---
app = Flask(__name__)
app.config["SECRET_KEY"] = "replace_this_with_a_random_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["UPLOAD_FOLDER"] = os.path.join("data", "resumes")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

ALLOWED_EXT = {"pdf", "docx", "txt"}


# --- Models ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    country = db.Column(db.String(50))
    password = db.Column(db.String(200), nullable=False)
    agree_terms = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Forms ---
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=1, max=50)])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired(), Length(min=6, max=20)])
    country = SelectField("Country", choices=[('India', 'India'), ('USA', 'USA'), ('Other', 'Other')], validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    agree_terms = BooleanField("I agree to the Terms & Conditions", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")



# --- Helpers ---
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# --- Routes ---
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check for existing username/email
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists. Please choose another.", "warning")
            return redirect(url_for("register"))
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("login"))

        # Hash password and create user
        hashed = generate_password_hash(form.password.data)
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data.lower(),
            phone=form.phone.data,
            country=form.country.data,
            password=hashed,
            agree_terms=form.agree_terms.data
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration completed successfully! Please login.", "success")
        return redirect(url_for("login"))  # Redirect to login page
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))  # Redirect to resume upload page
        flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)




@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = DashboardForm()
    result = None
    updated_resume_url = None  # URL for downloading updated resume
    resume_text = ""

    if request.method == "POST":
        # Get resume text from form or uploaded file
        resume_text = form.resume_text.data.strip() if form.resume_text.data else request.form.get("resume_text", "").strip()
        jd_text = form.job_text.data.strip() if form.job_text.data else request.form.get("job_text", "").strip()

        # Handle uploaded file
        f = form.resume_file.data if hasattr(form.resume_file, 'data') else request.files.get("resume_file")
        if f and getattr(f, "filename", None) and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            f.save(path)
            from extractor import extract_text_from_file
            resume_text = extract_text_from_file(path)
            os.remove(path)

        if not resume_text or not jd_text:
            flash("Please provide resume text (or upload file) and job description.", "warning")
            return render_template("dashboard.html", form=form, result=None, updated_resume_url=None)

        # Extract skills
        resume_skills = extract_skills_from_text(resume_text)
        jd_skills = extract_skills_from_text(jd_text)

        # Match
        try:
            result = match_resume(resume_text, jd_text, resume_skills, jd_skills)

            # Create updated PDF
            updated_resume_filename = f"updated_{secrets.token_hex(6)}.pdf"
            updated_resume_path = os.path.join(app.config["UPLOAD_FOLDER"], updated_resume_filename)
            create_updated_resume_pdf(resume_text, result['matched_skills'], jd_skills, updated_resume_path)

            # Provide URL for download
            updated_resume_url = url_for('download_file', filename=updated_resume_filename)

        except Exception as e:
            flash(f"Error during matching: {e}", "danger")
            result = None
            updated_resume_url = None

    return render_template("dashboard.html", form=form, result=result, updated_resume_url=updated_resume_url, resume_text=resume_text)


# Route for downloading updated resume
@app.route('/uploads/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route("/feedback", methods=["POST"])
@login_required
def feedback():
    rating = request.form.get("rating")
    comments = request.form.get("comments")
    # Save feedback to DB or file
    print(f"Feedback received: Rating={rating}, Comments={comments}")
    flash("Thank you for your feedback!", "success")
    return redirect(url_for("dashboard"))


# --- Run App ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)