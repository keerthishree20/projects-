import streamlit as st
import google.generativeai as genai
from datetime import datetime

st.set_page_config(
    page_title="🌏 Travel Itinerary Planner",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AI Travel Itinerary Planner")

st.markdown("""
Plan your trip with AI!  
✅ Enter your travel details below, and Gemini will create:
- Day-by-day itinerary
- Local attractions
- Estimated costs
- Travel tips
""")

API_KEY = "AIzaSyDPlV7ASZPWJPI26bHmzPRbosSfYzg9onA"
genai.configure(api_key=API_KEY)

with st.form("travel_form"):
    destination = st.text_input(
        "🗺️ Destination:",
        placeholder="e.g., Tokyo, Japan"
    )

    start_date = st.date_input(
        "📅 Start Date:",
        datetime.today()
    )

    end_date = st.date_input(
        "📅 End Date:"
    )

    preferences = st.text_area(
        "🎯 Preferences (optional):",
        placeholder="e.g., adventure, food, culture, relaxation, shopping"
    )

    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    if not destination or end_date < start_date:
        st.error("⚠️ Please enter a destination and ensure the dates are valid.")
    else:
        with st.spinner("🗺️ Building your itinerary…"):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")

                trip_days = (end_date - start_date).days + 1
                preferences_text = preferences if preferences.strip() else "general sightseeing and relaxation"

                prompt = f"""
You are an expert travel planner AI.

Plan a {trip_days}-day trip to **{destination}**, starting on {start_date.strftime('%Y-%m-%d')} and ending on {end_date.strftime('%Y-%m-%d')}.
The traveler prefers: {preferences_text}.

✅ For each day, list:
- Recommended attractions/activities
- Estimated costs per activity (in USD)
- A brief travel tip for the day

✅ At the end, add 3 general travel tips for the trip.

Format the output neatly with headings for each day.
"""

                response = model.generate_content(prompt)
                itinerary_text = response.text

                st.markdown("## 📝 Your Travel Itinerary")
                st.markdown(itinerary_text)

            except Exception as e:
                st.error(f"❌ Error: {e}")

st.sidebar.info("Powered by Gemini 1.5 Flash (API v2.0)")
st.sidebar.caption("Built with ❤️ using Streamlit")
