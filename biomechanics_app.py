# biomechanics_app.py
import streamlit as st
import pandas as pd
import numpy as np
import random
from PIL import Image
import os

st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")

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
# ---------------------------
elif st.session_state.step == 2:
    st.header("Step 2 — Foot & Activity Details")

    # Weight categories slider: show labels
    weight_index = st.slider("Weight group (kg)", 0, 3, 1)
    weight_map = ["Under 50 kg", "50–70 kg", "71–90 kg", "Over 90 kg"]
    weight_cat = weight_map[weight_index]

    # Activity slider 0=Low,1=Moderate,2=High
    activity_index = st.slider("Daily activity level", 0, 2, 1)
    activity_map = ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (frequent walking/running)"]
    activity_label = activity_map[activity_index]
    activity_key = ["Low", "Moderate", "High"][activity_index]

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
elif st.session_state.step == 3:
    st.header("Step 3 — Recommendation")
    data = st.session_state.get("temp", {})
    if not data:
        st.error("No input data found. Please go back and enter details.")
    else:
        age_cat = data["age_cat"]
        gender = data["gender"]
        weight_cat = data["weight_cat"]
        activity_label = data["activity_label"]
        activity_key = data["activity_key"]
        foot_type = data["foot_type"]
        footwear_type = data["footwear_type"]

        # Dynamic theme by activity
        if activity_key == "Low":
            bg = "#cce7ff"
        elif activity_key == "Moderate":
            bg = "#d0f0c0"
        else:
            bg = "#ffd6cc"
        st.markdown(f"""<style>.stApp{{background-color:{bg};}}</style>""", unsafe_allow_html=True)

        # Show animated silhouette if available
        sil = load_image("silhouette.gif")
        if sil:
            st.image(os.path.join(IMAGE_DIR, "silhouette.gif"), caption="Analyzing gait — visual reference", width=240)
        else:
            st.write("_(Animated silhouette not found — add images/silhouette.gif to repo to show animation.)_")

        # Biomechanics logic simplified
        if foot_type == "Flat Arch":
            arch_support = "High Arch Support"
        elif foot_type == "Normal Arch":
            arch_support = "Moderate Arch Support"
        else:
            arch_support = "Extra Cushioning"

        # Cushioning by weight category
        if weight_cat == "Over 90 kg":
            cushioning = "High Cushioning"
        elif weight_cat == "71–90 kg":
            cushioning = "Medium Cushioning"
        elif weight_cat == "50–70 kg":
            cushioning = "Medium Cushioning"
        else:
            cushioning = "Light Cushioning"

        # Shoe type suggestion refinement
        if activity_key == "High":
            shoe_suggestion = "Running shoes"
        elif activity_key == "Moderate":
            shoe_suggestion = "Cross-training shoes"
        else:
            shoe_suggestion = "Casual/fashion sneakers"

        # combine with user's footwear preference
        # If user's preference differs, show both recommended and preferred
        final_shoe = footwear_type if footwear_type == shoe_suggestion else f"{shoe_suggestion} (recommended) — you chose: {footwear_type}"

        # Material recommendation with justification
        shoe_name, material_bold, justification_italic = get_material_recommendation(foot_type, weight_cat, activity_key, footwear_type)

        # Comfort meter
        comfort_val, comfort_text = compute_comfort_level(cushioning)

        # Styled summary card (HTML)
        summary_html = f"""
        <div style="background-color:#ffffff; padding:16px; border-radius:12px; box-shadow: 0 2px 6px rgba(0,0,0,0.12);">
        <h3>👟 Biomechanics Summary</h3>
        <p><b>Age:</b> {age_cat} &nbsp; | &nbsp; <b>Gender:</b> {gender}</p>
        <p><b>Foot Type:</b> {foot_type} &nbsp; | &nbsp; <b>Activity:</b> {activity_label}</p>
        <p>🦶 <b>Arch Support:</b> {arch_support} &nbsp; • &nbsp; 🧽 <b>Cushioning:</b> {cushioning}</p>
        <p>🏷️ <b>Recommended Shoe Category:</b> {final_shoe}</p>
        <p>🔧 <b>Suggested Shoe:</b> {shoe_name}</p>
        <p>🧵 <b>Material Recommendation:</b> {material_bold} <br><i style="color: #444;">{justification_italic}</i></p>
        </div>
        """
        st.markdown(summary_html, unsafe_allow_html=True)

        # Comfort meter - show progress and text
        st.subheader("🌡️ Comfort Meter")
        st.progress(int(comfort_val * 100))
        st.write(comfort_text)

        # Add result to session history and show Save & Compare buttons
        result_entry = {
            "Age": age_cat,
            "Gender": gender,
            "Weight": weight_cat,
            "Activity": activity_label,
            "Foot Type": foot_type,
            "Recommended Shoe": shoe_name,
            "Material": material_bold,
            "Comfort": comfort_text
        }
        st.session_state.results.append(result_entry)

        # Virtual shoe wall (show images if available)
        st.subheader("👟 Virtual Shoe Wall")
        shoe_img_map = {
            "Running shoes": "shoe_running.png",
            "Cross-training shoes": "shoe_cross.png",
            "Casual/fashion sneakers": "shoe_casual.png",
            "Sandals or slippers": "shoe_sandal.png"
        }
        col_a, col_b, col_c, col_d = st.columns(4)
        for i, (label, fname) in enumerate(shoe_img_map.items()):
            img = load_image(fname)
            target_col = [col_a, col_b, col_c, col_d][i]
            with target_col:
                st.markdown(f"**{label}**")
                if img:
                    st.image(img, width=150)
                else:
                    st.write("_image missing_")

        # Tip of the day
        tips = [
            "Stretch your calves daily to reduce heel strain.",
            "Replace running shoes every 500 km for better support.",
            "High arches may benefit from extra cushioning.",
            "Flat feet often improve comfort with arch-support inserts."
        ]
        st.info("💡 Tip of the Day: " + random.choice(tips))

        # Voice assistant: speak final recommendation
        if st.button("🔊 Read recommendation aloud"):
            speak_text(f"Recommended shoe is {shoe_name}. Recommended material: {material_bold}. {justification_italic}")

        # Show Compare and history
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("← Back to Edit"):
                prev_step()
        with col2:
            if st.button("Show comparison table"):
                df = pd.DataFrame(st.session_state.results)
                st.dataframe(df)

        # Optionally export results
        if st.button("Export results to CSV"):
            df = pd.DataFrame(st.session_state.results)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name="footfit_results.csv", mime="text/csv")

# ---------------------------
# Upload dataset / Bulk analyze (footer)
# ---------------------------
st.markdown("---")
st.subheader("📂 Optional: Upload dataset for batch analysis")
uploaded = st.file_uploader("Upload CSV or XLSX (columns: AgeGroup, Gender, WeightGroup, FootType, Activity, PreferredFootwear)", type=["csv","xlsx"])
if uploaded:
    try:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        st.success(f"Loaded {len(df)} rows")
        st.dataframe(df.head())
        if st.button("Run batch recommendations"):
            out = []
            for _, r in df.iterrows():
                shoe_name, material_bold, justification = get_material_recommendation(r.get("FootType","Normal Arch"), r.get("WeightGroup","50–70 kg"), r.get("Activity","Moderate"), r.get("PreferredFootwear","Casual/fashion sneakers"))
                out.append({
                    "FootType": r.get("FootType",""),
                    "WeightGroup": r.get("WeightGroup",""),
                    "Activity": r.get("Activity",""),
                    "Recommended Shoe": shoe_name,
                    "Material": material_bold,
                    "Justification": justification
                })
            st.dataframe(pd.DataFrame(out))
    except Exception as e:
        st.error("Failed to load dataset: " + str(e))

