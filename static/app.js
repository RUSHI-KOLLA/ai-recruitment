/* ═══════════════════════════════════════════════════════
   AI Recruit — Dashboard Application
   ═══════════════════════════════════════════════════════ */

(() => {
  'use strict';

  // ── DOM refs ────────────────────────────────────────
  const $ = (s) => document.querySelector(s);
  const zoneCandidates   = $('#zone-candidates');
  const zoneJD           = $('#zone-jd');
  const fileCandidates   = $('#file-candidates');
  const fileJD           = $('#file-jd');
  const filenameCand     = $('#filename-candidates');
  const filenameJD       = $('#filename-jd');
  const btnRank          = $('#btn-rank');
  const btnSample        = $('#btn-sample');
  const loadingOverlay   = $('#loading-overlay');
  const jdSection        = $('#jd-section');
  const jdCard           = $('#jd-card');
  const jdTitle          = $('#jd-title');
  const jdDesc           = $('#jd-desc');
  const jdSkills         = $('#jd-skills');
  const jdExperience     = $('#jd-experience');
  const candidatesSection = $('#candidates-section');
  const candidatesCount  = $('#candidates-count');
  const candidatesGrid   = $('#candidates-grid');
  const toastContainer   = $('#toast-container');

  // ── State ───────────────────────────────────────────
  let selectedFiles = { candidates: null, jd: null };

  // ── Helpers ─────────────────────────────────────────
  function updateRankButtonState() {
    btnRank.disabled = !(selectedFiles.candidates && selectedFiles.jd);
  }

  // ── Toast Notifications ─────────────────────────────
  function showToast(message, type = 'error') {
    const toast = document.createElement('div');
    toast.className = `toast toast--${type}`;
    const icon = type === 'error' ? '✕' : '✓';
    toast.innerHTML = `<span class="toast__icon">${icon}</span><span>${message}</span>`;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.classList.add('toast--removing');
      toast.addEventListener('animationend', () => toast.remove());
    }, 4000);
  }

  // ── Loading ─────────────────────────────────────────
  function setLoading(on) {
    loadingOverlay.hidden = !on;
    document.body.style.overflow = on ? 'hidden' : '';
  }

  // ── File Upload Zones ───────────────────────────────
  function setupZone(zone, input, filenameEl, key) {
    // Click to browse
    zone.addEventListener('click', () => input.click());
    zone.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); }
    });

    // File selected via input
    input.addEventListener('change', () => {
      if (input.files.length) handleFile(input.files[0], zone, filenameEl, key);
    });

    // Drag events
    ['dragenter', 'dragover'].forEach((evt) =>
      zone.addEventListener(evt, (e) => { e.preventDefault(); zone.classList.add('drag-over'); })
    );
    ['dragleave', 'drop'].forEach((evt) =>
      zone.addEventListener(evt, () => zone.classList.remove('drag-over'))
    );
    zone.addEventListener('drop', (e) => {
      e.preventDefault();
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file, zone, filenameEl, key);
    });
  }

  function handleFile(file, zone, filenameEl, key) {
    if (!file.name.toLowerCase().endsWith('.csv')) {
      showToast('Please upload a CSV file.', 'error');
      return;
    }
    selectedFiles[key] = file;
    filenameEl.textContent = file.name;
    zone.classList.add('has-file');
    updateRankButtonState();
  }

  setupZone(zoneCandidates, fileCandidates, filenameCand, 'candidates');
  setupZone(zoneJD, fileJD, filenameJD, 'jd');

  // ── API Calls ───────────────────────────────────────
  async function apiUploadAndRank() {
    setLoading(true);
    try {
      // 1) Upload files
      const form = new FormData();
      form.append('candidates', selectedFiles.candidates);
      form.append('job', selectedFiles.jd);

      const uploadRes = await fetch('/api/upload', { method: 'POST', body: form });
      if (!uploadRes.ok) {
        const err = await uploadRes.json().catch(() => ({}));
        throw new Error(err.detail || err.error || 'Upload failed');
      }

      // 2) Rank
      const rankRes = await fetch('/api/rank', { method: 'POST' });
      if (!rankRes.ok) {
        const err = await rankRes.json().catch(() => ({}));
        throw new Error(err.detail || err.error || 'Ranking failed');
      }

      const data = await rankRes.json();
      renderResults(data);
      showToast('Candidates ranked successfully!', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  }

  async function apiSampleData() {
    setLoading(true);
    try {
      // 1) Load sample data
      const sampleRes = await fetch('/api/sample-data');
      if (!sampleRes.ok) throw new Error('Failed to load sample data');

      // 2) Rank using sample data
      const rankRes = await fetch('/api/rank', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ use_sample: true })
      });
      if (!rankRes.ok) {
        const err = await rankRes.json().catch(() => ({}));
        throw new Error(err.detail || err.error || 'Ranking failed');
      }

      const data = await rankRes.json();
      renderResults(data);
      showToast('Sample data ranked successfully!', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  }

  btnRank.addEventListener('click', apiUploadAndRank);
  btnSample.addEventListener('click', apiSampleData);

  // ── Render Results ──────────────────────────────────
  function renderResults(data) {
    renderJD(data.job || data.job_description);
    renderCandidates(data.candidates || data.ranked_candidates, data.job || data.job_description);
  }

  // ── Render Job Description ──────────────────────────
  function renderJD(jd) {
    if (!jd) return;
    jdTitle.textContent = jd.title || jd.job_title || 'Untitled Position';
    jdDesc.textContent  = jd.description || jd.job_description || '';

    // Skills
    const skills = jd.required_skills || jd.skills || [];
    jdSkills.innerHTML = '';
    (Array.isArray(skills) ? skills : skills.split(',')).forEach((s) => {
      const tag = document.createElement('span');
      tag.className = 'tag tag--jd';
      tag.textContent = s.trim();
      
      // Hover event listeners to highlight candidates possessing this skill
      tag.addEventListener('mouseenter', () => {
        highlightCandidatesWithSkill(s.trim());
      });
      tag.addEventListener('mouseleave', () => {
        resetHighlights();
      });
      
      jdSkills.appendChild(tag);
    });

    jdExperience.textContent = jd.preferred_experience || jd.experience || 'Not specified';
    jdSection.hidden = false;
    
    // Apply 3D tilt interaction to Job description card
    applyTilt(jdCard);
  }

  // ── Render Candidates ───────────────────────────────
  function renderCandidates(candidates, jd) {
    if (!candidates || !candidates.length) return;
    candidatesGrid.innerHTML = '';
    candidatesCount.textContent = `${candidates.length} candidates`;

    // Collect JD required skills (lowercase) for matching
    const rawSkills = jd?.required_skills || jd?.skills || [];
    const jdSkillSet = new Set(
      (Array.isArray(rawSkills) ? rawSkills : rawSkills.split(','))
        .map((s) => s.trim().toLowerCase())
    );

    candidates.forEach((c, i) => {
      const card = buildCandidateCard(c, i, jdSkillSet);
      candidatesGrid.appendChild(card);
      
      // Animate candidate card score percent count-up
      const pctEl = card.querySelector('.score-ring__pct');
      if (pctEl) {
        const targetPct = parseInt(pctEl.getAttribute('data-score'), 10);
        animateScoreText(pctEl, targetPct);
      }
      
      // Apply 3D tilt interaction
      applyTilt(card);
      
      // Observe for scroll reveal animation
      if (window.scrollObserver) {
        window.scrollObserver.observe(card);
      }
    });

    candidatesSection.hidden = false;
    // Scroll into view smoothly
    setTimeout(() => jdSection.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
  }

  // ── Build Candidate Card ────────────────────────────
  function buildCandidateCard(c, index, jdSkillSet) {
    const score = parseFloat(c.score ?? c.match_score ?? 0);
    const pct   = Math.round(score * 100);

    const card = document.createElement('div');
    card.className = 'candidate-card scroll-reveal reveal-up';
    card.style.animationDelay = `${index * 0.08}s`;

    // Score color
    let scoreColor = 'var(--red)';
    if (score > 0.7) scoreColor = 'var(--green)';
    else if (score > 0.4) scoreColor = 'var(--yellow)';

    // SVG ring
    const R = 38;
    const C = 2 * Math.PI * R;
    const offset = C - (score * C);

    // Skills
    const skills = c.skills || [];
    const skillTags = (Array.isArray(skills) ? skills : skills.split(','))
      .map((s) => s.trim())
      .filter(Boolean)
      .map((s) => {
        const isMatch = jdSkillSet.has(s.toLowerCase());
        return `<span class="tag ${isMatch ? 'tag--match' : ''}">${escapeHtml(s)}</span>`;
      }).join('');

    card.innerHTML = `
      <div class="rank-badge">#${index + 1}</div>
      <div class="card__top">
        <span class="card__name">${escapeHtml(c.name || 'Unknown')}</span>
        <div class="score-ring">
          <svg width="88" height="88" viewBox="0 0 88 88">
            <circle class="score-ring__bg" cx="44" cy="44" r="${R}" />
            <circle class="score-ring__fg"
              cx="44" cy="44" r="${R}"
              stroke="${scoreColor}"
              stroke-dasharray="${C}"
              stroke-dashoffset="${C}"
              style="--ring-circumference:${C};--ring-offset:${offset}"
            />
          </svg>
          <div class="score-ring__label">
            <span class="score-ring__pct" style="color:${scoreColor}" data-score="${pct}">0%</span>
            <span class="score-ring__sub">Score</span>
          </div>
        </div>
      </div>

      <div class="card__body">
        ${skillTags ? `
        <div class="card__skills">
          <div class="card__row">
            ${iconSvg('skills')}
            <span class="card__row-label">Skills</span>
          </div>
          <div class="tags" style="margin-top:4px;padding-left:24px">${skillTags}</div>
        </div>` : ''}

        ${c.experience ? `
        <div class="card__row">
          ${iconSvg('experience')}
          <div><span class="card__row-label">Experience</span> ${escapeHtml(truncate(c.experience, 100))}</div>
        </div>` : ''}

        ${c.education ? `
        <div class="card__row">
          ${iconSvg('education')}
          <div><span class="card__row-label">Education</span> ${escapeHtml(c.education)}</div>
        </div>` : ''}

        ${c.platform_activity ? `
        <div class="card__row">
          ${iconSvg('platform')}
          <div><span class="card__row-label">Platform</span> ${escapeHtml(truncate(c.platform_activity, 80))}</div>
        </div>` : ''}

        ${c.behavioral_signals ? `
        <div class="card__row">
          ${iconSvg('behavioral')}
          <div><span class="card__row-label">Behavioral</span> ${escapeHtml(truncate(c.behavioral_signals, 80))}</div>
        </div>` : ''}

        ${c.justification || c.ai_justification ? `
        <div class="card__justification">
          <div class="card__justification-label">
            ${iconSvg('ai')}
            AI Justification
          </div>
          ${escapeHtml(c.justification || c.ai_justification)}
        </div>` : ''}
      </div>
    `;
    return card;
  }

  // ── Inline SVG Icons ────────────────────────────────
  function iconSvg(type) {
    const icons = {
      skills: `<svg class="card__row-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M8 1l2 4 4.5.7-3.3 3.1.8 4.5L8 11.2 3.9 13.3l.8-4.5L1.5 5.7 6 5z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round" fill="none"/>
      </svg>`,
      experience: `<svg class="card__row-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
        <rect x="2" y="5" width="12" height="9" rx="2" stroke="currentColor" stroke-width="1.2" fill="none"/>
        <path d="M5 5V3.5A1.5 1.5 0 0 1 6.5 2h3A1.5 1.5 0 0 1 11 3.5V5" stroke="currentColor" stroke-width="1.2" fill="none"/>
      </svg>`,
      education: `<svg class="card__row-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M1 6l7-3 7 3-7 3z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round" fill="none"/>
        <path d="M4 7.5v4c0 1 1.8 2.5 4 2.5s4-1.5 4-2.5v-4" stroke="currentColor" stroke-width="1.2" fill="none"/>
      </svg>`,
      platform: `<svg class="card__row-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
        <rect x="2" y="2" width="12" height="12" rx="2" stroke="currentColor" stroke-width="1.2" fill="none"/>
        <path d="M5 11V7M8 11V5M11 11V8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
      </svg>`,
      behavioral: `<svg class="card__row-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="5" r="3" stroke="currentColor" stroke-width="1.2" fill="none"/>
        <path d="M2 14c0-3 2.7-5 6-5s6 2 6 5" stroke="currentColor" stroke-width="1.2" fill="none"/>
      </svg>`,
      ai: `<svg class="card__row-icon" width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M7 1v2M7 11v2M1 7h2M11 7h2M2.8 2.8l1.4 1.4M9.8 9.8l1.4 1.4M11.2 2.8l-1.4 1.4M4.2 9.8l-1.4 1.4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
        <circle cx="7" cy="7" r="2.5" stroke="currentColor" stroke-width="1.2" fill="none"/>
      </svg>`
    };
    return icons[type] || '';
  }

  // ── Utilities ───────────────────────────────────────
  function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = String(str);
    return div.innerHTML;
  }

  function truncate(str, max) {
    if (!str) return '';
    return str.length > max ? str.slice(0, max) + '…' : str;
  }

  // ── Motion Graphic Score Text Animation ───────────────
  function animateScoreText(element, targetValue) {
    let start = 0;
    const duration = 1200; // milliseconds
    const startTime = performance.now();
    
    function update(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out quad
      const easeProgress = progress * (2 - progress);
      const currentValue = Math.round(start + easeProgress * targetValue);
      element.textContent = `${currentValue}%`;
      
      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }
    requestAnimationFrame(update);
  }

  // ── Interactive 3D Tilt Card Effect ───────────────────
  function applyTilt(card) {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const xc = rect.width / 2;
      const yc = rect.height / 2;
      
      // Calculate rotation based on offset from card center
      const angleX = (yc - y) / 14; 
      const angleY = (x - xc) / 14;
      
      // Apply 3D rotation matrix
      card.style.transform = `rotateX(${angleX}deg) rotateY(${angleY}deg) translateY(-5px)`;
    });

    card.addEventListener('mouseleave', () => {
      // Reset card transform
      card.style.transform = '';
    });
  }

  // ── Interactive JD Skill Tag Matching Highlights ──────
  function highlightCandidatesWithSkill(skillName) {
    const targetSkill = skillName.toLowerCase();
    const cards = document.querySelectorAll('.candidate-card');
    
    cards.forEach((card) => {
      const candidateTags = card.querySelectorAll('.tag');
      let hasSkill = false;
      
      candidateTags.forEach((tag) => {
        if (tag.textContent.trim().toLowerCase() === targetSkill) {
          tag.classList.add('tag--active');
          hasSkill = true;
        } else {
          tag.classList.add('tag--dimmed');
        }
      });
      
      if (hasSkill) {
        card.classList.add('highlighted-card');
      } else {
        card.classList.add('dimmed-card');
      }
    });
  }

  function resetHighlights() {
    const cards = document.querySelectorAll('.candidate-card');
    cards.forEach((card) => {
      card.classList.remove('highlighted-card', 'dimmed-card');
      const tags = card.querySelectorAll('.tag');
      tags.forEach((tag) => {
        tag.classList.remove('tag--active', 'tag--dimmed');
      });
    });
  }

  // ── Interactive Canvas Particle Background Engine ─────
  function initParticles() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const particles = [];
    const maxParticles = 65;
    const connectionDist = 120;
    const mouse = { x: null, y: null, radius: 150 };

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    window.addEventListener('mousemove', (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    });

    window.addEventListener('mouseout', () => {
      mouse.x = null;
      mouse.y = null;
    });

    class Particle {
      constructor() {
        this.reset();
      }
      reset() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.45;
        this.vy = (Math.random() - 0.5) * 0.45;
        this.radius = Math.random() * 2 + 1;
        this.color = Math.random() > 0.5 ? 'rgba(30, 58, 95, 0.35)' : 'rgba(212, 145, 61, 0.25)';
      }
      update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;

        // Reactive physics force from mouse cursor interaction
        if (mouse.x !== null && mouse.y !== null) {
          const dx = this.x - mouse.x;
          const dy = this.y - mouse.y;
          const dist = Math.hypot(dx, dy);
          if (dist < mouse.radius) {
            const force = (mouse.radius - dist) / mouse.radius;
            this.x += (dx / dist) * force * 1.5;
            this.y += (dy / dist) * force * 1.5;
          }
        }
      }
      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
      }
    }

    for (let i = 0; i < maxParticles; i++) {
      particles.push(new Particle());
    }

    function animate() {
      ctx.clearRect(0, 0, width, height);

      // Connect adjacent nodes
      for (let i = 0; i < particles.length; i++) {
        const p1 = particles[i];
        p1.update();
        p1.draw();

        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dist = Math.hypot(p1.x - p2.x, p1.y - p2.y);
          if (dist < connectionDist) {
            const alpha = (1 - dist / connectionDist) * 0.12;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(30, 58, 95, ${alpha})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(animate);
    }
    animate();
  }

  // ── Scroll Reveal Observer ────────────────────────────
  function initScrollReveal() {
    window.scrollObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });

    document.querySelectorAll('.scroll-reveal').forEach(el => {
      window.scrollObserver.observe(el);
    });
  }

  // Initialize interactive features immediately
  initScrollReveal();
  initParticles();
})();
