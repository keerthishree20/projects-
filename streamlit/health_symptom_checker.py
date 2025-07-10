import streamlit as st
import google.generativeai as genai

# ---- APP CONFIG ----
st.set_page_config(
    page_title="🩺 Symptom Checker & Doctor Questions",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 AI Symptom Checker")

st.markdown("""
✅ Enter your **health symptoms** below.  
Gemini will:  
- Summarize **possible causes** (not a diagnosis!)  
- Suggest **questions to ask a doctor**  
""")

st.info("⚠️ Disclaimer: This is not medical advice. Always consult a licensed healthcare professional.")

# ---- CONFIGURE GEMINI ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"  # replace with your key
genai.configure(api_key=API_KEY)

# ---- FORM ----
with st.form("symptom_form"):
    symptoms = st.text_area(
        "📝 Describe your symptoms",
        placeholder="e.g., persistent headache, nausea, fatigue"
    )
    submitted = st.form_submit_button("Check Symptoms")

if submitted:
    if not symptoms.strip():
        st.error("⚠️ Please describe your symptoms.")
    else:
        with st.spinner("🔍 Analyzing symptoms…"):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")

                prompt = f"""
You are a helpful healthcare assistant AI (not a doctor).

The user describes these symptoms: {symptoms}

✅ Provide:
1. A short summary of possible causes or conditions related to these symptoms.
2. A clear disclaimer: this is not a diagnosis and the user must consult a doctor.
3. A list of 5 good questions the user can ask their doctor during the appointment.

Write clearly and professionally.
"""

                response = model.generate_content(prompt)
                result = response.text

                st.markdown("## 🩺 Symptom Analysis")
                st.markdown(result)

            except Exception as e:
                st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash")
st.sidebar.caption("Built with ❤️ using Streamlit")
