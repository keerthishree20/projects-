import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import random

# ---- CONFIG ----
st.set_page_config(page_title="🌈 Mood Journal", page_icon="📝", layout="wide")
st.title("📝 Daily Mood Journal & Emotional Wellness")

# ---- API KEY ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"
genai.configure(api_key=API_KEY)

# ---- SESSION STATE ----
if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

# ---- MOOD INPUT ----
mood_options = ["😊 Happy", "😞 Sad", "😡 Angry", "😌 Calm", "😔 Anxious", "😃 Excited"]
today = datetime.today().strftime("%Y-%m-%d")

with st.form("mood_form"):
    st.subheader(f"🌤️ How are you feeling today? ({today})")
    mood = st.selectbox("Select your mood:", options=mood_options)
    notes = st.text_area("🖋️ Add any notes about your day (optional):", height=100)
    submitted = st.form_submit_button("Log Mood")

if submitted:
    st.session_state["mood_log"].append({"date": today, "mood": mood, "notes": notes})
    st.success("✅ Mood logged!")

# ---- MOOD TREND ----
if st.session_state["mood_log"]:
    st.subheader("📈 Mood Trend")
    df = pd.DataFrame(st.session_state["mood_log"])
    df["date"] = pd.to_datetime(df["date"])
    df["mood_score"] = df["mood"].map({
        "😊 Happy": 5, "😃 Excited": 4,
        "😌 Calm": 3,
        "😔 Anxious": 2,
        "😞 Sad": 1, "😡 Angry": 0
    })
    chart_data = df.set_index("date")[["mood_score"]]
    st.line_chart(chart_data)

# ---- REFLECTION & MOTIVATION ----
if st.session_state["mood_log"]:
    latest_mood = st.session_state["mood_log"][-1]["mood"]
    latest_notes = st.session_state["mood_log"][-1]["notes"]

    with st.spinner("💭 Crafting journaling prompt and motivational quote…"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            prompt = f"""
You are an expert emotional wellness coach AI.

The user reported feeling **{latest_mood}** today.

Optional notes: {latest_notes}

Your tasks:
✅ Suggest a reflective journaling prompt the user can write about today.  
✅ Provide one short motivational quote to help improve their emotional health.

Output format:
### Journaling Prompt
…

### Motivational Quote
…
"""

            response = model.generate_content(prompt)
            output = response.text

            st.subheader("🪞 Reflection & Motivation")
            st.markdown(output)

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
