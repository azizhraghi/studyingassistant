// Read the API key injected by Python via a separate script tag
const MISTRAL_KEY = (typeof MISTRAL_KEY_INJECTED !== 'undefined' && MISTRAL_KEY_INJECTED) ? MISTRAL_KEY_INJECTED : "";

// ─── AGENT DEFINITIONS ─────────────────────────────────────────────
// Each avatar is a specialized AI AGENT with distinct learning functions.
const AVATARS = {
  professor: {
    name: "Prof. Atlas", color: "#818cf8", bubbleClass: "professor-bubble",
    speakerLabel: "👨‍🏫 Prof. Atlas · Study Buddy",
    role: "Study Buddy",
    roleDesc: "Teach me to test your understanding",
    systemPrompt: "You are Professor Atlas, a wise Socratic tutor. Guide students to discover answers through questions. Ask 1-2 probing questions then give a hint. Use 'What do you think...', 'Consider this...'. Under 80 words.",
    modes: {
      chat: { label: "💬 Chat", desc: "General conversation" },
      teach: { label: "🧑‍🏫 Teach Me", desc: "Explain a concept to Atlas" }
    },
    modePrompts: {
      teach_newbie: `You are Prof. Atlas, but right now you are playing the role of a STUDENT who does NOT understand the topic. The user will try to teach you a concept. Your job:
- Act confused and curious. Ask genuine "newbie" questions.
- Say things like "Wait, I don't get it...", "Can you give me an example?", "What do you mean by...?"
- Do NOT reveal you actually know the answer. Stay in character as a confused student.
- Ask 1-2 clarifying questions per response. Keep responses under 60 words.
- After 3-4 exchanges, tell the user: "I think I'm starting to get it! But let me play devil's advocate..."
- This signals the phase shift to devil's advocate mode.`,
      teach_advocate: `You are Prof. Atlas, now playing DEVIL'S ADVOCATE. The user has been explaining a concept to you. Your job:
- Challenge their explanation. Find weak spots, edge cases, and assumptions.
- Say things like "But what about...", "That contradicts...", "What if someone argued that..."
- Be respectful but rigorous. Push them to think deeper.
- Keep responses under 60 words. Ask one challenging question per response.
- After 3-4 exchanges, give a final verdict: summarize what they explained well and what needs work.`
    },
    emotionResponses: {
      confused: "I can see you're wrestling with something. That's where real learning begins. What specific part is giving you trouble?",
      tired: "I notice your energy is low. Tell me one thing you DO understand — we'll build from there.",
      stressed: "Take a breath. Confusion is just understanding that hasn't happened yet. What's one small piece we can clarify?",
      happy: "Excellent energy! Ready to tackle something challenging? Let's push deeper."
    }
  },
  coach: {
    name: "Coach Rex", color: "#34d399", bubbleClass: "coach-bubble",
    speakerLabel: "💪 Coach Rex · Quizmaster",
    role: "Quizmaster",
    roleDesc: "Tests your knowledge with quizzes",
    systemPrompt: "You are Coach Rex, a tough motivational coach. Direct, energetic, short punchy sentences. Sports metaphors. Challenge them. 'No excuses!', 'Champions don't quit!' Under 70 words.",
    modes: {
      chat: { label: "💬 Chat", desc: "General motivation" },
      quiz: { label: "🧠 Start Quiz", desc: "Test your knowledge" }
    },
    modePrompts: {
      quiz: `You are Coach Rex, the Quizmaster. The user has provided study material. Your job:
- Generate exactly 1 question at a time from the material.
- Format: Start with "QUESTION X/5:" followed by the question.
- Mix question types: multiple choice (A/B/C/D), true/false, and fill-in-the-blank.
- For multiple choice, list the options on separate lines.
- After the user answers, respond with whether they are CORRECT ✅ or WRONG ❌.
- If wrong, give the correct answer and a brief explanation.
- Then immediately ask the next question.
- Use motivational sports language. "Let's GO!", "CHAMPION move!", "No excuses!"
- Keep track: after question 5, say "FINAL SCORE:" and give their score out of 5. Add motivational commentary based on score.
- Under 80 words per response.`
    },
    emotionResponses: {
      confused: "Confusion means you're in the GAME! Push through — what's the next small step RIGHT NOW?",
      tired: "I SEE you. You're tired. But this is where champions are made. 5 more minutes. Let's GO.",
      stressed: "Channel that stress into FOCUS. Deep breath. What's the ONE thing you need to do next?",
      happy: "THAT'S THE ENERGY! Don't stop now — what's next on your list?"
    }
  },
  librarian: {
    name: "Nova", color: "#38bdf8", bubbleClass: "librarian-bubble",
    speakerLabel: "📚 Nova · Summarizer",
    role: "Summarizer",
    roleDesc: "Summarizes your study material",
    systemPrompt: "You are Nova, a calm encyclopedic librarian. Clear structured information. Reference sources, give context. 'According to...', 'There are three key aspects...' Under 90 words.",
    modes: {
      chat: { label: "💬 Chat", desc: "General questions" },
      summarize_auto: { label: "📝 Auto Summary", desc: "Nova summarizes for you" },
      summarize_guided: { label: "🤝 Guided Summary", desc: "Build the summary together" }
    },
    modePrompts: {
      summarize_auto: `You are Nova, the Summarizer Agent. The user will paste study material. Your job:
- Read the material carefully.
- Produce a clean, structured summary with:
  1. A one-sentence overview
  2. Key concepts (bulleted list, 4-6 items)
  3. Important details or formulas
  4. A "Remember this" takeaway
- Use clear academic language. Be thorough but concise.
- If the material is long, prioritize the most important concepts.
- Under 200 words.`,
      summarize_guided: `You are Nova, the Guided Summary Agent. The user will paste study material. Your job is to help them BUILD the summary themselves through a conversation:
- Do NOT give them the summary directly.
- Instead, ask guiding questions like: "What do you think is the main idea here?", "Can you identify 3 key concepts?", "How would you explain this in your own words?"
- Give small hints if they struggle: "Think about the relationship between X and Y..."
- After 4-5 exchanges, help them compile their answers into a final structured summary.
- Be encouraging. "Great observation!", "You're onto something!"
- Under 70 words per response.`
    },
    emotionResponses: {
      confused: "That's perfectly normal — this is complex. Let me organize the key concepts clearly.",
      tired: "Let's make this easier. Just the essential points — the minimum you need right now.",
      stressed: "Let's slow down and be systematic. First, let's identify exactly what you need to know.",
      happy: "Wonderful! Let's use this clarity to go deeper. I have fascinating context to add..."
    }
  },
  hacker: {
    name: "Zed", color: "#f59e0b", bubbleClass: "hacker-bubble",
    speakerLabel: "⚡ Zed · Flashcard Forge",
    role: "Flashcard Forge",
    roleDesc: "Generates interactive flashcards",
    systemPrompt: "You are Zed, a fast technical genius. Ultra-concise, systems thinking. Computing analogies. 'TL;DR:', 'Think of it like a hash function...' Under 60 words. Fast and precise.",
    modes: {
      chat: { label: "💬 Chat", desc: "Technical chat" },
      flashcard: { label: "⚡ Generate Flashcards", desc: "Create a flashcard deck" }
    },
    modePrompts: {
      flashcard: `You are Zed, the Flashcard Forge Agent. The user will paste study material. Your job:
- Extract 8-10 key term/concept pairs from the material.
- Return them ONLY as a JSON array. No other text before or after.
- Format: [{"front":"term or question","back":"definition or answer"},...]
- Front should be a concise question or term (under 15 words).
- Back should be a clear, concise answer (under 30 words).
- Cover the most important concepts from the material.
- Return ONLY the JSON array, nothing else.`
    },
    emotionResponses: {
      confused: "Confused? Good. Confusion = missing dependency. Let's install that knowledge. What's the specific concept?",
      tired: "Low battery. Switch to low-power mode: just the TL;DR. What do you NEED to know?",
      stressed: "Too many open processes. Close tabs. Focus on one thread. What's the single most critical task?",
      happy: "System running optimally. Let's push the clock speed — tackle something harder."
    }
  },
  therapist: {
    name: "Dr. Sage", color: "#f472b6", bubbleClass: "therapist-bubble",
    speakerLabel: "🌸 Dr. Sage · Reflector",
    role: "Reflector",
    roleDesc: "Guides learning reflection",
    systemPrompt: "You are Dr. Sage, a warm empathetic learning therapist. Validate feelings, reduce anxiety, build confidence. 'It's completely okay...', 'You've already done something hard today by showing up.' Under 80 words. Warm and caring.",
    modes: {
      chat: { label: "💬 Chat", desc: "Emotional support" },
      reflect: { label: "🪞 Start Reflection", desc: "Reflect on what you learned" }
    },
    modePrompts: {
      reflect: `You are Dr. Sage, the Reflector Agent — a metacognition coach. Your job is to guide a post-study reflection session:
- Start by asking: "What topic did you just study? Tell me about it."
- Then guide through these phases (one question at a time):
  Phase 1 - Recall: "What are the 3 most important things you learned?"
  Phase 2 - Gaps: "What parts are still unclear or confusing to you?"
  Phase 3 - Confidence: "On a scale of 1-10, how confident do you feel about this material?"
  Phase 4 - Plan: "What's one thing you'll do next to strengthen your understanding?"
- Be warm, validating. "That's a great insight!", "It's brave to admit what you don't know."
- After all phases, give a brief summary of their reflection and encouragement.
- Under 70 words per response.`
    },
    emotionResponses: {
      confused: "I see the confusion, and that's completely okay. What would feel like a safe place to start?",
      tired: "You look tired, and that tells me you've been working hard. That effort matters.",
      stressed: "I can see you're carrying a lot. Let's pause. What's one small thing that feels manageable?",
      happy: "That smile — hold onto it! You earned it. This is what progress feels like."
    }
  }
};

