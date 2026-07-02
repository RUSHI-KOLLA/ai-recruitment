import pandas as pd
from src.pipeline import RecruitmentPipeline
from src.data_loader import DataLoader
import os

def main():
    # Paths
    candidates_csv = "candidates.csv"
    job_csv = "job_description.csv"
    output_csv = "ranked_candidates.csv"
    
    # Create sample data if not exists
    loader = DataLoader()
    loader.create_sample_data(candidates_csv, job_csv)
    print(f"Sample data created at {candidates_csv} and {job_csv}")
    
    # Run pipeline
    pipeline = RecruitmentPipeline()
    print("Ranking candidates...")
    results = pipeline.run(candidates_csv, job_csv)
    
    # Format output
    output_data = []
    for candidate, score, justification in results:
        output_data.append({
            "Candidate ID": candidate.candidate_id,
            "Name": candidate.name,
            "Score": f"{score:.2f}",
            "Justification": justification
        })
        
    df_output = pd.DataFrame(output_data)
    df_output.to_csv(output_csv, index=False)
    print(f"Ranked output saved to {output_csv}")
    print("\nTop Candidates:")
    print(df_output.head())

if __name__ == "__main__":
    main()
