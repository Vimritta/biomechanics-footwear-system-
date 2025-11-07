# app.py — FootFit Analyzer (Final Professional Version)
import streamlit as st
import random
from PIL import Image
import os

st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")

# -------------------- Helper Functions --------------------
def load_image(filename):
    path = os.path.join("images", filename)
    return Image.open(path) if os.path.exists(path) else None

def speak_text(text):
    js = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.lang = 'en-US';
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)

def get_recommendation(foot_type, footwear, weight, activity):
    """Rule-based recommender"""
    if footwear == "Running shoes":
        brand = "Nike Air Zoom Pegasus"
        if "Flat" in foot_type:
            material = "**Dual-density foam midsole**"
            justification = "*Provides medial arch stability and support for overpronation.*"
        elif "High" in foot_type:
            material = "**Soft gel cushioning + mesh upper**"
            justification = "*Offers high shock absorption and breathability for high arches.*"
        else:
            material = "**EVA midsole + knit upper**"
            justification = "*Gives balanced flexibility and airflow for neutral runners.*"

    elif footwear == "Cross-training shoes":
        brand = "Reebok Nano X"
        material = "**Dense EVA midsole + rubber outsole**"
        justification = "*Provides side-to-side stability for multi-directional movement.*"

    elif footwear == "Casual/fashion sneakers":
        brand = "Adidas Stan Smith"
        material = "**Lightweight foam insole + leather upper**"
        justification = "*Ensures everyday comfort and timeless style.*"

    else:
        brand = "Skechers On-the-Go Sandal"
        material = "**Memory foam footbed + flexible sole**"
        justification = "*Offers cushioned support and breathability for relaxed use.*"

    if "Over 90" in weight:
        material += " and **reinforced heel padding**"
        justification += " Adds durability for heavier body weight."
    if "High" in activity:
        justification += " Ideal for frequent movement and long wear."

    return brand, material, justification

def tip_of_day():
    tips = [
        "Stretch your calves daily to reduce heel strain.",
        "Replace your shoes every 800 km of running.",
        "Use orthotic insoles if you experience arch pain.",
        "Let your shoes air-dry after workouts.",
        "Do simple ankle rotations to strengthen stabilizer muscles."
    ]
    return random.choice(tips)

# -------------------- Page Setup --------------------
if "step" not in st.session_state:
    st.session_state.step = 1

# -------------------- Step 1 --------------------
if st.session_state.step == 1:
    st.markdown(
        "<h1 style='color:black; font-weight:900;'>👟 Step 1 — Personal Information</h1>",
        unsafe_allow_html=True,
    )
    speak_text("Welcome to FootFit Analyzer. Let's start with your personal information.")

    st.markdown("<div style='color:black; font-weight:bold;'>Select your age group:</div>", unsafe_allow_html=True)
    age = st.radio("", ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"], horizontal=True)

    st.markdown("<div style='color:black; font-weight:bold;'>Select your gender:</div>", unsafe_allow_html=True)
    gender = st.radio("", ["Male", "Female"], horizontal=True)

    st.markdown("<div style='color:black; font-weight:bold;'>Select your weight group:</div>", unsafe_allow_html=True)
    weight = st.radio("", ["Under 50 kg", "50–70 kg", "71–90 kg", "Over 90 kg"], horizontal=True)

    if st.button("Next →"):
        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.weight = weight
        st.session_state.step = 2
        st.experimental_rerun()

# -------------------- Step 2 --------------------
elif st.session_state.step == 2:
    st.markdown(
        "<h1 style='color:black; font-weight:900;'>🦶 Step 2 — Foot & Activity Details</h1>",
        unsafe_allow_html=True,
    )
    speak_text("Now, please provide your foot and activity details.")

    st.markdown("<div style='color:black; font-weight:bold;'>Select your foot type:</div>", unsafe_allow_html=True)
    foot_type = st.radio("", ["Flat Arch", "Normal Arch", "High Arch"], horizontal=True)

    st.markdown("<div style='color:black; font-weight:bold;'>Select your daily activity level:</div>", unsafe_allow_html=True)
    activity = st.radio(
        "",
        ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (frequent walking/running)"],
        horizontal=True,
    )

    st.markdown("<div style='color:black; font-weight:bold;'>Select your preferred footwear type:</div>", unsafe_allow_html=True)
    footwear = st.radio("", ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step = 1
            st.experimental_rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.foot_type = foot_type
            st.session_state.activity = activity
            st.session_state.footwear = footwear
            st.session_state.step = 3
            st.experimental_rerun()

# -------------------- Step 3 --------------------
elif st.session_state.step == 3:
    age = st.session_state.age
    gender = st.session_state.gender
    weight = st.session_state.weight
    foot_type = st.session_state.foot_type
    activity = st.session_state.activity
    footwear = st.session_state.footwear

    # Dynamic background
    if "Low" in activity:
        bg, color = "#E3F2FD", "#0D47A1"
    elif "Moderate" in activity:
        bg, color = "#E8F5E9", "#1B5E20"
    else:
        bg, color = "#FFF3E0", "#BF360C"

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-color: {bg} !important;
        }}
        h1, h2, h3, p, div {{
            color: {color} !important;
            font-weight: bold !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1>🧠 Step 3 — Biomechanics Analysis & Recommendation</h1>", unsafe_allow_html=True)

    brand, material, justification = get_recommendation(foot_type, footwear, weight, activity)
    speak_text(f"Based on your biomechanics, we recommend the {brand}. {material}. {justification}")

    st.markdown("### 📊 Biomechanics Summary Card")
    st.markdown(
        f"""
        👤 **Age:** {age}  🚻 **Gender:** {gender}  
        ⚖️ **Weight:** {weight}  🏃 **Activity:** {activity}  
        🦶 **Foot Type:** {foot_type}  👟 **Preference:** {footwear}
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.success(f"👟 **Recommended Footwear Brand:** {brand}")
    st.info(f"🧵 **Material Suggestion:** {material}")
    st.write(f"💬 *{justification}*")

    # Virtual Shoe Wall (show shoe image)
    st.markdown("### 👟 Virtual Shoe Wall")
    if "Running" in footwear:
        st.image(load_image("running.png"), width=250)
    elif "Cross" in footwear:
        st.image(load_image("cross.png"), width=250)
    elif "Casual" in footwear:
        st.image(load_image("casual.png"), width=250)
    else:
        st.image(load_image("sandal.png"), width=250)

    st.markdown("---")
    st.info(f"💡 **Tip of the Day:** {tip_of_day()}")

    if st.button("🔁 Analyze Again"):
        st.session_state.step = 1
        st.experimental_rerun()






