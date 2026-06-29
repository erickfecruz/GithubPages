"""
build.py — Generates index.html (EN) and indexPT.html (PT) from content/*.json.

Run directly:  python scripts/build.py
Or via:        COMPILAR.bat
"""
import sys, json, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from utils import load, ROOT

CONTENT_EN = ROOT / "content" / "en"

OUTPUTS = {'en': ROOT / "index.html", 'pt': ROOT / "indexPT.html"}

# ── UI labels (all static text that appears in the page) ───────────────────────

LABELS = {
    'pt': {
        'html_lang':   'pt-BR',
        'nav_about':   'sobre',
        'nav_projects':'projetos',
        'nav_skills':  'skills',
        'nav_career':  'carreira',
        'section_about':   'SOBRE MIM',
        'current_company': 'EMPRESA ATUAL',
        'section_projects':'PROJETOS',
        'proj_h2_a':   'Trabalhos',
        'proj_h2_b':   'selecionados',
        'filter_all':      'TODOS',
        'filter_game':     'GAME DEV',
        'filter_academic': 'ACADÊMICO',
        'filter_data':     'DATA SCIENCE',
        'filter_web':      'WEB',
        'div_wildlife':  'WILDLIFE STUDIOS',
        'div_wildlife_period': '2021 → PRESENTE',
        'div_previous':  'AMBRA GAMING &amp; PROJETOS ANTERIORES',
        'div_academic':  'ACADÊMICO',
        'div_data':      'DATA SCIENCE',
        'div_web':       'WEB',
        'section_skills': 'HABILIDADES',
        'skills_h2_a':  'Skill',
        'skills_h2_b':  'tree',
        'tools_label':  'ENGINES &amp; FERRAMENTAS',
        'ach_label':    'CONQUISTAS',
        'section_career': 'TRAJETÓRIA',
        'career_h2_a':  'Carreira',
        'career_h2_b':  'profissional',
    },
    'en': {
        'html_lang':   'en',
        'nav_about':   'about',
        'nav_projects':'projects',
        'nav_skills':  'skills',
        'nav_career':  'career',
        'section_about':   'ABOUT ME',
        'current_company': 'CURRENT COMPANY',
        'section_projects':'PROJECTS',
        'proj_h2_a':   'Selected',
        'proj_h2_b':   'work',
        'filter_all':      'ALL',
        'filter_game':     'GAME DEV',
        'filter_academic': 'ACADEMIC',
        'filter_data':     'DATA SCIENCE',
        'filter_web':      'WEB',
        'div_wildlife':  'WILDLIFE STUDIOS',
        'div_wildlife_period': '2021 → PRESENT',
        'div_previous':  'AMBRA GAMING &amp; PREVIOUS PROJECTS',
        'div_academic':  'ACADEMIC',
        'div_data':      'DATA SCIENCE',
        'div_web':       'WEB',
        'section_skills': 'SKILLS',
        'skills_h2_a':  'Skill',
        'skills_h2_b':  'tree',
        'tools_label':  'ENGINES &amp; TOOLS',
        'ach_label':    'ACHIEVEMENTS',
        'section_career': 'CAREER',
        'career_h2_a':  'Professional',
        'career_h2_b':  'journey',
    },
}

# ── CSS ────────────────────────────────────────────────────────────────────────
# Plain string — no f-string escaping needed.

CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:    #0c0b10;
    --bg2:   #13121a;
    --gold:  #c9a84c;
    --goldA: rgba(201,168,76,.2);
    --goldB: rgba(201,168,76,.08);
    --w:     #ffffff;
    --w6:    rgba(255,255,255,.6);
    --w4:    rgba(255,255,255,.4);
    --w2:    rgba(255,255,255,.14);
    --w1:    rgba(255,255,255,.06);
    --mono:  'JetBrains Mono', monospace;
    --sans:  'Inter', sans-serif;
  }

  html { scroll-behavior: smooth; }
  body { background: var(--bg); color: var(--w); font-family: var(--sans); line-height: 1.6; overflow-x: hidden; }

  /* NAV */
  nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; display: flex; align-items: center; justify-content: space-between; padding: 18px 48px; background: rgba(12,11,16,.85); backdrop-filter: blur(12px); border-bottom: 1px solid var(--w1); }
  .nav-logo { font-family: var(--mono); font-size: 13px; color: var(--gold); letter-spacing: 2px; }
  .nav-burger { display: none; flex-direction: column; gap: 5px; background: none; border: none; cursor: pointer; padding: 6px; }
  .nav-burger span { display: block; width: 22px; height: 2px; background: var(--w4); border-radius: 1px; transition: all .25s; }
  .nav-burger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
  .nav-burger.open span:nth-child(2) { opacity: 0; }
  .nav-burger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
  .nav-links { display: flex; gap: 32px; }
  .nav-links a { font-size: 12px; color: var(--w4); text-decoration: none; letter-spacing: 1px; font-family: var(--mono); transition: color .2s; }
  .nav-links a:hover { color: var(--gold); }
  .nav-lang { display: flex; gap: 8px; }
  .nav-lang a { font-size: 11px; color: var(--w4); text-decoration: none; font-family: var(--mono); border: 1px solid var(--w2); padding: 3px 8px; border-radius: 3px; transition: all .2s; }
  .nav-lang a:hover, .nav-lang a.active { color: var(--gold); border-color: var(--goldA); }

  /* LAYOUT */
  section { padding: 100px 48px; max-width: 1100px; margin: 0 auto; }
  #projects { max-width: 100%; padding-left: 80px; padding-right: 80px; }
  .section-label { font-family: var(--mono); font-size: 10px; letter-spacing: 4px; color: var(--gold); margin-bottom: 20px; display: block; }
  .sep { display: block; width: 40px; height: 1px; background: var(--gold); margin: 18px 0; }

  /* HERO */
  #hero { min-height: 100vh; max-width: 100%; padding: 0; display: flex; align-items: center; position: relative; overflow: hidden; }
  #hero-canvas { position: absolute; inset: 0; width: 100%; height: 100%; }
  .hero-content { position: relative; z-index: 2; padding: 0 80px; max-width: 800px; }
  .hero-eyebrow { font-family: var(--mono); font-size: 11px; letter-spacing: 5px; color: var(--gold); margin-bottom: 20px; }
  .hero-name { font-size: clamp(52px, 9vw, 96px); font-weight: 800; line-height: .88; letter-spacing: -3px; }
  .hero-name span { color: var(--gold); }
  .hero-sub { font-family: var(--mono); font-size: 13px; color: var(--w4); margin-top: 18px; line-height: 1.8; }
  .hero-ctas { display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap; align-items: center; }
  .btn-primary { border: 1px solid var(--gold); color: var(--gold); padding: 12px 28px; border-radius: 4px; font-family: var(--mono); font-size: 11px; letter-spacing: 2px; text-decoration: none; transition: all .25s; }
  .btn-primary:hover { background: var(--goldA); }
  .btn-ghost { border: 1px solid var(--w2); color: var(--w4); padding: 12px 20px; border-radius: 4px; font-family: var(--mono); font-size: 11px; letter-spacing: 1px; text-decoration: none; transition: all .25s; }
  .btn-ghost:hover { border-color: var(--w4); color: var(--w6); }
  .hero-socials { display: flex; gap: 10px; margin-top: 28px; }
  .hero-socials a { width: 34px; height: 34px; border: 1px solid var(--w2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--w4); font-size: 13px; text-decoration: none; font-family: var(--mono); transition: all .2s; }
  .hero-socials a:hover { border-color: var(--gold); color: var(--gold); }
  .hero-scroll { position: absolute; bottom: 32px; left: 50%; transform: translateX(-50%); z-index: 2; display: flex; flex-direction: column; align-items: center; gap: 6px; color: var(--w4); font-family: var(--mono); font-size: 9px; letter-spacing: 2px; animation: bounce 2s ease-in-out infinite; }
  .scroll-line { width: 1px; height: 32px; background: linear-gradient(var(--goldA), transparent); }
  @keyframes bounce { 0%,100%{ transform:translateX(-50%) translateY(0) } 50%{ transform:translateX(-50%) translateY(6px) } }

  /* ABOUT */
  #about .about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: start; }
  .about-text h2 { font-size: 36px; font-weight: 700; line-height: 1.1; margin-bottom: 6px; }
  .about-text h2 span { color: var(--gold); }
  .about-text p { font-size: 14px; color: var(--w6); line-height: 1.85; margin-top: 16px; }
  .chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 18px; }
  .chip { display: inline-block; font-family: var(--mono); font-size: 10px; padding: 3px 9px; border-radius: 3px; border: 1px solid var(--goldA); color: var(--gold); }
  .chip.dim { border-color: var(--w2); color: var(--w4); }
  .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .stat-box { background: var(--goldB); border: 1px solid var(--goldA); border-radius: 8px; padding: 16px; text-align: center; }
  .stat-val { font-size: 28px; font-weight: 700; color: var(--gold); font-family: var(--mono); }
  .stat-lbl { font-size: 9px; color: var(--w4); letter-spacing: 2px; font-family: var(--mono); margin-top: 4px; }
  .current-box { grid-column: 1/-1; background: var(--goldB); border: 1px solid var(--goldA); border-radius: 8px; padding: 14px 16px; margin-top: 4px; }
  .current-box .lbl { font-family: var(--mono); font-size: 9px; color: var(--gold); letter-spacing: 2px; margin-bottom: 6px; }
  .current-box .val { font-size: 14px; color: var(--w); font-weight: 500; }
  .current-box .sub { font-size: 11px; color: var(--w4); margin-top: 2px; }

  /* PROJECTS */
  #projects h2 { font-size: 36px; font-weight: 700; margin-bottom: 8px; }
  #projects h2 span { color: var(--gold); }
  .filter-bar { display: flex; gap: 8px; margin-bottom: 32px; flex-wrap: wrap; }
  .filter-btn { font-family: var(--mono); font-size: 10px; letter-spacing: 1px; padding: 5px 14px; border-radius: 3px; border: 1px solid var(--w2); color: var(--w4); background: transparent; cursor: pointer; transition: all .2s; }
  .filter-btn:hover, .filter-btn.on { border-color: var(--gold); color: var(--gold); }
  .section-divider { font-family: var(--mono); font-size: 10px; letter-spacing: 3px; color: var(--gold); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--goldA); display: flex; justify-content: space-between; align-items: center; }
  .section-divider span { color: var(--w4); font-size: 9px; }
  .sub-label { font-family: var(--mono); font-size: 9px; letter-spacing: 3px; color: var(--w4); margin: 28px 0 14px; padding-top: 28px; border-top: 1px solid var(--w1); }

  /* Cards */
  .card-feat { background: var(--bg2); border: 1px solid var(--goldA); border-top: 2px solid var(--gold); border-radius: 10px; overflow: hidden; margin-bottom: 12px; display: grid; grid-template-columns: 1.5fr 1fr; }
  .card-feat img, .card-feat picture { width: 100%; display: block; }
  .card-feat img { height: 100%; min-height: 420px; object-fit: cover; }
  .card-feat picture img { height: 100%; min-height: 420px; object-fit: cover; width: 100%; }
  .card-feat-body { padding: 28px 24px; display: flex; flex-direction: column; justify-content: center; }
  .card-feat-body .eyebrow { font-family: var(--mono); font-size: 9px; color: var(--gold); letter-spacing: 2px; margin-bottom: 10px; }
  .card-feat-body h3 { font-size: 22px; font-weight: 700; margin-bottom: 4px; }
  .card-feat-body .studio { font-family: var(--mono); font-size: 9px; color: var(--gold); letter-spacing: 1px; margin-bottom: 12px; }
  .card-feat-body p { font-size: 12px; color: var(--w4); line-height: 1.75; }
  .card-title-link { color: inherit; text-decoration: none; transition: color .2s; }
  .card-title-link:hover { color: var(--gold); }
  .store-links { display: flex; gap: 8px; margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--w1); flex-wrap: wrap; }
  .store-badge { display: inline-flex; align-items: center; gap: 6px; font-family: var(--mono); font-size: 10px; letter-spacing: .5px; padding: 5px 11px; border-radius: 4px; border: 1px solid var(--w2); color: var(--w4); text-decoration: none; transition: all .2s; }
  .store-badge:hover { border-color: var(--goldA); color: var(--gold); }
  .bullets { font-size: 11px; color: var(--w4); line-height: 1.9; border-top: 1px solid var(--w1); padding-top: 10px; margin-top: 10px; }
  .bullets span { color: var(--gold); }
  .cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
  .cards-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .card { background: var(--bg2); border: 1px solid var(--w2); border-radius: 10px; overflow: hidden; transition: border-color .2s, transform .2s; }
  .card:hover { border-color: var(--goldA); transform: translateY(-2px); }
  .card img { width: 100%; height: 150px; object-fit: cover; object-position: top; display: block; }
  .card picture { display: block; } .card picture img { width: 100%; height: 150px; object-fit: cover; object-position: top; display: block; }
  .card-thumb { width: 100%; height: 150px; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 6px; }
  .card-thumb .icon { font-size: 26px; opacity: .6; }
  .card-thumb .label { font-family: var(--mono); font-size: 9px; letter-spacing: 2px; opacity: .5; }
  .card-body { padding: 14px; }
  .card-body h3 { font-size: 13px; font-weight: 600; margin-bottom: 3px; }
  .card-body .studio { font-family: var(--mono); font-size: 9px; color: var(--gold); letter-spacing: 1px; margin-bottom: 8px; }
  .card-body p { font-size: 11px; color: var(--w4); line-height: 1.6; margin-bottom: 8px; }
  .card-wide { display: grid; grid-template-columns: 1fr 2fr; }
  .card-wide img, .card-wide .card-thumb { height: 130px; }
  .card-wide picture { display: block; }
  .card-wide picture img { height: 130px; width: 100%; object-fit: cover; display: block; }
  .hidden { display: none; }

  /* SKILLS */
  #skills h2 { font-size: 36px; font-weight: 700; margin-bottom: 40px; }
  #skills h2 span { color: var(--gold); }
  .skills-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 36px 48px; }
  .skill-group h4 { font-family: var(--mono); font-size: 9px; letter-spacing: 3px; color: var(--w4); margin-bottom: 18px; }
  .xp-bar { margin: 10px 0; }
  .xp-meta { display: flex; justify-content: space-between; font-size: 11px; color: var(--w4); margin-bottom: 4px; }
  .xp-meta .val { color: var(--gold); font-family: var(--mono); }
  .xp-track { height: 5px; background: var(--w1); border-radius: 2px; overflow: hidden; }
  .xp-fill { height: 100%; background: var(--gold); border-radius: 2px; width: 0; transition: width 1.2s cubic-bezier(.4,0,.2,1); }
  .xp-fill.dim { background: var(--w2); }
  .skills-tools { margin-top: 36px; padding-top: 28px; border-top: 1px solid var(--w1); }
  .skills-tools h4 { font-family: var(--mono); font-size: 9px; letter-spacing: 3px; color: var(--w4); margin-bottom: 14px; }
  .achievements { margin-top: 32px; padding-top: 28px; border-top: 1px solid var(--w1); }
  .achievements h4 { font-family: var(--mono); font-size: 9px; letter-spacing: 3px; color: var(--w4); margin-bottom: 14px; }
  .ach-grid { display: flex; flex-wrap: wrap; gap: 8px; }
  .ach { background: var(--goldB); border: 1px solid var(--goldA); border-radius: 4px; padding: 7px 12px; font-size: 11px; color: var(--gold); font-family: var(--mono); }

  /* CAREER */
  #career h2 { font-size: 36px; font-weight: 700; margin-bottom: 40px; }
  #career h2 span { color: var(--gold); }
  .timeline { position: relative; padding-left: 28px; }
  .timeline::before { content: ''; position: absolute; left: 4px; top: 8px; bottom: 8px; width: 1px; background: var(--w1); }
  .tl-item { position: relative; padding: 0 0 36px 20px; }
  .tl-dot { position: absolute; left: -28px; top: 6px; width: 10px; height: 10px; border-radius: 50%; background: var(--gold); }
  .tl-dot.dim { background: var(--w2); }
  .tl-role { font-size: 15px; font-weight: 600; }
  .tl-role.dim { color: var(--w6); }
  .tl-period { font-family: var(--mono); font-size: 10px; color: var(--gold); letter-spacing: 1px; margin: 4px 0 8px; }
  .tl-period.dim { color: rgba(201,168,76,.4); }
  .tl-desc { font-size: 12px; color: var(--w4); line-height: 1.75; }

  /* FOOTER */
  footer { border-top: 1px solid var(--w1); padding: 32px 80px; display: flex; align-items: center; justify-content: space-between; }
  footer p { font-family: var(--mono); font-size: 10px; color: var(--w4); }
  footer .socials { display: flex; gap: 12px; }
  footer .socials a { font-family: var(--mono); font-size: 10px; color: var(--w4); text-decoration: none; letter-spacing: 1px; transition: color .2s; }
  footer .socials a:hover { color: var(--gold); }

  /* ── SLIDESHOW ──────────────────────────────────────── */
  .slideshow-wrap { position: relative; display: block; }
  .slideshow { position: relative; overflow: hidden; display: block; width: 100%; }
  .slideshow .slide { transition: opacity 0.9s ease; display: block; width: 100%; object-fit: cover; object-position: center; }
  .slideshow .slide:not(.active) { position: absolute; top: 0; left: 0; opacity: 0; }
  .slideshow .slide.active { opacity: 1; }
  .card-feat .slideshow, .card-feat .slideshow-wrap { height: 100%; min-height: 420px; }
  .card-feat .slideshow .slide { height: 100%; min-height: 420px; }
  .card .slideshow { height: 150px; }
  .card .slideshow .slide { height: 150px; }
  .card-wide .slideshow { height: 130px; }
  .card-wide .slideshow .slide { height: 130px; }
  .ss-dots { position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); display: flex; gap: 5px; z-index: 3; pointer-events: none; }
  .ss-dot { width: 5px; height: 5px; border-radius: 50%; background: rgba(255,255,255,0.28); transition: background 0.3s; }
  .ss-dot.on { background: var(--gold); }

  /* ── RESPONSIVE ──────────────────────────────────────── */

  @media (max-width: 768px) {
    nav { padding: 14px 20px; }
    .nav-burger { display: flex; }
    .nav-links {
      display: none;
      position: fixed; top: 57px; left: 0; right: 0;
      flex-direction: column; gap: 0;
      background: rgba(12,11,16,.97);
      border-bottom: 1px solid var(--w1);
    }
    .nav-links.open { display: flex; }
    .nav-links a { padding: 16px 20px; border-bottom: 1px solid var(--w1); font-size: 12px; letter-spacing: 2px; }

    section { padding: 80px 24px; }
    #projects { padding-left: 24px; padding-right: 24px; }
    .hero-content { padding: 0 24px; max-width: 100%; }
    .hero-eyebrow { font-size: 9px; letter-spacing: 3px; }
    .hero-name { letter-spacing: -2px; }

    #about .about-grid { grid-template-columns: 1fr; gap: 32px; }

    .card-feat { grid-template-columns: 1fr; }
    .card-feat img, .card-feat picture img { height: 260px; min-height: unset; }
    .card-feat .slideshow, .card-feat .slideshow-wrap { height: 260px; min-height: unset; }
    .card-feat .slideshow .slide { height: 260px; min-height: unset; }
    .cards-grid { grid-template-columns: repeat(2, 1fr); }
    .cards-grid-2 { grid-template-columns: repeat(2, 1fr); }
    .card-wide { grid-template-columns: 1fr; }
    .card-wide img, .card-wide picture img, .card-wide .card-thumb { height: 160px; width: 100%; }
    .card-wide .slideshow, .card-wide .slideshow .slide { height: 160px; width: 100%; }

    .skills-grid { grid-template-columns: 1fr; gap: 32px; }

    footer { flex-direction: column; gap: 12px; text-align: center; padding: 28px 20px; }
  }

  @media (max-width: 480px) {
    nav { padding: 12px 16px; }
    section { padding: 72px 16px; }
    #projects { padding-left: 16px; padding-right: 16px; }
    .hero-content { padding: 0 16px; }

    .cards-grid { grid-template-columns: 1fr; }
    .cards-grid-2 { grid-template-columns: 1fr; }
    .card img, .card picture img, .card-thumb { height: 180px; }
    .card .slideshow, .card .slideshow .slide { height: 180px; }
  }
