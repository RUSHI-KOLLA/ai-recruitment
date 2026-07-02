"""
Flask backend API for the AI Recruitment Dashboard.

Provides endpoints for candidate ranking, data upload, and health checks.
Integrates with the existing RecruitmentPipeline from src/.
"""

import os
import sys
import tempfile
import traceback
from dataclasses import asdict

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from src.pipeline import RecruitmentPipeline
from src.data_loader import DataLoader, Candidate, JobDescription

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__, static_folder="static")
CORS(app)

@app.after_request
def add_no_cache_headers(response):
    """Disable caching in development so static files are always fresh."""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Default sample data paths
SAMPLE_CANDIDATES = os.path.join(BASE_DIR, "candidates.csv")
SAMPLE_JOB = os.path.join(BASE_DIR, "job_description.csv")

# Temp storage for uploaded files (per-session, not production-grade)
_uploaded_files = {
    "candidates": None,
    "job": None,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _candidate_to_dict(candidate: Candidate) -> dict:
    """Convert a Candidate dataclass to a JSON-safe dict."""
    return {
        "candidate_id": candidate.candidate_id,
        "name": candidate.name,
        "experience": candidate.experience,
        "skills": candidate.skills,
        "education": candidate.education,
        "platform_activity": candidate.platform_activity,
        "behavioral_signals": candidate.behavioral_signals,
    }


def _job_to_dict(job: JobDescription) -> dict:
    """Convert a JobDescription dataclass to a JSON-safe dict."""
    return {
        "job_id": job.job_id,
        "title": job.title,
        "description": job.description,
        "required_skills": job.required_skills,
        "preferred_experience": job.preferred_experience,
    }


def _error_response(message: str, status_code: int = 400):
    """Return a standardised JSON error response."""
    return jsonify({"error": message}), status_code


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the static index.html."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    """Health-check endpoint."""
    return jsonify({"status": "healthy", "service": "ai-recruitment-api"})


@app.route("/api/sample-data", methods=["GET"])
def sample_data():
    """Load and return the sample candidates and job description as JSON."""
    try:
        loader = DataLoader()
        candidates = loader.load_candidates(SAMPLE_CANDIDATES)
        job = loader.load_job(SAMPLE_JOB)

        return jsonify({
            "candidates": [_candidate_to_dict(c) for c in candidates],
            "job": _job_to_dict(job),
        })
    except FileNotFoundError as exc:
        return _error_response(f"Sample data not found: {exc}", 404)
    except Exception as exc:
        return _error_response(f"Failed to load sample data: {exc}", 500)


@app.route("/api/upload", methods=["POST"])
def upload():
    """Accept CSV file uploads for candidates and/or job description.

    Expects multipart/form-data with optional fields:
      - candidates  (CSV file)
      - job         (CSV file)
    """
    try:
        saved = {}

        for field, key in [("candidates", "candidates"), ("job", "job")]:
            file = request.files.get(field)
            if file and file.filename:
                # Save to a temp file that persists until the next upload
                suffix = ".csv"
                fd, path = tempfile.mkstemp(suffix=suffix, prefix=f"recruit_{key}_")
                os.close(fd)
                file.save(path)
                _uploaded_files[key] = path
                saved[key] = file.filename

        if not saved:
            return _error_response("No files provided. Include 'candidates' and/or 'job' CSV files.", 400)

        return jsonify({
            "message": "Files uploaded successfully",
            "uploaded": saved,
        })
    except Exception as exc:
        return _error_response(f"Upload failed: {exc}", 500)


@app.route("/api/rank", methods=["POST"])
def rank():
    """Run the recruitment pipeline and return ranked candidates.

    Optionally accepts JSON body:
      { "use_sample": true }
    to explicitly use sample data instead of uploaded files.
    """
    try:
        body = request.get_json(silent=True) or {}
        use_sample = body.get("use_sample", False)

        # Determine paths
        candidates_path = SAMPLE_CANDIDATES if use_sample else (_uploaded_files.get("candidates") or SAMPLE_CANDIDATES)
        job_path = SAMPLE_JOB if use_sample else (_uploaded_files.get("job") or SAMPLE_JOB)

        # Validate files exist
        if not os.path.isfile(candidates_path):
            return _error_response(f"Candidates file not found: {candidates_path}", 404)
        if not os.path.isfile(job_path):
            return _error_response(f"Job description file not found: {job_path}", 404)

        # Load the job for the response
        loader = DataLoader()
        job = loader.load_job(job_path)

        # Run the pipeline
        pipeline = RecruitmentPipeline()
        results = pipeline.run(candidates_path, job_path)

        # Build response
        ranked_candidates = []
        for rank_pos, (candidate, score, justification) in enumerate(results, start=1):
            entry = _candidate_to_dict(candidate)
            entry["score"] = round(score, 4)
            entry["justification"] = justification
            entry["rank"] = rank_pos
            ranked_candidates.append(entry)

        return jsonify({
            "job": _job_to_dict(job),
            "candidates": ranked_candidates,
        })
    except Exception as exc:
        traceback.print_exc()
        return _error_response(f"Ranking failed: {exc}", 500)


# ---------------------------------------------------------------------------
# Static file catch-all (for JS, CSS, images, etc.)
# ---------------------------------------------------------------------------

@app.route("/<path:filename>")
def static_files(filename):
    """Serve any static file from the static/ directory."""
    return send_from_directory(app.static_folder, filename)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
