import streamlit as st
import google.generativeai as genai

# ---- PAGE CONFIG ----
st.set_page_config(page_title="🌐 Personal Website Generator", page_icon="🖥️", layout="wide")
st.title("🖥️ AI-Powered Personal Website Generator")

# ---- API KEY ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"
genai.configure(api_key=API_KEY)

# ---- USER INPUT ----
with st.form("website_form"):
    st.subheader("✨ Your Details")

    achievements = st.text_area(
        "🏆 Achievements",
        placeholder="List your key achievements here…",
        height=150
    )

    skills = st.text_area(
        "🧰 Skills",
        placeholder="List your skills here…",
        height=100
    )

    projects = st.text_area(
        "💼 Projects",
        placeholder="Briefly describe your notable projects here…",
        height=150
    )

    submitted = st.form_submit_button("Generate Website Content")

if submitted:
    if not (achievements.strip() and skills.strip() and projects.strip()):
        st.error("🚨 Please fill in all the fields.")
        st.stop()

    with st.spinner("🤔 Generating your personal website content…"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            # 📄 Safe prompt without syntax errors
            prompt = f"""
You are an expert web content writer and designer AI.

The user has provided the following:
---
Achievements:
{achievements}

Skills:
{skills}

Projects:
{projects}
---

Your tasks:
✅ Write an engaging About Me section, highlighting achievements and skills.  
✅ Write a Projects section with short descriptions of each project.  
✅ Suggest 3-5 blog post ideas relevant to the user's background.  
✅ Create a simple, clean HTML5 template for the personal website, with placeholders for About, Projects, and Blog sections.

Output format in Markdown:

### About Me
(about me text here)

### Projects
(projects text here)

### Blog Ideas
- Idea 1
- Idea 2
- Idea 3

### HTML Template
<html>
  <head>
    <title>My Personal Website</title>
  </head>
  <body>
    <section id="about">
      <h1>About Me</h1>
      <p>...</p>
    </section>
    <section id="projects">
      <h1>Projects</h1>
      <p>...</p>
    </section>
    <section id="blog">
      <h1>Blog</h1>
      <p>...</p>
    </section>
  </body>
</html>
"""

            response = model.generate_content(prompt)
            output = response.text

            st.success("✅ Content generated!")
            st.markdown(output)

        except Exception as e:
            st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
