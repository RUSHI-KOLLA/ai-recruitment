"""
Generate the hackathon submission PPTX using the Redrob template.
Populates all slides with concise, professional, executive-ready content that never overflows.
"""
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor

TEMPLATE = "/home/rushi/Downloads/Idea Submission Template _ Redrob.pptx"
OUTPUT = "/home/rushi/ai-recruitment/AI_Recruit_Submission.pptx"

prs = Presentation(TEMPLATE)

def set_text_box(slide, shape_index, paragraphs_data, custom_size=Pt(12)):
    """Replace text in a text box shape, keeping formatting clean and professional."""
    shape = slide.shapes[shape_index]
    tf = shape.text_frame
    tf.word_wrap = True

    # Capture font styling from template
    if tf.paragraphs and tf.paragraphs[0].runs:
        ref_run = tf.paragraphs[0].runs[0]
        ref_font_name = ref_run.font.name
        ref_font_color = ref_run.font.color.rgb if ref_run.font.color and ref_run.font.color.rgb else RGBColor(0x20, 0x27, 0x29)
    else:
        ref_font_name = "Manrope SemiBold"
        ref_font_color = RGBColor(0x20, 0x27, 0x29)

    # Clear existing paragraphs
    for i in range(len(tf.paragraphs) - 1, 0, -1):
        p = tf.paragraphs[i]._p
        p.getparent().remove(p)

    # Add clean paragraphs
    for idx, text in enumerate(paragraphs_data):
        if idx == 0:
            para = tf.paragraphs[0]
            para.clear()
        else:
            para = tf.add_paragraph()

        run = para.add_run()
        run.text = text
        run.font.name = ref_font_name
        run.font.size = custom_size
        run.font.color.rgb = ref_font_color
        
        # Add slight spacing after paragraphs for breathing room
        if text.strip() == "":
            para.space_after = Pt(4)
        else:
            para.space_after = Pt(6)


# ═══════════════════════════════════════════════════════
# SLIDE 0: Cover
# ═══════════════════════════════════════════════════════
slide0 = prs.slides[0]
set_text_box(slide0, 1, ["Team Name : AI Recruit"], Pt(14))
set_text_box(slide0, 3, ["Team Leader Name : Charishma Kottapalli"], Pt(14))
set_text_box(slide0, 2, [
    "Problem Statement : Build an AI system that ranks candidates the way a great recruiter would — "
    "understanding career trajectory, skills, and behavioral fit beyond keyword matching."
], Pt(13))


# ═══════════════════════════════════════════════════════
# SLIDE 1: Solution Overview
# ═══════════════════════════════════════════════════════
slide1 = prs.slides[1]
set_text_box(slide1, 2, [
    "What is your proposed solution?",
    "• AI Recruit is a Hybrid Intelligence Ranking System that mirrors human recruiter reasoning.",
    "• Stage 1 (Semantic Search): Uses Sentence-BERT vectors to evaluate conceptual similarity between job descriptions and resumes.",
    "• Stage 2 (LLM Reasoner): Conducts deep evaluation of career growth, leadership signals, and open-source contributions.",
    "",
    "What differentiates your approach?",
    "• Beyond Keywords: Understands that 'FastAPI' satisfies an 'API Design' requirement without exact string matching.",
    "• Holistic Profiling: Evaluates soft skills, mentorship history, and technical blogging alongside hard skills.",
    "• Instant Explainability: Every score is accompanied by a transparent, AI-generated justification."
], Pt(12))


# ═══════════════════════════════════════════════════════
# SLIDE 2: JD Understanding & Candidate Evaluation
# ═══════════════════════════════════════════════════════
slide2 = prs.slides[2]
set_text_box(slide2, 2, [
    "Key Requirements Extracted from JD:",
    "• Structured Parsing: Automatically extracts job titles, required skill vectors, and seniority expectations.",
    "• Semantic Mapping: Converts raw requirements into rich 384-dimensional vector representations.",
    "",
    "Critical Candidate Evaluation Signals:",
    "• Core Competencies (50% Weight): Direct and semantic overlap with mandatory job skills.",
    "• Seniority & Trajectory (30% Weight): Career level alignment (e.g., matching Senior Architect roles with progressive experience).",
    "• Platform Activity (10% Weight): Verified GitHub contributions, open-source maintenance, and active engineering presence.",
    "• Behavioral Traits (10% Weight): Evidence of strategic planning, team leadership, and mentorship."
], Pt(12))


