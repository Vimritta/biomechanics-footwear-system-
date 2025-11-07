# biomechanics_app.py
import streamlit as st
import random
import pyttsx3

# App configuration
st.set_page_config(page_title="FootFit Analyzer 👟", layout="wide", page_icon="👣")

# --------------------------
# Voice Assistant Setup
# --------------------------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# --------------------------
# Styling
# --------------------------
st.markdown("""
    <style>
        body {
            background-color: white;
        }
        .step-title {
            font-size: 28px;
            font-weight: 900;
            color: #000000;
            text-align: center;
            margin-top: 10px;
        }
        .question-label {
            font-weight: 700;
            color: #000000;
        }
        .recommender {
            font-size: 20px;
            font-weight: 800;
        }
        .highlight {
            color: #0044cc;
            font-weight: 900;
        }
        .tip {
            background-color: #e3f2fd;
            padding: 10px;
            border-radius: 12px;
            font-weight: 600;
            color: #003366;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Step 1: Personal Information
# --------------------------
st.markdown('<div class="step-title">Step 1️⃣: Personal Information</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    age = st.radio("👤 Select Age Range", ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"], key="age")
with col2:
    gender = st.radio("🚻 Gender", ["Male", "Female", "Other"], key="gender")
with col3:
    weight = st.radio("⚖️ Weight Range", ["Under 50 kg", "50–70 kg", "71–90 kg", "Over 90 kg"], key="weight")

# --------------------------
# Step 2: Foot & Activity
# --------------------------
st.markdown('<div class="step-title">Step 2️⃣: Foot & Activity</div>', unsafe_allow_html=True)
col4, col5 = st.columns(2)
with col4:
    foot_type = st.radio("🦶 Foot Type", ["Flat Arch", "Normal Arch", "High Arch"], key="foot_type")
with col5:
    activity = st.radio("🏃 Activity Level", ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (sports/fitness)"], key="activity")

preference = st.radio("👟 Footwear Preference", ["Running shoes", "Casuals", "Formal shoes", "Sandals"], key="preference")

# --------------------------
# Step 3: Biomechanical Analysis & Recommendations
# --------------------------
# Dynamic background based on activity
activity_colors = {
    "Low (mostly sitting)": "#fce4ec",
    "Moderate (walking/standing sometimes)": "#e8f5e9",
    "High (sports/fitness)": "#e3f2fd"
}
st.markdown(
    f"<div style='background-color:{activity_colors[activity]}; padding:15px; border-radius:15px;'>"
    f"<h3 style='text-align:center; font-weight:800;'>Step 3️⃣: Biomechanical Analysis & Recommendations</h3>",
    unsafe_allow_html=True
)

# Shoe recommendation logic
if preference == "Running shoes":
    shoe = "Cushioned Running Shoes"
elif preference == "Casuals":
    shoe = "Flexible Everyday Sneakers"
elif preference == "Formal shoes":
    shoe = "Orthopedic Leather Loafers"
else:
    shoe = "Arch Support Sandals"

# Material suggestion
if foot_type == "Flat Arch":
    material = "Firm midsoles with arch reinforcement"
elif foot_type == "High Arch":
    material = "Soft foam for better shock absorption"
else:
    material = "Balanced EVA midsoles for optimal comfort"

# Biomechanical analysis and tip
biomechanics = {
    "Flat Arch": "You tend to overpronate — choose footwear with motion control to stabilize your steps.",
    "High Arch": "You may underpronate — cushioned midsoles help absorb impact effectively.",
    "Normal Arch": "Your foot mechanics are balanced — go for shoes offering both support and flexibility."
}

tips = [
    "👣 Replace your shoes every 500–800 km to avoid injury.",
    "🧦 Use moisture-wicking socks to prevent blisters.",
    "🏃 Stretch your calves daily for better foot alignment.",
    "🦵 Choose shoes that match your activity intensity."
]

# --------------------------
# Display recommendations
# --------------------------
st.markdown(f"<div class='recommender'>🩴 Recommended Footwear: <span class='highlight'>{shoe}</span></div>", unsafe_allow_html=True)
st.markdown(f"<div class='recommender'>🧵 Material Suggestion: <span class='highlight'>{material}</span></div>", unsafe_allow_html=True)
st.markdown(f"<div class='recommender'>🧠 Biomechanical Insight: <span class='highlight'>{biomechanics[foot_type]}</span></div>", unsafe_allow_html=True)
st.markdown(f"<div class='tip'>💡 Tip of the Day: {random.choice(tips)}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# Voice Assistant Button
# --------------------------
if st.button("🎙️ Speak Recommendations"):
    summary_text = (
        f"Based on your age, weight, and foot type, "
        f"I recommend {shoe} made with {material}. "
        f"Biomechanically, {biomechanics[foot_type]} "
        f"And remember: {random.choice(tips)}"
    )
    speak(summary_text)
    st.success("Voice assistant has spoken your recommendations 🎧")







