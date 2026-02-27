def get_avatar_html(css_content: str, js_content: str) -> str:
    """
    Returns the complete HTML string for the Avatar Room, injecting the provided
    CSS and JavaScript.
    """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
{css_content}
</style>
</head>
<body>
<div id="room">

  <div id="room-header">
    <h1>🎭 The Avatar Room</h1>
    <p>Your AI agents — each with unique powers, adapting to how you feel in real time</p>
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

  <!-- FOCUS METER — cognitive load dashboard -->
  <div id="focus-meter">
    <div id="focus-label">🧠 Focus Level</div>
    <div id="focus-bar">
      <div id="focus-bar-fill"></div>
    </div>
    <div id="focus-status">Waiting for camera...</div>
  </div>

  <div id="avatars-grid">
    <div class="avatar-card" data-id="professor" onclick="selectAvatar('professor')">
      <div class="avatar-face" id="face-professor">
        <div class="avatar-hair"></div>
        <div class="avatar-brows"><div class="avatar-brow"></div><div class="avatar-brow"></div></div>
        <div class="avatar-eyes"><div class="avatar-eye"></div><div class="avatar-eye"></div></div>
        <div class="avatar-mouth" id="mouth-professor"></div>
      </div>
      <div class="avatar-name">Prof. Atlas</div>
      <div class="avatar-role">Study Buddy · Teach Me</div>
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
      <div class="avatar-role">Quizmaster · Test You</div>
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
      <div class="avatar-role">Summarizer · Your Notes</div>
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
      <div class="avatar-role">Flashcard Forge</div>
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
      <div class="avatar-role">Reflector · Metacognition</div>
      <div class="avatar-status" id="status-therapist">Here for you</div>
    </div>
  </div>

  <!-- MODE TOOLBAR — dynamically populated per avatar -->
  <div id="mode-toolbar"></div>

  <!-- MATERIAL UPLOAD ZONE — for modes that need study content -->
  <div id="material-zone">
    <div id="material-zone-inner">
      <label>📄 Paste your study material</label>
      <textarea id="material-input" placeholder="Paste your notes, chapter text, or any study material here..."></textarea>
      <div id="material-actions">
        <button id="material-submit" onclick="submitMaterial()">🚀 Submit Material</button>
        <label id="file-upload-label">📎 Upload File
          <input type="file" id="file-upload" accept=".txt,.md,.text,.pdf,.doc,.docx,.pptx,.csv" onchange="handleFileUpload(event)">
        </label>
      </div>
    </div>
  </div>

  <!-- FLASHCARD UI — shown when Zed generates cards -->
  <div id="flashcard-container">
    <div id="fc-header">
      <span id="fc-counter">1 / 10</span>
      <button id="fc-shuffle" onclick="shuffleCards()">🔀 Shuffle</button>
    </div>
    <div id="fc-card-wrapper" onclick="flipCard()">
      <div id="fc-card">
        <div class="fc-face" id="fc-front">
          <div id="fc-front-label">Question</div>
          <div id="fc-front-text">Loading...</div>
          <div id="fc-hint">Click to flip</div>
        </div>
        <div class="fc-face" id="fc-back">
          <div id="fc-back-label">Answer</div>
          <div id="fc-back-text">Loading...</div>
        </div>
      </div>
    </div>
    <div id="fc-nav">
      <button class="fc-nav-btn" onclick="prevCard()">← Previous</button>
      <button class="fc-nav-btn" onclick="nextCard()">Next →</button>
    </div>
  </div>

  <!-- INTERACTIVE QUIZ UI — shown when Coach Rex generates a quiz -->
  <div id="quiz-container">
    <div id="qz-progress-bar">
      <div id="qz-progress-fill"></div>
    </div>
    <div id="qz-header">
      <span id="qz-counter">Question 1 / 5</span>
      <span id="qz-type-badge">MCQ</span>
    </div>
    <div id="qz-question-card">
      <div id="qz-question-text">Loading question...</div>
      <div id="qz-options"></div>
      <div id="qz-fill-input-wrap">
        <input type="text" id="qz-fill-input" placeholder="Type your answer..." onkeydown="if(event.key==='Enter')submitFillAnswer()">
        <button id="qz-fill-submit" onclick="submitFillAnswer()">Submit</button>
      </div>
    </div>
    <div id="qz-explanation">
      <div id="qz-result-icon"></div>
      <div id="qz-explanation-text"></div>
    </div>
    <div id="qz-nav">
      <button id="qz-next-btn" onclick="nextQuizQuestion()">Next Question →</button>
    </div>
  </div>

  <!-- QUIZ SCORE CARD — shown after quiz completion -->
  <div id="quiz-score">
    <div id="qs-inner">
      <div id="qs-title">Quiz Complete</div>
      <div id="qs-score">0/5</div>
      <div id="qs-grade">🏆 Grade: A</div>
      <div id="qs-bar"><div id="qs-bar-fill"></div></div>
      <button id="qs-retake" onclick="retakeQuiz()">🔄 Retake Quiz</button>
    </div>
  </div>

  <!-- SYLLABUS ROADMAP UI — shown when Nova generates a roadmap -->
  <div id="roadmap-container">
    <div id="rm-header">
      <div id="rm-title">📅 Course Roadmap</div>
      <div id="rm-subtitle">Generated from your syllabus</div>
    </div>
    <div id="rm-timeline">
      <!-- Roadmap milestones will be injected here -->
    </div>
  </div>

  <div id="speech-bubble">
    <div id="bubble-inner" class="librarian-bubble">
      <div id="bubble-speaker" style="color:#38bdf8">📚 Nova · Summarizer</div>
      <div id="bubble-text">Welcome to the Avatar Room! I'm Nova, your Summarizer. Each tutor has unique powers — pick one and try their special modes! 🎓</div>
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

<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script>pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/face-api.js/0.22.2/face-api.min.js"></script>
<script>
{js_content}
</script>
</body>
</html>
"""
    return html