# ═══════════════════════════════════════════════════════
# SLIDE 3: Ranking Methodology
# ═══════════════════════════════════════════════════════
slide3 = prs.slides[3]
set_text_box(slide3, 2, [
    "Four-Stage Ranking Pipeline:",
    "1. Ingestion & Cleaning: Structured CSV parsing into validated Python dataclasses.",
    "2. Vector Encoding: Sentence-BERT (all-MiniLM-L6-v2) generates high-dimensional embeddings.",
    "3. Coarse Filtering: Cosine Similarity rapidly ranks candidates to identify the top-10 shortlist.",
    "4. Fine-Grained Scoring: LLM multi-signal evaluation computes final normalized scores (0.0 to 1.0).",
    "",
    "Core Algorithms & Heuristics:",
    "• Vector Similarity: Cosine distance measures conceptual relevance across disparate terminologies.",
    "• Weighted Multi-Signal Heuristic: Balances technical skills with behavioral and community signals.",
    "• Zero-Dependency Fallback: Integrated TF-IDF matrix scoring ensures robust runtime reliability."
], Pt(12))


# ═══════════════════════════════════════════════════════
# SLIDE 4: Explainability & Data Validation
# ═══════════════════════════════════════════════════════
slide4 = prs.slides[4]
set_text_box(slide4, 2, [
    "Transparent Ranking Decisions:",
    "• Human-Readable Proof: Each candidate output includes an explicit justification string.",
    "• Clear Attribution: Details exact skill matches, seniority alignment, and bonus signals.",
    "• Example Output: 'Matched skills: Python, AWS; Seniority aligned; Active open-source contributor.'",
    "",
    "Preventing Hallucinations & Bias:",
    "• Strict Grounding: LLM evaluation is strictly bounded to verified CSV input columns.",
    "• Deterministic Math: Base similarity is mathematically anchored by vector cosine distance.",
    "",
    "Handling Low-Quality or Incomplete Profiles:",
    "• Graceful Degradation: Missing optional fields (like platform activity) simply yield zero bonus without penalizing core skill scores.",
    "• Outlier Protection: Malformed profiles are safely sanitized during data ingestion."
], Pt(12))


# ═══════════════════════════════════════════════════════
# SLIDE 5: End-to-End Workflow
# ═══════════════════════════════════════════════════════
slide5 = prs.slides[5]
set_text_box(slide5, 2, [
    "Step-by-Step Execution Flow:",
    "",
    "• Step 1: Input — Recruiter uploads candidate and job description CSVs via the interactive web dashboard.",
    "• Step 2: Processing — Backend parses records and normalizes text fields for NLP encoding.",
    "• Step 3: Embedding — S-BERT transforms profiles into 384-dimensional semantic vector space.",
    "• Step 4: Shortlisting — Cosine similarity filters and ranks the top talent pool instantaneously.",
    "• Step 5: AI Evaluation — LLM reasoner synthesizes hard and soft signals into final rankings.",
    "• Step 6: Delivery — Interactive dashboard presents score rings, skill badges, and exportable CSV reports."
], Pt(12.5))


# ═══════════════════════════════════════════════════════
# SLIDE 6: System Architecture (Clean Structured Layout)
# ═══════════════════════════════════════════════════════
slide6 = prs.slides[6]
from pptx.enum.text import PP_ALIGN

txBox = slide6.shapes.add_textbox(Emu(480500), Emu(1350000), Emu(8180000), Emu(3200000))
tf = txBox.text_frame
tf.word_wrap = True

arch_steps = [
    ("1. PRESENTATION LAYER (Web Dashboard / CLI)", "HTML5 Glassmorphism UI, Reactive Particle Canvas, Flask REST API (Port 5000)"),
    ("                                  ▼", ""),
    ("2. DATA INGESTION & SANITIZATION MODULE", "CSV Parser, Dataclass Validation, Text Normalization & Clean-up"),
    ("                                  ▼", ""),
    ("3. COARSE RANKING ENGINE (Semantic Vector Space)", "Sentence-BERT (all-MiniLM-L6-v2) Embeddings → Cosine Similarity Filtering"),
    ("                                  ▼", ""),
    ("4. FINE-GRAINED LLM REASONER (Multi-Signal Evaluation)", "Skills (50%) + Seniority (30%) + Activity (10%) + Behavioral Traits (10%)"),
    ("                                  ▼", ""),
    ("5. EXPLAINABLE DELIVERY LAYER", "AI Justification Generator, Visual Score Rings, Exportable ranked_candidates.csv")
]

