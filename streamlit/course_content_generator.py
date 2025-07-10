import streamlit as st
import google.generativeai as genai

# ---- APP CONFIG ----
st.set_page_config(
    page_title="📚 Lesson Plan Generator",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI-Powered Lesson Plan Generator")

st.markdown("""
✅ Enter your teaching details below:  
- Subject  
- Grade Level  
- Topic  

Gemini will create:  
📖 Lesson plan | 🧩 Activities | ❓ Quiz questions & answers
""")

# ---- CONFIGURE GEMINI ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"  # replace with your key
genai.configure(api_key=API_KEY)

# ---- FORM ----
with st.form("lesson_form"):
    subject = st.text_input("📘 Subject", placeholder="e.g., Math, Science, History")
    grade = st.text_input("🎓 Grade Level", placeholder="e.g., 5th Grade, High School")
    topic = st.text_input("📚 Topic", placeholder="e.g., Fractions, Photosynthesis")
    submitted = st.form_submit_button("Generate Lesson Plan")

if submitted:
    if not subject or not grade or not topic:
        st.error("⚠️ Please fill in all fields.")
    else:
        with st.spinner("✨ Generating lesson plan…"):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")

                prompt = f"""
You are an expert teacher AI.

The educator wants to teach:
- Subject: {subject}
- Grade Level: {grade}
- Topic: {topic}

✅ Provide a clear and age-appropriate lesson plan that includes:
1. Learning Objectives
2. Step-by-step Lesson Structure
3. 2–3 Interactive Classroom Activities
4. 5 Quiz Questions WITH correct answers

Write clearly and formatted for easy reading.
"""

                response = model.generate_content(prompt)
                result = response.text

                st.markdown("## 📖 Lesson Plan Output")
                st.markdown(result)

            except Exception as e:
                st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash")
st.sidebar.caption("Built with ❤️ using Streamlit")
