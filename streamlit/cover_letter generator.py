import streamlit as st
import requests
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
GEMINI_API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"

# Gemini endpoint & model
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

st.set_page_config(page_title="Cover Letter Generator", layout="centered")
st.title("📝 Tailored Cover Letter Generator")

# User inputs
job_role = st.text_input("Job Role you’re applying for")
resume = st.file_uploader("Upload your Resume (PDF or TXT)", type=['pdf', 'txt'])

if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""

def extract_text_from_resume(uploaded_file):
    """
    Extracts text from PDF or TXT file.
    """
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    else:
        return ""

def generate_cover_letter(job_role, resume_text):
    """
    Calls Gemini 2.0 Flash model to generate the cover letter.
    """
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    prompt = f"""You are a professional career assistant.
Write a tailored, polite, and concise cover letter for the following job role based on the resume text.

Job Role: {job_role}

Resume:
{resume_text}

Only output the cover letter text, no extra explanation."""

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_URL, headers=headers, params=params, json=data, timeout=30)

    if response.status_code == 200:
        gemini_response = response.json()
        try:
            text = gemini_response['candidates'][0]['content']['parts'][0]['text']
            return text
        except (KeyError, IndexError):
            return "Error: Unexpected response from Gemini API."
    else:
        return f"Error: Gemini API returned status code {response.status_code}"

if st.button("✨ Generate Cover Letter"):
    if job_role and resume:
        resume_text = extract_text_from_resume(resume)

        if not resume_text.strip():
            st.error("Couldn’t extract text from your resume. Please check the file.")
        else:
            with st.spinner("Generating your tailored cover letter..."):
                cover_letter = generate_cover_letter(job_role, resume_text)

            st.session_state.cover_letter = cover_letter
            st.success("✅ Cover letter generated!")
    else:
        st.warning("⚠️ Please provide both job role and resume.")

if st.session_state.cover_letter:
    st.subheader("📄 Your Tailored Cover Letter:")
    st.text_area("Cover Letter", value=st.session_state.cover_letter, height=400)
