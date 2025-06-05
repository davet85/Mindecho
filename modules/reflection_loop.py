import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path

PROFILE_PATH = Path("database/user_profile.json")

def run_daily():
    st.header("📈 Daily Reflection – RCA Scoring")

    st.markdown("### Theme: *Weight*")
    reflection = st.text_area("What are you still carrying that no longer serves you?")

    if st.button("📝 Submit Reflection"):
        rca_score, tone, domains = analyze_reflection(reflection)

        entry = {
            "reflection_date": str(datetime.now().date()),
            "reflection_text": reflection,
            "rca_score": rca_score,
            "emotional_tone": tone,
            "active_domains": domains
        }

        # Save to profile
        profile = st.session_state["user_profile"]
        profile.setdefault("reflections", []).append(entry)
        st.session_state["user_profile"] = profile
        save_profile(profile)

        st.success("✅ Reflection recorded.")
        st.markdown(f"**RCA Score:** {rca_score}")
        st.markdown(f"**Emotional Tone:** {', '.join(tone)}")
        st.markdown(f"**Domains Activated:** {', '.join(domains)}")

def run_weekly():
    st.header("🧾 Weekly Growth Summary")

    reflections = st.session_state["user_profile"].get("reflections", [])
    if len(reflections) < 3:
        st.info("You need at least 3 reflections to generate a summary.")
        return

    last_week = [
        r for r in reflections
        if datetime.strptime(r["reflection_date"], "%Y-%m-%d") >= datetime.now() - timedelta(days=7)
    ]
    if not last_week:
        st.info("No reflections in the past 7 days.")
        return

    tones = [t for r in last_week for t in r["emotional_tone"]]
    scores = [r["rca_score"] for r in last_week]
    domains = [d for r in last_week for d in r["active_domains"]]

    most_common_tone = max(set(tones), key=tones.count)
    avg_score = round(sum(scores) / len(scores))
    dominant_domain = max(set(domains), key=domains.count)

    st.markdown(f"**Average RCA Score:** {avg_score}")
    st.markdown(f"**Dominant Emotional Tone:** {most_common_tone}")
    st.markdown(f"**Primary Focus Domain:** {dominant_domain.title()}")
    st.markdown(f"**Suggested Focus:** Deepen {dominant_domain.title()} engagement this week.")
    st.markdown(f"**This Week’s Word:** *Resonance*")

def analyze_reflection(text):
    """Simulated RCA scoring logic – replace with GPT or other model in production."""
    word_count = len(text.split())

    if word_count < 30:
        score = 20
        tone = ["avoidant"]
