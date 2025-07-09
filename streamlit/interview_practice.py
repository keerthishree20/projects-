import streamlit as st
import google.generativeai as genai

# ---- CONFIG ----
st.set_page_config(page_title="💼 AI Interview Simulator", page_icon="🎤", layout="wide")
st.title("🎤 AI Interview Simulator")

st.markdown("""
Select a **job role** and practice your interview skills!
✅ Gemini will ask you 3–5 role-specific questions.  
✅ You type your answers.  
✅ Gemini will analyze your responses and suggest improvements.
""")

# ---- API KEY ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"
genai.configure(api_key=API_KEY)

# ---- JOB ROLE SELECTION ----
job_roles = [
    "Software Engineer",
    "Data Analyst",
    "Product Manager",
    "UI/UX Designer",
    "Marketing Specialist"
]

job_role = st.selectbox("💼 Select a Job Role:", options=job_roles)

if st.button("Start Interview Simulation"):
    with st.spinner("🤔 Generating interview questions…"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            prompt = f"""
You are a professional interviewer AI.

The candidate has applied for the role of **{job_role}**.
✅ Generate 3–5 realistic and challenging interview questions specific to this role.
✅ Output them in a numbered list format.
"""

            response = model.generate_content(prompt)
            questions_text = response.text

            st.session_state["questions"] = questions_text

        except Exception as e:
            st.error(f"❌ Error: {e}")

if "questions" in st.session_state:
    st.markdown("## 📋 Interview Questions")
    st.markdown(st.session_state["questions"])

    answers = []
    for i, q in enumerate(st.session_state["questions"].split("\n")):
        if q.strip().startswith("1") or q.strip().startswith("2") or q.strip().startswith("3"):
            ans = st.text_area(f"📝 Your Answer to: {q.strip()}", key=f"answer_{i}")
            answers.append({"question": q.strip(), "answer": ans})

    if st.button("Submit Answers for Feedback"):
        with st.spinner("💬 Analyzing your answers…"):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")

                answer_text = "\n".join(
                    f"Q: {a['question']}\nA: {a['answer']}" for a in answers
                )

                feedback_prompt = f"""
You are an expert career coach.

Here are the candidate's answers to a simulated **{job_role}** interview:

{answer_text}

✅ For each answer, provide constructive feedback on:
- Clarity
- Depth
- Technical correctness (if applicable)
- Confidence

✅ Suggest how to improve each response.

Output your feedback in a clear numbered list.
"""

                feedback_response = model.generate_content(feedback_prompt)
                feedback_text = feedback_response.text

                st.markdown("## 📝 Feedback & Suggestions")
                st.markdown(feedback_text)

            except Exception as e:
                st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
