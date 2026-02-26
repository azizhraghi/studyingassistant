"""
The Avatar Room — AI agents as emotion-aware, speaking, lip-syncing avatars.
Uses face-api.js for real-time webcam emotion detection.
Avatars react to how the student FEELS, not just what they type.
"""

import streamlit as st
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Avatar Room | Student AI",
    page_icon="🎭",
    layout="wide",
)

st.markdown("""
<style>
    .stApp { background-color: #060810; color: #e2e8f0; }
    [data-testid="stSidebar"] { background-color: #0d1021; border-right: 1px solid #1e2240; }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎭 Avatar Room")
    st.markdown("---")
    if not os.getenv("MISTRAL_API_KEY"):
        api_key = st.text_input("🔑 Mistral API Key", type="password")
        if api_key:
            os.environ["MISTRAL_API_KEY"] = api_key
            st.success("✅ Key set!")
            st.rerun()
    else:
        st.success("✅ Mistral API loaded")
    st.markdown("---")
    st.markdown("### 🎭 Your Tutors")
    st.markdown("""
    <div style='font-size:0.82rem; color:#64748b; line-height:2.2'>
        👨‍🏫 <b style='color:#818cf8'>Prof. Atlas</b> — Socratic, wise<br>
        💪 <b style='color:#34d399'>Coach Rex</b> — Tough, motivating<br>
        📚 <b style='color:#38bdf8'>Nova</b> — Calm, encyclopedic<br>
        ⚡ <b style='color:#f59e0b'>Zed</b> — Fast, technical<br>
        🌸 <b style='color:#f472b6'>Dr. Sage</b> — Empathetic, caring
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 👁️ Emotion Detection")
    st.markdown("""
    <div style='font-size:0.8rem; color:#64748b; line-height:1.9'>
        😕 Confused → Professor explains<br>
        😴 Tired → Coach energizes<br>
        😰 Stressed → Dr. Sage calms<br>
        🤔 Focused → No interruption<br>
        😊 Happy → All celebrate
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='color:#475569;font-size:0.72rem;text-align:center'>
        ATLAS TBS Hackathon 2026<br>
        The AI that sees how you feel 👁️
    </div>
    """, unsafe_allow_html=True)

MISTRAL_KEY = os.getenv("MISTRAL_API_KEY", "")

AVATAR_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: #060810;
  font-family: 'Inter', system-ui, sans-serif;
  color: #e2e8f0;
}
#room {
  min-height: 100vh;
  background:
    radial-gradient(ellipse at 20% 50%, #1a0a2e 0%, transparent 60%),
    radial-gradient(ellipse at 80% 50%, #0a1a2e 0%, transparent 60%),
    linear-gradient(180deg, #060810 0%, #0a0d1a 100%);
  padding: 20px 16px;
}
#room-header { text-align:center; margin-bottom:18px; }
#room-header h1 {
  font-size:1.7rem; font-weight:900;
  background: linear-gradient(135deg, #818cf8, #f472b6, #38bdf8);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
#room-header p { color:#475569; font-size:0.82rem; margin-top:4px; }

/* Emotion bar */
#emotion-bar { display:flex; justify-content:center; gap:8px; margin-bottom:14px; flex-wrap:wrap; }
.emotion-pill {
  background:#0d1021; border:1px solid #1e2240;
  border-radius:20px; padding:4px 12px;
  font-size:0.75rem; color:#475569; transition:all 0.4s;
}
.emotion-pill.active { border-color:#818cf8; color:#e2e8f0; background:#1a1d40; box-shadow:0 0 10px rgba(129,140,248,0.3); }

#webcam-status { text-align:center; font-size:0.74rem; color:#475569; margin-bottom:10px; }
#webcam-status.active { color:#34d399; }
#webcam-status.error  { color:#f87171; }
#emotion-detected { text-align:center; font-size:0.8rem; color:#475569; min-height:22px; margin-bottom:10px; transition:all 0.4s; }
#emotion-detected.triggered { color:#818cf8; font-weight:600; }

/* Avatars Grid */
#avatars-grid {
  display:grid; grid-template-columns:repeat(5,1fr);
  gap:12px; max-width:900px;
  margin:0 auto 18px;
}
.avatar-card {
  background:#0d1021; border:1px solid #1e2240;
  border-radius:18px; padding:14px 10px;
  text-align:center; cursor:pointer;
  transition:all 0.3s ease; position:relative; overflow:hidden;
}
.avatar-card:hover { transform:translateY(-4px); }
.avatar-card.active { border-width:2px; transform:translateY(-6px); }
.avatar-card.speaking .avatar-face { animation:speakBounce 0.15s ease infinite alternate; }

.avatar-card[data-id="professor"].active { border-color:#818cf8; box-shadow:0 0 22px rgba(129,140,248,0.3); }
.avatar-card[data-id="coach"].active     { border-color:#34d399; box-shadow:0 0 22px rgba(52,211,153,0.3); }
.avatar-card[data-id="librarian"].active { border-color:#38bdf8; box-shadow:0 0 22px rgba(56,189,248,0.3); }
.avatar-card[data-id="hacker"].active    { border-color:#f59e0b; box-shadow:0 0 22px rgba(245,158,11,0.3); }
.avatar-card[data-id="therapist"].active { border-color:#f472b6; box-shadow:0 0 22px rgba(244,114,182,0.3); }

@keyframes speakBounce { from{transform:scale(1)} to{transform:scale(1.04)} }

/* Face */
.avatar-face {
  width:74px; height:74px; border-radius:50%;
  margin:0 auto 8px; position:relative; overflow:hidden;
  transition:all 0.3s;
}
.avatar-card[data-id="professor"] .avatar-face { background:radial-gradient(ellipse at 40% 35%,#7c6fa0 0%,#3d3060 40%,#1a1040 100%); box-shadow:0 0 0 3px #818cf840,0 6px 20px rgba(129,140,248,0.3); }
.avatar-card[data-id="coach"] .avatar-face     { background:radial-gradient(ellipse at 40% 35%,#5a8a70 0%,#2d5a45 40%,#0d2a1a 100%); box-shadow:0 0 0 3px #34d39940,0 6px 20px rgba(52,211,153,0.3); }
.avatar-card[data-id="librarian"] .avatar-face { background:radial-gradient(ellipse at 40% 35%,#5a7a9a 0%,#2d4a6a 40%,#0d1a3a 100%); box-shadow:0 0 0 3px #38bdf840,0 6px 20px rgba(56,189,248,0.3); }
.avatar-card[data-id="hacker"] .avatar-face    { background:radial-gradient(ellipse at 40% 35%,#8a7040 0%,#5a4a20 40%,#2a1a00 100%); box-shadow:0 0 0 3px #f59e0b40,0 6px 20px rgba(245,158,11,0.3); }
.avatar-card[data-id="therapist"] .avatar-face { background:radial-gradient(ellipse at 40% 35%,#9a6070 0%,#6a3a4a 40%,#3a0a1a 100%); box-shadow:0 0 0 3px #f472b640,0 6px 20px rgba(244,114,182,0.3); }

/* Glow ring while speaking */
.avatar-face::before {
  content:''; position:absolute; inset:-4px; border-radius:50%;
  opacity:0; transition:opacity 0.3s; z-index:-1;
}
.avatar-card[data-id="professor"] .avatar-face::before { box-shadow:0 0 20px 8px #818cf8; }
.avatar-card[data-id="coach"] .avatar-face::before     { box-shadow:0 0 20px 8px #34d399; }
.avatar-card[data-id="librarian"] .avatar-face::before { box-shadow:0 0 20px 8px #38bdf8; }
.avatar-card[data-id="hacker"] .avatar-face::before    { box-shadow:0 0 20px 8px #f59e0b; }
.avatar-card[data-id="therapist"] .avatar-face::before { box-shadow:0 0 20px 8px #f472b6; }
.avatar-card.speaking .avatar-face::before { opacity:1; animation:glowPulse 0.5s ease infinite alternate; }
@keyframes glowPulse { from{opacity:0.6} to{opacity:1} }

.avatar-hair {
  position:absolute; top:-2px; left:0; right:0; height:28px;
  border-radius:50% 50% 0 0; transition:all 0.3s;
}
.avatar-card[data-id="professor"] .avatar-hair { background:linear-gradient(180deg,#2d2050 0%,transparent 100%); border-top:3px solid #818cf8; }
.avatar-card[data-id="coach"] .avatar-hair     { background:linear-gradient(180deg,#1a3a28 0%,transparent 100%); border-top:3px solid #34d399; }
.avatar-card[data-id="librarian"] .avatar-hair { background:linear-gradient(180deg,#1a2a4a 0%,transparent 100%); border-top:3px solid #38bdf8; }
.avatar-card[data-id="hacker"] .avatar-hair    { background:linear-gradient(180deg,#2a1a00 0%,transparent 100%); border-top:3px solid #f59e0b; clip-path:polygon(0 0,15% 80%,30% 0,45% 80%,60% 0,75% 80%,90% 0,100% 0,100% 100%,0 100%); }
.avatar-card[data-id="therapist"] .avatar-hair { background:linear-gradient(180deg,#3a0a2a 0%,transparent 100%); border-top:3px solid #f472b6; height:36px; }

.avatar-brows { position:absolute; top:29%; left:50%; transform:translateX(-50%); display:flex; gap:13px; }
.avatar-brow  { width:11px; height:2px; background:#e2e8f0; border-radius:2px; transition:all 0.4s; }
.avatar-eyes  { position:absolute; top:36%; left:50%; transform:translateX(-50%); display:flex; gap:11px; }
.avatar-eye   { width:10px; height:10px; background:#e2e8f0; border-radius:50%; position:relative; transition:all 0.3s; }
.avatar-eye::after { content:''; position:absolute; width:5px; height:5px; background:#1a1040; border-radius:50%; top:2px; left:2px; }
.avatar-mouth {
  position:absolute; bottom:27%; left:50%; transform:translateX(-50%);
  width:20px; height:6px; background:transparent;
  border:2px solid #e2e8f0; border-top:none;
  border-radius:0 0 10px 10px; transition:all 0.08s;
}
.avatar-mouth.open-sm  { height:8px;  background:#2a0a1a; }
.avatar-mouth.open-md  { height:12px; background:#2a0a1a; border-radius:0 0 12px 12px; }
.avatar-mouth.open-lg  { height:15px; width:22px; background:#2a0a1a; border-radius:0 0 14px 14px; }
.avatar-mouth.open-xl  { height:18px; width:24px; background:#2a0a1a; border-radius:0 0 14px 14px; }
.avatar-mouth.smile    { border-color:#34d399; height:8px; }

/* Emotion face states */
.state-confused .avatar-brow:first-child { transform:rotate(10deg) translateY(-2px); }
.state-confused .avatar-brow:last-child  { transform:rotate(-10deg) translateY(-2px); }
.state-tired .avatar-eye { height:5px; border-radius:50% 50% 0 0; }
.state-tired .avatar-brow { transform:translateY(2px); opacity:0.6; }
.state-happy .avatar-brow { transform:translateY(-2px); }
.state-happy .avatar-mouth { border-color:#34d399; height:10px; }
.state-stressed .avatar-brow:first-child { transform:rotate(-8deg) translateY(-3px); }
.state-stressed .avatar-brow:last-child  { transform:rotate(8deg) translateY(-3px); }
.state-stressed .avatar-eye { width:11px; height:11px; }

.avatar-name { font-size:0.8rem; font-weight:700; margin-bottom:2px; }
.avatar-card[data-id="professor"] .avatar-name { color:#818cf8; }
.avatar-card[data-id="coach"] .avatar-name     { color:#34d399; }
.avatar-card[data-id="librarian"] .avatar-name { color:#38bdf8; }
.avatar-card[data-id="hacker"] .avatar-name    { color:#f59e0b; }
.avatar-card[data-id="therapist"] .avatar-name { color:#f472b6; }
.avatar-role   { font-size:0.67rem; color:#475569; margin-bottom:6px; }
.avatar-status { font-size:0.65rem; padding:2px 8px; border-radius:20px; background:#1a1d2e; color:#475569; transition:all 0.3s; }
.avatar-card.speaking .avatar-status { color:#e2e8f0; animation:blink 1s ease infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* Speech bubble */
#speech-bubble { max-width:760px; margin:0 auto 16px; }
#bubble-inner {
  background:#0d1021; border:1px solid #1e2240;
  border-radius:18px; padding:16px 20px; min-height:76px;
  font-size:0.92rem; line-height:1.7; color:#cbd5e1;
  transition:border-color 0.3s;
}
#bubble-inner.professor-bubble { border-color:#818cf840; }
#bubble-inner.coach-bubble     { border-color:#34d39940; }
#bubble-inner.librarian-bubble { border-color:#38bdf840; }
#bubble-inner.hacker-bubble    { border-color:#f59e0b40; }
#bubble-inner.therapist-bubble { border-color:#f472b640; }
#bubble-speaker { font-size:0.73rem; font-weight:700; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.08em; }
#bubble-text { transition:opacity 0.2s; }
#bubble-text.fading { opacity:0; }
#typing-indicator { display:none; }
#typing-indicator.visible { display:inline-flex; gap:4px; align-items:center; margin-top:4px; }
.typing-dot { width:6px; height:6px; background:#475569; border-radius:50%; animation:typingBounce 1s ease infinite; }
.typing-dot:nth-child(2) { animation-delay:0.15s; }
.typing-dot:nth-child(3) { animation-delay:0.3s; }
@keyframes typingBounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }

/* Chat */
#chat-area { max-width:760px; margin:0 auto; }
#chat-messages { max-height:180px; overflow-y:auto; margin-bottom:10px; display:flex; flex-direction:column; gap:6px; }
.chat-msg-user {
  background:linear-gradient(135deg,#2563eb,#1d4ed8);
  color:white; padding:8px 14px; border-radius:16px 16px 4px 16px;
  margin-left:25%; font-size:0.85rem;
}
.chat-msg-ai {
  background:#0d1021; border:1px solid #1e2240;
  color:#cbd5e1; padding:8px 14px; border-radius:16px 16px 16px 4px;
  margin-right:25%; font-size:0.85rem;
}

/* Input */
#input-row { display:flex; gap:8px; align-items:center; }
#user-input {
  flex:1; background:#0d1021; border:1px solid #1e2240;
  border-radius:24px; padding:11px 18px;
  color:#e2e8f0; font-size:0.88rem; outline:none;
  transition:border-color 0.3s; font-family:inherit;
}
#user-input:focus { border-color:#818cf8; }
#user-input::placeholder { color:#334155; }
#send-btn,#voice-btn,#cam-btn {
  width:42px; height:42px; border-radius:50%; border:none;
  cursor:pointer; font-size:1rem; transition:all 0.2s;
  display:flex; align-items:center; justify-content:center;
}
#send-btn { background:linear-gradient(135deg,#818cf8,#6366f1); color:white; }
#voice-btn { background:#1e2240; color:#94a3b8; }
#voice-btn.listening { background:linear-gradient(135deg,#ef4444,#f97316); color:white; animation:micPulse 1s ease infinite; }
@keyframes micPulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.1)} }
#cam-btn { background:#1e2240; color:#94a3b8; }
#cam-btn.active { background:linear-gradient(135deg,#34d399,#38bdf8); color:white; }
#send-btn:hover { transform:scale(1.1); }

#webcam-feed {
  position:fixed; bottom:10px; right:10px;
  width:80px; height:60px; border-radius:8px;
  border:1px solid #1e2240; opacity:0.4;
  display:none; z-index:100;
}
#webcam-feed.visible { display:block; }
</style>
</head>
<body>
<div id="room">

  <div id="room-header">
    <h1>🎭 The Avatar Room</h1>
    <p>Your AI tutors can see how you feel — they adapt to you in real time</p>
  </div>

  <div id="webcam-status">👁️ Click the camera button below to enable emotion detection</div>
  <div id="emotion-bar">
    <span class="emotion-pill" id="pill-neutral">😐 Neutral</span>
    <span class="emotion-pill" id="pill-happy">😊 Happy</span>
    <span class="emotion-pill" id="pill-confused">😕 Confused</span>
    <span class="emotion-pill" id="pill-tired">😴 Tired</span>
    <span class="emotion-pill" id="pill-stressed">😰 Stressed</span>
    <span class="emotion-pill" id="pill-focused">🤔 Focused</span>
  </div>
  <div id="emotion-detected"></div>

  <div id="avatars-grid">
    <div class="avatar-card" data-id="professor" onclick="selectAvatar('professor')">
      <div class="avatar-face" id="face-professor">
        <div class="avatar-hair"></div>
        <div class="avatar-brows"><div class="avatar-brow"></div><div class="avatar-brow"></div></div>
        <div class="avatar-eyes"><div class="avatar-eye"></div><div class="avatar-eye"></div></div>
        <div class="avatar-mouth" id="mouth-professor"></div>
      </div>
      <div class="avatar-name">Prof. Atlas</div>
      <div class="avatar-role">Socratic · Wise</div>
      <div class="avatar-status" id="status-professor">Listening...</div>
    </div>
    <div class="avatar-card" data-id="coach" onclick="selectAvatar('coach')">
      <div class="avatar-face" id="face-coach">
        <div class="avatar-hair"></div>
        <div class="avatar-brows"><div class="avatar-brow"></div><div class="avatar-brow"></div></div>
        <div class="avatar-eyes"><div class="avatar-eye"></div><div class="avatar-eye"></div></div>
        <div class="avatar-mouth" id="mouth-coach"></div>
      </div>
      <div class="avatar-name">Coach Rex</div>
      <div class="avatar-role">Tough · Motivating</div>
      <div class="avatar-status" id="status-coach">Ready!</div>
    </div>
    <div class="avatar-card active" data-id="librarian" onclick="selectAvatar('librarian')">
      <div class="avatar-face" id="face-librarian">
        <div class="avatar-hair"></div>
        <div class="avatar-brows"><div class="avatar-brow"></div><div class="avatar-brow"></div></div>
        <div class="avatar-eyes"><div class="avatar-eye"></div><div class="avatar-eye"></div></div>
        <div class="avatar-mouth" id="mouth-librarian"></div>
      </div>
      <div class="avatar-name">Nova</div>
      <div class="avatar-role">Calm · Encyclopedic</div>
      <div class="avatar-status" id="status-librarian">Speaking...</div>
    </div>
    <div class="avatar-card" data-id="hacker" onclick="selectAvatar('hacker')">
      <div class="avatar-face" id="face-hacker">
        <div class="avatar-hair"></div>
        <div class="avatar-brows"><div class="avatar-brow"></div><div class="avatar-brow"></div></div>
        <div class="avatar-eyes"><div class="avatar-eye"></div><div class="avatar-eye"></div></div>
        <div class="avatar-mouth" id="mouth-hacker"></div>
      </div>
      <div class="avatar-name">Zed</div>
      <div class="avatar-role">Fast · Technical</div>
      <div class="avatar-status" id="status-hacker">In the zone</div>
    </div>
    <div class="avatar-card" data-id="therapist" onclick="selectAvatar('therapist')">
      <div class="avatar-face" id="face-therapist">
        <div class="avatar-hair"></div>
        <div class="avatar-brows"><div class="avatar-brow"></div><div class="avatar-brow"></div></div>
        <div class="avatar-eyes"><div class="avatar-eye"></div><div class="avatar-eye"></div></div>
        <div class="avatar-mouth" id="mouth-therapist"></div>
      </div>
      <div class="avatar-name">Dr. Sage</div>
      <div class="avatar-role">Empathetic · Caring</div>
      <div class="avatar-status" id="status-therapist">Here for you</div>
    </div>
  </div>

  <div id="speech-bubble">
    <div id="bubble-inner" class="librarian-bubble">
      <div id="bubble-speaker" style="color:#38bdf8">📚 Nova · Librarian</div>
      <div id="bubble-text">Welcome to the Avatar Room! I'm Nova. Click any tutor to select them, then ask anything. Enable your camera and I'll detect how you're feeling — your tutors will automatically adapt to your emotional state. 🎓</div>
      <div id="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>
    </div>
  </div>

  <div id="chat-area">
    <div id="chat-messages"></div>
    <div id="input-row">
      <button id="cam-btn" onclick="toggleCamera()" title="Enable emotion detection">📷</button>
      <button id="voice-btn" onclick="toggleVoice()" title="Voice input">🎤</button>
      <input id="user-input" type="text" placeholder="Ask your tutor anything..." onkeydown="if(event.key==='Enter')sendMessage()">
      <button id="send-btn" onclick="sendMessage()">➤</button>
    </div>
  </div>

  <video id="webcam-feed" autoplay muted playsinline></video>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/face-api.js/0.22.2/face-api.min.js"></script>
<script>
const MISTRAL_KEY = "MISTRAL_KEY_PLACEHOLDER";

const AVATARS = {
  professor:{
    name:"Prof. Atlas",color:"#818cf8",bubbleClass:"professor-bubble",
    speakerLabel:"👨‍🏫 Prof. Atlas · Socratic",
    systemPrompt:"You are Professor Atlas, a wise Socratic tutor. Guide students to discover answers through questions. Ask 1-2 probing questions then give a hint. Use 'What do you think...', 'Consider this...'. Under 80 words.",
    emotionResponses:{
      confused:"I can see you're wrestling with something. That's where real learning begins. What specific part is giving you trouble? Let's break it down together.",
      tired:"I notice your energy is low. Tell me one thing you DO understand — we'll build from there.",
      stressed:"Take a breath. Confusion is just understanding that hasn't happened yet. What's one small piece we can clarify right now?",
      happy:"Excellent energy! Ready to tackle something challenging? Let's push deeper."
    }
  },
  coach:{
    name:"Coach Rex",color:"#34d399",bubbleClass:"coach-bubble",
    speakerLabel:"💪 Coach Rex · Motivator",
    systemPrompt:"You are Coach Rex, a tough motivational coach. Direct, energetic, short punchy sentences. Sports metaphors. Challenge them. 'No excuses!', 'Champions don't quit!' Under 70 words.",
    emotionResponses:{
      confused:"Confusion means you're in the GAME! Champions don't quit when it gets hard. Push through — what's the next small step RIGHT NOW?",
      tired:"I SEE you. You're tired. But this is where champions are made. 5 more minutes. Just 5. Let's GO.",
      stressed:"Channel that stress into FOCUS. Deep breath. What's the ONE thing you need to do next?",
      happy:"THAT'S THE ENERGY! Don't stop now — what's next on your list?"
    }
  },
  librarian:{
    name:"Nova",color:"#38bdf8",bubbleClass:"librarian-bubble",
    speakerLabel:"📚 Nova · Librarian",
    systemPrompt:"You are Nova, a calm encyclopedic librarian. Clear structured information. Reference sources, give context. 'According to...', 'There are three key aspects...' Under 90 words.",
    emotionResponses:{
      confused:"That's perfectly normal — this is complex. Let me organize the key concepts clearly. There are three things to understand here...",
      tired:"Let's make this easier. Just the essential points — the minimum you need to know right now.",
      stressed:"Let's slow down and be systematic. First, let's identify exactly what you need to know.",
      happy:"Wonderful! Let's use this clarity to go deeper. I have fascinating context to add..."
    }
  },
  hacker:{
    name:"Zed",color:"#f59e0b",bubbleClass:"hacker-bubble",
    speakerLabel:"⚡ Zed · Hacker",
    systemPrompt:"You are Zed, a fast technical genius. Ultra-concise, systems thinking. Computing analogies. 'TL;DR:', 'Think of it like a hash function...' Under 60 words. Fast and precise.",
    emotionResponses:{
      confused:"Confused? Good. Confusion = missing dependency. Let's install that knowledge. What's the specific concept that's undefined?",
      tired:"Low battery. Switch to low-power mode: just the TL;DR. What do you NEED to know?",
      stressed:"Too many open processes. Close tabs. Focus on one thread. What's the single most critical task?",
      happy:"System running optimally. Let's push the clock speed — tackle something harder."
    }
  },
  therapist:{
    name:"Dr. Sage",color:"#f472b6",bubbleClass:"therapist-bubble",
    speakerLabel:"🌸 Dr. Sage · Therapist",
    systemPrompt:"You are Dr. Sage, a warm empathetic learning therapist. Validate feelings, reduce anxiety, build confidence. 'It's completely okay...', 'You've already done something hard today by showing up.' Under 80 words. Warm and caring.",
    emotionResponses:{
      confused:"I see the confusion, and that's completely okay. Not understanding yet doesn't mean you can't. What would feel like a safe place to start?",
      tired:"You look tired, and that tells me you've been working hard. That effort matters. Can we take 60 seconds to breathe before we continue?",
      stressed:"I can see you're carrying a lot. Let's pause. You don't have to figure it all out at once. What's one small thing that feels manageable?",
      happy:"That smile — hold onto it! You earned it. This is what progress feels like. How does it feel to be understanding this?"
    }
  }
};

let currentAvatar = 'librarian';
let isSpeaking = false;
let lipSyncInterval = null;
let emotionInterval = null;
let cameraActive = false;
let speechRecognition = null;
let isListening = false;
let conversationHistory = [];
const mouthStates = ['','open-sm','open-md','open-lg','open-xl','open-md','open-sm',''];

function selectAvatar(id) {
  document.querySelectorAll('.avatar-card').forEach(c=>c.classList.remove('active'));
  document.querySelector(`[data-id="${id}"]`).classList.add('active');
  currentAvatar = id;
  const av = AVATARS[id];
  document.getElementById('bubble-inner').className = av.bubbleClass;
  document.getElementById('bubble-speaker').style.color = av.color;
  document.getElementById('bubble-speaker').textContent = av.speakerLabel;
  conversationHistory = [];
  setBubbleText(`Hi! I'm ${av.name}. What would you like to work on?`);
  speakText(`Hi! I'm ${av.name}. What would you like to work on?`, id);
}

function setBubbleText(text) {
  const el = document.getElementById('bubble-text');
  el.classList.add('fading');
  setTimeout(()=>{ el.textContent=text; el.classList.remove('fading'); },200);
}

function showTyping() {
  document.getElementById('typing-indicator').classList.add('visible');
  document.getElementById('bubble-text').textContent='';
}
function hideTyping() {
  document.getElementById('typing-indicator').classList.remove('visible');
}

function startLipSync(avatarId) {
  stopLipSync();
  const mouth = document.getElementById(`mouth-${avatarId}`);
  const card = document.querySelector(`[data-id="${avatarId}"]`);
  card.classList.add('speaking');
  document.getElementById(`status-${avatarId}`).textContent='🔊 Speaking...';
  let i=0;
  lipSyncInterval = setInterval(()=>{
    if(!isSpeaking){ stopLipSync(avatarId); return; }
    mouth.className = 'avatar-mouth ' + mouthStates[i%mouthStates.length];
    i++;
  }, 80+Math.random()*60);
}

function stopLipSync(avatarId) {
  clearInterval(lipSyncInterval);
  if(avatarId){
    const mouth=document.getElementById(`mouth-${avatarId}`);
    if(mouth) mouth.className='avatar-mouth';
    const card=document.querySelector(`[data-id="${avatarId}"]`);
    if(card) card.classList.remove('speaking');
    const st=document.getElementById(`status-${avatarId}`);
    if(st) st.textContent='Listening...';
  }
  isSpeaking=false;
}

function speakText(text, avatarId) {
  if(!text||!text.trim()) return;
  window.speechSynthesis.cancel();
  stopLipSync(currentAvatar);
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 0.95;
  utterance.pitch = avatarId==='coach'?1.1:avatarId==='therapist'?0.9:1.0;
  const voices = window.speechSynthesis.getVoices();
  const preferred = voices.find(v=>v.lang.startsWith('en')&&(v.name.includes('Google')||v.name.includes('Natural')));
  if(preferred) utterance.voice=preferred;
  utterance.onstart = ()=>{ isSpeaking=true; startLipSync(avatarId); };
  utterance.onend   = ()=>{ isSpeaking=false; stopLipSync(avatarId); };
  utterance.onerror = ()=>{ isSpeaking=false; stopLipSync(avatarId); };
  window.speechSynthesis.speak(utterance);
}

async function sendMessage(overrideText) {
  const input = document.getElementById('user-input');
  const text = overrideText||input.value.trim();
  if(!text) return;
  input.value='';
  addChatMessage(text,'user');
  conversationHistory.push({role:'user',content:text});
  showTyping();

  const av = AVATARS[currentAvatar];

  if(!MISTRAL_KEY||MISTRAL_KEY==='') {
    const fb="Please add your Mistral API key in the sidebar!";
    hideTyping(); setBubbleText(fb); addChatMessage(fb,'ai'); speakText(fb,currentAvatar); return;
  }

  try {
    const messages = [{role:'system',content:av.systemPrompt},...conversationHistory.slice(-8)];
    const response = await fetch('https://api.mistral.ai/v1/chat/completions',{
      method:'POST',
      headers:{'Content-Type':'application/json','Authorization':`Bearer ${MISTRAL_KEY}`},
      body:JSON.stringify({model:'mistral-large-latest',messages,max_tokens:150,temperature:0.7})
    });
    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content||"I couldn't process that. Try again.";
    conversationHistory.push({role:'assistant',content:reply});
    hideTyping(); setBubbleText(reply); addChatMessage(reply,'ai'); speakText(reply,currentAvatar);
  } catch(err) {
    hideTyping();
    const errMsg="Connection error. Check your API key.";
    setBubbleText(errMsg); addChatMessage(errMsg,'ai');
  }
}

function addChatMessage(text,role){
  const c=document.getElementById('chat-messages');
  const d=document.createElement('div');
  d.className=role==='user'?'chat-msg-user':'chat-msg-ai';
  d.textContent=text;
  c.appendChild(d);
  c.scrollTop=c.scrollHeight;
}

let lastEmotionTrigger='', lastTriggerTime=0;
function triggerEmotionResponse(emotion){
  const now=Date.now();
  if(emotion===lastEmotionTrigger&&now-lastTriggerTime<18000) return;
  lastEmotionTrigger=emotion; lastTriggerTime=now;
  const av=AVATARS[currentAvatar];
  const response=av.emotionResponses[emotion];
  if(!response) return;
  const labels={confused:'😕 Confusion detected',tired:'😴 Tiredness detected',stressed:'😰 Stress detected',happy:'😊 Happiness detected'};
  const det=document.getElementById('emotion-detected');
  det.textContent=`${labels[emotion]} — ${av.name} is responding...`;
  det.classList.add('triggered');
  setTimeout(()=>det.classList.remove('triggered'),4000);
  conversationHistory.push({role:'user',content:`[Emotion: ${emotion}]`});
  conversationHistory.push({role:'assistant',content:response});
  setBubbleText(response);
  addChatMessage(`[🎭 ${av.name} noticed you look ${emotion}]`,'ai');
  addChatMessage(response,'ai');
  speakText(response,currentAvatar);
  document.querySelectorAll('.avatar-face').forEach(f=>f.className=`avatar-face state-${emotion}`);
  setTimeout(()=>document.querySelectorAll('.avatar-face').forEach(f=>f.className='avatar-face'),5000);
}

function updateEmotionUI(emotion){
  document.querySelectorAll('.emotion-pill').forEach(p=>p.classList.remove('active'));
  const pill=document.getElementById(`pill-${emotion}`);
  if(pill) pill.classList.add('active');
}

async function toggleCamera(){
  const btn=document.getElementById('cam-btn');
  const video=document.getElementById('webcam-feed');
  const status=document.getElementById('webcam-status');
  if(cameraActive){
    cameraActive=false; clearInterval(emotionInterval);
    if(video.srcObject) video.srcObject.getTracks().forEach(t=>t.stop());
    video.classList.remove('visible'); btn.classList.remove('active'); btn.textContent='📷';
    status.textContent='👁️ Camera off'; status.className='';
    return;
  }
  try {
    status.textContent='⏳ Loading emotion detection...';
    try {
      await Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri('https://cdnjs.cloudflare.com/ajax/libs/face-api.js/0.22.2/weights'),
        faceapi.nets.faceExpressionNet.loadFromUri('https://cdnjs.cloudflare.com/ajax/libs/face-api.js/0.22.2/weights'),
      ]);
    } catch(e) {
      startSimulatedEmotions();
      cameraActive=true; btn.classList.add('active'); btn.textContent='🟢';
      status.textContent='🎭 Demo emotion mode (simulated for demo)';
      status.className='active'; return;
    }
    const stream=await navigator.mediaDevices.getUserMedia({video:true});
    video.srcObject=stream; video.classList.add('visible');
    cameraActive=true; btn.classList.add('active'); btn.textContent='🟢';
    status.textContent='✅ Emotion detection active — your tutors can see you!';
    status.className='active';
    emotionInterval=setInterval(async()=>{
      if(!cameraActive) return;
      try {
        const det=await faceapi.detectSingleFace(video,new faceapi.TinyFaceDetectorOptions()).withFaceExpressions();
        if(det){
          const exp=det.expressions;
          const sorted=Object.entries(exp).sort((a,b)=>b[1]-a[1]);
          const [top,score]=sorted[0];
          let mapped='neutral';
          if(score>0.5){
            if(top==='happy') mapped='happy';
            else if(top==='sad'||top==='disgusted') mapped='tired';
            else if(top==='fearful'||top==='angry') mapped='stressed';
            else if(top==='surprised') mapped='confused';
            else mapped='focused';
          }
          updateEmotionUI(mapped);
          if(['happy','tired','stressed','confused'].includes(mapped)&&score>0.65)
            triggerEmotionResponse(mapped);
        }
      } catch(e){}
    },2500);
  } catch(err){
    status.textContent=`❌ Camera error: ${err.message}`;
    status.className='error';
  }
}

function startSimulatedEmotions(){
  const sequence=['neutral','focused','confused','focused','happy','focused','stressed','focused','neutral'];
  let i=0;
  emotionInterval=setInterval(()=>{
    const e=sequence[i%sequence.length];
    updateEmotionUI(e);
    if(['happy','confused','stressed'].includes(e)) triggerEmotionResponse(e);
    i++;
  },9000);
}

function toggleVoice(){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){alert('Voice not supported. Try Chrome.');return;}
  const btn=document.getElementById('voice-btn');
  if(isListening){
    speechRecognition.stop(); isListening=false;
    btn.classList.remove('listening'); btn.textContent='🎤'; return;
  }
  speechRecognition=new SR();
  speechRecognition.lang='en-US'; speechRecognition.continuous=false; speechRecognition.interimResults=false;
  speechRecognition.onstart=()=>{isListening=true;btn.classList.add('listening');btn.textContent='⏹️';};
  speechRecognition.onresult=(e)=>{
    const t=e.results[0][0].transcript;
    document.getElementById('user-input').value=t;
    sendMessage(t);
  };
  speechRecognition.onend=()=>{isListening=false;btn.classList.remove('listening');btn.textContent='🎤';};
  speechRecognition.start();
}

window.onload=()=>{
  window.speechSynthesis.getVoices();
  setTimeout(()=>window.speechSynthesis.getVoices(),500);
  setTimeout(()=>{
    speakText("Welcome to the Avatar Room! I'm Nova. Enable your camera and I'll detect how you're feeling — your tutors will adapt to you automatically.", 'librarian');
  },800);
};
</script>
</body>
</html>"""

# Inject the API key
avatar_html_final = AVATAR_HTML.replace("MISTRAL_KEY_PLACEHOLDER", MISTRAL_KEY)

components.html(avatar_html_final, height=860, scrolling=True)
