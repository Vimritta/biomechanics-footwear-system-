# app.py
import streamlit as st
import os
from PIL import Image
import random
import textwrap

# ---------------------------
# Config
# ---------------------------
st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")

IMAGE_DIR = "images"  # put all images/GIFs here (see list below)

# ---------------------------
# Helpers
# ---------------------------
def load_image(name, fallback=None):
    path = os.path.join(IMAGE_DIR, name)
    try:
        if os.path.exists(path):
            return Image.open(path)
    except Exception:
        pass
    return fallback

def speak_text(text):
    html = f"""
    <script>
    const msg = new SpeechSynthesisUtterance({repr(text)});
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(html, height=0)

def map_age_index(i):
    labels = ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"]
    return labels[int(i)]

def map_weight_val(w):
    if w < 50:
        return "Under 50 kg"
    if w < 71:
        return "50–70 kg"
    if w < 91:
        return "71–90 kg"
    return "Over 90 kg"

def map_activity_index(i):
    labels = ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (frequent walking/running)"]
    return labels[int(i)]

def map_gender_index(i):
    return ["Male", "Female"][int(i)]

# Recommendation logic (shoe brand, material (bold), justification (italic))
def recommend(foot_type, weight_group, activity, footwear_pref, age_group, gender):
    # Base brand suggestions per footwear type (examples)
    brands = {
        "Running shoes": ["Nike Air Zoom", "ASICS Gel-Nimbus", "Adidas Ultraboost"],
        "Cross-training shoes": ["Nike Metcon", "Reebok Nano", "Under Armour TriBase"],
        "Casual/fashion sneakers": ["New Balance 574", "Vans Old Skool", "Converse Chuck Taylor"],
        "Sandals or slippers": ["Crocs Classic Clog", "Birkenstock Arizona", "Teva Original"]
    }
    brand = random.choice(brands.get(footwear_pref, ["Generic FootFit Shoe"]))

    # Material + justification rules
    if footwear_pref == "Running shoes":
        if foot_type == "Flat Arch":
            material = "**Dual-density EVA midsole + Arch-stability foam**"
            justification = "*Justification: Dual-density EVA supports the medial arch and prevents over-pronation while cushioning repeated impact.*"
        elif foot_type == "High Arch":
            material = "**EVA midsole + Responsive gel insert**"
            justification = "*Justification: Additional shock absorption and a gel insert disperse high-pressure points common with high arches.*"
        else:
            material = "**Lightweight mesh upper + Balanced foam midsole**"
            justification = "*Justification: Breathable upper and balanced cushioning suit neutral-footed runners.*"
    elif footwear_pref == "Cross-training shoes":
        material = "**Dense EVA + Reinforced lateral upper + TPU heel counter**"
        justification = "*Justification: Dense EVA and reinforced upper provide lateral stability for multi-directional movements.*"
    elif footwear_pref == "Casual/fashion sneakers":
        material = "**Soft foam midsole + Textile upper**"
        justification = "*Justification: Comfortable for daily wear with breathable textile uppers and soft foam for casual cushioning.*"
    else:  # Sandals/slippers
        material = "**Soft EVA footbed + contoured cork or foam support**"
        justification = "*Justification: Soft footbed for comfort and a contoured profile to support arches during light activity.*"

    # Weight-based reinforcement
    if weight_group == "Over 90 kg":
        # strengthen material wording
        material = material.replace("EVA", "Thick EVA").replace("Dense EVA", "High-density EVA").replace("soft foam", "high-density foam")
        justification = justification.replace("provides", "provides extra").replace("comfortable", "more durable and comfortable")

    # Activity nuance
    if "High" in activity:
        material += " **+ Breathable knit upper**"
        justification = justification[:-1] + " Ideal for frequent activity.*"
    elif "Low" in activity:
        material += " **+ Soft rubber outsole for comfort**"
        justification = justification[:-1] + " Better for low-activity comfort.*"

    # Gender nuance (minor)
    if gender == "Female":
        justification = "Designed for narrower heels and a more contoured fit. " + justification

    # Age nuance example: younger users prefer trendy designs (not functional change)
    if "Under 18" in age_group:
        brand = brand + " (Youth Edition)"

    return brand, material, justification

# ---------------------------
# UI Utilities: theme / CSS
# ---------------------------
def set_activity_theme(activity_key):
    # activity_key: "Low", "Moderate", "High"
    if activity_key == "Low":
        color = "#d8ecff"  # calm blue
        accent = "#3478b6"
    elif activity_key == "Moderate":
        color = "#e8f9e9"  # light green
        accent = "#2e8b57"
    else:
        color = "#ffe9d6"  # energetic orange
        accent = "#e55300"
    css = f"""
    <style>
    .stApp {{ background: {color}; }}
    .summary-card {{ background: white; border-radius: 10px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }}
    .highlight-box {{ border-left: 6px solid {accent}; padding:12px; border-radius:8px; background: rgba(255,255,255,0.6); }}
    .shoe-wall img {{ max-width:120px; margin:6px; border-radius:8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    .foot-type-selected {{ border: 3px solid {accent}; border-radius:8px; padding:4px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------------------------
# Session & Wizard state
# ---------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'inputs' not in st.session_state:
    st.session_state.inputs = {}
if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False

# ---------------------------
# Title / Logo
# ---------------------------
col1, col2 = st.columns([1, 8])
with col1:
    logo = load_image("logo.png")
    if logo:
        st.image(logo, width=110)
    else:
        st.markdown("<h3>👟 FootFit Analyzer</h3>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 style='margin-top:8px'>FootFit Analyzer — Biomechanics Footwear Profiler</h1>", unsafe_allow_html=True)
st.write("A biomechanics-informed recommender that suggests **shoe brand**, **materials** and explains *why*.")

st.markdown("---")

# ---------------------------
# STEP 1 — Personal Info (slider-based as requested)
# ---------------------------
if st.session_state.step == 1:
    st.header("Step 1 — Personal Info")
    st.write("Use sliders for a modern interactive feel. The label beneath each slider shows the selected option.")

    age_i = st.slider("Age group", min_value=0, max_value=5, value=1, format="%d")
    age_label = map_age_index(age_i)
    st.caption(f"Selected age group: **{age_label}**")

    gender_i = st.slider("Gender (0 = Male, 1 = Female)", min_value=0, max_value=1, value=0, step=1)
    gender_label = map_gender_index(gender_i)
    st.caption(f"Selected gender: **{gender_label}**")

    weight_val = st.slider("Weight (kg)", min_value=30, max_value=120, value=68, step=1)
    weight_label = map_weight_val(weight_val)
    st.caption(f"Weight category: **{weight_label}**")

    next_col1, next_col2 = st.columns([1,1])
    with next_col2:
        if st.button("Next →"):
            st.session_state.inputs.update({
                "age_group": age_label,
                "gender": gender_label,
                "weight_val": weight_val,
                "weight_group": weight_label
            })
            st.session_state.step = 2

# ---------------------------
# STEP 2 — Foot details & activity
# ---------------------------
elif st.session_state.step == 2:
    st.header("Step 2 — Foot & Activity Details")

    # Activity slider (0..2)
    activity_i = st.slider("Daily activity level (0=Low,1=Moderate,2=High)", min_value=0, max_value=2, value=1, step=1)
    activity_label = map_activity_index(activity_i)
    st.caption(f"Selected: **{activity_label}**")

    # Foot type visualization: images with clickable buttons (highlight selected)
    st.subheader("👣 Foot Type — click an option")
    foot_options = [
        ("flat.png", "Flat Arch"),
        ("normal.png", "Normal Arch"),
        ("high_arch.png", "High Arch")
    ]

    cols = st.columns(3)
    selected_ft = st.session_state.inputs.get("foot_type", "Normal Arch")
    for i, (fname, label) in enumerate(foot_options):
        with cols[i]:
            img = load_image(fname)
            if img:
                # show selected border if chosen
                if st.button(label + (" ✅" if label == selected_ft else "")):
                    selected_ft = label
                # Render with an additional CSS wrapper for selected
                if label == selected_ft:
                    st.markdown(f"<div class='foot-type-selected'>{st.image(img, caption=label, width=140) or ''}</div>", unsafe_allow_html=True)
                else:
                    st.image(img, caption=label, width=140)
            else:
                if st.button(label + (" ✅" if label == selected_ft else "")):
                    selected_ft = label
                st.write(label)

    # Footwear preference selectbox (discrete choices)
    footwear_pref = st.selectbox("Type of footwear you prefer", ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"])

    back_col, next_col = st.columns([1,1])
    with back_col:
        if st.button("← Back"):
            st.session_state.step = 1
    with next_col:
        if st.button("Next →"):
            st.session_state.inputs.update({
                "activity_label": activity_label,
                "activity_key": "Low" if "Low" in activity_label else ("Moderate" if "Moderate" in activity_label else "High"),
                "foot_type": selected_ft,
                "footwear_pref": footwear_pref
            })
            st.session_state.step = 3

# ---------------------------
# STEP 3 — Analysis & Recommendation
# ---------------------------
elif st.session_state.step == 3:
    st.header("Step 3 — Recommendation & Biomechanics Summary")
    # Set activity theme color
    set_activity_theme(st.session_state.inputs.get("activity_key", "Moderate"))

    age_group = st.session_state.inputs.get("age_group", "18–25")
    gender = st.session_state.inputs.get("gender", "Male")
    weight_group = st.session_state.inputs.get("weight_group", "50–70 kg")
    activity_label = st.session_state.inputs.get("activity_label", "Moderate (walking/standing sometimes)")
    foot_type = st.session_state.inputs.get("foot_type", "Normal Arch")
    footwear_pref = st.session_state.inputs.get("footwear_pref", "Running shoes")

    # Analyze button (triggers animated GIF + TTS)
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1,1,2])
    with analyze_col1:
        if st.button("Analyze"):
            st.session_state.analyze_clicked = True
            # run TTS on the result after computing below

    with analyze_col3:
        if st.button("🔁 Start Over"):
            st.session_state.step = 1
            st.session_state.inputs = {}
            st.session_state.analyze_clicked = False
            st.experimental_rerun()

    # Compute recommendation
    brand, material, justification = recommend(foot_type, weight_group, activity_label, footwear_pref, age_group, gender)

    # Animated GIF when analyze clicked
    if st.session_state.analyze_clicked:
        gif = load_image("walking.gif")
        if gif:
            # Use html to place gif on right column
            st.markdown("<div style='display:flex; align-items:center; gap:12px;'>"
                        f"<img src='{os.path.join(IMAGE_DIR, 'walking.gif')}' width='220' style='border-radius:8px; box-shadow: 0 6px 18px rgba(0,0,0,0.12);'/>"
                        "</div>", unsafe_allow_html=True)
        # speak final short text
        speak_text(f"Recommendation ready. {brand} recommended. {material}.")

    # Summary card (styled)
    summary_md = f"""
    <div class="summary-card">
      <h3>🧠 Biomechanics Summary</h3>
      <p class="highlight-box">
        👤 <b>Age:</b> {age_group} &nbsp; &nbsp; 🚻 <b>Gender:</b> {gender} <br/>
        ⚖️ <b>Weight:</b> {weight_group} &nbsp; 🏃 <b>Activity:</b> {activity_label} <br/>
        🦶 <b>Foot Type:</b> {foot_type} &nbsp; 👟 <b>Preference:</b> {footwear_pref}
      </p>
    </div>
    """
    st.markdown(summary_md, unsafe_allow_html=True)

    # Recommendation display with bold material and italic justification
    st.markdown("---")
    rec_col1, rec_col2 = st.columns([2,1])
    with rec_col1:
        st.success(f"👟 **Recommended Shoe:** {brand}")
        st.info(f"🧵 **Material:** {material}")
        st.write(f"💬 {justification}")

        # Tip of the day
        tips = [
            "Stretch your calves daily to reduce heel strain.",
            "Replace running shoes every 500–800 km.",
            "Use orthotic insoles when experiencing arch pain.",
            "Air-dry shoes after workouts to prevent odor and damage.",
            "Perform ankle rotations to strengthen stabilizers."
        ]
        st.markdown(f"💡 **Tip of the Day:** *{random.choice(tips)}*")

        # Offer a short downloadable summary (text)
        summary_text = textwrap.dedent(f"""
        FootFit Analyzer - Recommendation
        ---------------------------------
        Age group: {age_group}
        Gender: {gender}
        Weight group: {weight_group}
        Activity level: {activity_label}
        Foot type: {foot_type}
        Preferred footwear: {footwear_pref}

        Recommended Shoe: {brand}
        Material: {material}
        Justification: {justification}
        """)
        st.download_button("📄 Download Recommendation (txt)", summary_text, file_name="footfit_recommendation.txt")

    # Virtual Shoe Wall (show a few sample images matching footwear type)
    with rec_col2:
        st.subheader("👟 Virtual Shoe Wall")
        sample_map = {
            "Running shoes": ["running1.png", "running2.png"],
            "Cross-training shoes": ["cross1.png", "cross2.png"],
            "Casual/fashion sneakers": ["casual1.png", "casual2.png"],
            "Sandals or slippers": ["sandal1.png", "sandal2.png"]
        }
        imgs = sample_map.get(footwear_pref, [])
        # Show images in a row
        html_images = "<div class='shoe-wall'>"
        for im in imgs:
            p = os.path.join(IMAGE_DIR, im)
            if os.path.exists(p):
                html_images += f"<img src='{p}' width='110' />"
        html_images += "</div>"
        st.markdown(html_images, unsafe_allow_html=True)

    # Voice assistant control
    if st.checkbox("🔊 Read recommendation aloud"):
        speak_text(f"I recommend {brand}. Material: {material}. {justification}")

    # Back button
    if st.button("← Back"):
        st.session_state.step = 2



