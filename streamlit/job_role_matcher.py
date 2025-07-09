import streamlit as st
import google.generativeai as genai

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Career Recommender", page_icon="💼")
st.title("💼 Career Recommender with Gemini")

# ---- API KEY ----
# Your API Key is hardcoded here
api_key = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"

# Configure Gemini
genai.configure(api_key=api_key)

# ---- USER INPUT FORM ----
with st.form("career_form"):
    skills = st.text_area("🧰 Your Skills", placeholder="e.g., Python, data analysis, project management")
    experience = st.text_area("🗓️ Your Experience", placeholder="e.g., 3 years in software development")
    interests = st.text_area("✨ Your Interests", placeholder="e.g., AI, sustainability, startups")
    submitted = st.form_submit_button("Suggest Careers")

# ---- PROCESS & OUTPUT ----
if submitted:
    if not (skills and experience and interests):
        st.error("🚨 Please fill in all the fields before submitting.")
        st.stop()

    with st.spinner("🤔 Thinking..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            prompt = f"""
You are a career advisor AI.
The user has the following profile:

Skills: {skills}
Experience: {experience}
Interests: {interests}

Your task:
- Recommend the **top 5 job roles** and the **industries** they fit in.
- For each job role, include:
  - Industry name
  - Why it matches the user’s profile (justification)
  - What skills/upskilling are required to be competitive

Format the response in Markdown like this:

### 1. Job Role — *Industry*
- **Justification:** …
- **Required Upskilling:** …

Do not add any extra text.
"""

            response = model.generate_content(prompt)
            answer = response.text

            st.success("✅ Recommendations ready!")
            st.markdown(answer)

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash ✨")
st.sidebar.caption("Built with ❤️ using Streamlit")