"""

# ── JS ─────────────────────────────────────────────────────────────────────────

JS = """
(function() {
  // Hero canvas — gold grid + connected particles
  const canvas = document.getElementById('hero-canvas');
  const ctx = canvas.getContext('2d');
  let W, H, pts;

  function init() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
    pts = Array.from({length: 55}, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - .5) * .45, vy: (Math.random() - .5) * .45
    }));
  }

  function tick() {
    ctx.fillStyle = '#0c0b10';
    ctx.fillRect(0, 0, W, H);

    ctx.strokeStyle = 'rgba(201,168,76,0.04)';
    ctx.lineWidth = .5;
    for (let x = 0; x < W; x += 60) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
    for (let y = 0; y < H; y += 60) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }

    pts.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
    });

    pts.forEach((a, i) => {
      pts.slice(i + 1).forEach(b => {
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < 140) {
          ctx.strokeStyle = `rgba(201,168,76,${(1 - d / 140) * .22})`;
          ctx.lineWidth = .8;
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      });
      ctx.fillStyle = 'rgba(201,168,76,.7)';
      ctx.beginPath(); ctx.arc(a.x, a.y, 1.5, 0, Math.PI * 2); ctx.fill();
    });

    requestAnimationFrame(tick);
  }

  init();
  window.addEventListener('resize', init);
  tick();
})();

