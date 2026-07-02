# AI Recruitment System: Approach and Architecture

## 1. The Problem
Recruiters often miss top talent because traditional keyword filters are too rigid. They lack the ability to understand context, career trajectory, and behavioral signals.

## 2. Our Solution: Hybrid Intelligence Ranking
We built a system that combines **Semantic Search** (for broad, context-aware filtering) and **LLM-based Reasoning** (for deep, recruiter-like evaluation).

### Architecture Overview
The system operates in a two-stage pipeline:

#### Stage 1: Coarse Ranking (Semantic Search)
- **Embedding Generation:** We use `sentence-transformers` (`all-MiniLM-L6-v2`) to convert both job descriptions and candidate profiles into high-dimensional vectors.
- **Vector Space Matching:** Instead of keyword matching, we calculate the **Cosine Similarity** between the job vector and candidate vectors.
- **Goal:** Efficiently narrow down hundreds of candidates to a top-N shortlist based on conceptual similarity.

#### Stage 2: Fine-Grained Ranking (LLM Reasoner)
- **Contextual Analysis:** The top candidates from Stage 1 are passed to an LLM.
- **Deep Evaluation:** The LLM doesn't just check for skills; it analyzes:
    - **Career Progression:** Is the candidate's growth trajectory aligned with the role?
    - **Platform Activity:** Does their open-source or blogging activity indicate genuine passion and expertise?
    - **Behavioral Signals:** Do they exhibit leadership, mentorship, or strategic thinking?
- **Scoring & Justification:** The LLM assigns a final score and, crucially, provides a **justification** for why the candidate is a fit.

## 3. Key Technical Choices
- **S-BERT:** Chosen for its balance of speed and accuracy in semantic similarity tasks.
- **Hybrid Scoring:** Combining quantitative similarity (vectors) with qualitative reasoning (LLM) ensures both efficiency and depth.
- **Data Model:** Designed to capture "soft signals" (activity, behavioral traits) alongside "hard skills".

## 4. Workflow
`Data Loading` $\rightarrow$ `Vector Embedding` $\rightarrow$ `Cosine Similarity` $\rightarrow$ `LLM Re-ranking` $\rightarrow$ `Ranked Shortlist`
