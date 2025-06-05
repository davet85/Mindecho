import streamlit as st
import os
from dotenv import load_dotenv
from modules import onboarding, avatar_engine, task_engine, reflection_loop, premium_logic

# === INIT ===
st.write("🔧 Loading environment...")
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OpenAI API key missing. Please set it in .env or Streamlit Secrets.")
    st.stop()

st.write("✅ API Key loaded")

# === SESSION STATE SETUP ===
st.session_state.setdefault("onboarding_complete", False)
st.session_state.setdefault("user_profile", {})
st.session_state.setdefault("level", 1)
st.session_state.setdefault("last_level_up_date", None)
st.session_state.setdefault("page", "home")

st.set_page_config(page_title="MindEcho", layout="centered")
st.title("🧠 Welcome to MindEcho")

# === NAVIGATION DEBUG ===
st.sidebar.title("Navigation")
if st.button("Debug: Reset All"):
    st.session_state.clear()
    st.rerun()

if st.session_state["onboarding_complete"]:
    with st.sidebar:
        if st.button("🧩 Tasks"):
            st.session_state.page = "tasks"
        if st.button("📈 Daily"):
            st.session_state.page = "daily"
        if st.button("📊 Weekly"):
            st.session_state.page = "weekly"
        if st.button("💎 Premium"):
            st.session_state.page = "premium"

# === ONBOARDING FLOW ===
try:
    if not st.session_state["onboarding_complete"]:
        st.write("🔹 Running onboarding...")
        onboarding.run_onboarding()

    elif "avatar" not in st.session_state["user_profile"]:
        st.write("🔹 Running avatar assignment...")
        avatar_engine.run_avatar_assignment(st.session_state["user_profile"])

    elif st.session_state.page == "tasks":
        st.write("🔹 Running task engine...")
        task_engine.run_task_engine(st.session_state["user_profile"])

    elif st.session_state.page == "daily":
        st.write("🔹 Running daily reflection...")
        reflection_loop.run_daily_reflection()

    elif st.session_state.page == "weekly":
        st.write("🔹 Running weekly summary...")
        reflection_loop.run_weekly_summary()

    elif st.session_state.page == "premium":
        st.write("🔹 Running premium console...")
        premium_logic.run_premium_dashboard()

    else:
        st.info("✅ Use the sidebar to begin.")
except Exception as e:
    st.error(f"🔥 Uncaught exception: {e}")
