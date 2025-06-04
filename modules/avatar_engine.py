import streamlit as st

AVATARS = {
    "emotional": {
        "id": "Observer",
        "descriptor": "The Observer helps you track internal shifts and master emotional self-awareness."
    },
    "physical": {
        "id": "Guardian",
        "descriptor": "The Guardian protects your energy and reinforces physical vitality through routine and care."
    },
    "intellectual": {
        "id": "Philosopher",
        "descriptor": "The Philosopher guides your mind through deep reflection and the pursuit of clarity."
    },
    "social": {
        "id": "Healer",
        "descriptor": "The Healer supports you in reconnecting and repairing the threads of human connection."
    },
    "spiritual": {
        "id": "Oracle",
        "descriptor": "The Oracle speaks from beyond the veil, guiding your inner alignment and spiritual clarity."
    },
    "occupational": {
        "id": "Strategist",
        "descriptor": "The Strategist helps you navigate your path, purpose, and professional momentum."
    },
    "financial": {
        "id": "Ledger",
        "descriptor": "The Ledger brings order and insight to your material life, ensuring financial clarity."
    },
    "environmental": {
        "id": "Architect",
        "descriptor": "The Architect designs external environments to reflect and support your internal state."
    }
}

def run_avatar_assignment(user_profile):
    st.header("🧙 Avatar Assignment & Customization")

    # === Auto Assignment ===
    weakest_domain = min(user_profile["domains"], key=user_profile["domains"].get)
    avatar = AVATARS.get(weakest_domain, AVATARS["emotional"])
    
    st.markdown(f"**Assigned Avatar:** {avatar['id']}")
    st.markdown(f"*{avatar['descriptor']}*")

    # === Customization ===
    st.subheader("🎨 Customize Your Avatar")
    tone = st.selectbox("How should your guide speak to you?", ["Tactical", "Compassionate", "Neutral"])
    voice = st.selectbox("Choose a voice style:", ["Male", "Female", "Androgynous"])
    style = st.selectbox("Choose an appearance style:", ["Warrior", "Monk", "Sage", "Architect"])

    if st.button("Save Avatar"):
        st.session_state["user_profile"]["avatar"] = {
            "id": avatar["id"],
            "domain": weakest_domain,
            "descriptor": avatar["descriptor"],
            "tone": tone,
            "voice": voice,
            "style": style
        }
        st.success("✅ Avatar saved.")
