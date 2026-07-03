"""
ui.py
-----
Self-contained HTML page for the Gmail AI Agent chat interface.
Imported by main.py and served at GET /.
The POST /chat backend endpoint is called via fetch() — no coupling changes.
"""

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Gmail AI Agent · IBM WatsonX</title>
<style>
/* ─────────────────────────────────────────────
   RESET
───────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }

/* ─────────────────────────────────────────────
   ROOT TOKENS
───────────────────────────────────────────── */
:root {
  --bg:          #07090f;
  --surface:     rgba(255,255,255,0.04);
  --surface2:    rgba(255,255,255,0.07);
  --border:      rgba(255,255,255,0.09);
  --border2:     rgba(255,255,255,0.14);
  --text:        #e8eaed;
  --text-muted:  rgba(232,234,237,0.45);
  --blue:        #4285f4;
  --blue-dim:    rgba(66,133,244,0.18);
  --blue-glow:   rgba(66,133,244,0.35);
  --red:         #ea4335;
  --green:       #34a853;
  --yellow:      #fbbc04;
  --sidebar-w:   270px;
}

/* ─────────────────────────────────────────────
   BODY & STARFIELD BACKGROUND
───────────────────────────────────────────── */
body {
  font-family: "Google Sans", "Segoe UI", system-ui, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text);
  background: var(--bg);
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

/* Deep-space mesh wallpaper */
body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background:
    /* Gmail colors as large soft glows */
    radial-gradient(ellipse 90% 70% at 15%  5%,  rgba(66,133,244,0.22) 0%, transparent 55%),
    radial-gradient(ellipse 70% 55% at 85% 85%,  rgba(234,67,53,0.16)  0%, transparent 50%),
    radial-gradient(ellipse 55% 65% at 65% 25%,  rgba(52,168,83,0.11)  0%, transparent 50%),
    radial-gradient(ellipse 80% 45% at 5%  75%,  rgba(251,188,4,0.10)  0%, transparent 50%),
    /* Subtle star-like noise */
    radial-gradient(ellipse 30% 30% at 50% 50%,  rgba(66,133,244,0.06) 0%, transparent 70%);
}

/* Floating particle dots */
body::after {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background-image:
    radial-gradient(circle 1.5px at 10%  20%, rgba(255,255,255,0.25) 0%, transparent 100%),
    radial-gradient(circle 1px   at 25%  65%, rgba(255,255,255,0.18) 0%, transparent 100%),
    radial-gradient(circle 2px   at 45%  15%, rgba(66,133,244,0.4)   0%, transparent 100%),
    radial-gradient(circle 1px   at 60%  75%, rgba(255,255,255,0.15) 0%, transparent 100%),
    radial-gradient(circle 1.5px at 75%  35%, rgba(52,168,83,0.35)   0%, transparent 100%),
    radial-gradient(circle 1px   at 88%  55%, rgba(255,255,255,0.20) 0%, transparent 100%),
    radial-gradient(circle 2px   at 30%  88%, rgba(234,67,53,0.30)   0%, transparent 100%),
    radial-gradient(circle 1px   at 92%  18%, rgba(251,188,4,0.35)   0%, transparent 100%),
    radial-gradient(circle 1px   at 55%  50%, rgba(255,255,255,0.12) 0%, transparent 100%),
    radial-gradient(circle 1.5px at 18%  45%, rgba(66,133,244,0.28)  0%, transparent 100%);
}

/* ─────────────────────────────────────────────
   HEADER
───────────────────────────────────────────── */
header {
  position: relative;
  z-index: 20;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0 24px;
  height: 62px;
  background: rgba(7,9,15,0.75);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}

/* Coloured accent line under header */
header::after {
  content: "";
  position: absolute;
  bottom: -1px; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    var(--blue) 0%, var(--green) 33%, var(--yellow) 66%, var(--red) 100%);
  opacity: 0.7;
}

