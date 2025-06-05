import streamlit as st
import json
from datetime import datetime
from pathlib import Path

PROFILE_PATH = Path("database/user_profile.json")

def run():
    st.header("💎 MindEcho Premium Console")

    profile = st.session_state.get("user_profile", {})
    premium = profile.get("premium", {
        "insight_boost": False,
        "dashboard": False,
        "avatars": [],
        "streak_saver_used": 0,
        "rebirths": 0
    })

    # === Premium Overview ===
    st.markdown("### 🧩 Unlocked Features")
    for key, value in premium.items():
        st.write(f"- **{key}**: {value}")

    st.divider()
    st.subheader("⚙️ Simulate Premium Feature Use")

    if st.button("🧠 Unlock Insight Boost"):
        premium["insight_boost"] = True
        st.success("✅ Insight Boost unlocked!")

    if st.button("🎭 Unlock Avatar: Daemon"):
        if "Daemon" not in premium["avatars"]:
            premium["avatars"].append("Daemon")
            st.success("✅ Daemon avatar added!")

    if st.button("🔄 Use Streak Saver"):
        premium["streak_saver_used"] += 1
        st.success("🌀 Streak Saver used. One missed day forgiven.")

    if st.button("♻️ Rebirth Now"):
        premium["rebirths"] += 1
        st.session_state["level"] = 1
        st.session_state["last_level_up_date"] = datetime.now().strftime("%Y-%m-%d")
        st.session_state["tasks"] = []
        st.session_state["tasks_completed"] = []
        profile["reflections"] = []
        st.success("♻️ Rebirth cycle started.")

    # Update profile and persist
    profile["premium"] = premium
    st.session_state["user_profile"] = profile
    save_profile(profile)

def save_profile(profile):
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PROFILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