// Nav hamburger
function toggleNav() {
  const links  = document.querySelector('.nav-links');
  const burger = document.querySelector('.nav-burger');
  links.classList.toggle('open');
  burger.classList.toggle('open');
}
document.querySelectorAll('.nav-links a').forEach(function(a) {
  a.addEventListener('click', function() {
    document.querySelector('.nav-links').classList.remove('open');
    document.querySelector('.nav-burger').classList.remove('open');
  });
});

// XP bars — animate on scroll into view
(function() {
  let fired = false;
  const obs = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting && !fired) {
      fired = true;
      document.querySelectorAll('.xp-fill').forEach(function(el, i) {
        setTimeout(function() { el.style.width = el.dataset.w + '%'; }, i * 100);
      });
    }
  }, { threshold: 0.3 });
  const section = document.getElementById('skills');
  if (section) obs.observe(section);
})();

// Project filter
function filterCards(cat, btn) {
  document.querySelectorAll('.filter-btn').forEach(function(b) { b.classList.remove('on'); });
  btn.classList.add('on');
  document.querySelectorAll('[data-cat]').forEach(function(el) {
    const show = cat === 'all' || el.dataset.cat === cat;
    el.classList.toggle('hidden', !show);
    el.style.display = show ? '' : 'none';
  });
}

