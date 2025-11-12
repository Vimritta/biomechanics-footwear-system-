# app.py — FootFit Analyzer (light pastel violet navigation + white dropdowns + pastel rec boxes)
import streamlit as st
import os
from PIL import Image
import random
import textwrap
import base64
import html as html_mod

# ---------------------------
# Config
# ---------------------------
st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")
IMAGE_DIR = "images"

# ---------------------------
# Helper Functions
# ---------------------------
def load_image(name):
    path = os.path.join(IMAGE_DIR, name)
    try:
        if os.path.exists(path):
            return Image.open(path)
    except Exception:
        pass
    return None

def speak_text(text):
    html = f"""
    <script>
    const msg = new SpeechSynthesisUtterance({repr(text)});
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(html, height=0)

def greeting_message(age_group, gender):
    """Generate greeting message based on age and gender"""
    if "Under 18" in age_group:
        return "Hey young champ! Ready to step up?" if gender == "Male" else "Hey young star! Ready to shine?"
    elif "18–25" in age_group:
        return "Hello, young runner!" if gender == "Male" else "Hello, young athlete!"
    elif "26–35" in age_group or "36–50" in age_group:
        return "Hi there, active gentleman!" if gender == "Male" else "Hi there, active lady!"
    elif "51–65" in age_group:
        return "Good day, sir! Let’s find comfort and performance!" if gender == "Male" else "Good day, ma’am! Let’s find comfort and performance!"
    else:
        return "Welcome, wise walker! Let’s make each step easy!" if gender == "Male" else "Welcome, graceful walker! Let’s make each step easy!"

# ---------------------------
# Initialize session states
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "inputs" not in st.session_state:
    st.session_state.inputs = {}
if "analyze_clicked" not in st.session_state:
    st.session_state.analyze_clicked = False

# ---------------------------
# STEP 1 — Personal Details
# ---------------------------
if st.session_state.step == 1:
    st.header("Step 1 — Personal Details")
    with st.form("personal_form"):
        age_group = st.selectbox("Select your age group:", ["Under 18", "18–25", "26–35", "36–50", "51–65", "65+"])
        gender = st.selectbox("Select your gender:", ["Male", "Female"])
        weight_group = st.selectbox("Select your weight range:", ["Below 50 kg", "50–70 kg", "71–90 kg", "Above 90 kg"])
        submitted = st.form_submit_button("Next ➡️")

        if submitted:
            st.session_state.inputs.update({
                "age_group": age_group,
                "gender": gender,
                "weight_group": weight_group,
            })
            st.session_state.step = 2
            st.experimental_rerun()

# ---------------------------
# STEP 2 — Foot & Activity Details
# ---------------------------
elif st.session_state.step == 2:
    st.header("Step 2 — Foot & Activity Details")
    with st.form("foot_form"):
        activity_label = st.selectbox("Select your activity level:", [
            "Sedentary (mostly sitting)",
            "Moderate (walking/standing sometimes)",
            "Active (running or frequent walking)",
        ])
        activity_key = activity_label.split(" ")[0]
        foot_type = st.selectbox("Select your foot type:", ["Normal Arch", "Flat Arch", "High Arch"])
        footwear_pref = st.selectbox("Preferred type of footwear:", ["Running shoes", "Casual shoes", "Formal shoes"])
        submitted = st.form_submit_button("Next ➡️")

        if submitted:
            st.session_state.inputs.update({
                "activity_label": activity_label,
                "activity_key": activity_key,
                "foot_type": foot_type,
                "footwear_pref": footwear_pref,
            })
            st.session_state.step = 3
            st.experimental_rerun()

# ---------------------------
# Recommendation Function (Simplified)
# ---------------------------
def recommend(foot_type, weight, activity, footwear_pref, age, gender):
    """Simple logic to recommend brand, material, justification"""
    brands = {
        "Running shoes": ["Nike Zoom", "Adidas Ultraboost", "Puma Velocity"],
        "Casual shoes": ["Skechers GoWalk", "Clarks Flex", "Vans Comfort"],
        "Formal shoes": ["Bata Leather", "Hush Puppies", "Ecco Classic"],
    }

    materials = {
        "Normal Arch": "Mesh with cushioned sole",
        "Flat Arch": "Orthopedic support sole with arch padding",
        "High Arch": "Flexible midsole with heel cushioning",
    }

    brand = random.choice(brands.get(footwear_pref, ["Nike Air"]))
    material = materials.get(foot_type, "Standard Comfort Foam")
    justification = f"{brand} suits {activity.lower()} activities for {gender.lower()}s with {foot_type.lower()} and {weight.lower()}."
    return brand, material, justification

# ---------------------------
# STEP 3 — Recommendation & Biomechanics Summary
# ---------------------------
elif st.session_state.step == 3:
    st.header("Step 3 — Recommendation & Biomechanics Summary")

    age_group = st.session_state.inputs.get("age_group")
    gender = st.session_state.inputs.get("gender")
    weight_group = st.session_state.inputs.get("weight_group")
    activity_label = st.session_state.inputs.get("activity_label")
    activity_key = st.session_state.inputs.get("activity_key")
    foot_type = st.session_state.inputs.get("foot_type")
    footwear_pref = st.session_state.inputs.get("footwear_pref")

    col_a1, col_a2, col_a3 = st.columns([1,1,2])
    with col_a1:
        if st.button("Analyze"):
            st.session_state.analyze_clicked = True
    with col_a3:
        if st.button("🔁 Start Over"):
            st.session_state.step = 1
            st.session_state.inputs = {}
            st.session_state.analyze_clicked = False
            st.experimental_rerun()

    brand, material, justification = recommend(
        foot_type, weight_group, activity_label, footwear_pref, age_group, gender
    )

    if st.session_state.analyze_clicked:
        # Greeting
        greet_text = greeting_message(age_group, gender)
        st.markdown(f"<h3 style='color:#6a0dad; font-weight:700;'>{greet_text}</h3>", unsafe_allow_html=True)
        speak_text(greet_text)

        # GIF
        gif_url = "https://i.pinimg.com/originals/e8/ef/28/e8ef28560911f51810df9b0581819650.gif"
        st.markdown(
            f"<img src='{gif_url}' width='250' style='border-radius:10px; margin-bottom:15px;'/>",
            unsafe_allow_html=True,
        )

        speak_text(f"Recommendation ready. I recommend {brand} with {material} for you.")

        # Summary
        st.markdown("---")
        st.markdown(
            f"""
            <div style='background-color:#f3e8ff; padding:15px; border-radius:12px;'>
                <h3>🧠 <b>Biomechanics Summary</b></h3>
                👤 <b>Age:</b> {age_group} &nbsp; 🚻 <b>Gender:</b> {gender} <br/>
                ⚖️ <b>Weight:</b> {weight_group} &nbsp; 🏃 <b>Activity:</b> {activity_label} <br/>
                🦶 <b>Foot Type:</b> {foot_type} &nbsp; 👟 <b>Preference:</b> {footwear_pref}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Recommendation Display
        st.markdown(
            f"""
            <div style='background-color:#e0d4fc; padding:20px; border-radius:16px;'>
                <h3>👟 <b>Recommended Footwear:</b> {brand}</h3>
                <p style='font-size:18px;'><b>Material Suggestion:</b> {material}</p>
                <p>{justification}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Tip of the Day
        tips = [
            "Replace your running shoes every 500–800 km for best comfort.",
            "Choose shoes with breathable material to prevent moisture build-up.",
            "Stretch your feet daily to maintain flexibility and arch strength.",
            "Always try on shoes in the evening—your feet expand slightly during the day.",
        ]
        tip = random.choice(tips)
        st.markdown(
            f"""
            <div style='background-color:#fff3b0; padding:15px; border-radius:12px; margin-top:20px;'>
                <h4>💡 Tip of the Day</h4>
                <p style='font-size:17px;'>{tip}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        speak_text(tip)


