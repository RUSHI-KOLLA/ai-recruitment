from .data_loader import DataLoader, Candidate, JobDescription
from .embedding_engine import EmbeddingEngine
from .ranker import LLMRanker
from typing import List, Tuple

class RecruitmentPipeline:
    def __init__(self, api_key: str = None):
        self.loader = DataLoader()
        self.embedding_engine = EmbeddingEngine()
        self.ranker = LLMRanker(api_key=api_key)

    def run(self, candidates_path: str, job_path: str) -> List[Tuple[Candidate, float, str]]:
        # 1. Load data
        candidates = self.loader.load_candidates(candidates_path)
        job = self.loader.load_job(job_path)
        
        # 2. Coarse ranking using semantic search
        semantic_ranked = self.embedding_engine.rank_by_semantic_similarity(job, candidates)
        
        # Take top N for fine-grained LLM ranking (e.g., top 10)
        top_candidates = [c for c, sim in semantic_ranked[:10]]
        
        # 3. Fine-grained ranking using LLM
        final_ranked = self.ranker.rank_candidates(job, top_candidates)
        
        return final_ranked
