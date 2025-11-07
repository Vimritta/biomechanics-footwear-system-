# biomechanics_app.py — FootFit Analyzer with Voice Assistant
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")

# --------------------------- Helper Functions ---------------------------
def load_image(filename):
    path = os.path.join("images", filename)
    return Image.open(path) if os.path.exists(path) else None

def map_activity_index(value):
    return ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (running or standing often)"][value]

# --------------------------- Voice Assistant ---------------------------
def speak_text(text):
    """Inject JS to speak text via browser speechSynthesis API"""
    js = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.lang = 'en-US';
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)

# --------------------------- Custom CSS ---------------------------
custom_style = """
<style>
body, [data-testid="stAppViewContainer"] {
    background-color: white !important;
    color: black !important;
    font-weight: bold !important;
}
h1, h2, h3, h4 { color: black !important; font-weight: 800 !important; }
.step3-text { font-weight: bold !important; }
</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# --------------------------- Session State ---------------------------
if "step" not in st.session_state: st.session_state.step = 1
if "inputs" not in st.session_state: st.session_state.inputs = {}

# --------------------------- STEP 1 ---------------------------
if st.session_state.step == 1:
    st.title("👣 Step 1 — Personal Details")
    speak_text("Welcome to FootFit Analyzer. Let's start with your personal details.")

    st.subheader("Select your Age Range")
    age = st.radio("", ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"], horizontal=True)

    st.subheader("Select your Gender")
    gender = st.radio("", ["Male", "Female"], horizontal=True)

    st.subheader("Select your Weight Range")
    weight = st.radio("", ["Under 50 kg", "50–70 kg", "71–90 kg", "91–110 kg", "Over 110 kg"], horizontal=True)

    col1, col2 = st.columns([1,1])
    with col2:
        if st.button("Next →"):
            st.session_state.inputs.update({"age": age, "gender": gender, "weight": weight})
            st.session_state.step = 2
            st.experimental_rerun()

# --------------------------- STEP 2 ---------------------------
elif st.session_state.step == 2:
    st.title("🏃 Step 2 — Foot & Activity Details")
    speak_text("Now let's check your foot type and activity level.")

    activity_i = st.slider("Select your daily activity level", 0, 2, 1, step=1)
    activity_label = map_activity_index(activity_i)
    st.caption(f"Selected: **{activity_label}**")

    st.subheader("👣 Foot Type — choose one")
    foot_options = {"Flat Arch": "flat.png", "Normal Arch": "normal.png", "High Arch": "high_arch.png"}
    if "foot_type" not in st.session_state: st.session_state.foot_type = "Normal Arch"

    cols = st.columns(len(foot_options))
    for (label, img_file), col in zip(foot_options.items(), cols):
        with col:
            img = load_image(img_file)
            if img: st.image(img, caption=label, width=140)
            selected = st.session_state.foot_type == label
            if st.button(f"{'✅ ' if selected else ''}{label}", key=f"ft_{label}"):
                st.session_state.foot_type = label
    st.write(f"👉 Selected Foot Type: **{st.session_state.foot_type}**")

    st.subheader("👟 Type of Footwear You Prefer")
    options = ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"]
    if "footwear_pref" not in st.session_state: st.session_state.footwear_pref = "Running shoes"

    st.session_state.footwear_pref = st.radio("", options, horizontal=True, key="footwear_pref")
    st.write(f"👉 Selected Footwear: **{st.session_state.footwear_pref}**")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("← Back"): st.session_state.step = 1; st.experimental_rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.inputs.update({
                "activity_label": activity_label,
                "foot_type": st.session_state.foot_type,
                "footwear_pref": st.session_state.footwear_pref
            })
            st.session_state.step = 3
            st.experimental_rerun()

# --------------------------- STEP 3 ---------------------------
elif st.session_state.step == 3:
    inputs = st.session_state.inputs
    activity = inputs["activity_label"]

    # Dynamic background color logic
    if "Low" in activity: bg, text = "#D3EAF2", "#084B83"
    elif "Moderate" in activity: bg, text = "#FFF3CD", "#795548"
    else: bg, text = "#FDE2E4", "#C21807"

    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: {bg} !important;
        color: {text} !important;
    }}
    h1, h2, h3, h4, h5, h6, p, div {{
        color: {text} !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.title("🧠 Step 3 — Biomechanics Summary & Recommendation")
    speak_text("Here is your personalized biomechanics summary and footwear recommendation.")

    st.write(f"👤 **Age:** {inputs['age']}   🚻 **Gender:** {inputs['gender']}")
    st.write(f"⚖️ **Weight:** {inputs['weight']}   🏃 **Activity:** {inputs['activity_label']}")
    st.write(f"🦶 **Foot Type:** {inputs['foot_type']}   👟 **Preference:** {inputs['footwear_pref']}")
    st.markdown("---")

    # Recommender
    recommendation = "Neutral Cushioned Shoes"
    if "Flat" in inputs["foot_type"]:
        recommendation = "Stability or Motion Control Shoes for extra arch support"
    elif "High" in inputs["foot_type"]:
        recommendation = "Cushioned Shoes with soft midsoles for shock absorption"

    if "Cross" in inputs["footwear_pref"]:
        recommendation += " — great for varied workouts!"
    elif "Casual" in inputs["footwear_pref"]:
        recommendation += " — look stylish with added comfort!"
    elif "Sandals" in inputs["footwear_pref"]:
        recommendation += " — choose orthopedic soles for daily wear."

    st.success(f"💡 **Recommended Footwear:** {recommendation}")
    speak_text(f"Based on your profile, I recommend {recommendation}")

    st.markdown("---")
    if st.button("← Back"):
        st.session_state.step = 2
        st.experimental_rerun()






