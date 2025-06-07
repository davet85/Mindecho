import streamlit as st
import os
from modules import onboarding, avatar_engine, task_engine, reflection_loop, premium_logic

# === API Key Fetch: Secrets First, then .env fallback ===
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY is missing. Set it in Streamlit secrets or a .env file.")
    st.stop()

# === Streamlit Config ===
st.set_page_config(page_title="MindEcho", layout="centered")
st.title("🧠 Welcome to MindEcho")

# === Session State Defaults ===
st.session_state.setdefault("onboarding_complete", False)
st.session_state.setdefault("user_profile", {})
st.session_state.setdefault("level", 1)
st.session_state.setdefault("page", "home")

# === Sidebar Navigation ===
st.sidebar.title("🧭 Navigation")
if st.sidebar.button("🏁 Restart"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if st.session_state["onboarding_complete"]:
    if st.sidebar.button("🧩 Tasks"):
        st.session_state.page = "tasks"
    if st.sidebar.button("📈 Daily Reflection"):
        st.session_state.page = "daily"
    if st.sidebar.button("📊 Weekly Summary"):
        st.session_state.page = "weekly"
    if st.sidebar.button("💎 Premium Console"):
        st.session_state.page = "premium"

# === App Routing Logic ===
try:
    if not st.session_state["onboarding_complete"]:
        onboarding.run()

    elif "avatar" not in st.session_state["user_profile"]:
        avatar_engine.run(st.session_state["user_profile"])

    elif st.session_state.page == "tasks":
        task_engine.run(st.session_state["user_profile"])

    elif st.session_state.page == "daily":
        reflection_loop.run_daily()

    elif st.session_state.page == "weekly":
        reflection_loop.run_weekly()

    elif st.session_state.page == "premium":
        premium_logic.run()

    else:
        st.info("✅ Use the sidebar to begin your journey.")
except Exception as e:
    st.error(f"🔥 An unexpected error occurred: {e}")
