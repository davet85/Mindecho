import streamlit as st
from datetime import datetime, timedelta

# === Hardcoded Level Requirements ===
LEVELS = {
    1: {"min_days": 1, "tasks": 3, "reflection": True},
    2: {"min_days": 2, "tasks": 5, "rca_min": 35},
    3: {"min_days": 5},
    4: {"min_days": 7},
    5: {"min_days": 10},
    6: {"min_days": 14},
    7: {"min_days": 21},
    8: {"min_days": 30},
    9: {"min_days": 90},
    10: {"min_days": 0}  # Capstone logic
}

# === Task Examples (replace or expand later) ===
DEFAULT_TASKS = [
    {"title": "Clean 1 surface", "type": "action", "symbol": "This task will quiet the noise."},
    {"title": "Walk for 10 minutes", "type": "action", "symbol": "Reclaim momentum through motion."},
    {"title": "Name 3 fears", "type": "reflection", "symbol": "You disarm the unseen by naming it."},
    {"title": "Define a 1-month goal", "type": "planning", "symbol": "Clarity begins with aim."}
]

def run_task_engine(user_profile):
    st.header("🎮 Task Engine – Level Progression")
    
    level = st.session_state.get("level", 1)
    tier = user_profile.get("functional_tier", 2)
    avatar_domain = user_profile.get("avatar", {}).get("domain", "emotional")
    
    st.markdown(f"**Current Level:** {level}")
    st.markdown(f"**Avatar Domain:** {avatar_domain.title()}")
    
    today = datetime.now().date()
    last_level_up_str = st.session_state.get("last_level_up_date")
    last_level_up = datetime.strptime(last_level_up_str, "%Y-%m-%d").date() if last_level_up_str else today
    days_elapsed = (today - last_level_up).days

    required_days = LEVELS[level]["min_days"]
    if days_elapsed < required_days:
        st.warning(f"⏳ Minimum {required_days} days required between levels. ({days_elapsed} elapsed)")
        return

    if "tasks" not in st.session_state:
        st.session_state["tasks"] = DEFAULT_TASKS[:3]
        st.session_state["tasks_completed"] = []

    st.subheader("🧩 Your Tasks")
    for i, task in enumerate(st.session_state["tasks"]):
        completed = st.checkbox(f"{task['title']} — _{task['symbol']}_", key=f"task_{i}")
        if completed and task["title"] not in st.session_state["tasks_completed"]:
            st.session_state["tasks_completed"].append(task["title"])

    if len(st.session_state["tasks_completed"]) >= 3:
        st.subheader("📝 Final Reflection")
        reflection = st.text_area("Write your integration reflection here:")
        if st.button("Submit & Level Up"):
            process_level_up(reflection)

def process_level_up(reflection_text):
    st.session_state["level"] = st.session_state.get("level", 1) + 1
    st.session_state["last_level_up_date"] = datetime.now().strftime("%Y-%m-%d")
    st.session_state["tasks"] = []
    st.session_state["tasks_completed"] = []
    st.success("🎉 Level Up! You're making progress.")
    st.write("Your reflection was saved and your path continues.")