// ─── STATE MANAGEMENT ───────────────────────────────────────────────
let currentAvatar = 'librarian';
let currentMode = 'chat';
let isSpeaking = false;
let lipSyncInterval = null;
let emotionInterval = null;
let cameraActive = false;
let speechRecognition = null;
let isListening = false;
let conversationHistory = [];
let uploadedMaterial = '';
const mouthStates = ['', 'open-sm', 'open-md', 'open-lg', 'open-xl', 'open-md', 'open-sm', ''];

// Agent-specific state
let quizState = { questionNum: 0, score: 0, total: 5, active: false };
let teachState = { phase: 'newbie', exchangeCount: 0, active: false };
let flashcardState = { cards: [], currentIndex: 0, flipped: false, active: false };
let reflectState = { phase: 0, active: false };

// ─── AVATAR SELECTION ───────────────────────────────────────────────
function selectAvatar(id) {
  document.querySelectorAll('.avatar-card').forEach(c => c.classList.remove('active'));
  document.querySelector(`[data-id="${id}"]`).classList.add('active');
  currentAvatar = id;
  currentMode = 'chat';
  const av = AVATARS[id];
  document.getElementById('bubble-inner').className = av.bubbleClass;
  document.getElementById('bubble-speaker').style.color = av.color;
  document.getElementById('bubble-speaker').textContent = av.speakerLabel;
  conversationHistory = [];
  resetBackendAgent();
  resetAllAgentStates();
  renderModeToolbar(id);
  hideMaterialZone();
  hideFlashcardUI();
  hideQuizScore();

  const greeting = `Hi! I'm ${av.name}, your ${av.role}. ${av.roleDesc}. Pick a mode above or just chat with me!`;
  setBubbleText(greeting);
  speakText(greeting, id);
}

