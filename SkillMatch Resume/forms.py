from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

# ---------------- Dashboard Form ----------------
class DashboardForm(FlaskForm):
    resume_file = FileField("Upload Resume")
    resume_text = TextAreaField("Paste Resume Text")
    job_text = TextAreaField("Job Description", validators=[DataRequired()])
    use_sbert = BooleanField("Use semantic model (SBERT)")
    submit = SubmitField("Match")


# ---------------- Registration Form ----------------
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[Optional(), Length(min=7, max=15)])
    country = SelectField("Country", choices=[
        ("India", "India"), ("USA", "USA"), ("UK", "UK"), ("Other", "Other")
    ])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    agree_terms = BooleanField("I agree to the Terms and Conditions", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


# ---------------- Login Form ----------------
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
