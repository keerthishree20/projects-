import streamlit as st
import google.generativeai as genai

# ---- APP CONFIG ----
st.set_page_config(
    page_title="💼 Freelancer Proposal & Documents Generator",
    page_icon="🧾",
    layout="wide"
)

st.title("💼 AI Freelancer Proposal, Invoice & Agreement Generator")

st.markdown("""
✅ Select your **service** and enter client details.  
Gemini will generate:  
- 📄 Customized proposal  
- 🧾 Invoice draft  
- 📜 Service agreement  
""")

# ---- CONFIGURE GEMINI ----
API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"  # replace with your key
genai.configure(api_key=API_KEY)

# ---- FORM ----
with st.form("freelancer_form"):
    service = st.selectbox(
        "🛠️ Service You Offer",
        [
            "Web Design",
            "Mobile App Development",
            "Graphic Design",
            "Content Writing",
            "SEO Optimization",
            "Social Media Management",
            "Custom (enter below)"
        ]
    )

    if service == "Custom (enter below)":
        service = st.text_input("✍️ Enter Custom Service", placeholder="e.g., Video Editing")

    client_name = st.text_input("👤 Client Name", placeholder="e.g., John Doe")
    client_company = st.text_input("🏢 Client Company", placeholder="e.g., Acme Corp.")
    project_scope = st.text_area("📋 Project Scope / Notes", placeholder="Describe what the client wants…")

    submitted = st.form_submit_button("Generate Documents")

if submitted:
    if not service or not client_name or not client_company or not project_scope:
        st.error("⚠️ Please fill in all fields.")
    else:
        with st.spinner("📝 Creating your documents…"):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")

                prompt = f"""
You are an expert freelancer assistant AI.

The freelancer offers the service: {service}
Client's Name: {client_name}
Client's Company: {client_company}
Project Scope / Notes: {project_scope}

✅ Generate the following three documents in clear sections:

📄 Proposal:
- Title
- Introduction
- Objectives
- Deliverables
- Timeline
- Price Estimate

🧾 Invoice:
- Freelancer Info (use placeholder)
- Client Info
- Service Description
- Amount
- Payment Terms

📜 Service Agreement:
- Scope of Work
- Payment Terms
- Timeline & Deadlines
- Confidentiality
- Termination Clause

Write in clear, professional language and format.
"""

                response = model.generate_content(prompt)
                documents = response.text

                st.markdown("## 📄 Generated Documents")
                st.markdown(documents)

            except Exception as e:
                st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash")
st.sidebar.caption("Built with ❤️ using Streamlit")
