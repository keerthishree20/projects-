import streamlit as st
import google.generativeai as genai

# ---- APP CONFIG ----
st.set_page_config(
    page_title="🚀 AI Pitch Deck Generator",
    page_icon="📊",
    layout="wide"
)

st.title("🚀 AI Startup Pitch Deck Generator")

st.markdown("""
✅ Enter your startup idea, target market, and vision.  
Gemini will generate a **complete pitch deck outline**, including:  
- Problem & Solution  
- Market Size & Opportunity  
- Business/Revenue Model  
- Competitive Advantage  
- Team  
- Roadmap  
- Closing Slide  
""")

# ---- CONFIGURE GEMINI ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"  # replace with your key
genai.configure(api_key=API_KEY)

# ---- FORM ----
with st.form("pitch_form"):
    idea = st.text_area(
        "💡 Startup Idea",
        placeholder="e.g., AI-powered mental health chatbot for Gen Z"
    )

    market = st.text_area(
        "🌍 Target Market",
        placeholder="e.g., College students in the US"
    )

    vision = st.text_area(
        "🔭 Vision",
        placeholder="e.g., To make mental health support affordable, accessible, and stigma-free"
    )

    submitted = st.form_submit_button("Generate Pitch Deck")

if submitted:
    if not idea.strip() or not market.strip() or not vision.strip():
        st.error("⚠️ Please fill in all fields.")
    else:
        with st.spinner("📊 Building your pitch deck…"):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")

                prompt = f"""
You are a startup pitch expert AI.

The user provides:
- Startup Idea: {idea}
- Target Market: {market}
- Vision: {vision}

✅ Generate a clear and compelling **pitch deck outline** with slides:
1. Title Slide
2. Problem
3. Solution
4. Market Size & Opportunity
5. Revenue Model
6. Competitive Advantage
7. Go-to-Market Strategy
8. Team
9. Roadmap
10. Closing & Call-to-Action

✅ For each slide, give:
- Title
- Bullet points of key content

Make it concise and persuasive.
"""

                response = model.generate_content(prompt)
                deck = response.text

                st.markdown("## 📊 Your Pitch Deck Outline")
                st.markdown(deck)

            except Exception as e:
                st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash")
st.sidebar.caption("Built with ❤️ using Streamlit")