/* Gmail logo mark */
.hd-logo {
  flex-shrink: 0;
  width: 36px; height: 36px;
  border-radius: 8px;
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border2);
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 18px rgba(66,133,244,0.25);
}

.hd-text { flex: 1; min-width: 0; }
.hd-text h1 {
  font-size: 16px; font-weight: 700;
  letter-spacing: -0.2px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.hd-text p {
  font-size: 11px; color: var(--text-muted);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

/* IBM WatsonX pill */
.hd-watsonx {
  display: flex; align-items: center; gap: 8px;
  padding: 5px 12px 5px 8px;
  border-radius: 22px;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border2);
  flex-shrink: 0;
}
.hd-watsonx-logo {
  width: 22px; height: 22px; border-radius: 5px;
  background: linear-gradient(135deg, #1d3bd1, #4285f4);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 900; color: #fff;
  font-family: "IBM Plex Sans", sans-serif;
  letter-spacing: -0.5px;
}
.hd-watsonx span { font-size: 11px; font-weight: 600; color: var(--text-muted); }
.hd-watsonx strong { font-size: 11px; font-weight: 700; color: #7baaf7; }

/* Live dot */
.hd-live {
  display: flex; align-items: center; gap: 6px;
  font-size: 11px; font-weight: 600;
  color: #57bb6e; flex-shrink: 0;
}
.hd-live::before {
  content: "";
  width: 7px; height: 7px; border-radius: 50%;
  background: #57bb6e;
  box-shadow: 0 0 8px #57bb6e;
  animation: livepulse 2s ease-in-out infinite;
}
@keyframes livepulse { 0%,100%{ opacity:1; box-shadow:0 0 8px #57bb6e; } 50%{ opacity:0.5; box-shadow:0 0 3px #57bb6e; } }

/* ─────────────────────────────────────────────
   LAYOUT
───────────────────────────────────────────── */
.layout {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* ─────────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────────── */
.sidebar {
  width: var(--sidebar-w);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: rgba(7,9,15,0.6);
  border-right: 1px solid var(--border);
  backdrop-filter: blur(12px);
  overflow-y: auto;
  overflow-x: hidden;
  padding: 18px 12px 24px;
  gap: 4px;
}
.sidebar::-webkit-scrollbar { width: 3px; }
.sidebar::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

/* Sidebar brand block */
.sb-brand {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px 16px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 8px;
  flex-shrink: 0;
}
.sb-brand-icon {
  width: 40px; height: 40px; border-radius: 10px;
  background: linear-gradient(135deg, rgba(66,133,244,0.25), rgba(52,168,83,0.15));
  border: 1px solid var(--border2);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.sb-brand-text p  { font-size: 13px; font-weight: 700; color: var(--text); }
.sb-brand-text span { font-size: 11px; color: var(--text-muted); }

.sb-label {
  font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; color: rgba(232,234,237,0.28);
  padding: 10px 10px 5px;
}

.sb-btn {
  display: flex; align-items: flex-start; gap: 10px;
  width: 100%;
  padding: 9px 12px;
  border-radius: 9px;
  border: 1px solid transparent;
  background: transparent;
  color: rgba(232,234,237,0.7);
  font-size: 13px; font-family: inherit;
  line-height: 1.4;
  text-align: left; cursor: pointer;
  transition: all 0.15s ease;
  flex-shrink: 0;
}
.sb-btn:hover {
  background: var(--surface2);
  border-color: var(--border2);
  color: var(--text);
  transform: translateX(2px);
}
.sb-btn .sb-icon {
  font-size: 15px; flex-shrink: 0; margin-top: 1px; width: 20px; text-align: center;
}
.sb-btn .sb-sub { font-size: 10px; color: var(--text-muted); margin-top: 1px; display: block; }

.sb-divider { height: 1px; background: var(--border); margin: 8px 4px; flex-shrink: 0; }

/* Sidebar info card */
.sb-card {
  margin-top: auto;
  padding: 14px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(66,133,244,0.1), rgba(52,168,83,0.06));
  border: 1px solid rgba(66,133,244,0.22);
  flex-shrink: 0;
}
.sb-card-title { font-size: 12px; font-weight: 700; color: #7baaf7; margin-bottom: 6px; }
.sb-card p { font-size: 11px; color: var(--text-muted); line-height: 1.55; }

/* Sidebar model badge */
.sb-model {
  display: flex; align-items: center; gap: 8px;
  padding: 9px 12px;
  border-radius: 9px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  margin: 4px 0 8px;
  flex-shrink: 0;
}
.sb-model-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: linear-gradient(135deg, var(--blue), var(--green));
  flex-shrink: 0;
}
.sb-model span { font-size: 11px; color: var(--text-muted); }
.sb-model strong { font-size: 11px; font-weight: 700; color: var(--text); }

/* ─────────────────────────────────────────────
   CHAT COLUMN
───────────────────────────────────────────── */
.chat-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* ── HERO (empty state) ── */
.hero {
  flex: 1;
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 48px 24px;
  text-align: center;
}
.hero.visible { display: flex; }

/* Big Gmail icon */
.hero-icon-wrap {
  position: relative;
  width: 96px; height: 96px;
}
.hero-icon-ring {
  position: absolute; inset: -6px;
  border-radius: 28px;
  border: 1.5px solid transparent;
  background: linear-gradient(135deg, rgba(66,133,244,0.5), rgba(52,168,83,0.4), rgba(234,67,53,0.4)) border-box;
  -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: destination-out;
  mask-composite: exclude;
  animation: spin-ring 8s linear infinite;
}
@keyframes spin-ring { to { transform: rotate(360deg); } }
.hero-icon {
  width: 96px; height: 96px;
  border-radius: 22px;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border2);
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 12px 40px rgba(66,133,244,0.25), 0 0 0 1px rgba(255,255,255,0.04);
}

.hero h2 { font-size: 28px; font-weight: 700; letter-spacing: -0.5px; }
.hero h2 span { background: linear-gradient(90deg, #4285f4, #34a853); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero > p { font-size: 14px; color: var(--text-muted); max-width: 420px; }

/* Capability cards */
.hero-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  max-width: 500px;
  width: 100%;
  margin-top: 6px;
}
.hero-card {
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  text-align: left;
  cursor: pointer;
  transition: all 0.16s ease;
}
.hero-card:hover {
  background: var(--surface2);
  border-color: rgba(66,133,244,0.35);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(66,133,244,0.15);
}
.hero-card .hc-icon { font-size: 20px; margin-bottom: 6px; }
.hero-card .hc-title { font-size: 13px; font-weight: 600; color: var(--text); }
.hero-card .hc-desc  { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

/* ── MESSAGES ── */
#messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  scroll-behavior: smooth;
}
#messages::-webkit-scrollbar { width: 4px; }
#messages::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

.msg { display: flex; gap: 12px; max-width: 880px; width: 100%; align-self: flex-start; }
.msg.user { align-self: flex-end; flex-direction: row-reverse; }

/* Avatars */
.msg-av {
  width: 34px; height: 34px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; font-weight: 700; font-size: 11px;
  margin-top: 2px;
}
.msg.user  .msg-av {
  background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
  color: #fff; font-size: 10px;
  box-shadow: 0 2px 10px rgba(66,133,244,0.4);
}
.msg.agent .msg-av {
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border2);
}

/* Bubbles */
.msg-body { display: flex; flex-direction: column; gap: 4px; max-width: calc(100% - 46px); }
.msg-name { font-size: 11px; font-weight: 600; color: var(--text-muted); padding: 0 4px; }
.msg.user .msg-name { text-align: right; }
.msg-bubble {
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px; line-height: 1.65;
}
.msg.user .msg-bubble {
  background: linear-gradient(135deg, rgba(66,133,244,0.38), rgba(66,133,244,0.22));
  border: 1px solid rgba(66,133,244,0.4);
  border-bottom-right-radius: 5px;
  color: var(--text);
}
.msg.agent .msg-bubble {
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border);
  border-bottom-left-radius: 5px;
  color: var(--text);
  white-space: pre-wrap;
  font-family: inherit;
}

/* Email list styling inside agent bubble */
.msg.agent .msg-bubble .email-item {
  border-bottom: 1px solid rgba(255,255,255,0.07);
  padding: 6px 0;
}
.msg.agent .msg-bubble .email-item:last-child { border-bottom: none; }

/* Timestamp */
.msg-ts { font-size: 10px; color: rgba(232,234,237,0.22); padding: 0 4px; }
.msg.user .msg-ts { text-align: right; }

/* ── TYPING ── */
.typing-wrap {
  display: none;
  align-items: center;
  gap: 12px;
  padding: 0 28px 6px;
}
.typing-wrap.on { display: flex; }

.typing-bubble {
  display: flex; gap: 5px;
  padding: 10px 16px;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border);
  border-radius: 16px;
  border-bottom-left-radius: 5px;
}
.typing-bubble span {
  width: 7px; height: 7px; border-radius: 50%;
  background: rgba(255,255,255,0.35);
  animation: tdot 1.3s ease-in-out infinite;
}
.typing-bubble span:nth-child(2) { animation-delay: 0.18s; }
.typing-bubble span:nth-child(3) { animation-delay: 0.36s; }
@keyframes tdot {
  0%,60%,100% { transform: translateY(0); background: rgba(255,255,255,0.3); }
  30% { transform: translateY(-7px); background: #7baaf7; }
}

.typing-label {
  font-size: 11px; color: var(--text-muted);
  animation: fadeinout 1.8s ease-in-out infinite;
}
@keyframes fadeinout { 0%,100%{ opacity:0.4; } 50%{ opacity:1; } }

/* ── INPUT BAR ── */
.input-wrap {
  flex-shrink: 0;
  padding: 14px 24px 18px;
  background: rgba(7,9,15,0.7);
  border-top: 1px solid var(--border);
  backdrop-filter: blur(16px);
}

.input-box {
  display: flex; align-items: flex-end; gap: 10px;
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border2);
  border-radius: 18px;
  padding: 10px 10px 10px 18px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.input-box:focus-within {
  border-color: rgba(66,133,244,0.6);
  box-shadow: 0 0 0 3px rgba(66,133,244,0.12), 0 2px 20px rgba(66,133,244,0.1);
}

#userInput {
  flex: 1; background: transparent;
  border: none; outline: none;
  color: var(--text); font-size: 14px;
  font-family: inherit; resize: none;
  min-height: 26px; max-height: 150px;
  line-height: 1.55; overflow-y: auto;
}
#userInput::placeholder { color: rgba(232,234,237,0.28); }

#sendBtn {
  width: 40px; height: 40px; border-radius: 12px;
  border: none; flex-shrink: 0;
  background: linear-gradient(135deg, #4285f4 0%, #1a6fe8 100%);
  color: #fff; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 3px 12px rgba(66,133,244,0.45);
  transition: transform 0.12s, opacity 0.15s, box-shadow 0.2s;
}
#sendBtn:hover  { transform: scale(1.06); box-shadow: 0 5px 18px rgba(66,133,244,0.55); }
#sendBtn:active { transform: scale(0.96); }
#sendBtn:disabled { opacity: 0.3; cursor: not-allowed; transform: none; box-shadow: none; }
#sendBtn svg { width: 18px; height: 18px; }

.input-footer {
  display: flex; justify-content: space-between; align-items: center;
  padding: 6px 4px 0;
}
.input-hint { font-size: 11px; color: rgba(232,234,237,0.2); }
.input-api-note { font-size: 10px; color: rgba(232,234,237,0.15); }

/* ─────────────────────────────────────────────
   WATERMARK
───────────────────────────────────────────── */
.watermark {
  position: fixed; bottom: 74px; right: 18px;
  z-index: 30; pointer-events: none;
  display: flex; align-items: center; gap: 6px;
  font-size: 10px; color: rgba(232,234,237,0.18);
}
.watermark-icon {
  width: 16px; height: 16px; border-radius: 4px;
  background: linear-gradient(135deg,#1d3bd1,#4285f4);
  display: flex; align-items: center; justify-content: center;
  font-size: 9px; font-weight: 900; color: #fff;
}

/* ─────────────────────────────────────────────
   SCROLLBAR (Firefox)
───────────────────────────────────────────── */
#messages { scrollbar-width: thin; scrollbar-color: var(--border2) transparent; }
.sidebar   { scrollbar-width: thin; scrollbar-color: var(--border2) transparent; }
</style>
</head>
<body>

<!-- ═══════════════════ HEADER ═══════════════════ -->
<header>
  <div class="hd-logo">
    <!-- Gmail SVG envelope -->
    <svg viewBox="0 0 48 48" width="24" height="24" xmlns="http://www.w3.org/2000/svg">
      <path fill="#4285F4" d="M6 40h6V22.8L6 18v20a2 2 0 0 0 2 2z"/>
      <path fill="#34A853" d="M36 40h6a2 2 0 0 0 2-2V18l-8 4.8V40z"/>
      <path fill="#FBBC04" d="M36 10H12l12 8 12-8z"/>
      <path fill="#EA4335" d="M6 18l6 4.8L24 18l12 4.8L42 18 24 10 6 18z"/>
    </svg>
  </div>

  <div class="hd-text">
    <h1>Gmail AI Agent</h1>
    <p>Natural language inbox management · LangGraph ReAct</p>
  </div>

  <div class="hd-watsonx">
    <div class="hd-watsonx-logo">W</div>
    <span>IBM WatsonX &nbsp;</span><strong>granite-4-h-small</strong>
  </div>

  <div class="hd-live">Live</div>
</header>

<!-- ═══════════════════ LAYOUT ═══════════════════ -->
<div class="layout">

  <!-- ════ SIDEBAR ════ -->
  <aside class="sidebar">

    <div class="sb-brand">
      <div class="sb-brand-icon">
        <svg viewBox="0 0 48 48" width="24" height="24" xmlns="http://www.w3.org/2000/svg">
          <path fill="#4285F4" d="M6 40h6V22.8L6 18v20a2 2 0 0 0 2 2z"/>
          <path fill="#34A853" d="M36 40h6a2 2 0 0 0 2-2V18l-8 4.8V40z"/>
          <path fill="#FBBC04" d="M36 10H12l12 8 12-8z"/>
          <path fill="#EA4335" d="M6 18l6 4.8L24 18l12 4.8L42 18 24 10 6 18z"/>
        </svg>
      </div>
      <div class="sb-brand-text">
        <p>Gmail Agent</p>
        <span>AI-powered inbox</span>
      </div>
    </div>

    <!-- Active model -->
    <div class="sb-model">
      <div class="sb-model-dot"></div>
      <div>
        <span>Model &nbsp;</span><strong>granite-4-h-small</strong>
      </div>
    </div>

    <div class="sb-label">Read</div>
    <button class="sb-btn" onclick="send('List my last 5 emails')">
      <span class="sb-icon">📋</span>
      <span>List last 5 emails<span class="sb-sub">Inbox overview</span></span>
    </button>
    <button class="sb-btn" onclick="send('Show my unread emails')">
      <span class="sb-icon">📬</span>
      <span>Unread emails<span class="sb-sub">Filter unread only</span></span>
    </button>
    <button class="sb-btn" onclick="send('Show emails from my boss')">
      <span class="sb-icon">👤</span>
      <span>Emails from a sender<span class="sb-sub">Filter by person</span></span>
    </button>
    <button class="sb-btn" onclick="fillInput('Read the email with ID ')">
      <span class="sb-icon">🔍</span>
      <span>Read full email<span class="sb-sub">Paste a message ID</span></span>
    </button>

    <div class="sb-divider"></div>
    <div class="sb-label">Compose</div>
    <button class="sb-btn" onclick="fillInput('Send an email to ')">
      <span class="sb-icon">✉️</span>
      <span>Send new email<span class="sb-sub">To · Subject · Body</span></span>
    </button>

    <div class="sb-divider"></div>
    <div class="sb-label">Manage</div>
    <button class="sb-btn" onclick="fillInput('Permanently delete the email with ID ')">
      <span class="sb-icon">🗑️</span>
      <span>Delete an email<span class="sb-sub">Permanent — irreversible</span></span>
    </button>

    <div class="sb-card">
      <div class="sb-card-title">💡 Pro tip</div>
      <p>Use plain English. The AI reads your intent and picks the right Gmail action automatically.</p>
    </div>

  </aside>

  <!-- ════ CHAT ════ -->
  <div class="chat-col">

    <!-- Hero empty state -->
    <div class="hero visible" id="hero">
      <div class="hero-icon-wrap">
        <div class="hero-icon-ring"></div>
        <div class="hero-icon">
          <svg viewBox="0 0 48 48" width="56" height="56" xmlns="http://www.w3.org/2000/svg">
            <path fill="#4285F4" d="M6 40h6V22.8L6 18v20a2 2 0 0 0 2 2z"/>
            <path fill="#34A853" d="M36 40h6a2 2 0 0 0 2-2V18l-8 4.8V40z"/>
            <path fill="#FBBC04" d="M36 10H12l12 8 12-8z"/>
            <path fill="#EA4335" d="M6 18l6 4.8L24 18l12 4.8L42 18 24 10 6 18z"/>
          </svg>
        </div>
      </div>

      <h2>What's in your <span>inbox</span>?</h2>
      <p>Ask me anything about your Gmail — list, read, compose, or delete using plain English.</p>

      <div class="hero-cards">
        <div class="hero-card" onclick="send('List my last 5 emails')">
          <div class="hc-icon">📋</div>
          <div class="hc-title">List emails</div>
          <div class="hc-desc">See your recent inbox</div>
        </div>
        <div class="hero-card" onclick="send('Show my unread emails')">
          <div class="hc-icon">📬</div>
          <div class="hc-title">Unread emails</div>
          <div class="hc-desc">Filter what's new</div>
        </div>
        <div class="hero-card" onclick="fillInput('Send an email to ')">
          <div class="hc-icon">✉️</div>
          <div class="hc-title">Compose email</div>
          <div class="hc-desc">Write and send</div>
        </div>
        <div class="hero-card" onclick="fillInput('Read the email with ID ')">
          <div class="hc-icon">🔍</div>
          <div class="hc-title">Read an email</div>
          <div class="hc-desc">Open by message ID</div>
        </div>
      </div>
    </div>

    <!-- Messages list -->
    <div id="messages"></div>

    <!-- Typing indicator -->
    <div class="typing-wrap" id="typingWrap">
      <div class="msg-av agent-av" style="width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.14);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
        <svg viewBox="0 0 48 48" width="18" height="18" xmlns="http://www.w3.org/2000/svg">
          <path fill="#4285F4" d="M6 40h6V22.8L6 18v20a2 2 0 0 0 2 2z"/>
          <path fill="#34A853" d="M36 40h6a2 2 0 0 0 2-2V18l-8 4.8V40z"/>
          <path fill="#FBBC04" d="M36 10H12l12 8 12-8z"/>
          <path fill="#EA4335" d="M6 18l6 4.8L24 18l12 4.8L42 18 24 10 6 18z"/>
        </svg>
      </div>
      <div class="typing-bubble">
        <span></span><span></span><span></span>
      </div>
      <span class="typing-label">Agent is thinking…</span>
    </div>

    <!-- Input bar -->
    <div class="input-wrap">
      <div class="input-box">
        <textarea
          id="userInput"
          placeholder="Ask about your Gmail inbox — e.g. 'List my last 5 emails'"
          rows="1"
        ></textarea>
        <button id="sendBtn" title="Send  (Enter)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>
      <div class="input-footer">
        <span class="input-hint">Enter to send · Shift+Enter for new line</span>
        <span class="input-api-note">POST /chat · granite-4-h-small · us-south</span>
      </div>
    </div>

  </div><!-- /chat-col -->
</div><!-- /layout -->

<!-- Watermark -->
<div class="watermark">
  <div class="watermark-icon">W</div>
  IBM WatsonX · granite-4-h-small
</div>

<script>
// ─── DOM refs ────────────────────────────────────
const msgList   = document.getElementById('messages');
const input     = document.getElementById('userInput');
const sendBtn   = document.getElementById('sendBtn');
const typingW   = document.getElementById('typingWrap');
const heroEl    = document.getElementById('hero');

// ─── Auto-resize textarea ────────────────────────
input.addEventListener('input', resize);
function resize() {
  input.style.height = 'auto';
  input.style.height = Math.min(input.scrollHeight, 150) + 'px';
}

// ─── Keyboard shortcut ───────────────────────────
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
});
sendBtn.addEventListener('click', handleSend);

// ─── Fill input (cursor at end) ──────────────────
function fillInput(text) {
  input.value = text;
  input.focus();
  resize();
  input.setSelectionRange(text.length, text.length);
}

// ─── Send directly without waiting for input ─────
function send(text) {
  fillInput(text);
  handleSend();
}

// ─── Timestamp helper ────────────────────────────
function ts() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// ─── Append a message bubble ─────────────────────
function appendMsg(role, text) {
  // Hide hero
  heroEl.classList.remove('visible');

  const wrap = document.createElement('div');
  wrap.className = 'msg ' + role;

  // Avatar
  const av = document.createElement('div');
  av.className = 'msg-av';
  if (role === 'user') {
    av.textContent = 'You';
  } else {
    av.innerHTML = '<svg viewBox="0 0 48 48" width="18" height="18" xmlns="http://www.w3.org/2000/svg"><path fill="#4285F4" d="M6 40h6V22.8L6 18v20a2 2 0 0 0 2 2z"/><path fill="#34A853" d="M36 40h6a2 2 0 0 0 2-2V18l-8 4.8V40z"/><path fill="#FBBC04" d="M36 10H12l12 8 12-8z"/><path fill="#EA4335" d="M6 18l6 4.8L24 18l12 4.8L42 18 24 10 6 18z"/></svg>';
  }

  // Body
  const body = document.createElement('div');
  body.className = 'msg-body';

  const name = document.createElement('div');
  name.className = 'msg-name';
  name.textContent = role === 'user' ? 'You' : 'Gmail Agent';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.textContent = text;

  const time = document.createElement('div');
  time.className = 'msg-ts';
  time.textContent = ts();

  body.appendChild(name);
  body.appendChild(bubble);
  body.appendChild(time);

  wrap.appendChild(av);
  wrap.appendChild(body);
  msgList.appendChild(wrap);
  msgList.scrollTop = msgList.scrollHeight;
}

// ─── Main send handler ───────────────────────────
async function handleSend() {
  const text = input.value.trim();
  if (!text) return;

  input.value = '';
  resize();
  sendBtn.disabled = true;

  appendMsg('user', text);

  // Show typing
  typingW.classList.add('on');
  msgList.scrollTop = msgList.scrollHeight;

  try {
    const res = await fetch('/chat', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ message: text })
    });

    typingW.classList.remove('on');

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      appendMsg('agent', '\u26a0\ufe0f Error ' + res.status + ': ' + (err.detail || res.statusText));
      return;
    }

    const data = await res.json();
    appendMsg('agent', data.reply);

  } catch (err) {
    typingW.classList.remove('on');
    appendMsg('agent', '\u26a0\ufe0f Could not reach the server. Is it running at http://127.0.0.1:8000?');
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}
</script>
</body>
</html>"""
