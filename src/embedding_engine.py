from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List
from .data_loader import Candidate, JobDescription

class EmbeddingEngine:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self.use_dl = True
        except ImportError:
            print("SentenceTransformers not found. Falling back to TF-IDF.")
            self.use_dl = False

    def get_embedding(self, text: str):
        if self.use_dl:
            return self.model.encode([text])[0]
        else:
            # TF-IDF doesn't provide a single embedding for a single text easily
            # without a corpus. We'll handle TF-IDF in rank_by_semantic_similarity.
            return None

    def rank_by_semantic_similarity(self, job: JobDescription, candidates: List[Candidate]) -> List[tuple]:
        job_text = f"{job.title}: {job.description} Required skills: {', '.join(job.required_skills)}"
        
        if self.use_dl:
            job_embedding = self.get_embedding(job_text)
            candidate_texts = [c.to_text() for c in candidates]
            candidate_embeddings = self.model.encode(candidate_texts)
            similarities = cosine_similarity([job_embedding], candidate_embeddings)[0]
        else:
            # TF-IDF Fallback
            candidate_texts = [c.to_text() for c in candidates]
            all_texts = [job_text] + candidate_texts
            vectorizer = TfidfVectorizer().fit_transform(all_texts)
            vectors = vectorizer.toarray()
            job_vector = vectors[0].reshape(1, -1)
            candidate_vectors = vectors[1:]
            similarities = cosine_similarity(job_vector, candidate_vectors)[0]
        
        ranked = []
        for idx, sim in enumerate(similarities):
            ranked.append((candidates[idx], sim))
            
        return sorted(ranked, key=lambda x: x[1], reverse=True)
