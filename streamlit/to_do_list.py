import streamlit as st
import google.generativeai as genai

# 📋 Page config
st.set_page_config(page_title="Task Planner Dashboard", page_icon="🗂️", layout="wide")
st.title("🗂️ AI-Powered Task Planner Dashboard")

# 🔑 Gemini API Key
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"
genai.configure(api_key=API_KEY)

# 📝 User input
with st.form("task_form"):
    tasks = st.text_area(
        "📋 Enter your task list (one task per line):",
        placeholder="e.g.\nDesign landing page\nWrite blog post\nPrepare presentation",
        height=200
    )
    submitted = st.form_submit_button("Generate Plan")

if submitted:
    if not tasks.strip():
        st.error("🚨 Please enter at least one task.")
        st.stop()

    with st.spinner("🤔 Thinking…"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            prompt = f"""
You are an expert project manager AI.  

The user provides a task list:
---
{tasks}
---

For each task:
✅ Suggest clear subtasks.
✅ Estimate realistic time required for each subtask (in hours).
✅ Identify any dependencies (e.g., Task A depends on Task B).
✅ Highlight possible productivity blockers.

Output format (Markdown):

### Task: <Task Name>

#### Subtasks
- Subtask 1 (Estimated: X hours)
- Subtask 2 (Estimated: Y hours)

#### Dependencies
- <dependency or "None">

#### Possible Blockers
- <blocker or "None">
"""

            response = model.generate_content(prompt)
            output = response.text

            st.success("✅ Plan generated!")
            st.markdown(output)

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