// Slideshows — auto-advance every 5 seconds with crossfade
(function() {
  function initSlideshow(wrap) {
    var ss     = wrap.querySelector('.slideshow');
    var slides = ss ? ss.querySelectorAll('.slide') : [];
    if (slides.length < 2) return;
    var dots = wrap.querySelectorAll('.ss-dot');
    var idx  = 0;
    slides[0].classList.add('active');
    if (dots.length) dots[0].classList.add('on');

    // Preload next images on first tick
    setInterval(function() {
      slides[idx].classList.remove('active');
      if (dots.length) dots[idx].classList.remove('on');
      idx = (idx + 1) % slides.length;
      slides[idx].classList.add('active');
      if (dots.length) dots[idx].classList.add('on');
    }, 5000);
  }
  document.querySelectorAll('.slideshow-wrap').forEach(initSlideshow);
})();
"""

# ── Content loading ────────────────────────────────────────────────────────────

def load_lang(filename, lang):
    """Load from content/en/ when lang='en', fall back to content/ if not found."""
    if lang == 'en':
        en_path = CONTENT_EN / filename
        if en_path.exists():
            with open(en_path, encoding='utf-8') as f:
                return json.load(f)
    return load(filename)


# ── HTML helpers ───────────────────────────────────────────────────────────────

def desc(text):
    """Convert bare newlines to <br> for safety."""
    return text.replace('\n', '<br>')


def chip(text, dim=False):
    cls = 'chip dim' if dim else 'chip'
    return f'<span class="{cls}">{text}</span>'


def chips_html(tags, tags_secondary=None):
    parts = [chip(t) for t in (tags or [])]
    parts += [chip(t, dim=True) for t in (tags_secondary or [])]
    return '<div class="chips">' + ''.join(parts) + '</div>'


_ANDROID_ICON = (
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink:0">'
    '<path d="M3 22V2l18 10L3 22z"/>'
    '</svg>'
)
_IOS_ICON = (
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink:0">'
    '<path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>'
    '</svg>'
)


def _title_link(p):
    link  = p.get('link', '')
    title = p['title']
    if link:
        return f'<h3><a href="{link}" target="_blank" rel="noopener" class="card-title-link">{title}</a></h3>'
    return f'<h3>{title}</h3>'


def store_links_html(p):
    android = p.get('link_android', '')
    ios     = p.get('link_ios', '')
    if not android and not ios:
        return ''
    parts = []
    if android:
        parts.append(
            f'<a href="{android}" target="_blank" rel="noopener" class="store-badge">'
            f'{_ANDROID_ICON}Google Play</a>'
        )
    if ios:
        parts.append(
            f'<a href="{ios}" target="_blank" rel="noopener" class="store-badge">'
            f'{_IOS_ICON}App Store</a>'
        )
    return '<div class="store-links">' + ''.join(parts) + '</div>'


def img_html(p):
    """
    Returns one of:
    - <div class="slideshow-wrap"> with crossfade slides if p['images'] has >1 entry
    - <picture> with mobile srcset if a -mobile variant file exists
    - plain <img>
    - placeholder <div> if no image data at all
    """
    local    = p.get('image', '')
    fallback = p.get('image_url_fallback', '')
    images   = p.get('images') or ([local] if local else [])

    icon_map    = {'game': '&#9830;', 'data': '&#128202;', 'web': '&#127760;'}
    icon        = icon_map.get(p['category'], '&#9830;')
    placeholder = (
        f'<div class="card-thumb" style="background:linear-gradient(135deg,#1a1820,#0c0b10);">'
        f'<div class="icon">{icon}</div>'
        f'<div class="label">{p["title"].upper()}</div>'
        f'</div>'
    )

    if not images and not fallback:
        return placeholder

    # ── Slideshow (multiple images) ──────────────────────
    if len(images) > 1:
        slides = ''
        for i, src in enumerate(images):
            loading = 'eager' if i == 0 else 'lazy'
            err = f'onerror="this.src=\'{fallback}\'"' if (i == 0 and fallback) else 'onerror="this.style.display=\'none\'"'
            slides += f'<img src="{src}" class="slide" alt="{p["title"]}" {err} loading="{loading}">'
        dots = ''.join('<div class="ss-dot"></div>' for _ in images)
        return (
            f'<div class="slideshow-wrap">'
            f'<div class="slideshow">{slides}</div>'
            f'<div class="ss-dots">{dots}</div>'
            f'</div>'
        )

    # ── Single image ─────────────────────────────────────
    src     = (images[0] if images else '') or fallback
    if not src:
        return placeholder

    onerror = f'onerror="this.src=\'{fallback}\'"' if (src != fallback and fallback) else 'onerror="this.style.opacity=\'0\'"'

    # Check for -mobile variant (e.g. midasmerge-mobile.jpg)
    if src.startswith('assets/'):
        lpath       = Path(src)
        mobile_full = ROOT / lpath.parent / (lpath.stem + '-mobile' + lpath.suffix)
        if mobile_full.exists():
            mobile_src = str(lpath.parent / (lpath.stem + '-mobile' + lpath.suffix)).replace('\\', '/')
            return (
                f'<picture>'
                f'<source media="(max-width:480px)" srcset="{mobile_src}">'
                f'<img src="{src}" alt="{p["title"]}" {onerror} loading="lazy">'
                f'</picture>'
            )

    return f'<img src="{src}" alt="{p["title"]}" {onerror} loading="lazy">'


# ── Section renderers ──────────────────────────────────────────────────────────

def render_nav(h, lang):
    L = LABELS[lang]
    active_pt = 'active' if lang == 'pt' else ''
    active_en = 'active' if lang == 'en' else ''
    return f"""<!-- NAV -->
