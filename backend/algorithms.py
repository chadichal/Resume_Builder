import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class ResumeMatchingAlgorithm:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
    def tfidf_keyword_matching(self, resume_text, job_description):
        """TF-IDF based keyword matching algorithm"""
        documents = [resume_text, job_description]
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Extract important keywords
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        resume_keywords = tfidf_matrix[0].toarray()[0]
        job_keywords = tfidf_matrix[1].toarray()[0]
        
        # Get top keywords
        top_resume_indices = resume_keywords.argsort()[-10:][::-1]
        top_job_indices = job_keywords.argsort()[-10:][::-1]
        
        top_resume_keywords = [feature_names[i] for i in top_resume_indices]
        top_job_keywords = [feature_names[i] for i in top_job_indices]
        
        return {
            'similarity_score': similarity,
            'resume_keywords': top_resume_keywords,
            'job_keywords': top_job_keywords
        }
    
    def experience_level_matcher(self, resume_years, required_years):
        """Match experience level with fuzzy logic"""
        if resume_years < required_years * 0.7:
            return 0.5  # Underqualified
        elif resume_years >= required_years * 0.7 and resume_years <= required_years * 1.3:
            return 1.0  # Well matched
        else:
            return 0.8  # Overqualified
    
    def skill_gap_analysis(self, resume_skills, required_skills):
        """Analyze skill gaps between resume and job requirements"""
        resume_skills_set = set(s.lower() for s in resume_skills)
        required_skills_set = set(s.lower() for s in required_skills)
        
        matching_skills = resume_skills_set.intersection(required_skills_set)
        missing_skills = required_skills_set - resume_skills_set
        extra_skills = resume_skills_set - required_skills_set
        
        match_percentage = (len(matching_skills) / len(required_skills_set)) * 100 if required_skills_set else 0
        
        return {
            'match_percentage': match_percentage,
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'extra_skills': list(extra_skills)
        }

class NLPSentenceProcessor:
    def __init__(self):
        self.sentence_patterns = {
            'action_verbs': ['developed', 'implemented', 'managed', 'created', 'designed', 'led', 'achieved'],
            'quantifiable': re.compile(r'\b\d+%|\d+\+|\d+\s+(years?|months?|projects?)\b', re.IGNORECASE)
        }
    
    def extract_action_verbs(self, text):
        """Extract action verbs from text"""
        words = text.split()
        return [word for word in words if word.lower() in self.sentence_patterns['action_verbs']]
    
    def extract_quantifiable_achievements(self, text):
        """Extract quantifiable achievements from text"""
        return self.sentence_patterns['quantifiable'].findall(text)
    
    def score_sentence_quality(self, text):
        """Score the quality of achievement sentences"""
        score = 0
        if self.extract_action_verbs(text):
            score += 0.5
        if self.extract_quantifiable_achievements(text):
            score += 0.5
        return min(1.0, score)