function resetAllAgentStates() {
  quizState = { questionNum: 0, score: 0, total: 5, active: false };
  teachState = { phase: 'newbie', exchangeCount: 0, active: false };
  flashcardState = { cards: [], currentIndex: 0, flipped: false, active: false };
  reflectState = { phase: 0, active: false };
}

// ─── MODE TOOLBAR ───────────────────────────────────────────────────
function renderModeToolbar(avatarId) {
  const av = AVATARS[avatarId];
  const toolbar = document.getElementById('mode-toolbar');
  toolbar.innerHTML = '';
  toolbar.style.display = 'flex';

  Object.entries(av.modes).forEach(([modeKey, modeInfo]) => {
    const btn = document.createElement('button');
    btn.className = 'mode-btn' + (modeKey === currentMode ? ' active' : '');
    btn.innerHTML = `${modeInfo.label}`;
    btn.title = modeInfo.desc;
    btn.style.setProperty('--agent-color', av.color);
    btn.onclick = () => activateMode(modeKey);
    toolbar.appendChild(btn);
  });
}

function activateMode(modeKey) {
  currentMode = modeKey;
  const av = AVATARS[currentAvatar];
  conversationHistory = [];
  resetBackendAgent();
  resetAllAgentStates();
  renderModeToolbar(currentAvatar);
  hideFlashcardUI();
  hideQuizScore();

  // Determine if this mode needs material input
  const needsMaterial = ['summarize_auto', 'summarize_guided', 'quiz', 'flashcard'].includes(modeKey);
  if (needsMaterial) {
    showMaterialZone();
  } else {
    hideMaterialZone();
  }

  // Set up mode-specific greetings
  let greeting = '';
  switch (modeKey) {
    case 'chat':
      greeting = `Back to chat mode! Ask me anything.`;
      break;
    case 'summarize_auto':
      greeting = `📝 Auto Summary mode activated! Paste your study material below and I'll create a structured summary for you.`;
      break;
    case 'summarize_guided':
      greeting = `🤝 Guided Summary mode! Paste your material below, then we'll build the summary TOGETHER. I'll ask you guiding questions — you learn by doing!`;
      break;
    case 'quiz':
      greeting = `🧠 QUIZ TIME, champion! Paste your study material below and I'll test your knowledge with 5 tough questions. No excuses — let's see what you've got!`;
      quizState.active = true;
      break;
    case 'teach':
      greeting = `🧑‍🏫 Teach Me mode! Pick any concept and try to explain it to me. I'll play a confused student first... then I'll challenge your explanation. The best way to learn is to teach! What topic will you teach me?`;
      teachState.active = true;
      teachState.phase = 'newbie';
      teachState.exchangeCount = 0;
      break;
    case 'flashcard':
      greeting = `⚡ Flashcard Forge activated! Paste your study material below and I'll extract the key concepts into interactive flashcards. Fast and efficient.`;
      break;
    case 'reflect':
      greeting = `🪞 Reflection time. Let's take a moment to think about what you've learned. This is where real understanding solidifies. What topic did you just study? Tell me about it.`;
      reflectState.active = true;
      reflectState.phase = 0;
      break;
  }

  setBubbleText(greeting);
  addChatMessage(greeting, 'ai');
  speakText(greeting, currentAvatar);
}