<nav>
  <div class="nav-logo">EC</div>
  <button class="nav-burger" onclick="toggleNav()" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
  <div class="nav-links">
    <a href="#about">{L['nav_about']}</a>
    <a href="#projects">{L['nav_projects']}</a>
    <a href="#skills">{L['nav_skills']}</a>
    <a href="#career">{L['nav_career']}</a>
  </div>
  <div class="nav-lang">
    <a href="{h.get('lang_pt', 'indexPT.html')}" class="{active_pt}">PT</a>
    <a href="{h.get('lang_en', 'index.html')}" class="{active_en}">EN</a>
  </div>
</nav>"""


def render_hero(h):
    first, *rest = h['name'].split(' ', 1)
    last = rest[0] if rest else ''
    return f"""
<!-- HERO -->
<section id="hero" style="padding:0;max-width:100%;">
  <canvas id="hero-canvas"></canvas>
  <div class="hero-content">
    <div class="hero-eyebrow">{h['eyebrow']}</div>
    <h1 class="hero-name">{first}<br><span>{last}</span></h1>
    <div class="sep"></div>
    <p class="hero-sub">{h['subtitle']}<br>{h['location']}</p>
    <div class="hero-ctas">
      <a href="{h['cta_primary_href']}" class="btn-primary">{h['cta_primary_label']}</a>
      <a href="{h['cta_secondary_href']}" target="_blank" class="btn-ghost">{h['cta_secondary_label']}</a>
    </div>
    <div class="hero-socials">
      <a href="mailto:{h['email']}" title="Email">@</a>
      <a href="{h['github']}" target="_blank" title="GitHub" style="font-size:11px;">gh</a>
    </div>
  </div>
  <div class="hero-scroll"><div class="scroll-line"></div><span>scroll</span></div>
