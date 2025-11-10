# app.py — FootFit Analyzer (light pastel violet navigation + white dropdowns + pastel rec boxes)
import streamlit as st
import os
from PIL import Image
import random
import textwrap
import base64  # added for pink download button

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

def speak_text(text):
    html = f"""
    <script>
    const msg = new SpeechSynthesisUtterance({repr(text)});
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
    """White theme + white dropdowns + light pastel violet navigation buttons"""
    css = """
    <style>
    .stApp { background-color: white; color: black; }

    .stMarkdown, .stText, .stSelectbox, .stRadio, label, div, p, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }

    div[data-baseweb="select"], ul, li {
        background-color: white !important;
        color: black !important;
    }
    li:hover { background-color: #f0f0f0 !important; }

    select, textarea, input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
        border-radius: 6px;
        padding: 6px;
    }

    .stButton>button {
        background-color: #d9c2f0 !important;
        color: black !important;
        border: 1px solid #b495d6 !important;
        border-radius: 6px;
        font-weight: 600 !important;
    }
    .stButton>button:hover { background-color: #cbb3eb !important; }

    /* ORANGE read aloud label */
    div.stCheckbox label {
        color: orange !important;
        font-weight: bold !important;
    }
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
    .summary-card {{
        background: white; border-radius: 10px;
        padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        font-weight: 600; color: #111;
    }}
    .highlight-box {{
        border-left: 6px solid {accent};
        padding:12px; border-radius:8px;
        background: rgba(255,255,255,0.6);
        font-weight: 600; color: #111;
    }}
    .rec-shoe {{
        background-color: #b8f5c1 !important;
        color: #000 !important;
        font-weight: bold;
        font-size: 1.2em;
        border-radius: 8px;
        padding: 10px;
    }}
    .rec-material {{
        background-color: #cfe9ff !important;
        color: #000 !important;
        font-weight: bold;
        font-size: 1.1em;
        border-radius: 8px;
        padding: 10px;
    }}
    .stButton>button {{
        background-color: #d9c2f0 !important;
        color: black !important;
        border: 1px solid #b495d6 !important;
        border-radius: 6px;
        font-weight: 600 !important;
    }}
    .stButton>button:hover {{ background-color: #cbb3eb !important; }}
    /* Orange label for Read aloud */
    div.stCheckbox label {{
        color: orange !important;
        font-weight: bold !important;
    }}
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
# STEP 3 — Recommendation
# ---------------------------
set_activity_theme("Moderate")  # preview theme

st.header("Step 3 — Recommendation & Biomechanics Summary")
st.markdown('<div class="rec-shoe">👟 <b>Recommended Shoe:</b> Nike Air Zoom</div>', unsafe_allow_html=True)
st.markdown('<div class="rec-material">🧵 <b>Material:</b> Lightweight mesh upper + Balanced foam midsole</div>', unsafe_allow_html=True)
st.write("💬 Justification: Breathable upper and balanced cushioning suit neutral-footed runners.")
st.write("💡 Tip of the Day: Air-dry shoes after workouts to prevent odor and damage.")

# ✅ Pink download button
summary_text = "Recommended Shoe: Nike Air Zoom\nMaterial: Lightweight mesh upper + Balanced foam midsole\nJustification: Breathable upper and balanced cushioning suit neutral-footed runners."
b64 = base64.b64encode(summary_text.encode()).decode()
download_href = f"""
<a download="footfit_recommendation.txt" href="data:text/plain;base64,{b64}"
   style="background-color:#ff4da6; color:white; padding:10px 14px; border-radius:8px;
          text-decoration:none; font-weight:bold; display:inline-block;">
   📄 Download Recommendation (txt)
</a>
"""
st.markdown(download_href, unsafe_allow_html=True)

# ✅ Orange “Read aloud” checkbox
read_aloud = st.checkbox("🔊 Read recommendation aloud")
if read_aloud:
    speak_text(summary_text)

st.button("← Back")







