"""
The Avatar Room — AI agents as emotion-aware, speaking, lip-syncing avatars.
Uses face-api.js for real-time webcam emotion detection.
Avatars react to how the student FEELS, not just what they type.
"""

import streamlit as st
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv

# Import our new core HTML builder
from core.avatar_html import get_avatar_html

# Load environment variables explicitly from the current directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path, override=True)
else:
    load_dotenv() # Fallback

# Set up the Streamlit page
st.set_page_config(
    page_title="Avatar Room | Student AI",
    page_icon="🎭",
    layout="wide",
)

# Hide default Streamlit chrome
st.markdown("""
<style>
    .stApp { background-color: #060810; color: #e2e8f0; }
    [data-testid="stSidebar"] { background-color: #0d1021; border-right: 1px solid #1e2240; }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Build the Sidebar
with st.sidebar:
    st.markdown("## 🎭 Avatar Room")
    st.markdown("---")
    
    # API Key Management
    mistral_key = os.getenv("MISTRAL_API_KEY")
    
    if not mistral_key:
        st.warning("⚠️ Mistral API Key not found in .env")
        api_key = st.text_input("🔑 Enter Mistral API Key", type="password")
        if api_key:
            os.environ["MISTRAL_API_KEY"] = api_key
            st.success("✅ Key set for this session!")
            st.rerun()
    else:
        st.success("✅ Mistral API key loaded")
        # Optional: Show masked key to confirm it's what they expect
        st.info(f"Using key starting with: {mistral_key[:4]}***")
        
    st.markdown("---")

    st.markdown("### 🎭 Your AI Agents")
    st.markdown("""
    <div style='font-size:0.82rem; color:#64748b; line-height:2.4'>
        👨‍🏫 <b style='color:#818cf8'>Prof. Atlas</b> — <span style='color:#94a3b8'>Study Buddy</span><br>
        <span style='font-size:0.72rem; margin-left:24px'>Teach him to test your understanding</span><br>
        💪 <b style='color:#34d399'>Coach Rex</b> — <span style='color:#94a3b8'>Quizmaster</span><br>
        <span style='font-size:0.72rem; margin-left:24px'>Quizzes, tests & knowledge checks</span><br>
        📚 <b style='color:#38bdf8'>Nova</b> — <span style='color:#94a3b8'>Summarizer</span><br>
        <span style='font-size:0.72rem; margin-left:24px'>Auto-summary or guided co-build</span><br>
        ⚡ <b style='color:#f59e0b'>Zed</b> — <span style='color:#94a3b8'>Flashcard Forge</span><br>
        <span style='font-size:0.72rem; margin-left:24px'>Interactive flashcard generation</span><br>
        🌸 <b style='color:#f472b6'>Dr. Sage</b> — <span style='color:#94a3b8'>Reflector</span><br>
        <span style='font-size:0.72rem; margin-left:24px'>Metacognition & self-reflection</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 👁️ Emotion Detection")
    st.markdown("""
    <div style='font-size:0.8rem; color:#64748b; line-height:1.9'>
        😕 Confused → Agent explains<br>
        😴 Tired → Agent energizes<br>
        😰 Stressed → Agent calms<br>
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

# Main Application Logic
def main():
    # 1. Get the Mistral Key (re-read after sidebar may have set it)
    mistral_key = os.getenv("MISTRAL_API_KEY", "")
    
    # Ensure no stray quotes from .env
    mistral_key = mistral_key.strip().strip('"').strip("'")
    
    # 2. Read the static CSS and JS files
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    try:
        with open(os.path.join(static_dir, "style.css"), "r", encoding="utf-8") as f:
            css_content = f.read()
        with open(os.path.join(static_dir, "script.js"), "r", encoding="utf-8") as f:
            js_content = f.read()
    except FileNotFoundError:
        st.error("Static files not found! Ensure 'static/style.css' and 'static/script.js' exist.")
        return

    # 3. Assemble the final HTML
    avatar_html_final = get_avatar_html(css_content, js_content)

    # 4. Render the component in Streamlit
    components.html(avatar_html_final, height=860, scrolling=True)

# Always call main — Streamlit doesn't reliably set __name__ == "__main__"
main()