</section>"""


def render_about(a, lang):
    L = LABELS[lang]
    name_parts = a.get('name', 'Erick Cruz').split(' ', 1)
    first, last = name_parts[0], (name_parts[1] if len(name_parts) > 1 else '')
    bio = ''.join(f'<p>{p}</p>' for p in a['bio_paragraphs'])
    stats = ''.join(
        f'<div class="stat-box"><div class="stat-val">{s["value"]}</div><div class="stat-lbl">{s["label"]}</div></div>'
        for s in a['stats']
    )
    primary_chips   = ''.join(chip(s) for s in a['skills_primary'])
    secondary_chips = ''.join(chip(s, dim=True) for s in a['skills_secondary'])
    skill_chips = f'<div class="chips" style="margin-top:20px;">{primary_chips}</div><div class="chips" style="margin-top:8px;">{secondary_chips}</div>'
    return f"""
<!-- ABOUT -->
<section id="about">
  <span class="section-label">{L['section_about']}</span>
  <div class="about-grid">
    <div class="about-text">
      <h2>{first} <span>{last}</span></h2>
      <div class="sep"></div>
      {bio}
      {skill_chips}
    </div>
    <div>
      <div class="stats-grid">
        {stats}
        <div class="current-box">
          <div class="lbl">{L['current_company']}</div>
          <div class="val">{a['current_company']}</div>
          <div class="sub">{a['current_role']} · {a.get('current_location', '')}</div>
        </div>
      </div>
    </div>
  </div>
</section>"""


def _card_featured(p):
    bullets = ''
    if p.get('bullets'):
        items   = ''.join(f'<span>·</span> {b}<br>' for b in p['bullets'])
        bullets = f'<div class="bullets">{items}</div>'
    return f"""
  <div class="card-feat" data-cat="{p['category']}">
    {img_html(p)}
    <div class="card-feat-body">
      {_title_link(p)}
      <div class="studio">{p.get('studio_label', '').upper()}</div>
      <p>{desc(p['description'])}</p>
      {bullets}
      {chips_html(p.get('tags'), p.get('tags_secondary'))}
      {store_links_html(p)}
    </div>
  </div>"""


def _card_grid(p):
    return f"""
    <div class="card" data-cat="{p['category']}">
      {img_html(p)}
      <div class="card-body">
        {_title_link(p)}
        <div class="studio">{p.get('studio_label', '').upper()}</div>
        <p>{desc(p['description'])}</p>
        {chips_html(p.get('tags'), p.get('tags_secondary'))}
        {store_links_html(p)}
      </div>
    </div>"""


def _card_wide(p):
    return f"""
  <div class="card card-wide" data-cat="{p['category']}" style="display:grid;">
    {img_html(p)}
    <div class="card-body" style="padding:18px 20px;">
      <h3>{p['title']}</h3>
      <div class="studio">{p.get('studio_label', '').upper()}</div>
      <p>{desc(p['description'])}</p>
      {chips_html(p.get('tags'), p.get('tags_secondary'))}
    </div>
  </div>"""


CARD_RENDERERS = {'featured': _card_featured, 'grid': _card_grid, 'wide': _card_wide}


def render_projects(data, lang):
    L        = LABELS[lang]
    projects = data['projects']

    def by_section(section, layout=None):
        return [p for p in projects
                if p.get('section') == section
                and (layout is None or p['layout'] == layout)]

    wildlife_feat = by_section('wildlife', 'featured')
    wildlife_grid = by_section('wildlife', 'grid')
    prev_feat     = by_section('previous', 'featured')
    prev_grid     = by_section('previous', 'grid')
    academic      = by_section('academic')
    data_proj     = by_section('data')
    web_proj      = by_section('web')

    feat_html      = ''.join(_card_featured(p) for p in wildlife_feat)
    wgrid_html     = '<div class="cards-grid">' + ''.join(_card_grid(p) for p in wildlife_grid) + '</div>' if wildlife_grid else ''
    prev_feat_html = ''.join(_card_featured(p) for p in prev_feat)
    prev_html      = '<div class="cards-grid-2">' + ''.join(_card_grid(p) for p in prev_grid) + '</div>' if prev_grid else ''
    acad_feat  = [p for p in academic if p['layout'] == 'featured']
    acad_grid  = [p for p in academic if p['layout'] == 'grid']
    acad_other = [p for p in academic if p['layout'] not in ('featured', 'grid')]
    academic_html = (
        ''.join(_card_featured(p) for p in acad_feat) +
        ('<div class="cards-grid-2">' + ''.join(_card_grid(p) for p in acad_grid) + '</div>' if acad_grid else '') +
        ''.join(CARD_RENDERERS[p['layout']](p) for p in acad_other)
    )
    data_html      = '<div class="cards-grid-2">' + ''.join(CARD_RENDERERS[p['layout']](p) for p in data_proj) + '</div>' if data_proj else ''
    web_html       = '<div class="cards-grid-2">' + ''.join(CARD_RENDERERS[p['layout']](p) for p in web_proj) + '</div>' if web_proj else ''

    return f"""