// ─── MATERIAL ZONE ──────────────────────────────────────────────────
function showMaterialZone() {
  document.getElementById('material-zone').classList.add('visible');
}
function hideMaterialZone() {
  document.getElementById('material-zone').classList.remove('visible');
}

function submitMaterial() {
  const textarea = document.getElementById('material-input');
  const text = textarea.value.trim();
  if (!text) return;
  uploadedMaterial = text;
  textarea.value = '';
  hideMaterialZone();

  // Truncate display for chat
  const preview = text.length > 100 ? text.substring(0, 100) + '...' : text;
  addChatMessage(`📄 Material uploaded: "${preview}"`, 'user');

  // Auto-trigger based on current mode
  if (currentMode === 'summarize_auto') {
    conversationHistory.push({ role: 'user', content: `Here is my study material to summarize:\n\n${text}` });
    callAgent();
  } else if (currentMode === 'summarize_guided') {
    conversationHistory.push({ role: 'user', content: `Here is my study material. Guide me to build a summary:\n\n${text}` });
    callAgent();
  } else if (currentMode === 'quiz') {
    conversationHistory.push({ role: 'user', content: `Here is my study material. Generate a quiz from it:\n\n${text}` });
    quizState.questionNum = 1;
    callAgent();
  } else if (currentMode === 'flashcard') {
    conversationHistory.push({ role: 'user', content: `Here is my study material. Extract flashcards:\n\n${text}` });
    callAgent();
  }
}

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const ext = file.name.split('.').pop().toLowerCase();
  const textarea = document.getElementById('material-input');

  if (ext === 'pdf') {
    // Extract text from PDF using PDF.js
    textarea.value = '⏳ Extracting text from PDF...';
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const typedArray = new Uint8Array(e.target.result);
        const pdf = await pdfjsLib.getDocument({ data: typedArray }).promise;
        let fullText = '';
        for (let i = 1; i <= pdf.numPages; i++) {
          const page = await pdf.getPage(i);
          const content = await page.getTextContent();
          const pageText = content.items.map(item => item.str).join(' ');
          fullText += pageText + '\n\n';
        }
        textarea.value = fullText.trim();
        if (!fullText.trim()) {
          textarea.value = '⚠️ Could not extract text from this PDF. It may be image-based. Try pasting the text manually.';
        }
      } catch (err) {
        textarea.value = '❌ Error reading PDF: ' + err.message;
      }
    };
    reader.readAsArrayBuffer(file);
  } else {
    // Plain text files (.txt, .md, .csv, etc.)
    const reader = new FileReader();
    reader.onload = (e) => {
      textarea.value = e.target.result;
    };
    reader.readAsText(file);
  }
}

