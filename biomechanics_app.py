# app.py
import streamlit as st
import pyttsx3
import random

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="👟 FootFit Analyzer", layout="wide", page_icon="👟")

# ---------------------------
# GLOBAL STYLE
# ---------------------------
st.markdown("""
    <style>
    body {
        background-color: white !important;
    }
    .step-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .step-title {
        color: black;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    .stRadio > div {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .stRadio > div > label {
        background-color: #f8f8f8;
        color: black;
        font-weight: 700;
        padding: 10px 16px;
        border-radius: 10px;
        border: 2px solid #000;
        cursor: pointer;
        transition: 0.2s;
    }
    .stRadio > div > label:hover {
        background-color: #d3d3d3;
    }
    .stRadio > div > label[data-checked="true"] {
        background-color: #000;
        color: white !important;
    }
    .result-box {
        padding: 20px;
        border-radius: 16px;
        color: white;
        font-weight: 700;
    }
    .bold-text {
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def biomechanical_analysis(age_group, gender, weight, activity, foot_type, footwear_pref):
    # Simplified rule-based biomechanical logic
    cushioning = ""
    arch_support = ""
    recommended_shoe = ""
    material = ""
    justification = ""
    tip = ""

    if activity == "Running":
        recommended_shoe = "Cushioned Running Shoes"
        material = "Breathable Mesh with EVA Midsole"
        justification = "Running requires shock absorption and flexibility for high-impact motion."
        tip = "Replace your running shoes every 600–800 km to prevent injury."
    elif activity == "Walking":
        recommended_shoe = "Comfort Walking Shoes"
        material = "Soft Leather with Rubber Outsole"
        justification = "Walking needs comfort, midsole cushioning, and natural motion flexibility."
        tip = "Choose shoes that bend easily at the ball of your foot."
    elif activity == "Training / Gym":
        recommended_shoe = "Cross Training Shoes"
        material = "Synthetic Upper with Wide Base"
        justification = "Training shoes provide stability for multidirectional movement."
        tip = "Check the heel-to-toe drop for your comfort and stability."
    elif activity == "Casual":
        recommended_shoe = "Everyday Sneakers"
        material = "Canvas or Knit Upper"
        justification = "Casual wear needs style and moderate support for all-day comfort."
        tip = "Use insoles for better posture support during long hours."
    elif activity == "Hiking":
        recommended_shoe = "Trail Hiking Boots"
        material = "Waterproof Leather with Traction Sole"
        justification = "Hiking requires ankle support, traction, and waterproofing."
        tip = "Ensure good grip soles for steep or slippery surfaces."

    # Adjust background color by activity
    colors = {
        "Running": "#008080",
        "Walking": "#004080",
        "Training / Gym": "#6A0DAD",
        "Casual": "#2E8B57",
        "Hiking": "#A0522D"
    }
    bg_color = colors.get(activity, "#333333")

    return recommended_shoe, material, justification, tip, bg_color

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# ---------------------------
# STEP 1: PERSONAL INFORMATION
# ---------------------------
st.markdown('<div class="step-box">', unsafe_allow_html=True)
st.markdown('<div class="step-title">Step 1️⃣: Personal Information</div>', unsafe_allow_html=True)

age_group = st.radio("Select Age Group:", 
    ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"],
    horizontal=True)

gender = st.radio("Select Gender:", ["Male", "Female"], horizontal=True)
weight = st.radio("Select Weight Range:", ["Under 50 kg", "50–70 kg", "71–90 kg", "Above 90 kg"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# STEP 2: FOOT & PREFERENCE DETAILS
# ---------------------------
st.markdown('<div class="step-box">', unsafe_allow_html=True)
st.markdown('<div class="step-title">Step 2️⃣: Foot & Preference Details</div>', unsafe_allow_html=True)

activity = st.radio("Select Activity Level:", ["Running", "Walking", "Training / Gym", "Casual", "Hiking"], horizontal=True)
foot_type = st.radio("Select Foot Type:", ["Flat Foot", "Normal Arch", "High Arch"], horizontal=True)
footwear_pref = st.radio("Preferred Type of Footwear:", ["Sport", "Casual", "Formal"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# STEP 3: RECOMMENDATION ENGINE
# ---------------------------
recommended_shoe, material, justification, tip, bg_color = biomechanical_analysis(age_group, gender, weight, activity, foot_type, footwear_pref)

st.markdown(f"""
    <div class="result-box" style="background-color:{bg_color};">
        <h3 class="bold-text">Step 3️⃣: Personalized Recommendation</h3>
        <p class="bold-text">👟 <b>Recommended Footwear:</b> {recommended_shoe}</p>
        <p class="bold-text">🧵 <b>Material Suggestion:</b> {material}</p>
        <p class="bold-text">📊 <b>Biomechanical Justification:</b> {justification}</p>
        <p class="bold-text">💡 <b>Tip of the Day:</b> {tip}</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# VOICE ASSISTANT
# ---------------------------
if st.button("🔊 Read Out Recommendation"):
    voice_text = f"Your recommended footwear is {recommended_shoe}. The suggested material is {material}. {justification}. Tip of the day: {tip}."
    speak_text(voice_text)
    st.success("Voice assistant activated successfully!")

st.markdown("<br><center>👟 <b>Powered by FootFit Analyzer – Biomechanics meets AI</b></center>", unsafe_allow_html=True)







