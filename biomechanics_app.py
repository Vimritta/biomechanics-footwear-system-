# app.py — FootFit Analyzer (light pastel violet navigation + white dropdowns + pastel rec boxes)
import streamlit as st
import os
from PIL import Image
import random
import textwrap
import base64  # added for pink download button
import json
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

def speak_text(text):
    """
    Safely injects JS to speak the provided text.
    Uses json.dumps to build a safe JS string literal.
    Note: Browsers typically require an explicit user gesture to allow audio playback.
    """
    safe_js_string = json.dumps(text)
    html = f"""
    <script>
    (function() {{
        try {{
            const msg = new SpeechSynthesisUtterance({safe_js_string});
            msg.rate = 1.0;
            // cancel any previous speech
            try {{ window.speechSynthesis.cancel(); }} catch(e) {{ }}
            window.speechSynthesis.speak(msg);
        }} catch(e) {{
            console.log("Speech error:", e);
        }}
    }})();
    </script>
    """
    # small height so Streamlit won't reserve a lot of space
    st.components.v1.html(html, height=10)

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
            justification = "Dual-density EVA supports the medial arch and prevents over-pronation while cushioning repeated impact."
        elif foot_type == "High Arch":
            material = "EVA midsole + Responsive gel insert"
            justification = "Additional shock absorption and a gel insert disperse high-pressure points common with high arches."
        else:
            material = "Lightweight mesh upper + Balanced foam midsole"
            justification = "Breathable upper and balanced cushioning suit neutral-footed runners."
    elif footwear_pref == "Cross-training shoes":
        material = "Dense EVA + Reinforced lateral upper + TPU heel counter"
        justification = "Dense EVA and reinforced upper provide lateral stability for multi-directional movements."
    elif footwear_pref == "Casual/fashion sneakers":
        material = "Soft foam midsole + Textile upper"
        justification = "Comfortable for daily wear with breathable textile uppers and soft foam for casual cushioning."
    else:
        material = "Soft EVA footbed + contoured cork or foam support"
        justification = "Soft footbed for comfort and a contoured profile to support arches during light activity."

    if weight_group == "Over 90 kg":
        material = material.replace("EVA", "Thick EVA").replace("Dense EVA", "High-density EVA").replace("soft foam", "high-density foam")
        justification = justification.replace("provides", "provides extra").replace("comfortable", "more durable and comfortable")

    if "High" in activity:
        material += " + Breathable knit upper"
        if justification.endswith("."):
            justification = justification[:-1] + " Ideal for frequent activity."
        else:
            justification += " Ideal for frequent activity."
    elif "Low" in activity:
        material += " + Soft rubber outsole for comfort"
        if justification.endswith("."):
            justification = justification[:-1] + " Better for low-activity comfort."
        else:
            justification += " Better for low-activity comfort."

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

    /* Stronger selector for checkbox label to ensure orange colour */
    div.stCheckbox label, div.stCheckbox div[data-testid="stMarkdownContainer"] {
        color: orange !important;
        font-weight: bold !important;
        opacity: 1 !important;
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

    /* Stronger selector for checkbox label to ensure orange colour */
    div.stCheckbox label, div.stCheckbox div[data-testid="stMarkdownContainer"] {{
        color: orange !important;
        font-weight: bold !important;
        opacity: 1 !important;
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
# flag to avoid repeated speak on reruns if needed
if 'last_spoken_hash' not in st.session_state:
    st.session_state.last_spoken_hash = None

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
   with rec_col1:
    # Shoe Recommendation
    st.markdown(f"<div style='background-color:#b2fab4;padding:12px;border-radius:10px;font-weight:600;'>👟 Recommended Shoe: <b>{brand}</b></div>", unsafe_allow_html=True)

    # Material Recommendation
    st.markdown(f"<div style='background-color:#d7e3fc;padding:12px;border-radius:10px;font-weight:600;'>🧵 Material: <b>{material}</b></div>", unsafe_allow_html=True)

    # Justification (Brown pastel)
    st.markdown(
        f"""
        <div style='background-color:#d2b48c;padding:12px;border-radius:10px;font-weight:600;'>
        💬 Justification: {justification}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tip of the Day (Yellow pastel)
    tips = [
        "Stretch your calves daily to reduce heel strain.",
        "Replace running shoes every 500–800 km.",
        "Use orthotic insoles when experiencing arch pain.",
        "Air-dry shoes after workouts to prevent odor and damage.",
        "Perform ankle rotations to strengthen stabilizers."
    ]
    tip_text = random.choice(tips)
    st.markdown(
        f"""
        <div style='background-color:#fff4b3;padding:12px;border-radius:10px;font-weight:600;'>
        💡 Tip of the Day: {tip_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ✅ Read-Aloud Button (Voice Assistant)
    tts_text = f"Recommended shoe is {brand}. Material suggestion is {material}. Justification: {justification}. Tip of the day: {tip_text}."
    tts_html = f"""
        <script>
        function speakText() {{
            var text = `{tts_text}`;
            var speech = new SpeechSynthesisUtterance(text);
            speech.pitch = 1;
            speech.rate = 1;
            speech.volume = 1;
            speech.lang = 'en-US';
            window.speechSynthesis.speak(speech);
        }}
        </script>
        <button onclick="speakText()" style="
            background-color:#ba68c8;
            color:white;
            border:none;
            padding:10px 20px;
            border-radius:10px;
            font-weight:600;
            margin-top:10px;
            cursor:pointer;
        ">🔊 Read Aloud</button>
    """
    st.markdown(tts_html, unsafe_allow_html=True)

    # ✅ Download Recommendation (Pink button)
    rec_text = f"Recommended Shoe: {brand}\nMaterial: {material}\nJustification: {justification}\nTip of the Day: {tip_text}"
    b64 = base64.b64encode(rec_text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="recommendation.txt"><button style="background-color:#ff4081;color:white;border:none;padding:10px 20px;border-radius:10px;font-weight:600;cursor:pointer;">💾 Download Recommendation (txt)</button></a>'
    st.markdown(href, unsafe_allow_html=True)


    with rec_col2:
        st.subheader("👟 Virtual Shoe Wall")
        sample_map = {
            "Running shoes": ["running1.png", "running2.png"],
            "Cross-training shoes": ["cross1.png", "cross2.png"],
            "Casual/fashion sneakers": ["casual1.png", "casual2.png"],
            "Sandals or slippers": ["sandal1.png", "sandal2.png"]
        }
        imgs = sample_map.get(footwear_pref, [])
        html_images = "<div style='display:flex; flex-wrap:wrap;'>"
        for im in imgs:
            p = os.path.join(IMAGE_DIR, im)
            if os.path.exists(p):
                html_images += f"<img src='{p}' width='110' style='margin:6px; border-radius:8px;'/>"
        html_images += "</div>"
        st.markdown(html_images, unsafe_allow_html=True)

    # ---------------------------
    # Read-aloud button (explicit user gesture)
    # ---------------------------
    # Use a button (explicit gesture) rather than a checkbox so browsers allow audio playback.
    if st.session_state.analyze_clicked:
        if st.button("🔊 Read recommendation aloud", key="read_btn"):
            speak_payload = f"Recommendation ready. I recommend {brand}. Material: {material}. Justification: {justification}"
            payload_hash = hash(speak_payload)
            # speak only if different from last spoken payload
            if st.session_state.last_spoken_hash != payload_hash:
                speak_text(speak_payload)
                st.session_state.last_spoken_hash = payload_hash

    if st.button("← Back", key="back_to_step2"):
        st.session_state.step = 2


   