<!-- PROJECTS -->
<section id="projects">
  <span class="section-label">{L['section_projects']}</span>
  <h2>{L['proj_h2_a']} <span>{L['proj_h2_b']}</span></h2>
  <div style="height:8px;"></div>

  <div class="filter-bar">
    <button class="filter-btn on" onclick="filterCards('all',this)">{L['filter_all']}</button>
    <button class="filter-btn" onclick="filterCards('game',this)">{L['filter_game']}</button>
    <button class="filter-btn" onclick="filterCards('academic',this)">{L['filter_academic']}</button>
    <button class="filter-btn" onclick="filterCards('data',this)">{L['filter_data']}</button>
    <button class="filter-btn" onclick="filterCards('web',this)">{L['filter_web']}</button>
  </div>

  <div class="section-divider" data-cat="game">{L['div_wildlife']}<span>{L['div_wildlife_period']}</span></div>
  {feat_html}
  {wgrid_html}

  <div class="sub-label" data-cat="game">{L['div_previous']}</div>
  {prev_feat_html}
  {prev_html}

  <div class="sub-label" data-cat="academic">{L['div_academic']}</div>
  {academic_html}

  <div class="sub-label" data-cat="data">{L['div_data']}</div>
  {data_html}

  <div class="sub-label" data-cat="web">{L['div_web']}</div>
  {web_html}
</section>"""


def render_skills(s, lang):
    L = LABELS[lang]

    groups_html = ''
    for g in s['groups']:
        chips = ''.join(chip(sk) for sk in g['skills'])
        groups_html += f"""
    <div class="skill-group">
      <h4>{g['label']}</h4>
      <div class="chips" style="margin-top:10px;">{chips}</div>
    </div>"""

    ach_html = ''.join(f'<span class="ach">{a}</span>' for a in s['achievements'])

    return f"""
<!-- SKILLS -->
<section id="skills">
  <span class="section-label">{L['section_skills']}</span>
  <h2>{L['skills_h2_a']} <span>{L['skills_h2_b']}</span></h2>
  <div class="skills-grid">{groups_html}
  </div>
  <div class="achievements">
    <h4>{L['ach_label']}</h4>
    <div class="ach-grid">{ach_html}</div>
  </div>
</section>"""


def render_career(c, lang):
    L     = LABELS[lang]
    items = []
    for i, e in enumerate(c['entries']):
        dot_cls    = 'tl-dot' if e.get('active') else 'tl-dot dim'
        role_cls   = 'tl-role' if e.get('active') else 'tl-role dim'
        period_cls = 'tl-period' if e.get('active') else 'tl-period dim'
        tags       = chips_html(e.get('tags'), e.get('tags_secondary')) if e.get('tags') else ''
        pb_style   = 'padding-bottom:0;' if i == len(c['entries']) - 1 else ''
        items.append(f"""
    <div class="tl-item" style="{pb_style}">
      <div class="{dot_cls}"></div>
      <div class="{role_cls}">{e['role']} · {e['company']}</div>
      <div class="{period_cls}">{e['period']} · {e['location']}</div>
      <div class="tl-desc">{desc(e['description'])}</div>
      <div class="tl-tags chips" style="margin-top:10px;">{tags}</div>
    </div>""")

    return f"""
<!-- CAREER -->
<section id="career">
  <span class="section-label">{L['section_career']}</span>
  <h2>{L['career_h2_a']} <span>{L['career_h2_b']}</span></h2>
  <div class="timeline">{''.join(items)}
  </div>
</section>"""


# ── Entry point ────────────────────────────────────────────────────────────────

def build(lang='pt'):
    print(f"\n  [{lang.upper()}] Carregando dados...")
    hero   = load_lang("hero.json",    lang)
    about  = load_lang("about.json",   lang)
    proj   = load_lang("projects.json",lang)
    skills = load_lang("skills.json",  lang)
    career = load_lang("career.json",  lang)
    year   = datetime.date.today().year
    L      = LABELS[lang]
    out    = OUTPUTS[lang]

    print(f"  [{lang.upper()}] Gerando HTML...")
    html = f"""<!DOCTYPE html>
<html lang="{L['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{hero['name']} — Senior Game Engineer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

{render_nav(hero, lang)}
{render_hero(hero)}
{render_about(about, lang)}
{render_projects(proj, lang)}
{render_skills(skills, lang)}
{render_career(career, lang)}

<!-- FOOTER -->
<footer>
  <p>&copy; {year} {hero['name']} &middot; {hero['email']}</p>
  <div class="socials">
    <a href="{hero['github']}" target="_blank">GitHub</a>
    <a href="{hero['cta_secondary_href']}" target="_blank">LinkedIn</a>
    <a href="mailto:{hero['email']}">Email</a>
  </div>
</footer>

<script>{JS}</script>
</body>
</html>"""

    out.write_text(html, encoding='utf-8')
    print(f"  [{lang.upper()}] Gerado: {out}")


if __name__ == "__main__":
    build('pt')
    build('en')
    print(f"\n  PT: file:///{str(OUTPUTS['pt']).replace(chr(92), '/')}")
    print(f"  EN: file:///{str(OUTPUTS['en']).replace(chr(92), '/')}")
    input("\n  [ Enter para fechar ] ")
