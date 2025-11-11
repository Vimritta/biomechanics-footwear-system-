# app.py — FootFit Analyzer (light pastel violet navigation + white dropdowns + pastel rec boxes)
import streamlit as st
import os
from PIL import Image
import random
import textwrap
import base64  # added for pink download button
import html as html_mod

# ---------------------------
# Config
# ---------------------------
st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")
IMAGE_DIR = "images"

# ---------------------------
# Helpers
# ---------------------------
def load_image(name):
    path = os.path.join(IMAGE_DIR, name)
    try:
        if os.path.exists(path):
            return Image.open(path)
    except Exception:
        pass
    return None

# ---------------------------
# Updated speak_text function with native language support
# ---------------------------
def speak_text_native(brand, material, justification, tip=None):
    lang = st.session_state.voice_lang

    # Translate Material and Tip phrases
    if lang == "Sinhala":
        greeting = "ආයුබෝවන්! ඔබේ නිර්දේශය මෙන්න."
        material_label = "ද්‍රව්‍යය"
        tip_label = "දින උපදෙස"
    elif lang == "Tamil":
        greeting = "வணக்கம்! உங்கள் பரிந்துரை இதோ."
        material_label = "பொருள்"
        tip_label = "நாள் குறிப்பு"
    else:  # English
        greeting = "Hello! Here is your recommendation."
        material_label = "Material"
        tip_label = "Tip of the Day"

    # Construct full sentence
    sentence = f"{greeting} {brand} பரிந்துரைக்கப்படுகிறது. {material_label}: {material}. {justification}"
    if tip:
        sentence += f" {tip_label}: {tip}"
    
    html = f"""
    <script>
    const msg = new SpeechSynthesisUtterance({repr(sentence)});
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(html, height=0)

# ---------------------------
# Recommender logic
# ---------------------------
def recommend(foot_type, weight_group, activity, footwear_pref, age_group, gender):
    brands = {
        "Running shoes": ["Nike Air Zoom", "ASICS Gel-Nimbus", "Adidas Ultraboost"],
        "Cross-training shoes": ["Nike Metcon", "Reebok Nano", "Under Armour TriBase"],
        "Casual/fashion sneakers": ["New Balance 574", "Vans Old Skool", "Converse Chuck Taylor"],
        "Sandals or slippers": ["Crocs Classic Clog", "Birkenstock Arizona", "Teva Original"]
    }
    brand = random.choice(brands.get(footwear_pref, ["Generic FootFit Shoe"]))

    if footwear_pref == "Running shoes":
        if foot_type == "Flat Arch":
            material = "Dual-density EVA midsole + Arch-stability foam"
            justification = "Justification: Dual-density EVA supports the medial arch and prevents over-pronation while cushioning repeated impact."
        elif foot_type == "High Arch":
            material = "EVA midsole + Responsive gel insert"
            justification = "Justification: Additional shock absorption and a gel insert disperse high-pressure points common with high arches."
        else:
            material = "Lightweight mesh upper + Balanced foam midsole"
            justification = "Justification: Breathable upper and balanced cushioning suit neutral-footed runners."
    elif footwear_pref == "Cross-training shoes":
        material = "Dense EVA + Reinforced lateral upper + TPU heel counter"
        justification = "Justification: Dense EVA and reinforced upper provide lateral stability for multi-directional movements."
    elif footwear_pref == "Casual/fashion sneakers":
        material = "Soft foam midsole + Textile upper"
        justification = "Justification: Comfortable for daily wear with breathable textile uppers and soft foam for casual cushioning."
    else:
        material = "Soft EVA footbed + contoured cork or foam support"
        justification = "Justification: Soft footbed for comfort and a contoured profile to support arches during light activity."

    if weight_group == "Over 90 kg":
        material = material.replace("EVA", "Thick EVA").replace("Dense EVA", "High-density EVA").replace("soft foam", "high-density foam")
        justification = justification.replace("provides", "provides extra").replace("comfortable", "more durable and comfortable")

    if "High" in activity:
        material += " + Breathable knit upper"
        justification = justification[:-1] + " Ideal for frequent activity.*"
    elif "Low" in activity:
        material += " + Soft rubber outsole for comfort"
        justification = justification[:-1] + " Better for low-activity comfort.*"

    if gender == "Female":
        justification = "Designed for narrower heels and a more contoured fit. " + justification

    if "Under 18" in age_group:
        brand = brand + " (Youth Edition)"

    return brand, material, justification

# ---------------------------
# Themes
# ---------------------------
def set_white_theme():
    css = """
    <style>
    .stApp { background-color: white; color: black; }
    div[data-baseweb="select"] { background-color: white !important; color: black !important; }
    div[data-baseweb="select"] span { color: black !important; }
    div[data-baseweb="select"] div { background-color: white !important; color: black !important; }
    ul, li { background-color: white !important; color: black !important; }
    li:hover { background-color: #f0f0f0 !important; color: black !important; }
    select, textarea, input { background-color: white !important; color: black !important; border: 1px solid #ccc !important; border-radius: 6px; padding: 6px; }
    .stButton>button { background-color: #d9c2f0 !important; color: black !important; border: 1px solid #b495d6 !important; border-radius: 6px; font-weight: 600 !important; }
    .stButton>button:hover { background-color: #cbb3eb !important; }
    div.stCheckbox label, div.stCheckbox div[data-testid="stMarkdownContainer"] { color: orange !important; font-weight: bold !important; opacity: 1 !important; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def set_activity_theme(activity_key):
    if activity_key == "Low":
        color = "#d8ecff"; accent = "#3478b6"
    elif activity_key == "Moderate":
        color = "#e8f9e9"; accent = "#2e8b57"
    else:
        color = "#ffe9d6"; accent = "#e55300"

    css = f"""
    <style>
    .stApp {{ background: {color}; color: #111 !important; }}
    .summary-card {{ background: white; border-radius: 10px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); font-weight: 600; color: #111; }}
    .highlight-box {{ border-left: 6px solid {accent}; padding:12px; border-radius:8px; background: rgba(255,255,255,0.6); font-weight: 600; color: #111; }}
    .rec-shoe {{ background-color: #b8f5c1 !important; color: #000 !important; font-weight: bold; font-size: 1.2em; border-radius: 8px; padding: 10px; }}
    .rec-material {{ background-color: #cfe9ff !important; color: #000 !important; font-weight: bold; font-size: 1.1em; border-radius: 8px; padding: 10px; }}
    .stButton>button {{ background-color: #d9c2f0 !important; color: black !important; border: 1px solid #b495d6 !important; border-radius: 6px; font-weight: 600 !important; }}
    .stButton>button:hover {{ background-color: #cbb3eb !important; }}
    div.stCheckbox label, div.stCheckbox div[data-testid="stMarkdownContainer"] {{ color: orange !important; font-weight: bold !important; opacity: 1 !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------------------------
# Session initialization
# ---------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'inputs' not in st.session_state:
    st.session_state.inputs = {}
if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False
if 'foot_type' not in st.session_state:
    st.session_state.foot_type = "Normal Arch"
if 'footwear_pref' not in st.session_state:
    st.session_state.footwear_pref = "Running shoes"
if 'voice_lang' not in st.session_state:
    st.session_state.voice_lang = "English"

# ---------------------------
# Header
# ---------------------------
col1, col2 = st.columns([1, 8])
with col1:
    logo = load_image("logo.png")
    if logo:
        st.image(logo, width=100)
    else:
        st.markdown("<h3>👟 FootFit Analyzer</h3>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 style='margin-top:8px'>FootFit Analyzer — Biomechanics Footwear Profiler</h1>", unsafe_allow_html=True)
st.write("A biomechanics-informed recommender that suggests shoe brand, materials and explains why.")
st.markdown("---")

# ---------------------------
# Voice assistant language selection
# ---------------------------
voice_col1, voice_col2, voice_col3 = st.columns([1,1,1])
with voice_col1:
    if st.button("🇬🇧 English", key="lang_en"):
        st.session_state.voice_lang = "English"
with voice_col2:
    if st.button("🇱🇰 Sinhala", key="lang_si"):
        st.session_state.voice_lang = "Sinhala"
with voice_col3:
    if st.button("🇮🇳 Tamil", key="lang_ta"):
        st.session_state.voice_lang = "Tamil"

# ---------------------------
# STEP 1 — Personal Info
# ---------------------------
if st.session_state.step == 1:
    set_white_theme()
    st.header("Step 1 — Personal Info")

    age_label = st.selectbox("Select your Age Group", ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"], index=1)
    gender_label = st.selectbox("Select Gender", ["Male", "Female"], index=0)
    weight_label = st.selectbox("Select Weight Category", ["Under 50 kg", "50–70 kg", "71–90 kg", "Over 90 kg"], index=1)

    next_col1, next_col2 = st.columns([1,1])
    with next_col2:
        if st.button("Next →", key="to_step2"):
            st.session_state.inputs.update({
                "age_group": age_label,
                "gender": gender_label,
                "weight_group": weight_label,
            })
            st.session_state.step = 2

# ---------------------------
# STEP 2 — Foot & Activity
# ---------------------------
elif st.session_state.step == 2:
    set_white_theme()
    st.header("Step 2 — Foot & Activity Details")

    activity_label = st.selectbox(
        "Select your Daily Activity Level",
        ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (frequent walking/running)"],
        index=1
    )
    st.session_state.inputs["activity_label"] = activity_label
    st.session_state.inputs["activity_key"] = (
        "Low" if "Low" in activity_label else ("Moderate" if "Moderate" in activity_label else "High")
    )

    st.subheader("👣 Foot Type — choose one")
    foot_options = [("Flat Arch","flat.png"), ("Normal Arch","normal.png"), ("High Arch","high_arch.png")]
    cols = st.columns(len(foot_options))
    for (label, imgfile), col in zip(foot_options, cols):
        with col:
            img = load_image(imgfile)
            selected = (st.session_state.foot_type == label)
            if img:
                st.image(img, caption=label, width=140)
            if st.button(label, key=f"ftbtn_{label}"):
                st.session_state.foot_type = label
                st.session_state.inputs["foot_type"] = label

    st.write(f"👉 Currently selected foot type: {st.session_state.foot_type}")

    st.subheader("👟 Type of footwear you prefer")
    options = ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"]
    new_pref = st.selectbox("Select preferred footwear", options, index=options.index(st.session_state.footwear_pref))
    st.session_state.footwear_pref = new_pref
    st.session_state.inputs["footwear_pref"] = new_pref

    st.write(f"👉 Currently selected footwear: {st.session_state.footwear_pref}")

    back_col, next_col = st.columns([1,1])
    with back_col:
        if st.button("← Back", key="back_step1"):
            st.session_state.step = 1
    with next_col:
        if st.button("Next →", key="to_step3"):
            st.session_state.step = 3

# ---------------------------
# STEP 3 — Recommendation
# ---------------------------
elif st.session_state.step == 3:
    st.header("Step 3 — Recommendation & Biomechanics Summary")

    def get_val(key, default):
        return st.session_state.inputs.get(key, st.session_state.get(key, default))

    age_group = get_val("age_group", "18–25")
    gender = get_val("gender", "Male")
    weight_group = get_val("weight_group", "50–70 kg")
    activity_label = get_val("activity_label", "Moderate (walking/standing sometimes)")
    activity_key = get_val("activity_key", "Moderate")
    foot_type = get_val("foot_type", "Normal Arch")
    footwear_pref = get_val("footwear_pref", "Running shoes")

    set_activity_theme(activity_key)

    col_a1, col_a2, col_a3 = st.columns([1,1,2])
    with col_a1:
        if st.button("Analyze", key="analyze_btn"):
            st.session_state.analyze_clicked = True
    with col_a3:
        if st.button("🔁 Start Over", key="start_over"):
            st.session_state.step = 1
            st.session_state.inputs = {}
            st.session_state.foot_type = "Normal Arch"
            st.session_state.footwear_pref = "Running shoes"
            st.session_state.analyze_clicked = False

    brand, material, justification = recommend(
        foot_type, weight_group, activity_label, footwear_pref, age_group, gender
    )

    tips = [
        "Stretch your calves daily to reduce heel strain.",
        "Replace running shoes every 500–800 km.",
        "Use orthotic insoles when experiencing arch pain.",
        "Air-dry shoes after workouts to prevent odor and damage.",
        "Perform ankle rotations to strengthen stabilizers."
    ]
    tip_text = random.choice(tips)

    if st.session_state.analyze_clicked:
        gif_path = os.path.join(IMAGE_DIR, "walking.gif")
        if os.path.exists(gif_path):
            st.markdown(
                f"<img src='{gif_path}' width='220' style='border-radius:8px;'/>",
                unsafe_allow_html=True,
            )
        speak_text_native(brand, material, justification, tip_text)

    summary_md = f"""
    <div class="summary-card">
      <h3>🧠 <b>Biomechanics Summary</b></h3>
      <p class="highlight-box">
        👤 <b>Age:</b> {age_group} &nbsp; 🚻 <b>Gender:</b> {gender} <br/>
        ⚖️ <b>Weight:</b> {weight_group} &nbsp; 🏃 <b>Activity:</b> {activity_label} <br/>
        🦶 <b>Foot Type:</b> {foot_type} &nbsp; 👟 <b>Preference:</b> {footwear_pref}
      </p>
    </div>
    """
    st.markdown(summary_md, unsafe_allow_html=True)
    st.markdown("---")

    rec_col1, rec_col2 = st.columns([2,1])
    with rec_col1:
        st.markdown(f"<div class='rec-shoe'>👟 <b>Recommended Shoe:</b> {brand}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='rec-material'>🧵 <b>Material:</b> {material}</div>", unsafe_allow_html=True)

        justification_safe = html_mod.escape(justification)
        st.markdown(
            (
                "<div style=\""
                "background-color:#d2b48c;"
                "border-left:6px solid #8b6f47;"
                "padding:10px 14px;"
                "border-radius:8px;"
                "margin-top:8px;"
                "font-weight:600;"
                "color:#222;"
                "\">"
                "💬 Justification: " + justification_safe +
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="
                background-color:#fff9c4;
                border-left:6px solid #ffd54f;
                padding:10px 14px;
                border-radius:8px;
                margin-top:8px;
                font-weight:600;
                color:#333;">
                💡 Tip of the Day: {tip_text}
            </div>
            """,
            unsafe_allow_html=True,
        )

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

        b64 = base64.b64encode(summary_text.encode()).decode()
        download_href = f"""
        <a download="footfit_recommendation.txt" href="data:text/plain;base64,{b64}"
           style="background

