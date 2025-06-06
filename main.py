import streamlit as st
import os
from modules import onboarding, avatar_engine, task_engine, reflection_loop, premium_logic

# === API Key Fetch (Hybrid Safe) ===
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ Missing OpenAI API Key. Set it in secrets.toml or .env.")
    st.stop()

# === SESSION STATE ===
st.session_state.setdefault("onboarding_complete", False)
st.session_state.setdefault("user_profile", {})
st.session_state.setdefault("level", 1)
st.session_state.setdefault("page", "home")

# === SIDEBAR ===
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

# === ROUTING ===
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
        st.info("✅ Use the sidebar to begin.")
except Exception as e:
    st.error(f"🔥 An error occurred: {e}")
