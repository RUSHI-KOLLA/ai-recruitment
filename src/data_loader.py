import pandas as pd
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Candidate:
    candidate_id: str
    name: str
    experience: str
    skills: List[str]
    education: str
    platform_activity: Optional[str] = None
    behavioral_signals: Optional[str] = None
    
    def to_text(self) -> str:
        return f"Name: {self.name}\nExperience: {self.experience}\nSkills: {', '.join(self.skills)}\nEducation: {self.education}\nActivity: {self.platform_activity}\nSignals: {self.behavioral_signals}"

@dataclass
class JobDescription:
    job_id: str
    title: str
    description: str
    required_skills: List[str]
    preferred_experience: str

class DataLoader:
    def load_candidates(self, file_path: str) -> List[Candidate]:
        df = pd.read_csv(file_path)
        candidates = []
        for _, row in df.iterrows():
            # Assuming skills are comma-separated in the CSV
            skills = row['skills'].split(',') if isinstance(row['skills'], str) else []
            candidates.append(Candidate(
                candidate_id=str(row['candidate_id']),
                name=row['name'],
                experience=row['experience'],
                skills=[s.strip() for s in skills],
                education=row['education'],
                platform_activity=row.get('platform_activity', ''),
                behavioral_signals=row.get('behavioral_signals', '')
            ))
        return candidates

    def load_job(self, file_path: str) -> JobDescription:
        df = pd.read_csv(file_path)
        row = df.iloc[0]
        skills = row['required_skills'].split(',') if isinstance(row['required_skills'], str) else []
        return JobDescription(
            job_id=str(row['job_id']),
            title=row['title'],
            description=row['description'],
            required_skills=[s.strip() for s in skills],
            preferred_experience=row['preferred_experience']
        )

    def create_sample_data(self, candidates_path: str, job_path: str):
        candidates_df = pd.DataFrame([
            {
                "candidate_id": "C1",
                "name": "Alice Smith",
                "experience": "5 years as a Backend Engineer at TechCorp. Expert in Python, FastAPI, and AWS.",
                "skills": "Python,FastAPI,AWS,PostgreSQL,Docker",
                "education": "BS in Computer Science",
                "platform_activity": "Active contributor to several open source Python libraries.",
                "behavioral_signals": "Strong leadership qualities, mentored 3 junior developers."
            },
            {
                "candidate_id": "C2",
                "name": "Bob Jones",
                "experience": "2 years as a Junior Developer. Familiar with Java and Spring Boot.",
                "skills": "Java,Spring Boot,MySQL",
                "education": "BS in IT",
                "platform_activity": "Occasional blogger on tech trends.",
                "behavioral_signals": "Quick learner, eager to take on new challenges."
            },
            {
                "candidate_id": "C3",
                "name": "Charlie Brown",
                "experience": "8 years as a Senior Software Architect. Deep knowledge of distributed systems and Go.",
                "skills": "Go,Kubernetes,Distributed Systems,gRPC,Redis",
                "education": "MS in Computer Science",
                "platform_activity": "Maintainer of a popular Go networking library.",
                "behavioral_signals": "Strategic thinker, excellent at system design."
            }
        ])
        candidates_df.to_csv(candidates_path, index=False)
        
        job_df = pd.DataFrame([
            {
                "job_id": "J1",
                "title": "Senior Backend Engineer",
                "description": "We are looking for a Senior Backend Engineer with strong experience in Python and cloud infrastructure. You will design scalable APIs and manage AWS deployments.",
                "required_skills": "Python,AWS,API Design",
                "preferred_experience": "5+ years of professional experience"
            }
        ])
        job_df.to_csv(job_path, index=False)
