import streamlit as st
import json
from pathlib import Path

PROFILE_PATH = Path("database/user_profile.json")
DIMENSIONS = [
    "Emotional", "Physical", "Intellectual", "Social",
    "Spiritual", "Occupational", "Financial", "Environmental"
]

def run():
    st.header("🧾 MindEcho Onboarding")

    # === Phase 1: Basic Info Form ===
    if "step" not in st.session_state:
        st.session_state["step"] = "info"

    if st.session_state["step"] == "info":
        with st.form("user_info_form"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=10, max_value=120)
            email = st.text_input("Email")
            sentence = st.text_input("Who are you in one sentence?")
            code = st.text_input("Enter verification code (dummy)")

            use_tools = st.text_input("Do you use any self-development tools now?")
            growth_time = st.text_input("How much time do you spend per week on your growth?")
            pay_support = st.selectbox("Would you pay for a guide or AI to support you?", ["Yes", "No", "Maybe"])

            submitted = st.form_submit_button("Continue to Wellness Assessment")

        if submitted:
            st.session_state["basic_info"] = {
                "name": name,
                "age": age,
                "email": email,
                "sentence": sentence,
                "marketing": {
                    "uses_tools": use_tools,
                    "growth_time": growth_time,
                    "would_pay": pay_support
                }
            }
            st.session_state["step"] = "assessment"

    # === Phase 2: Domain Assessment ===
    if st.session_state["step"] == "assessment":
        st.subheader("🧠 8-Domain Wellness Assessment")
        scores = {}
        for dim in DIMENSIONS:
            score = st.slider(f"{dim} Wellness", 1, 10, 5)
            scores[dim.lower()] = int(score * 10)

        if st.button("Next: Narrative Input"):
            st.session_state["domain_scores"] = scores
            st.session_state["step"] = "narrative"

    # === Phase 3: Freeform Narrative ===
    if st.session_state["step"] == "narrative":
        st.subheader("📝 Your Story")
        narrative = st.text_area("Describe your current struggles, where you are in life, and who you want to become.")

        if st.button("Analyze and Complete Onboarding"):
            profile = {
                **st.session_state["basic_info"],
                "domains": st.session_state["domain_scores"],
                "narrative": narrative
            }

            profile["composite_score"] = sum(profile["domains"].values())
            profile["functional_tier"] = assign_functional_tier(profile["composite_score"])
            profile["emotional_tone"] = "unclear, reflective, searching"  # Placeholder

            save_profile(profile)
            st.session_state["user_profile"] = profile
            st.session_state["onboarding_complete"] = True
            st.success("✅ Onboarding complete!")

def assign_functional_tier(score):
    if score < 300:
        return 1
    elif score < 500:
        return 2
    elif score < 650:
        return 3
    return 4

def save_profile(profile):
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PROFILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
