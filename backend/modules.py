from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re

class AIContentGenerator:
    def __init__(self):
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        # Use a smaller model for text generation
        self.generator = pipeline('text2text-generation', 
                                 model='google/flan-t5-small')
        
    def generate_career_objective(self, name, job_role, experience_level, skills):
        """Generate career objective based on user input"""
        prompt = f"Write a professional career objective for {name} applying for {job_role} position. Experience level: {experience_level}. Skills: {skills}. Keep it concise and professional."
        
        try:
            result = self.generator(prompt, max_length=100, num_return_sequences=1)
            return result[0]['generated_text']
        except:
            return f"Experienced professional seeking {job_role} position to leverage expertise and contribute to organizational success."
    
    def enhance_skills(self, job_role, current_skills):
        """Suggest additional skills based on job role"""
        skill_prompts = {
            'software engineer': ['Python', 'Java', 'SQL', 'Git', 'Docker', 'AWS'],
            'data scientist': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics', 'TensorFlow'],
            'web developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'MongoDB'],
            'project manager': ['Agile', 'Scrum', 'JIRA', 'Risk Management', 'Stakeholder Management']
        }
        
        default_skills = ['Communication', 'Problem Solving', 'Team Collaboration', 'Time Management']
        
        for key in skill_prompts:
            if key in job_role.lower():
                suggested = list(set(skill_prompts[key] + current_skills))
                return suggested[:10]
        
        return list(set(default_skills + current_skills))[:10]
    
    def enhance_project_description(self, project_title, description, technologies):
        """Rewrite project description with professional language"""
        prompt = f"Rewrite this project description professionally. Project: {project_title}. Description: {description}. Technologies: {technologies}"
        
        try:
            result = self.generator(prompt, max_length=150, num_return_sequences=1)
            return result[0]['generated_text']
        except:
            return f"Developed {project_title} using {technologies}. {description}"
    
    def generate_experience_summary(self, company, role, duration, achievements):
        """Generate professional experience summary"""
        prompt = f"Write a professional experience summary for {role} at {company} for {duration}. Achievements: {achievements}"
        
        try:
            result = self.generator(prompt, max_length=150, num_return_sequences=1)
            return result[0]['generated_text']
        except:
            return f"Served as {role} at {company} for {duration}, achieving {achievements}"

class ATSScorer:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def extract_keywords(self, job_description):
        """Extract important keywords from job description using TF-IDF"""
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([job_description])
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # Get top keywords by TF-IDF score
            scores = tfidf_matrix.toarray()[0]
            top_indices = scores.argsort()[-20:][::-1]
            
            keywords = [feature_names[i] for i in top_indices if scores[i] > 0.1]
            return keywords
        except:
            # Fallback keyword extraction
            words = re.findall(r'\w+', job_description.lower())
            return list(set(words))[:20]
    
    def calculate_ats_score(self, resume_text, job_description):
        """Calculate ATS compatibility score"""
        score_components = {}
        
        # Keyword match score (40%)
        keywords = self.extract_keywords(job_description)
        matched_keywords = [k for k in keywords if k.lower() in resume_text.lower()]
        keyword_score = (len(matched_keywords) / len(keywords)) * 40 if keywords else 30
        score_components['keyword_match'] = keyword_score
        
        # Content relevance using cosine similarity (30%)
        try:
            resume_embedding = self.sentence_model.encode([resume_text])
            job_embedding = self.sentence_model.encode([job_description])
            similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
            relevance_score = similarity * 30
        except:
            relevance_score = 20
        score_components['relevance'] = relevance_score
        
        # Format compliance score (20%)
        format_score = self.check_format_compliance(resume_text) * 20
        score_components['format'] = format_score
        
        # Section completeness (10%)
        completeness_score = self.check_section_completeness(resume_text) * 10
        score_components['completeness'] = completeness_score
        
        total_score = sum(score_components.values())
        
        feedback = self.generate_feedback(score_components, matched_keywords)
        
        return total_score, feedback, score_components
    
    def check_format_compliance(self, resume_text):
        """Check if resume follows ATS-friendly format"""
        score = 1.0
        
        # Check for tables (bad for ATS)
        if re.search(r'<table|\\begin{tabular}', resume_text, re.IGNORECASE):
            score -= 0.2
        
        # Check for images (bad for ATS)
        if re.search(r'<img|\\includegraphics', resume_text, re.IGNORECASE):
            score -= 0.2
        
        # Check for proper headings
        required_headings = ['education', 'experience', 'skills']
        for heading in required_headings:
            if not re.search(rf'\b{heading}\b', resume_text, re.IGNORECASE):
                score -= 0.1
        
        return max(0.5, score)
    
    def check_section_completeness(self, resume_text):
        """Check if all required sections are present"""
        required_sections = ['education', 'skills']
        optional_sections = ['experience', 'projects', 'certifications']
        
        present_required = sum(1 for section in required_sections 
                              if re.search(rf'\b{section}\b', resume_text, re.IGNORECASE))
        present_optional = sum(1 for section in optional_sections 
                              if re.search(rf'\b{section}\b', resume_text, re.IGNORECASE))
        
        score = (present_required / len(required_sections)) * 0.6 + \
                (present_optional / len(optional_sections)) * 0.4
        
        return score
    
    def generate_feedback(self, score_components, matched_keywords):
        """Generate ATS feedback based on scores"""
        feedback = []
        
        if score_components['keyword_match'] < 30:
            feedback.append("Keyword optimization needed. Try adding more industry-specific terms.")
        
        if score_components['relevance'] < 20:
            feedback.append("Resume content could be more relevant to the job description.")
        
        if score_components['format'] < 15:
            feedback.append("Consider using simpler formatting for better ATS parsing.")
        
        if score_components['completeness'] < 8:
            feedback.append("Add missing sections to improve completeness.")
        
        feedback.append(f"Matched keywords: {', '.join(matched_keywords[:10])}")
        
        return " | ".join(feedback)