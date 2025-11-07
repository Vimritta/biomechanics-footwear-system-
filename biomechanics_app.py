# biomechanics_app.py
import streamlit as st
import pandas as pd
import numpy as np
import random
from PIL import Image
import os

st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟", color="red")

# ---------------------------
# Helper utilities
# ---------------------------
IMAGE_DIR = "images"  # folder where you should put icons and GIFs

def load_image(name):
    path = os.path.join(IMAGE_DIR, name)
    if os.path.exists(path):
        return Image.open(path)
    return None

def speak_text(text):
    # Use browser TTS via HTML/JS (works in Streamlit)
    html = f"""
    <script>
    var msg = new SpeechSynthesisUtterance({repr(text)});
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(html, height=0)

def get_material_recommendation(foot_type, weight_cat, activity_level, footwear_type):
    # weight_cat: "Under 50", "50-70", "71-90", "Over 90"
    # return (footwear_name, material_bold, justification_italic)
    # Simple rule-based logic - extendable
    # Map footwear_type to category recommendation
    if footwear_type == "Running shoes":
        shoe_name = "Cushioned Running Shoe"
        if foot_type == "Flat Arch":
            material = ("**Lightweight Mesh + Arch Stability Foam**",
                        "*Justification: Mesh upper improves airflow; arch-stability foam supports medial arch during frequent impact.*")
        elif foot_type == "High Arch":
            material = ("**EVA + Responsive Midsole**",
                        "*Justification: EVA with responsive foam provides extra shock absorption for high arches.*")
        else:
            material = ("**Breathable Mesh + Balanced Midsole**",
                        "*Justification: Balanced cushioning with breathable upper for most runners.*")
    elif footwear_type == "Cross-training shoes":
        shoe_name = "Cross-Training Shoe"
        material = ("**Dense EVA + Reinforced Upper**",
                    "*Justification: Dense midsole for lateral stability during multi-directional movements.*")
    elif footwear_type == "Casual/fashion sneakers":
        shoe_name = "Casual Lifestyle Sneaker"
        material = ("**Light Foam + Textile Upper**",
                    "*Justification: Comfortable daily wear material with moderate cushioning.*")
    else:  # Sandals or slippers
        shoe_name = "Comfort Sandal"
        material = ("**Soft EVA Footbed + Breathable Strap**",
                    "*Justification: Soft footbed for comfort; open upper for ventilation.*")

    # Weight-based override for heavier users
    if weight_cat == "Over 90" and "EVA" in material[0] or "Foam" in material[0]:
        material = (material[0].replace("EVA", "Thick EVA").replace("Foam", "High-density Foam"),
                    material[1].replace("provides", "provides extra").replace("moderate", "increased"))
    return shoe_name, material[0], material[1]

def compute_comfort_level(cushioning):
    if cushioning == "High Cushioning":
        return 0.95, "😄 Excellent Comfort"
    if cushioning == "Medium Cushioning":
        return 0.7, "🙂 Moderate Comfort"
    return 0.4, "😐 Basic Comfort"

# ---------------------------
# Title / Logo / Banner
# ---------------------------
col_logo, col_title = st.columns([1, 8])
with col_logo:
    logo = load_image("logo.png")
    if logo:
        st.image(logo, width=120)
    else:
        st.markdown("**FootFit Analyzer**")
with col_title:
    st.markdown("<h1 style='margin-top:10px'>👟 FootFit Analyzer — Biomechanics Footwear Profiler</h1>", unsafe_allow_html=True)
st.write("A simple science-based recommender that suggests footwear type and **material** based on biomechanics.")

st.markdown("---")

# ---------------------------
# Wizard Steps
# ---------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'results' not in st.session_state:
    st.session_state.results = []

def next_step():
    st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# ---------------------------
# Step 1: Personal info
if st.session_state.step == 1:
    st.header("Step 1 — Personal Info")

    # Age group dropdown (option box)
    age_cat = st.selectbox(
        "Select your Age Group",
        ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"]
    )

    # Gender dropdown (option box)
    gender = st.selectbox(
        "Select your Gender",
        ["Male", "Female"]
    )

    st.write(f"Selected: **{age_cat}**, **{gender}**")

    # Next button
    st.write("")
    coln1, coln2 = st.columns([1,1])
    with coln1:
        if st.button("Next →"):
            next_step()


    # Next button
    st.write("")
    coln1, coln2 = st.columns([1,1])
    with coln1:
        if st.button("Next →"):
            next_step()

# ---------------------------
# Step 2: Foot details & activity
elif st.session_state.step == 2:
    st.header("Step 2 — Foot & Activity Details")

    # Weight group dropdown
    weight_cat = st.selectbox(
        "Select your Weight Group",
        ["Under 50 kg", "50–70 kg", "71–90 kg", "Over 90 kg"]
    )

    # Activity level dropdown
    activity_label = st.selectbox(
        "Select your Daily Activity Level",
        [
            "Low (mostly sitting)",
            "Moderate (walking/standing sometimes)",
            "High (frequent walking/running)"
        ]
    )

    # Create a short version (used later for background color logic)
    if "Low" in activity_label:
        activity_key = "Low"
    elif "Moderate" in activity_label:
        activity_key = "Moderate"
    else:
        activity_key = "High"


    # Foot type visualization using small icons
    st.write("👣 Foot Type — click to select")
    colf1, colf2, colf3 = st.columns(3)
    foot_choice = None
    ft_selected = None
    foot_images = [("flat.png","Flat Arch"), ("normal.png","Normal Arch"), ("high_arch.png","High Arch")]
    for i, (fname, label) in enumerate(foot_images):
        img = load_image(fname)
        if i == 0:
            with colf1:
                if img:
                    if st.button(label):
                        ft_selected = label
                    st.image(img, caption=label, width=120)
                else:
                    if st.button(label):
                        ft_selected = label
        elif i == 1:
            with colf2:
                if img:
                    if st.button(label):
                        ft_selected = label
                    st.image(img, caption=label, width=120)
                else:
                    if st.button(label):
                        ft_selected = label
        else:
            with colf3:
                if img:
                    if st.button(label):
                        ft_selected = label
                    st.image(img, caption=label, width=120)
                else:
                    if st.button(label):
                        ft_selected = label

    # If a foot type hasn't just been selected via button, provide a fallback radio
    if not ft_selected:
        ft_selected = st.radio("Or choose foot type:", ["Flat Arch", "Normal Arch", "High Arch"])

    # Footwear preference
    footwear_type = st.selectbox("Type of footwear you prefer", ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"])

    st.write("")
    cols = st.columns([1,1,1])
    with cols[0]:
        if st.button("← Back"):
            prev_step()
    with cols[2]:
        if st.button("Next →"):
            # save intermediate answers
            st.session_state.temp = {
                "age_cat": age_cat,
                "gender": gender,
                "weight_cat": weight_cat,
                "activity_label": activity_label,
                "activity_key": activity_key,
                "foot_type": ft_selected,
                "footwear_type": footwear_type
            }
            next_step()

# ---------------------------
# Step 3: Recommendation & UI output
# ---------------------------
# ========== STEP 3 ==========
elif st.session_state.step == 3:
    st.header("Step 3 — Footwear & Material Recommendation")

    st.markdown("### 🧠 Biomechanical Analysis Results")

    # Retrieve stored data safely
    age_cat = st.session_state.get("age_cat", "18–25")
    gender = st.session_state.get("gender", "Male")
    weight_cat = st.session_state.get("weight_cat", "50–70 kg")
    activity_label = st.session_state.get("activity_label", "Moderate (walking/standing sometimes)")
    foot_type = st.session_state.get("foot_type", "Normal Arch")
    footwear_type = st.session_state.get("footwear_type", "Running shoes")

    # ----------- Recommendation Rules -----------
    footwear_recommendation = ""
    material_recommendation = ""
    justification = ""

    # Foot type–based logic
    if foot_type == "Flat Arch":
        footwear_recommendation = "Stability Running Shoe"
        material_recommendation = "Dual-Density Foam Midsole"
        justification = "Provides arch support and prevents over-pronation."
    elif foot_type == "Normal Arch":
        footwear_recommendation = "Neutral Cushioning Shoe"
        material_recommendation = "Lightweight Mesh and EVA Foam"
        justification = "Ensures flexibility and balanced shock absorption."
    else:  # High Arch
        footwear_recommendation = "High-Cushion Shoe"
        material_recommendation = "Soft Gel or Memory Foam Insole"
        justification = "Improves pressure distribution and heel comfort."

    # Activity & weight modifiers
    if "High" in activity_label:
        material_recommendation += " with Breathable Knit Upper"
        justification += " Ideal for frequent walking or running."
    elif "Low" in activity_label:
        material_recommendation += " with Soft Rubber Outsole"
        justification += " Adds comfort for prolonged sitting or light walking."

    if "Over 90" in weight_cat:
        material_recommendation += " and Reinforced Heel Padding"
        justification += " Offers additional stability for heavier load bearing."

    # Gender nuance
    if gender == "Female":
        justification += " Designed to fit narrower heels and softer midsoles."

    # ---------- Display Recommendation ----------
    st.success(f"👟 **Recommended Footwear:** {footwear_recommendation}")
    st.info(f"🧵 **Suggested Material:** {material_recommendation}")
    st.write(f"💬 *{justification}*")

    # Show summary card
    st.markdown("---")
    st.subheader("Your Selection Summary")
    st.write(f"👤 **Age Group:** {age_cat}")
    st.write(f"🚻 **Gender:** {gender}")
    st.write(f"⚖️ **Weight Group:** {weight_cat}")
    st.write(f"🏃 **Activity Level:** {activity_label}")
    st.write(f"🦶 **Foot Type:** {foot_type}")
    st.write(f"👟 **Footwear Preference:** {footwear_type}")

    # Tip of the day
    import random
    tips = [
        "Stretch your calves daily to reduce heel strain.",
        "Replace your shoes every 500–800 km of running.",
        "Use orthotic insoles if you experience arch pain.",
        "Let your shoes air-dry after workouts.",
        "Do simple ankle rotations to strengthen stabilizer muscles."
    ]
    st.markdown(f"💡 **Tip of the Day:** *{random.choice(tips)}*")

    # Navigation
    st.markdown("---")
    if st.button("🔁 Analyze Again"):
        st.session_state.step = 1


