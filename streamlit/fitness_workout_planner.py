import streamlit as st
import google.generativeai as genai

# ---- CONFIG ----
st.set_page_config(
    page_title="🏋️ Weekly Workout Planner",
    page_icon="💪",
    layout="wide"
)

st.title("💪 AI Weekly Workout Planner")

st.markdown("""
Plan your weekly fitness routine with AI!  
✅ Enter your fitness details below, and Gemini will create:
- Weekly workout schedule
- Video links for exercises
- Daily log template
""")

# ---- API KEY ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"
genai.configure(api_key=API_KEY)

# ---- INPUT FORM ----
with st.form("fitness_form"):
    goals = st.text_area(
        "🎯 Your Fitness Goals:",
        placeholder="e.g., lose weight, build muscle, improve flexibility"
    )

    health_status = st.text_area(
        "❤️ Your Current Health Status:",
        placeholder="e.g., beginner, recovering from injury, intermediate level"
    )

    time_availability = st.text_input(
        "⏰ Time Availability (minutes per day):",
        placeholder="e.g., 30, 45, 60"
    )

    submitted = st.form_submit_button("Generate Workout Plan")

if submitted:
    if not goals.strip() or not health_status.strip() or not time_availability.strip():
        st.error("⚠️ Please fill in all fields.")
    else:
        with st.spinner("🏋️ Building your workout plan…"):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")

                prompt = f"""
You are an expert fitness coach AI.

The user provides the following information:
- Fitness goals: {goals}
- Current health status: {health_status}
- Time availability per day: {time_availability} minutes

✅ Build a weekly workout schedule tailored to the user.
✅ For each day, list:
  - Exercises
  - Estimated duration per exercise
  - 1-2 YouTube links or suggested keywords for exercise videos

✅ At the end, create a simple daily log template that the user can fill in.

Write clearly and make it beginner-friendly if needed.
"""

                response = model.generate_content(prompt)
                workout_plan = response.text

                st.markdown("## 📝 Your Weekly Workout Plan")
                st.markdown(workout_plan)

            except Exception as e:
                st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
