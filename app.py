from click import prompt
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="CampusBuddy",
    page_icon="🎓",
    layout="wide"
)
st.markdown("""
<style>

/* Sidebar Width */
[data-testid="stSidebar"]{
    min-width:260px;
    max-width:260px;
}

/* Reduce top padding */
.block-container{
    padding-top:1rem;
}

/* Center Chat Area */
.main .block-container{
    max-width:900px;
    margin:auto;
}

/* Chat Input */
div[data-testid="stChatInput"]{
    max-width:700px !important;
    margin:auto !important;
}
/* Hide Streamlit Menu */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

</style>
""", unsafe_allow_html=True)

# Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# Session State
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# =========================
# Sidebar
# =========================

col1, col2 = st.sidebar.columns([1,2])

with col1:
    st.image("assets/logo.png", width=40)

with col2:
    st.markdown("### CampusBuddy")

st.sidebar.markdown(
"""
<div style='
height:1px;
background:linear-gradient(
90deg,
#00E5FF,
#A855F7,
#FF4D9D
);
margin:15px 0;
'>
</div>
""",
unsafe_allow_html=True
)
st.sidebar.markdown("### 🤖 AI Assistant")
st.sidebar.markdown(
"""
<div style='
height:1px;
background:linear-gradient(
90deg,
#00E5FF,
#A855F7,
#FF4D9D
);
margin:15px 0;
'>
</div>
""",
unsafe_allow_html=True
)
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    
    if st.sidebar.button("➕ New Chat"):    
        st.session_state.messages = []
        st.session_state.chat_history = []
    st.rerun()

    st.sidebar.markdown("---")

st.sidebar.markdown("### 💬 Recent Chats")
st.sidebar.markdown("---")

if st.sidebar.button("➕ New Chat", use_container_width=True):

    st.session_state.messages = []

    st.rerun()
if len(st.session_state.chat_history) == 0:
    st.sidebar.caption("No chats yet")

for i, chat in enumerate(reversed(st.session_state.chat_history[-10:])):

    if st.sidebar.button(
        chat,
        key=f"chat_{i}",
        use_container_width=True
    ):
        st.sidebar.success(f"Selected: {chat}")
st.sidebar.markdown("---")

# Display Previous Messages

for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
  
# =========================
# System Prompt
# =========================

system_prompt = """
You are CampusBuddy AI Assistant.

Help students with:
- Programming
- Academics
- AI & Machine Learning
- General Knowledge
- Career Guidance
- Resume Building
- Placements
- Projects
- DSA

Provide clear, accurate and student-friendly answers.
"""

# =========================
# Chat Input
# =========================

prompt = st.chat_input("Ask CampusBuddy anything...")
send_btn = prompt is not None

if send_btn and prompt:

    if len(st.session_state.messages) == 0:
        st.session_state.chat_history.append(prompt)
    if len(st.session_state.messages) == 0:

        chat_title = prompt[:30]

        st.session_state.chat_history.append(chat_title)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for msg in st.session_state.messages:
        messages.append(
            {
                "role": msg["role"],
                "content": msg["content"]
            }
        )

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )

        bot_reply = response.choices[0].message.content

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_reply
            }
        )

        with st.chat_message("assistant"):
            st.markdown(bot_reply)

    except Exception as e:
        st.error(f"❌ Error: {e}")