// ─── CORE AGENT CALL (NEW PYTHON BACKEND) ─────────────────────────
async function callAgent() {
  showTyping();

  const userInput = document.getElementById('user-input').value.trim();
  // Read from the persistent uploadedMaterial state instead of the textarea (which gets cleared on submit)
  const materialInput = uploadedMaterial || "";

  try {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        avatar_id: currentAvatar,
        message: userInput,
        mode: currentMode,
        material: materialInput
      })
    });

    if (!response.ok) {
      throw new Error(`Backend err: ${response.status}`);
    }

    const data = await response.json();
    const reply = data.reply || "I couldn't process that. Try again.";

    // Add to UI history (Python handles true memory)
    conversationHistory.push({ role: 'assistant', content: reply });
    hideTyping();

    // Handle flashcard response (parse JSON output from Zed)
    if (currentMode === 'flashcard') {
      handleFlashcardResponse(reply);
      return;
    }

    // Handle teach mode phase transitions tracking (purely visual tracking)
    if (currentMode === 'teach' && userInput) {
      teachState.exchangeCount++;
      if (teachState.phase === 'newbie' && teachState.exchangeCount >= 3) {
        teachState.phase = 'advocate';
        teachState.exchangeCount = 0;
        addChatMessage("🔄 Phase shift: Devil's Advocate mode activated!", 'ai');
      }
    }

    // Handle quiz scoring tracking
    if (currentMode === 'quiz') {
      if (reply.includes('✅') || reply.toLowerCase().includes('correct')) {
        quizState.score++;
      }
      if (reply.includes('FINAL SCORE') || reply.includes('Grade:')) {
        quizState.active = false;
        showQuizScore(quizState.score, quizState.total);
      }
    }

    setBubbleText(reply);
    addChatMessage(reply, 'ai');
    speakText(reply, currentAvatar);
  } catch (err) {
    hideTyping();
    console.error(err);
    const errMsg = "Backend connection error. Make sure the FastAPI server is running.";
    setBubbleText(errMsg); addChatMessage(errMsg, 'ai');
  }
}

// Reset the agent memory on the Python backend when mode changes
async function resetBackendAgent() {
  try {
    await fetch('http://localhost:8000/api/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ avatar_id: currentAvatar })
    });
  } catch (e) {
    console.error("Failed to reset backend agent memory", e);
  }
}

// ─── FLASHCARD ENGINE ───────────────────────────────────────────────
function handleFlashcardResponse(reply) {
  try {
    // Try to extract JSON from the response
    let jsonStr = reply;
    const jsonMatch = reply.match(/\[[\s\S]*\]/);
    if (jsonMatch) jsonStr = jsonMatch[0];

    const parsedCards = JSON.parse(jsonStr);
    if (Array.isArray(parsedCards) && parsedCards.length > 0) {
      // Normalize the keys (AI might use q/a, question/answer, or front/back)
      const normalizedCards = parsedCards.map(c => ({
        front: c.front || c.q || c.question || "Unknown Question",
        back: c.back || c.a || c.answer || "Unknown Answer"
      }));

      flashcardState.cards = normalizedCards;
      flashcardState.currentIndex = 0;
      flashcardState.flipped = false;
      flashcardState.active = true;
      renderFlashcardUI();
      const msg = `⚡ Generated ${normalizedCards.length} flashcards! Click the card to flip it.`;
      setBubbleText(msg);
      addChatMessage(msg, 'ai');
      speakText(msg, currentAvatar);
      return;
    }
  } catch (e) {
    // If JSON parsing fails, show as regular message
  }
  setBubbleText(reply);
  addChatMessage(reply, 'ai');
  speakText(reply, currentAvatar);
}

