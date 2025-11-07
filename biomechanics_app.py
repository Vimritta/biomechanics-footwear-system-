# biomech_app_final.py
import streamlit as st
from PIL import Image
import os
import random

# ------------------ APP CONFIG ------------------
st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")

# ------------------ IMAGE LOADER ------------------
def load_image(name):
    path = os.path.join("images", name)
    return Image.open(path) if os.path.exists(path) else None

# ------------------ THEME FUNCTIONS ------------------
def set_background(color):
    """Set static background color (white for Step 1 and 2)."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
            transition: background-color 0.6s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def set_activity_theme(activity_level):
    """Dynamic background for Step 3 based on activity."""
    if "Low" in activity_level:
        color = "#e6f2ff"  # calm blue
    elif "Moderate" in activity_level:
        color = "#e8f8ef"  # soft green
    else:
        color = "#fff2e0"  # energetic orange
    set_background(color)

# ------------------ HEADER ------------------
logo = load_image("logo.png")
col1, col2 = st.columns([1, 8])
if logo:
    col1.image(logo, width=120)
col2.markdown("<h1>👟 FootFit Analyzer — Biomechanics Profiler</h1>", unsafe_allow_html=True)
st.markdown("---")

# ------------------ SESSION STATE ------------------
if "step" not in st.session_state:
    st.session_state.step = 1

# ------------------ STEP CONTROL ------------------
def next_step():
    st.session_state.step += 1
def prev_step():
    st.session_state.step -= 1

# ------------------ STEP 1: PERSONAL INFO ------------------
if st.session_state.step == 1:
    set_background("white")

    st.header("Step 1 — Personal Information")
    age = st.selectbox("Select your Age Group", ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"])
    gender = st.radio("Select your Gender", ["Male", "Female"])

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Next →"):
            st.session_state.age = age
            st.session_state.gender = gender
            next_step()

# ------------------ STEP 2: FOOT DETAILS ------------------
elif st.session_state.step == 2:
    set_background("white")

    st.header("Step 2 — Biomechanical Details")
    weight = st.selectbox("Select your Weight Group", ["Under 50 kg", "50–70 kg", "71–90 kg", "Over 90 kg"])
    activity = st.selectbox("Select your Daily Activity Level",
                            ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (frequent walking/running)"])
    foot_type = st.selectbox("Select your Foot Type", ["Flat Arch", "Normal Arch", "High Arch"])
    footwear_type = st.selectbox("Type of footwear you prefer",
                                 ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"])

    # Foot type image preview
    st.markdown("### 👣 Foot Type Visualization")
    col1, col2, col3 = st.columns(3)
    img_flat = load_image("flat.png")
    img_normal = load_image("normal.png")
    img_high = load_image("high_arch.png")
    if img_flat: col1.image(img_flat, caption="Flat Arch", width=120)
    if img_normal: col2.image(img_normal, caption="Normal Arch", width=120)
    if img_high: col3.image(img_high, caption="High Arch", width=120)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back"):
            prev_step()
    with col3:
        if st.button("Next →"):
            st.session_state.weight = weight
            st.session_state.activity = activity
            st.session_state.foot_type = foot_type
            st.session_state.footwear_type = footwear_type
            next_step()

# ------------------ STEP 3: RECOMMENDATION ------------------
elif st.session_state.step == 3:
    activity = st.session_state.get("activity", "Moderate (walking/standing sometimes)")
    set_activity_theme(activity)  # 🎨 Auto color change only here

    st.header("Step 3 — Personalized Recommendation")

    age = st.session_state.get("age", "")
    gender = st.session_state.get("gender", "")
    weight = st.session_state.get("weight", "")
    foot_type = st.session_state.get("foot_type", "")
    footwear_type = st.session_state.get("footwear_type", "")

    # --- Recommendation logic ---
    if foot_type == "Flat Arch":
        shoe = "Stability Running Shoe"
        material = "Dual-Density Foam Midsole"
        justification = "Provides arch support and prevents over-pronation."
    elif foot_type == "High Arch":
        shoe = "Cushioned Shoe"
        material = "Soft Gel or Memory Foam"
        justification = "Improves shock absorption and heel comfort."
    else:
        shoe = "Neutral Cushion Shoe"
        material = "Breathable Mesh + EVA Foam"
        justification = "Offers balanced flexibility and comfort."

    if "Casual" in footwear_type:
        shoe = "Casual Sneaker"
        material = "Lightweight Textile Upper + Soft Foam Sole"
        justification = "Comfortable for daily wear with flexible material."

    # --- Biomechanics Summary ---
    st.markdown(f"""
    <div style='background-color:white; padding:20px; border-radius:15px; box-shadow:0 0 10px rgba(0,0,0,0.1);'>
    <h3>🧠 Biomechanics Summary</h3>
    <p>👤 <b>Age:</b> {age} &nbsp;&nbsp; 🚻 <b>Gender:</b> {gender}</p>
    <p>⚖️ <b>Weight:</b> {weight} &nbsp;&nbsp; 🏃 <b>Activity:</b> {activity}</p>
    <p>🦶 <b>Foot Type:</b> {foot_type} &nbsp;&nbsp; 👟 <b>Preference:</b> {footwear_type}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Recommendation Output ---
    st.success(f"👟 **Recommended Footwear:** {shoe}")
    st.info(f"🧵 **Material:** {material}")
    st.write(f"💬 *{justification}*")

    # --- Virtual Shoe Wall / Animation ---
    gif = None
    if "Low" in activity:
        gif = load_image("sitting.gif")
    elif "Moderate" in activity:
        gif = load_image("walking.gif")
    else:
        gif = load_image("running.gif")
    if gif:
        st.image(gif, caption="Biomechanical Activity", width=250)

    # --- Tip of the Day ---
    tips = [
        "Stretch your calves daily to reduce heel strain.",
        "Replace your shoes every 500–800 km of running.",
        "Use orthotic insoles if you experience arch pain.",
        "Let your shoes air-dry after workouts.",
        "Do simple ankle rotations to strengthen stabilizer muscles."
    ]
    st.markdown(f"💡 **Tip of the Day:** *{random.choice(tips)}*")

    st.markdown("---")
    if st.button("🔁 Analyze Again"):
        st.session_state.step = 1