for idx, (title, desc) in enumerate(arch_steps):
    if idx == 0:
        p1 = tf.paragraphs[0]
    else:
        p1 = tf.add_paragraph()
    
    r1 = p1.add_run()
    r1.text = title
    r1.font.name = "Manrope ExtraBold" if "▼" not in title else "Manrope SemiBold"
    r1.font.size = Pt(13) if "▼" not in title else Pt(11)
    r1.font.color.rgb = RGBColor(0x1E, 0x3A, 0x5F) if "▼" not in title else RGBColor(0xD4, 0x91, 0x3D)
    
    if desc:
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = "    ↳ " + desc
        r2.font.name = "Manrope SemiBold"
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = RGBColor(0x5A, 0x6B, 0x63)
        p2.space_after = Pt(8)
    else:
        p1.space_after = Pt(2)


# ═══════════════════════════════════════════════════════
# SLIDE 7: Results & Performance
# ═══════════════════════════════════════════════════════
slide7 = prs.slides[7]
set_text_box(slide7, 2, [
    "Demonstrated Ranking Quality:",
    "• Accurate Prioritization: Properly ranks high-skill matches over pure years of experience when core technical alignment is superior.",
    "• Holistic Differentiation: Effectively separates candidates with identical skill titles by evaluating open-source contributions and leadership traits.",
    "",
    "Runtime & Compute Efficiency:",
    "• High-Speed Execution: Full pipeline evaluates and ranks 100+ candidates in under 2 seconds.",
    "• Lightweight Architecture: Optimized vector math runs efficiently on standard CPU hardware without requiring expensive GPUs.",
    "• Self-Contained Reliability: Integrated fallback scoring guarantees zero downtime even in offline or air-gapped environments."
], Pt(12))


# ═══════════════════════════════════════════════════════
# SLIDE 8: Technologies Used (Concise & Well-Spaced)
# ═══════════════════════════════════════════════════════
slide8 = prs.slides[8]
set_text_box(slide8, 2, [
    "Frontend Architecture:",
    "• HTML5 & CSS3: Premium Navy & Gold glassmorphism design with responsive grid layouts.",
    "• Vanilla JavaScript (ES6+): Interactive particle physics canvas and 3D hover micro-animations.",
    "",
    "Backend & API:",
    "• Python 3.12 & Flask: Lightweight, robust REST API serving structured JSON responses.",
    "",
    "Machine Learning & NLP Stack:",
    "• Sentence-Transformers (S-BERT): 'all-MiniLM-L6-v2' for high-accuracy semantic embeddings.",
    "• Scikit-Learn: Cosine similarity vector distance and TF-IDF matrix fallback.",
    "• Pandas & NumPy: High-performance data manipulation and CSV ingestion.",
    "",
    "Why This Stack? Maximum speed, zero frontend build complexity, and proven NLP accuracy."
], Pt(11.5))


# ═══════════════════════════════════════════════════════
# SLIDE 9: Submission Assets & Team
# ═══════════════════════════════════════════════════════
slide9 = prs.slides[9]
set_text_box(slide9, 2, [
    "Official GitHub Repository:",
    "• https://github.com/RUSHI-KOLLA/ai-recruitment (Clean, documented, and ready to run)",
    "",
    "Included Submission Deliverables:",
    "• Complete codebase with web dashboard and CLI pipeline",
    "• AI_Recruit_Submission.pdf (Executive approach presentation)",
    "• ranked_candidates.csv (Verified output formatting)",
    "",
    "Team Members (AI Recruit):",
    "• Charishma Kottapalli (Leader) — kottapallicharishma@gmail.com",
    "• Kolla Rushikesh — kollarushi2006@gmail.com",
    "• Sahil Kumar — kumarsahil282006@gmail.com",
    "• Gaurav Singh — g.singh200293@gmail.com"
], Pt(12))


# Save
prs.save(OUTPUT)
print(f"✅ Clean, professional presentation saved to: {OUTPUT}")