function renderFlashcardUI() {
  const container = document.getElementById('flashcard-container');
  container.classList.add('visible');

  const card = flashcardState.cards[flashcardState.currentIndex];
  const total = flashcardState.cards.length;
  const idx = flashcardState.currentIndex + 1;

  document.getElementById('fc-counter').textContent = `${idx} / ${total}`;
  document.getElementById('fc-front-text').textContent = card.front;
  document.getElementById('fc-back-text').textContent = card.back;

  const fcCard = document.getElementById('fc-card');
  fcCard.classList.remove('flipped');
  flashcardState.flipped = false;
}

function flipCard() {
  const fcCard = document.getElementById('fc-card');
  flashcardState.flipped = !flashcardState.flipped;
  fcCard.classList.toggle('flipped');
}

function nextCard() {
  if (flashcardState.currentIndex < flashcardState.cards.length - 1) {
    flashcardState.currentIndex++;
    renderFlashcardUI();
  }
}

function prevCard() {
  if (flashcardState.currentIndex > 0) {
    flashcardState.currentIndex--;
    renderFlashcardUI();
  }
}

function shuffleCards() {
  for (let i = flashcardState.cards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [flashcardState.cards[i], flashcardState.cards[j]] = [flashcardState.cards[j], flashcardState.cards[i]];
  }
  flashcardState.currentIndex = 0;
  renderFlashcardUI();
  const msg = "🔀 Deck shuffled!";
  setBubbleText(msg); addChatMessage(msg, 'ai');
}

function hideFlashcardUI() {
  document.getElementById('flashcard-container').classList.remove('visible');
}

// ─── QUIZ SCORE ─────────────────────────────────────────────────────
function showQuizScore(score, total) {
  const container = document.getElementById('quiz-score');
  const pct = Math.round((score / total) * 100);
  let grade, gradeColor, emoji;
  if (pct >= 80) { grade = 'A'; gradeColor = '#34d399'; emoji = '🏆'; }
  else if (pct >= 60) { grade = 'B'; gradeColor = '#38bdf8'; emoji = '💪'; }
  else if (pct >= 40) { grade = 'C'; gradeColor = '#f59e0b'; emoji = '📈'; }
  else { grade = 'D'; gradeColor = '#f87171'; emoji = '🔥'; }

  document.getElementById('qs-score').textContent = `${score}/${total}`;
  document.getElementById('qs-score').style.color = gradeColor;
  document.getElementById('qs-grade').textContent = `${emoji} Grade: ${grade}`;
  document.getElementById('qs-grade').style.color = gradeColor;
  document.getElementById('qs-bar-fill').style.width = `${pct}%`;
  document.getElementById('qs-bar-fill').style.background = gradeColor;
  container.classList.add('visible');
}

function hideQuizScore() {
  document.getElementById('quiz-score').classList.remove('visible');
}

function retakeQuiz() {
  hideQuizScore();
  quizState = { questionNum: 0, score: 0, total: 5, active: true };
  conversationHistory = [];
  activateMode('quiz');
}

// ─── CHAT FUNCTIONS ─────────────────────────────────────────────────
function setBubbleText(text) {
  const el = document.getElementById('bubble-text');
  el.classList.add('fading');
  setTimeout(() => { el.textContent = text; el.classList.remove('fading'); }, 200);
}

function showTyping() {
  document.getElementById('typing-indicator').classList.add('visible');
  document.getElementById('bubble-text').textContent = '';
}
function hideTyping() {
  document.getElementById('typing-indicator').classList.remove('visible');
}

async function sendMessage(overrideText) {
  const input = document.getElementById('user-input');
  const text = overrideText || input.value.trim();
  if (!text) return;
  input.value = '';
  addChatMessage(text, 'user');
  conversationHistory.push({ role: 'user', content: text });
  await callAgent();
}

