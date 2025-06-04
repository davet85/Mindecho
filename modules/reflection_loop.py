import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path

PROFILE_PATH = Path("database/user_profile.json")

def run_daily_reflection():
    st.header("📈 Daily Reflection – RCA Analysis")

    st.markdown("### Theme: *Weight*")
    reflection = st.text_area("What are you still carrying that no longer serves you?")

    if st.button("Submit Reflection"):
        rca_score, tone, domains = analyze_reflection(reflection)

        reflection_data = {
            "reflection_date": str(datetime.now().date()),
            "reflection_text": reflection,
            "rca_score": rca_score,
            "emotional_tone": tone,
            "active_domains": domains
        }

        # Save reflection to user profile
        user_profile = st.session_state["user_profile"]
        user_profile.setdefault("reflections", []).append(reflection_data)
        st.session_state["user_profile"] = user_profile
        save_profile(user_profile)

        st.success("✅ Reflection saved.")
        st.write(f"**RCA Score:** {rca_score}")
        st.write(f"**Emotional Tone:** {', '.join(tone)}")
        st.write(f"**Active Domains:** {', '.join(domains)}")


def analyze_reflection(text):
    """Placeholder for GPT analysis logic. Replace with actual GPT call."""
    length = len(text.split())

    if length < 30:
        score = 20
        tone = ["avoidant", "shallow", "distant"]
    elif length < 60:
        score = 45
        tone = ["honest", "fragmented", "tentative"]
    elif length < 120:
        score = 65
        tone = ["insightful", "reflective", "emotional"]
    else:
        score = 85
        tone = ["coherent", "symbolic", "integrated"]

    # Simulated domain tagging (to be GPT-driven)
    domains = ["emotional"]
    if "family" in text.lower():
        domains.append("social")
    if "faith" in text.lower() or "god" in text.lower():
        domains.append("spiritual")
    if "work" in text.lower() or "career" in text.lower():
        domains.append("occupational")

    return score, tone, list(set(domains))


def run_weekly_summary():
    st.header("🧾 Weekly Growth Summary")
    reflections = st.session_state["user_profile"].get("reflections", [])
    if len(reflections) < 3:
        st.info("You need at least 3 reflections to generate a summary.")
        return

    last_week = [r for r in reflections if datetime.strptime(r["reflection_date"], "%Y-%m-%d") >= datetime.now() - timedelta(days=7)]
    if not last_week:
        st.info("No reflections in the past 7 days.")
        return

    tones = [t for r in last_week for t in r["emotional_tone"]]
    scores = [r["rca_score"] for r in last_week]
    domains = [d for r in last_week for d in r["active_domains"]]

    most_common_tone = max(set(tones), key=tones.count)
    avg_score = sum(scores) / len(scores)
    dominant_domain = max(set(domains), key=domains.count)

    st.markdown(f"**Average RCA Score:** {round(avg_score)}")
    st.markdown(f"**Dominant Emotional Tone:** {most_common_tone}")
    st.markdown(f"**Primary Focus Domain:** {dominant_domain.title()}")
    st.markdown(f"**Suggested Focus:** Deepen {dominant_domain.title()} engagement this week.")
    st.markdown(f"**This Week’s Word:** *Resonance*")


def save_profile(profile):
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PROFILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
