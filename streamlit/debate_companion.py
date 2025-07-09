import streamlit as st
import google.generativeai as genai

# ---- CONFIG ----
st.set_page_config(page_title="🎤 Debate & Essay Helper", page_icon="🗣️", layout="wide")
st.title("🗣️ Debate & Essay Prep with Gemini")

st.markdown("""
Enter a topic below, and Gemini will help you prepare by providing:
✅ Pros  
✅ Cons  
✅ Arguments  
✅ Citations
""")

# ---- API KEY ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"
genai.configure(api_key=API_KEY)

# ---- INPUT ----
topic = st.text_input("💡 Enter your topic:", placeholder="e.g., AI should be regulated")

if st.button("Generate Debate Prep") and topic.strip():
    with st.spinner("🤔 Analyzing topic and preparing arguments…"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            # Prompt for Gemini
            prompt = f"""
You are an expert debate and essay preparation assistant AI.

The user wants to prepare for a debate or essay on the following topic:
---
**Topic:** {topic}
---

Your tasks:
✅ Provide at least 3 clear PROS for this topic, with short explanations.  
✅ Provide at least 3 clear CONS for this topic, with short explanations.  
✅ Write a few supporting arguments or points for each side, phrased in persuasive language.  
✅ Include at least 2-3 citations or references to credible sources (you can mention they are examples).  

Output format in Markdown:
### 🟢 Pros
- Point 1
- Point 2
- Point 3

### 🔴 Cons
- Point 1
- Point 2
- Point 3

### 🗣️ Supporting Arguments
- Argument for pro
- Argument for con

### 📚 Citations
- Source 1
- Source 2
- Source 3
"""

            response = model.generate_content(prompt)
            output = response.text

            st.markdown(output)

        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("⬆️ Enter a topic above and click **Generate Debate Prep**.")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