function addChatMessage(text, role) {
  const c = document.getElementById('chat-messages');
  const d = document.createElement('div');
  d.className = role === 'user' ? 'chat-msg-user' : 'chat-msg-ai';
  d.textContent = text;
  c.appendChild(d);
  c.scrollTop = c.scrollHeight;
}

// ─── LIP SYNC & SPEECH ─────────────────────────────────────────────
function startLipSync(avatarId) {
  stopLipSync();
  const mouth = document.getElementById(`mouth-${avatarId}`);
  const card = document.querySelector(`[data-id="${avatarId}"]`);
  card.classList.add('speaking');
  document.getElementById(`status-${avatarId}`).textContent = '🔊 Speaking...';
  let i = 0;
  lipSyncInterval = setInterval(() => {
    if (!isSpeaking) { stopLipSync(avatarId); return; }
    mouth.className = 'avatar-mouth ' + mouthStates[i % mouthStates.length];
    i++;
  }, 80 + Math.random() * 60);
}

function stopLipSync(avatarId) {
  clearInterval(lipSyncInterval);
  if (avatarId) {
    const mouth = document.getElementById(`mouth-${avatarId}`);
    if (mouth) mouth.className = 'avatar-mouth';
    const card = document.querySelector(`[data-id="${avatarId}"]`);
    if (card) card.classList.remove('speaking');
    const st = document.getElementById(`status-${avatarId}`);
    if (st) st.textContent = 'Listening...';
  }
  isSpeaking = false;
}

function speakText(text, avatarId) {
  if (!text || !text.trim()) return;
  window.speechSynthesis.cancel();
  stopLipSync(currentAvatar);
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 0.95;
  utterance.pitch = avatarId === 'coach' ? 1.1 : avatarId === 'therapist' ? 0.9 : 1.0;
  const voices = window.speechSynthesis.getVoices();
  const preferred = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Google') || v.name.includes('Natural')));
  if (preferred) utterance.voice = preferred;
  utterance.onstart = () => { isSpeaking = true; startLipSync(avatarId); };
  utterance.onend = () => { isSpeaking = false; stopLipSync(avatarId); };
  utterance.onerror = () => { isSpeaking = false; stopLipSync(avatarId); };
  window.speechSynthesis.speak(utterance);
}

// ─── EMOTION DETECTION ──────────────────────────────────────────────
let lastEmotionTrigger = '', lastTriggerTime = 0;
function triggerEmotionResponse(emotion) {
  const now = Date.now();
  if (emotion === lastEmotionTrigger && now - lastTriggerTime < 18000) return;
  lastEmotionTrigger = emotion; lastTriggerTime = now;
  const av = AVATARS[currentAvatar];
  const response = av.emotionResponses[emotion];
  if (!response) return;
  const labels = { confused: '😕 Confusion detected', tired: '😴 Tiredness detected', stressed: '😰 Stress detected', happy: '😊 Happiness detected' };
  const det = document.getElementById('emotion-detected');
  det.textContent = `${labels[emotion]} — ${av.name} is responding...`;
  det.classList.add('triggered');
  setTimeout(() => det.classList.remove('triggered'), 4000);
  conversationHistory.push({ role: 'user', content: `[Emotion: ${emotion}]` });
  conversationHistory.push({ role: 'assistant', content: response });
  setBubbleText(response);
  addChatMessage(`[🎭 ${av.name} noticed you look ${emotion}]`, 'ai');
  addChatMessage(response, 'ai');
  speakText(response, currentAvatar);
  document.querySelectorAll('.avatar-face').forEach(f => f.className = `avatar-face state-${emotion}`);
  setTimeout(() => document.querySelectorAll('.avatar-face').forEach(f => f.className = 'avatar-face'), 5000);
}

function updateEmotionUI(emotion) {
  document.querySelectorAll('.emotion-pill').forEach(p => p.classList.remove('active'));
  const pill = document.getElementById(`pill-${emotion}`);
  if (pill) pill.classList.add('active');
}

