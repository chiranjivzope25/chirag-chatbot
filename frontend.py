import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Chirag Chatbot", layout="wide")

# --- Force Dark Theme ---
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.stTextInput > div > div > input {
    background-color: #262730;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("💬 Chat History")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.sidebar.write(f"🧑 {msg['content']}")
    else:
        st.sidebar.write(f"🅲 {msg['content']}")

# Title
st.title("🅲 Chirag Chatbot")

# Chat display
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style='text-align:right; margin:10px;'>
            <span style='background:#1E90FF; padding:10px; border-radius:10px; color:white;'>
                🧑 {msg['content']}
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align:left; margin:10px;'>
            <span style='background:#2D2D2D; padding:10px; border-radius:10px; color:white;'>
                🅲 {msg['content']}
            </span>
        </div>
        """, unsafe_allow_html=True)

# --- INPUT FORM (ENTER TO SEND) ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", key="input")
    submit = st.form_submit_button("Send")

if submit and user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": user_input}
        )
        reply = response.json()["reply"]
    except:
        reply = "⚠️ Backend not connected!"

    # Save bot reply
    st.session_state.messages.append({"role": "bot", "content": reply})

    st.rerun()

# Clear chat button
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()