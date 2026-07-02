import openai
from typing import List, Tuple
from .data_loader import Candidate, JobDescription

class LLMRanker:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key

    def rank_candidates(self, job: JobDescription, candidates: List[Candidate]) -> List[Tuple[Candidate, float, str]]:
        # In a real scenario, we would call the LLM API.
        # Here we simulate the LLM's reasoning process.
        
        results = []
        for candidate in candidates:
            score, justification = self._simulate_llm_scoring(job, candidate)
            results.append((candidate, score, justification))
            
        return sorted(results, key=lambda x: x[1], reverse=True)

    def _simulate_llm_scoring(self, job: JobDescription, candidate: Candidate) -> Tuple[float, str]:
        # This is a mock of what an LLM would do: 
        # analyze the mapping between job requirements and candidate profile.
        
        score = 0.0
        justification = []
        
        # Check required skills
        matched_skills = [s for s in job.required_skills if any(rs in candidate.skills for rs in [s])]
        score += (len(matched_skills) / len(job.required_skills)) * 0.5
        if matched_skills:
            justification.append(f"Matched skills: {', '.join(matched_skills)}")
        
        # Check experience (simple heuristic for mock)
        if "Senior" in job.title and "Senior" in candidate.experience:
            score += 0.3
            justification.append("Matches seniority level")
        elif "Junior" in job.title and "Junior" in candidate.experience:
            score += 0.3
            justification.append("Matches seniority level")
        
        # Behavioral signals and activity
        if candidate.platform_activity and ("contributor" in candidate.platform_activity.lower() or "maintainer" in candidate.platform_activity.lower()):
            score += 0.2
            justification.append("Strong platform activity")
            
        if candidate.behavioral_signals and ("leadership" in candidate.behavioral_signals.lower() or "strategic" in candidate.behavioral_signals.lower()):
            score += 0.1
            justification.append("Positive behavioral signals")
            
        score = min(score, 1.0)
        return score, "; ".join(justification)
