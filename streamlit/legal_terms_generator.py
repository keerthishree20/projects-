import streamlit as st
import google.generativeai as genai

# ---- CONFIG ----
st.set_page_config(
    page_title="📜 Legal Terms Generator",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Legal Terms, Policies & Disclaimers Generator")

st.markdown("""
Enter a short description of your **product or service**, and Gemini will generate:
✅ Legal Terms & Conditions  
✅ Cancellation Policy  
✅ Disclaimers  
in **user-friendly language**.
""")

# ---- API KEY ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"
genai.configure(api_key=API_KEY)

# ---- INPUT ----
product_desc = st.text_area(
    "📝 Describe your product or service:",
    placeholder="e.g., An online subscription-based fitness coaching app offering personalized workout plans and nutrition advice."
)

if st.button("Generate Legal Content") and product_desc.strip():
    with st.spinner("🤔 Drafting legal terms and policies…"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            # Gemini prompt
            prompt = f"""
You are an expert legal writing assistant AI.

The user describes their product/service as:
---
{product_desc}
---

Your task is to generate clear, user-friendly legal content:
✅ Terms & Conditions: include acceptable use, payment, intellectual property, etc.  
✅ Cancellation Policy: clear rules about cancellations, refunds, and timelines.  
✅ Disclaimers: limitations of liability, no guarantee of results, etc.

Write in plain English and easy to understand, but still legally sound.

Output format in Markdown:

### 📜 Terms & Conditions
…

### 🔄 Cancellation Policy
…

### ⚠️ Disclaimers
…
"""

            response = model.generate_content(prompt)
            output = response.text

            st.markdown(output)

        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("⬆️ Describe your product/service above and click **Generate Legal Content**.")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
