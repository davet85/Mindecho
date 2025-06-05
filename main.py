# === modules/onboarding.py ===
import streamlit as st

def run():
    st.subheader("🚀 Onboarding")
    name = st.text_input("What's your name?")
    age = st.number_input("Your age:", min_value=10, max_value=100)
    email = st.text_input("Email address")
    sentence = st.text_area("Who are you in one sentence?")

    if st.button("Complete Onboarding"):
        st.session_state.user_profile = {
            "name": name,
            "age": age,
            "email": email,
            "sentence": sentence
        }
        st.session_state.onboarding_complete = True
        st.success("🎉 Onboarding complete!")

# === modules/avatar_engine.py ===
import streamlit as st

def run(user_profile):
    st.subheader("🎭 Assigning Your Avatar")
    avatar = st.selectbox("Choose your symbolic guide:", [
        "Observer", "Guardian", "Philosopher", "Healer",
        "Oracle", "Strategist", "Ledger", "Architect"
    ])
    user_profile["avatar"] = avatar
    st.session_state.user_profile = user_profile
    st.success(f"✅ Avatar '{avatar}' assigned.")

# === modules/task_engine.py ===
import streamlit as st

def run(user_profile):
    st.subheader("📋 Task Engine")
    st.write("Assigned tasks will appear here.")
    st.write(f"Your avatar: {user_profile.get('avatar', 'N/A')}")

# === modules/reflection_loop.py ===
import streamlit as st

def run_daily():
    st.subheader("📝 Daily Reflection")
    reflection = st.text_area("What did you notice about yourself today?")
    if st.button("Submit Reflection"):
        st.success("📈 Reflection submitted.")

def run_weekly():
    st.subheader("📆 Weekly Summary")
    st.write("Your weekly summary will be generated here.")

# === modules/premium_logic.py ===
import streamlit as st

def run():
    st.subheader("💎 Premium Console")
    st.write("Premium tools coming soon.")
