import streamlit as st
import os
from dotenv import load_dotenv
from modules import onboarding, avatar_engine, task_engine, reflection_loop, premium_logic
from modules import utils

# === INIT ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OpenAI API key missing. Please set it in .env")
    st.stop()

# === SESSION STATE SETUP ===
st.session_state.setdefault("onboarding_complete", False)
st.session_state.setdefault("user_profile", {})
st.session_state.setdefault("level", 1)
st.session_state.setdefault("last_level_up_date", None)

# === PAGE LAYOUT ===
st.set_page_config(page_title="MindEcho", layout="centered")
st.title("🧠 Welcome to MindEcho")

# === BLOCK 1: ONBOARDING ===
if not st.session_state["onboarding_complete"]:
    onboarding.run_onboarding()

# === BLOCK 2: AVATAR ASSIGNMENT ===
elif "avatar" not in st.session_state["user_profile"]:
    st.success("✅ Onboarding complete.")
    avatar_engine.run_avatar_assignment(st.session_state["user_profile"])

# === BLOCK 3: TASK ENGINE ===
elif st.button("🧩 Task Engine"):
    task_engine.run_task_engine(st.session_state["user_profile"])

# === BLOCK 4: RCA REFLECTION + SUMMARY ===
elif st.button("📈 Daily Reflection"):
    reflection_loop.run_daily_reflection()

elif st.button("📊 Weekly Summary"):
    reflection_loop.run_weekly_summary()

# === BLOCK 5: PREMIUM SUITE ===
elif st.button("💎 Premium Console"):
    premium_logic.run_premium_dashboard()