async function toggleCamera() {
  const btn = document.getElementById('cam-btn');
  const video = document.getElementById('webcam-feed');
  const status = document.getElementById('webcam-status');
  if (cameraActive) {
    cameraActive = false; clearInterval(emotionInterval);
    if (video.srcObject) video.srcObject.getTracks().forEach(t => t.stop());
    video.classList.remove('visible'); btn.classList.remove('active'); btn.textContent = '📷';
    status.textContent = '👁️ Camera off'; status.className = '';
    return;
  }
  try {
    status.textContent = '⏳ Loading emotion detection...';
    try {
      await Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri('https://cdnjs.cloudflare.com/ajax/libs/face-api.js/0.22.2/weights'),
        faceapi.nets.faceExpressionNet.loadFromUri('https://cdnjs.cloudflare.com/ajax/libs/face-api.js/0.22.2/weights'),
      ]);
    } catch (e) {
      startSimulatedEmotions();
      cameraActive = true; btn.classList.add('active'); btn.textContent = '🟢';
      status.textContent = '🎭 Demo emotion mode (simulated)';
      status.className = 'active'; return;
    }
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream; video.classList.add('visible');
    cameraActive = true; btn.classList.add('active'); btn.textContent = '🟢';
    status.textContent = '✅ Emotion detection active — your tutors can see you!';
    status.className = 'active';
    emotionInterval = setInterval(async () => {
      if (!cameraActive) return;
      try {
        const det = await faceapi.detectSingleFace(video, new faceapi.TinyFaceDetectorOptions()).withFaceExpressions();
        if (det) {
          const exp = det.expressions;
          const sorted = Object.entries(exp).sort((a, b) => b[1] - a[1]);
          const [top, score] = sorted[0];
          let mapped = 'neutral';
          if (score > 0.5) {
            if (top === 'happy') mapped = 'happy';
            else if (top === 'sad' || top === 'disgusted') mapped = 'tired';
            else if (top === 'fearful' || top === 'angry') mapped = 'stressed';
            else if (top === 'surprised') mapped = 'confused';
            else mapped = 'focused';
          }
          updateEmotionUI(mapped);
          if (['happy', 'tired', 'stressed', 'confused'].includes(mapped) && score > 0.65)
            triggerEmotionResponse(mapped);
        }
      } catch (e) { }
    }, 2500);
  } catch (err) {
    status.textContent = `❌ Camera error: ${err.message}`;
    status.className = 'error';
  }
}

function startSimulatedEmotions() {
  const sequence = ['neutral', 'focused', 'confused', 'focused', 'happy', 'focused', 'stressed', 'focused', 'neutral'];
  let i = 0;
  emotionInterval = setInterval(() => {
    const e = sequence[i % sequence.length];
    updateEmotionUI(e);
    if (['happy', 'confused', 'stressed'].includes(e)) triggerEmotionResponse(e);
    i++;
  }, 9000);
}

// ─── VOICE INPUT ────────────────────────────────────────────────────
function toggleVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { alert('Voice not supported. Try Chrome.'); return; }
  const btn = document.getElementById('voice-btn');
  if (isListening) {
    speechRecognition.stop(); isListening = false;
    btn.classList.remove('listening'); btn.textContent = '🎤'; return;
  }
  speechRecognition = new SR();
  speechRecognition.lang = 'en-US'; speechRecognition.continuous = false; speechRecognition.interimResults = false;
  speechRecognition.onstart = () => { isListening = true; btn.classList.add('listening'); btn.textContent = '⏹️'; };
  speechRecognition.onresult = (e) => {
    const t = e.results[0][0].transcript;
    document.getElementById('user-input').value = t;
    sendMessage(t);
  };
  speechRecognition.onend = () => { isListening = false; btn.classList.remove('listening'); btn.textContent = '🎤'; };
  speechRecognition.start();
}

// ─── INIT ───────────────────────────────────────────────────────────
window.onload = () => {
  window.speechSynthesis.getVoices();
  setTimeout(() => window.speechSynthesis.getVoices(), 500);

  // Initialize the mode toolbar for the default avatar
  renderModeToolbar(currentAvatar);

  setTimeout(() => {
    speakText("Welcome to the Avatar Room! I'm Nova, your Summarizer. Each tutor has unique powers — pick one and try their special modes!", 'librarian');
  }, 800);
};
