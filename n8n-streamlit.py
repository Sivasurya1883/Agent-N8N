import streamlit as st
import requests
import uuid
from collections import defaultdict
from supabase import create_client, Client

# Supabase setup
SUPABASE_URL = "your url"
SUPABASE_KEY = "your key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

WEBHOOK_URL = "https://siva1883.app.n8n.cloud/webhook/invoke-supabase-agent"

AGENT_EMAIL = "sivasuriya81@gmail.com"  # update this as needed

# ------------------- Auth + Utility ------------------------

def login(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return res
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return None

def signup(email: str, password: str):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        return res
    except Exception as e:
        st.error(f"Signup failed: {str(e)}")
        return None

def generate_session_id():
    return str(uuid.uuid4())

def init_session_state():
    if "auth" not in st.session_state:
        st.session_state.auth = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

def handle_logout():
    st.session_state.auth = None
    st.session_state.session_id = None
    st.session_state.messages = []
    st.rerun()

def auth_ui():
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            auth = login(email, password)
            if auth:
                st.session_state.auth = auth
                st.session_state.session_id = generate_session_id()
                st.rerun()

    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            auth = signup(email, password)
            if auth:
                st.success("Sign up successful! Please log in.")

# ------------------- Chat & Storage ------------------------

def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def fetch_all_chat_histories():
    try:
        response = supabase.table("n8n_chat_histories").select("*").order("id", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"Failed to fetch chat histories: {str(e)}")
        return []

def group_chats_by_session(chat_data):
    sessions = defaultdict(list)
    for row in chat_data:
        session_id = row["session_id"]
        message = row.get("message")
        if message:
            sessions[session_id].append(message)
    return sessions

def agent_dashboard():
    st.subheader("🕵️ Agent Dashboard - Chat History Viewer")
    chat_data = fetch_all_chat_histories()
    grouped = group_chats_by_session(chat_data)

    for session_id, messages in grouped.items():
        with st.expander(f"Session ID: {session_id} ({len(messages)} messages)"):
            for msg in messages:
                msg_type = msg.get("type", "unknown").capitalize()
                content = msg.get("content", "")
                st.markdown(f"**{msg_type}**: {content}")

# ------------------- App Entry ------------------------

def main():
    st.set_page_config(page_title="AI Chat", layout="centered")
    st.title("🤖 AI Chat Interface")
    init_session_state()

    if st.session_state.auth is None:
        auth_ui()
    else:
        user_email = st.session_state.auth.user.email
        st.sidebar.success(f"Logged in as {user_email}")
        st.sidebar.info(f"Session ID: {st.session_state.session_id}")

        if st.sidebar.button("Logout"):
            handle_logout()

        # Agent mode
        if user_email == AGENT_EMAIL:
            agent_dashboard()
            return

        # User chat mode
        display_chat()
        if prompt := st.chat_input("What is your message?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            payload = {
                "chatInput": prompt,
                "sessionId": st.session_state.session_id
            }

            access_token = st.session_state.auth.session.access_token
            headers = {"Authorization": f"Bearer {access_token}"}

            with st.spinner("AI is thinking..."):
                response = requests.post(WEBHOOK_URL, json=payload, headers=headers)

            if response.status_code == 200:
                ai_message = response.json().get("output", "Sorry, I couldn't generate a response.")
                st.session_state.messages.append({"role": "assistant", "content": ai_message})
                with st.chat_message("assistant"):
                    st.markdown(ai_message)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()
