# AI Recruit — Hybrid Intelligence Candidate Ranking System

AI Recruit is a premium talent acquisition dashboard designed to go beyond rigid, keyword-based resume filtering. By leveraging a **two-stage hybrid pipeline** (combining S-BERT semantic vector embeddings with LLM reasoning), the system acts like a human recruiter—analyzing career growth, behavioral signals, platform activity, and skill alignment to deliver a trusted shortlist.

---

## 🌟 Key Features

* **Two-Stage Hybrid Ranking Pipeline:**
  1. **Stage 1 (Coarse Filtering):** Generates Sentence-BERT (S-BERT) embeddings for candidate profiles and job descriptions, ranking candidates using **Cosine Similarity**.
  2. **Stage 2 (Fine Re-ranking):** Passes the top candidates to a simulated LLM ranker that scores profiles based on career progression, behavioral traits, and open-source contribution metrics.
* **Premium Dashboard UI:** A beautiful, responsive user interface featuring a **Classic Navy & Gold** theme with full glassmorphism cards and smooth drop shadows.
* **Interactive Motion Design:** 
  * Responsive particle canvas background reacting to cursor physics.
  * Interactive 3D tilt hover effects on candidate cards.
  * Smooth scroll-triggered fade-in reveals.
* **AI-Generated Justifications:** Provides human-readable, detailed explanations of *why* each candidate was ranked at their respective score.

---

## 🛠️ Tech Stack

* **Frontend:** Vanilla HTML5, CSS3 Custom Properties (CSS variables), Vanilla JavaScript (ES6+)
* **Backend:** Flask (Python 3), Flask-CORS
* **Machine Learning & NLP:** `sentence-transformers` (`all-MiniLM-L6-v2`), `scikit-learn` (TF-IDF fallback & Cosine Similarity)
* **Data Processing:** `pandas`, `numpy`

---

## 📁 Project Structure

```text
ai-recruitment/
├── src/
│   ├── data_loader.py        # Parses CSV files into dataclasses
│   ├── embedding_engine.py   # Handles vector embedding & cosine similarity
│   ├── ranker.py             # LLM re-ranking simulation & justification
│   └── pipeline.py           # Orchestrates the two-stage ranking pipeline
├── static/
│   ├── index.html            # Main dashboard interface
│   ├── style.css             # Premium Navy & Gold responsive styling
│   └── app.js                # Frontend controller, animations, & particle canvas
├── docs/
│   └── APPROACH.md           # Architectural detail document
├── app.py                    # Flask API server
├── main.py                   # CLI entrypoint for local execution
├── candidates.csv            # Sample candidate profiles
├── job_description.csv       # Sample job description
├── requirements.txt          # Python dependencies
└── .gitignore                # Git exclusions
```

---

## 🚀 Setup and Installation

### Prerequisites
Make sure you have **Python 3.8+** installed.

### 1. Clone and Navigate to the Repository
```bash
git clone https://github.com/RUSHI-KOLLA/ai-recruitment.git
cd ai-recruitment
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application

#### Option A: Run the Web Dashboard
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

#### Option B: Run the CLI Tool
```bash
python main.py
```
This runs the pipeline directly and outputs the results to `ranked_candidates.csv`.

---

## 📊 Evaluation Logic (Stages)
1. **Semantic Vector Similarity:** Maps candidates contextually against the job description (e.g., matching concepts like "FastAPI" and "API Design" even without exact keyword matches).
2. **LLM Refinement:** Scans behavioral signals (e.g., leadership, mentorship) and active platform presence (e.g., open-source maintainers/contributors) to compute the final suitability score.
