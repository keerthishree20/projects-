import streamlit as st
import google.generativeai as genai

# ---- PAGE CONFIG ----
st.set_page_config(page_title="📘 Learning Plan Generator", page_icon="🎯")
st.title("🎯 AI-Powered Learning Plan Generator")

# ---- API KEY ----
# Gemini v2.0 works with gemini-1.5-flash-latest
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"

genai.configure(api_key=API_KEY)

# ---- TOPICS ----
topics = [
    "Data Science",
    "UI/UX Design",
    "Machine Learning",
    "Web Development",
    "Cybersecurity",
    "Cloud Computing",
    "Artificial Intelligence",
    "Mobile App Development",
    "DevOps",
    "Blockchain"
]

# ---- FORM ----
with st.form("learning_plan_form"):
    topic = st.selectbox("📂 Choose a Topic", options=topics)
    level = st.selectbox("🎓 Current Skill Level", options=["Beginner", "Intermediate", "Advanced"])
    time_commitment = st.text_input("⏳ Weekly Time Commitment (hours)", value="10")
    submitted = st.form_submit_button("Generate Learning Plan")

if submitted:
    if not topic or not level or not time_commitment:
        st.error("🚨 Please fill all the fields.")
        st.stop()

    with st.spinner("🧠 Thinking..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            prompt = f"""
You are an expert career and education advisor AI.
Your task: Create a **step-by-step learning plan** for the user to master the topic: **{topic}**.

Details:
- User skill level: {level}
- Weekly time commitment: {time_commitment} hours

Output must include:
✅ Step-by-step learning roadmap
✅ Recommended free & paid resources for each step
✅ 2-3 project ideas relevant to the topic
✅ Key checkpoints/milestones with estimated timelines (in weeks)

Format your response in Markdown clearly, using headings and bullet points.
"""

            response = model.generate_content(prompt)
            output = response.text

            st.success("✅ Learning plan ready!")
            st.markdown(output)

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
