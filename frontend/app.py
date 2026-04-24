import streamlit as st
import requests

# =========================
# Config
# =========================
API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="Document Chatbot", page_icon="🤖", layout="centered")

# =========================
# Custom CSS
# =========================
st.markdown(
    """
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .main-header h1 {
        color: #4A90D9;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #888;
        font-size: 1.1rem;
    }
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }
    .sidebar-info {
        padding: 1rem;
        background: #1E1E2E;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .doc-badge {
        display: inline-block;
        background: #4A90D9;
        color: white;
        padding: 4px 10px;
        border-radius: 15px;
        margin: 3px;
        font-size: 0.85rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/chatbot.png", width=80)
    st.markdown("## 📚 Document Chatbot")
    st.markdown("---")

    st.markdown("### 📄 Loaded Documents")
    st.markdown(
        """
    <span class='doc-badge'>📝 webscraping.txt</span><br>
    <span class='doc-badge'>📕 oops_java.pdf</span>
    <span class='doc-badge'>📕 قانون الإجراءات الجنائية.pdf</span>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### 💡 Example Questions")
    example_questions = [
        "What is web scraping?",
        "Explain OOP in Java",
        "What are the 4 pillars of OOP?",
        "How does BeautifulSoup work?",
    ]
    for q in example_questions:
        if st.button(f"➜ {q}", key=q, use_container_width=True):
            st.session_state["example_question"] = q

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Powered by Gemini + LangChain + FAISS")

# =========================
# Header
# =========================
st.markdown(
    """
<div class='main-header'>
    <h1>🤖 Document Chatbot</h1>
    <p>Ask anything about your uploaded documents</p>
</div>
""",
    unsafe_allow_html=True,
)

# =========================
# Chat State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# Welcome message
# =========================
if len(st.session_state.messages) == 0:
    st.markdown(
        """
    <div style='text-align:center; padding: 2rem; color: #888;'>
        <p style='font-size: 3rem;'>💬</p>
        <p style='font-size: 1.2rem;'>Start a conversation by typing below<br>or pick an example from the sidebar!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# =========================
# Display chat history
# =========================
for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "human" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# =========================
# Handle example question
# =========================
if "example_question" in st.session_state:
    prompt = st.session_state.pop("example_question")
else:
    prompt = st.chat_input("💬 Ask me anything about your documents...")

# =========================
# Process prompt
# =========================
if prompt:
    # Show user message
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("human", avatar="🧑"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("ai", avatar="🤖"):
        with st.spinner("🔍 Searching documents & thinking..."):
            try:
                res = requests.post(API_URL, json={"text": prompt}, timeout=120)
                res.raise_for_status()
                answer = res.json()["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "ai", "content": answer})

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Cannot connect to backend. Make sure the API server is running!"
                )
                st.code(
                    "cd ~/rag_project/backend\nuvicorn main:app --reload",
                    language="bash",
                )

            except requests.exceptions.Timeout:
                st.error("⏳ Request timed out. The server might be busy, try again.")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
