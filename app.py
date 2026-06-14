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

# Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# Session State
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "notes_count" not in st.session_state:
    st.session_state.notes_count = 0

if "quiz_count" not in st.session_state:
    st.session_state.quiz_count = 0
if len(st.session_state.messages) == 0:
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "👋 Welcome to CampusBuddy! Ask me about coding, academics, AI, projects, placements, or career guidance."
        }
    )
# =========================
# Sidebar
# =========================

st.sidebar.markdown("""
<h2 style='
color:white;
font-weight:800;
'>
🎓 CampusBuddy
</h2>
""", unsafe_allow_html=True)
st.sidebar.image("assets/logo.png", width=90)
st.sidebar.markdown("""
<span style='color:#94A3B8'>
Your AI-Powered<br>
Campus Companion
</span>
""", unsafe_allow_html=True)

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

st.sidebar.markdown("### 🚀 Quick Access")

mode = st.sidebar.radio(
    "Select Mode",
    [
        "🤖 AI Assistant",
        "📚 Study Help",
        "💻 Coding Mentor",
        "🎯 Career Guidance"
    ]
)

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
    st.rerun()

# =========================
# Main Page
# =========================
st.markdown("""
<div style='padding-top:20px;'>

<h1 style='
background: linear-gradient(
90deg,
#00E5FF,
#A855F7,
#FF4D9D
);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
font-size:64px;
font-weight:900;
margin-bottom:0;
'>
CampusBuddy
</h1>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<h4 style='color:#CBD5E1; margin-top:0;'>
🚀 Study Smarter • Code Better • Build Your Future
</h4>
""", unsafe_allow_html=True)

# Quick Action Buttons```python
st.markdown(f"""
<div style="
background:rgba(34,211,238,0.08);
border:1px solid rgba(34,211,238,0.3);
padding:15px;
border-radius:15px;
margin-bottom:15px;
">

<h4 style="margin:0;color:#22D3EE;">
⚡ Current Mode
</h4>

<p style="margin:5px 0 0 0;color:white;">
{mode}
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:#0F172A;
padding:15px;
border-radius:18px;
border:1px solid rgba(168,85,247,.25);
margin-bottom:15px;
">

<h3 style="color:#A855F7;">
🚀 What CampusBuddy Can Do
</h3>

📚 Notes &nbsp;&nbsp;&nbsp;
🧠 Quiz &nbsp;&nbsp;&nbsp;
💻 Coding &nbsp;&nbsp;&nbsp;
🎓 Academics &nbsp;&nbsp;&nbsp;
🎯 Career &nbsp;&nbsp;&nbsp;
🚀 Projects

</div>
""", unsafe_allow_html=True)
# =========================
# Statistics Cards
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="
    background:rgba(0,229,255,.08);
    padding:20px;
    border-radius:18px;
    text-align:center;
    border:1px solid rgba(0,229,255,.3);
    ">
    <h3>📚</h3>
    <h2>{}</h2>
    <p>Notes</p>
    </div>
    """.format(st.session_state.notes_count), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
    background:rgba(168,85,247,.08);
    padding:20px;
    border-radius:18px;
    text-align:center;
    border:1px solid rgba(168,85,247,.3);
    ">
    <h3>🧠</h3>
    <h2>{}</h2>
    <p>Quizzes</p>
    </div>
    """.format(st.session_state.quiz_count), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
    background:rgba(255,77,157,.08);
    padding:20px;
    border-radius:18px;
    text-align:center;
    border:1px solid rgba(255,77,157,.3);
    ">
    <h3>💬</h3>
    <h2>{}</h2>
    <p>Chats</p>
    </div>
    """.format(len(st.session_state.messages)), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="
    background:rgba(34,211,238,.08);
    padding:20px;
    border-radius:18px;
    text-align:center;
    border:1px solid rgba(34,211,238,.3);
    ">
    <h3>🎯</h3>
    <h2>24/7</h2>
    <p>Available</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Tabs
# =========================

tab1, tab2, tab3 = st.tabs(
    ["🤖 Chat", "📚 Notes", "🧠 Quiz"]
)

with tab2:

    st.subheader("📚 AI Notes Generator")

    topic = st.text_input(
        "Enter Topic",
        key="notes_topic"
    )

    if st.button(
        "Generate Notes",
        key="notes_btn"
    ):

        if topic:

            with st.spinner("Generating Notes..."):

                notes_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role":"system",
                            "content":"Create student-friendly notes."
                        },
                        {
                            "role":"user",
                            "content":f"""
Generate detailed notes on {topic}.

Include:
1. Introduction
2. Key Concepts
3. Examples
4. Advantages
5. Interview Questions
6. Summary
"""
                        }
                    ]
                )

                notes = notes_response.choices[0].message.content
                st.session_state.notes_count += 1
                st.markdown(notes)
with tab3:

    st.subheader("🧠 AI Quiz Generator")

    quiz_topic = st.text_input(
        "Enter Quiz Topic",
        key="quiz_topic"
    )

    if st.button(
        "Generate Quiz",
        key="quiz_btn"
    ):

        if quiz_topic:

            with st.spinner("Generating Quiz..."):

                quiz_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role":"system",
                            "content":"Create MCQ quizzes."
                        },
                        {
                            "role":"user",
                            "content":f"""
Generate 10 multiple choice questions on {quiz_topic}.

Format exactly like:

Q1. Question?

A) Option 1
B) Option 2
C) Option 3
D) Option 4

✅ Correct Answer: A

Leave a blank line between questions.

Include:
- Question
- 4 options
- Correct Answer
"""
                        }
                    ]
                )

                quiz = quiz_response.choices[0].message.content
                st.session_state.quiz_count += 1
                st.markdown(quiz)
    
with tab1:

    # Display Previous Messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
# =========================
# Chat Input
# =========================

prompt = st.chat_input(
    "Ask CampusBuddy anything..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        if mode == "📚 Study Help":
            system_prompt = """
You are CampusBuddy Study Assistant.

Help students with:
- Notes
- Assignments
- Exam Preparation
- MCQs
- Academic Concepts

Explain topics in simple language with examples.
"""

        elif mode == "💻 Coding Mentor":
            system_prompt = """
You are CampusBuddy Coding Mentor.

Help students with:
- Python
- C
- Java
- Data Structures
- Algorithms
- Projects
- Debugging

Provide code examples whenever possible.
"""

        elif mode == "🎯 Career Guidance":
            system_prompt = """
You are CampusBuddy Career Guide.

Help students with:
- Resume Building
- LinkedIn
- Internships
- Placements
- Interview Preparation
- Career Roadmaps

Give practical advice.
"""

        else:
            system_prompt = """
You are CampusBuddy AI Assistant.

Help students with:
- Programming
- Academics
- AI & Machine Learning
- General Knowledge
- Career Guidance

Provide clear and accurate answers.
"""

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

        with st.chat_message("assistant"):

            with st.spinner("🤖 CampusBuddy is thinking..."):

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,      
                    temperature=0.7,
                    max_tokens=1024
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
st.markdown("""
<hr>

<div style='text-align:center;color:#94A3B8;padding:20px'>

<h3 style='
background:linear-gradient(90deg,#00E5FF,#A855F7,#FF4D9D);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:5px;
'>
🎓 CampusBuddy
</h3>

CampusBuddy © 2026<br>
Built with ❤️ using Streamlit + Groq

</div>
""", unsafe_allow_html=True)