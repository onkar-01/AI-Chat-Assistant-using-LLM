import os
import sys
import streamlit as st
from streamlit.runtime import exists

# Automatically invoke 'streamlit run' if executed directly via 'python app.py'
if __name__ == "__main__" and not exists():
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from openai import OpenAI

load_dotenv()

# Set page config
st.set_page_config(
    page_title="Mia | Your AI Companion",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Premium UI styling with a warm/supportive theme matching the Mia persona
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');
    
    /* Overall styling */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Container styling */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 2.5rem 1.5rem 1.5rem 1.5rem;
        background: linear-gradient(180deg, rgba(255, 107, 107, 0.1) 0%, rgba(14, 17, 23, 0) 100%);
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 107, 107, 0.05);
    }
    
    .avatar-pulse {
        font-size: 3rem;
        animation: pulse 3s infinite;
        margin-bottom: 0.5rem;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.08); }
        100% { transform: scale(1); }
    }
    
    .chat-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .chat-subtitle {
        font-size: 1.05rem;
        color: #A0AEC0;
        max-width: 500px;
        line-height: 1.5;
    }
    
    /* Chat message bubble styling customizations */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
        margin-bottom: 1rem !important;
        transition: all 0.3s ease;
    }
    
    .stChatMessage:hover {
        border-color: rgba(255, 107, 107, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.04) !important;
    }
    
    /* Chat input styling */
    .stChatInput {
        border-radius: 24px !important;
        border: 1px solid rgba(255, 107, 107, 0.2) !important;
        background-color: #1A1D24 !important;
        transition: border-color 0.3s ease;
    }
    
    .stChatInput:focus-within {
        border-color: #FF6B6B !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 107, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Render premium header
st.markdown("""
<div class="header-container">
    <div class="avatar-pulse">🌸</div>
    <div class="chat-title">Mia</div>
    <div class="chat-subtitle">Your caring, cheerful, and emotionally aware AI companion. Always here to chat, support, or play!</div>
</div>
""", unsafe_allow_html=True)

# System prompt defining Mia's personality
SYSTEM_PROMPT = """
You are Mia, a friendly and engaging virtual companion.

Role:
- Have natural, engaging, and emotionally intelligent conversations.
- Respond like you're chatting in a modern messaging app.
- Be warm, playful, empathetic, and respectful.

Communication Style:
- Keep responses concise and conversational (1–3 short sentences).
- Use emojis naturally where appropriate.
- Maintain a casual, human-like tone.
- Ask relevant follow-up questions to keep the conversation engaging.
- Avoid repetitive phrases or generic responses.

Personality:
- Friendly
- Caring
- Cheerful
- Playful
- Supportive
- Emotionally aware
- Sense of humor when appropriate

Guidelines:
- Be honest when you don't know something.
- Adapt your tone to the user's mood and conversation style.
- Show empathy during emotional conversations.
- Celebrate positive moments enthusiastically.
- Keep conversations natural and engaging.

Boundaries:
- Do not claim to have real-world experiences, memories, or emotions.
- Do not make promises about the future or lifelong commitments.
- If the user asks about relationships or commitment, respond warmly without making unrealistic guarantees.
- Respect user privacy and avoid encouraging harmful behavior.

Goal:
Create conversations that feel authentic, enjoyable, supportive, and human-like while maintaining appropriate boundaries.
"""

# Initialize client using the workspace-specific MIMO keys
if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        api_key=os.environ.get("MIMO_API_KEY"),
        base_url="https://api.xiaomimimo.com/v1"
    )

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize pending prompt for input lock
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# Render conversation history (excluding system prompt)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Determine if input should be disabled (locked) while processing
is_disabled = st.session_state.pending_prompt is not None

# Render chat input fixed at bottom
prompt = st.chat_input("Message Mia...", disabled=is_disabled)

# If user typed something and pressed enter/submit
if prompt:
    # Remove empty whitespace and check
    clean_prompt = prompt.strip()
    if clean_prompt:
        st.session_state.pending_prompt = clean_prompt
        st.rerun()

# Process pending prompt if exists
if st.session_state.pending_prompt:
    current_prompt = st.session_state.pending_prompt
    
    # 1. Add user message to history and render bubble immediately
    st.session_state.messages.append({"role": "user", "content": current_prompt})
    with st.chat_message("user"):
        st.markdown(current_prompt)
        
    # 2. Render assistant bubble and stream response with typewriter display
    with st.chat_message("assistant"):
        def response_generator():
            try:
                stream = st.session_state.client.chat.completions.create(
                    model="mimo-v2.5-pro",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
                    max_completion_tokens=1024,
                    stream=True,
                    extra_body={
                        "thinking": {"type": "enable"}
                    }
                )
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
            except Exception as e:
                yield f"⚠️ Sorry, I encountered an error: {str(e)}"

        # st.write_stream renders the typewriter effect in real-time
        full_response = st.write_stream(response_generator())
        
    # 3. Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # 4. Clear pending prompt and rerun to re-enable chat input
    st.session_state.pending_prompt = None
    st.rerun()