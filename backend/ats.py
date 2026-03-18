from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_ats_score(resume_text, job_desc):
    documents = [resume_text, job_desc]

    tfidf = TfidfVectorizer(stop_words='english')
    matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

    score = round(similarity * 100, 2)

    # Extract keywords
    feature_names = tfidf.get_feature_names_out()
    resume_words = set(resume_text.lower().split())
    job_words = set(job_desc.lower().split())

    matched = list(resume_words.intersection(job_words))
    missing = list(job_words - resume_words)

    return score, matched[:10], missing[:10]