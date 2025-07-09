import streamlit as st
import google.generativeai as genai

# ---- PAGE CONFIG ----
st.set_page_config(page_title="📧 Email Thread Assistant", page_icon="✉️")
st.title("✉️ Email Thread Summarizer & Responder")

# ---- API KEY ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"

genai.configure(api_key=API_KEY)

# ---- FORM ----
with st.form("email_form"):
    email_thread = st.text_area(
        "📩 Paste your Email Thread",
        height=300,
        placeholder="Paste the entire email conversation here…"
    )
    tone = st.selectbox(
        "🎭 Desired Response Tone",
        options=["Professional", "Casual", "Assertive"]
    )
    submitted = st.form_submit_button("Generate Summary & Response")

if submitted:
    if not email_thread.strip():
        st.error("🚨 Please paste an email thread before submitting.")
        st.stop()

    with st.spinner("🤔 Thinking…"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            prompt = f"""
You are an expert email assistant AI.  

The following is a long email thread:  
---
{email_thread}
---

Your tasks:
1️⃣ Summarize the main points of the conversation in a few sentences.  
2️⃣ List clear, actionable items discussed or required.  
3️⃣ Draft a reply to the thread in a **{tone} tone**, addressing all necessary points, ready to copy and send.

Output format (Markdown):
### Summary
…

### Action Items
- Item 1
- Item 2

### Suggested Reply
…
"""

            response = model.generate_content(prompt)
            result = response.text

            st.success("✅ Done!")
            st.markdown(result)

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
