from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resumes = db.relationship('Resume', backref='user', lazy=True)

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Personal Information
    full_name = db.Column(db.String(100))
    professional_title = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(200))
    portfolio = db.Column(db.String(200))
    profile_image = db.Column(db.String(200))
    
    # Professional Details
    job_role = db.Column(db.String(100))
    experience_level = db.Column(db.String(20))  # fresher/experienced
    resume_tone = db.Column(db.String(20))  # professional/technical/modern
    
    # AI Generated Content
    career_objective = db.Column(db.Text)
    skills_suggestions = db.Column(db.Text)
    experience_summary = db.Column(db.Text)
    
    # Education
    education = db.Column(db.Text)  # JSON string
    
    # Experience (for experienced)
    experience = db.Column(db.Text)  # JSON string
    
    # Projects
    projects = db.Column(db.Text)  # JSON string
    
    # Skills
    technical_skills = db.Column(db.Text)  # JSON string
    soft_skills = db.Column(db.Text)  # JSON string
    tools = db.Column(db.Text)  # JSON string
    
    # Additional Sections
    certifications = db.Column(db.Text)  # JSON string
    achievements = db.Column(db.Text)  # JSON string
    languages = db.Column(db.Text)  # JSON string
    publications = db.Column(db.Text)  # JSON string
    
    # ATS Score
    ats_score = db.Column(db.Float, default=0.0)
    ats_feedback = db.Column(db.Text)
    
    # Template Selection
    template_id = db.Column(db.Integer, default=1)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OTPVerification(db.Model):
    __tablename__ = 'otp_verification'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    otp = db.Column(db.String(6))
    purpose = db.Column(db.String(20))  # email_verification, phone_verification
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)