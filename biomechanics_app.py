# app.py — FootFit Analyzer (light pastel violet navigation + white dropdowns + pastel rec boxes)
import streamlit as st
import os
from PIL import Image
import random
import textwrap

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

    /* General text color */
    .stMarkdown, .stText, .stSelectbox, .stRadio, label, div, p, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }

    /* Dropdowns: white background and white open list */
    div[data-baseweb="select"] {
        background-color: white !important;
        color: black !important;
    }
    div[data-baseweb="select"] span {
        color: black !important;
    }
    div[data-baseweb="select"] div {
        background-color: white !important;
        color: black !important;
    }
    ul, li {
        background-color: white !important;
        color: black !important;
    }
    li:hover {
        background-color: #f0f0f0 !important;
        color: black !important;
    }

    select, textarea, input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
        border-radius: 6px;
        padding: 6px;
    }

    /* Navigation buttons (Next, Back) — light pastel violet */
    .stButton>button {
        background-color: #d9c2f0 !important;
        color: black !important;
        border: 1px solid #b495d6 !important;
        border-radius: 6px;
        font-weight: 600 !important;
    }
    .stButton>button:hover {
        background-color: #cbb3eb !important;
    }

    /* ✅ Download button — pink */
    div[data-testid="stDownloadButton"] > button {
        background-color: #ff4da6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: bold !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #ff66b2 !important;
    }

    /* Checkbox label bold */
    label[for*="read_aloud"] {
        font-weight: bold !important;
        color: #111 !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def set_activity_theme(activity_key):
    """Activity-based theme (Step 3)"""
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

    /* Recommended shoe & material boxes */
    .rec-shoe {{
        background-color: #b8f5c1 !important; /* pastel green */
        color: #000 !important;
        font-weight: bold;
        font-size: 1.2em;
        border-radius: 8px;
        padding: 10px;
    }}
    .rec-material {{
        background-color: #cfe9ff !important; /* pastel blue */
        color: #000 !important;
        font-weight: bold;
        font-size: 1.1em;
        border-radius: 8px;
        padding: 10px;
    }}

    /* Buttons — pastel violet */
    .stButton>button {{
        background-color: #d9c2f0 !important;
        color: black !important;
        border: 1px solid #b495d6 !important;
        border-radius: 6px;
        font-weight: 600 !important;
    }}
    .stButton>button:hover {{
        background-color: #cbb3eb !important;
    }}

    /* ✅ Download button — pink */
    div[data-testid="stDownloadButton"] > button {{
        background-color: #ff4da6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: bold !important;
    }}
    div[data-testid="stDownloadButton"] > button:hover {{
        background-color: #ff66b2 !important;
    }}

    /* Checkbox label bold */
    label[for*="read_aloud"] {{
        font-weight: bold !important;
        color: #111 !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------------------------
# (rest of your code continues exactly the same below)
# ---------------------------

# ... 👇 Keep everything after this line unchanged — same as your provided code








