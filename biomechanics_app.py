# app.py — FootFit Analyzer (light pastel violet navigation + white dropdowns + pastel rec boxes)
import streamlit as st
import os
from PIL import Image
import random
import textwrap
import base64
import html as html_mod
import json
import tempfile

# Try to import gTTS for server-side TTS fallback (recommended)
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except Exception:
    GTTS_AVAILABLE = False

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

def speak_browser(text, lang="en-US"):
    """Browser-side TTS using SpeechSynthesis (fallback)."""
    safe_text = json.dumps(text)
    safe_lang = json.dumps(lang)
    html = f"""
    <script>
    (function() {{
        try {{
            const msg = new SpeechSynthesisUtterance({safe_text});
            msg.rate = 1.0;
            msg.lang = {safe_lang};
            try {{ window.speechSynthesis.cancel(); }} catch(e) {{}}
            window.speechSynthesis.speak(msg);
        }} catch (e) {{ console.log("Speech error:", e); }}
    }})();
    </script>
    """
    st.components.v1.html(html, height=10)

def speak_server_gtts(text, lang_code):
    """Server-side TTS using gTTS -> saves MP3 to temp file."""
    try:
        t = gTTS(text=text, lang=lang_code)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp.close()
        t.save(tmp.name)
        return tmp.name
    except Exception as e:
        print("gTTS error:", e)
        return None

def speak_text_reliable(text, lang_tag):
    """Primary attempt: server-side gTTS. Fallback: browser TTS."""
    if isinstance(lang_tag, tuple):
        gtts_code, browser_code = lang_tag
    else:
        gtts_code, browser_code = (lang_tag, lang_tag)

    if GTTS_AVAILABLE and gtts_code:
        mp3_path = speak_server_gtts(text, gtts_code)
        if mp3_path:
            try:
                st.audio(mp3_path, format="audio/mp3")
                return
            except Exception:
                pass
    speak_browser(text, browser_code)

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

    # Material and justification logic
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
# STEP 1 — Personal Info
# ---------------------------
if st.session_state.step == 1:
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
    st.header("Step 2 — Foot & Activity Details")
    activity_label = st.selectbox(
        "Select your Daily Activity Level",
        ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (frequent walking/running)"],
        index=1
    )
    st.session_state.inputs["activity_label"] = activity_label
    st.session_state.inputs["activity_key"] = ("Low" if "Low" in activity_label else ("Moderate" if "Moderate" in activity_label else "High"))

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
# STEP 3 — Recommendation & Voice Assistant
# ---------------------------
elif st.session_state.step == 3:
    st.header("Step 3 — Recommendation & Biomechanics Summary")

    # Get inputs
    def get_val(key, default):
        return st.session_state.inputs.get(key, st.session_state.get(key, default))

    age_group = get_val("age_group", "18–25")
    gender = get_val("gender", "Male")
    weight_group = get_val("weight_group", "50–70 kg")
    activity_label = get_val("activity_label", "Moderate (walking/standing sometimes)")
    activity_key = get_val("activity_key", "Moderate")
    foot_type = get_val("foot_type", "Normal Arch")
    footwear_pref = get_val("footwear_pref", "Running shoes")

    # Voice assistant UI
    st.markdown("### 🗣️ Voice Assistant Settings")
    c1, c2 = st.columns([1, 1])
    with c1:
        voice_enabled = st.checkbox("Enable Voice Assistant", value=False)
    with c2:
        language = st.selectbox("Language", ["English 🇬🇧", "Sinhala 🇱🇰", "Tamil 🇮🇳"], index=0)

    # Map language to (gTTS_code, browser_code)
    lang_map = {
        "English 🇬🇧": ("en", "en-US"),
        "Sinhala 🇱🇰": ("si", "si-LK"),
        "Tamil 🇮🇳": ("ta", "ta-IN")
    }
    gtts_code, browser_code = lang_map.get(language, ("en", "en-US"))

    # Recommendation
    brand, material, justification = recommend(
        foot_type, weight_group, activity_label, footwear_pref, age_group, gender
    )

    # Display summary card
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

    # Recommendation boxes
    rec_col1, rec_col2 = st.columns([2,1])
    with rec_col1:
        st.markdown(f"<div class='rec-shoe'>👟 <b>Recommended Shoe:</b> {brand}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='rec-material'>🧵 <b>Material:</b> {material}</div>", unsafe_allow_html=True)
        justification_safe = html_mod.escape(justification)
        st.markdown(
            (f"<div style='background-color:#d2b48c; border-left:6px solid #8b6f47; "
             f"padding:10px 14px; border-radius:8px; margin-top:8px; font-weight:600; color:#222;'>"
             f"💬 Justification: {justification_safe}</div>"),
            unsafe_allow_html=True
        )

        # Tip of the day
        tips = [
            "Stretch your calves daily to reduce heel strain.",
            "Replace running shoes every 500–800 km.",
            "Use orthotic insoles when experiencing arch pain.",
            "Air-dry shoes after workouts to prevent odor and damage.",
            "Perform ankle rotations to strengthen stabilizers."
        ]
        tip_text = random.choice(tips)
        st.markdown(f"""
        <div style="background-color:#fff9c4; border-left:6px solid #ffd54f; padding:10px 14px; border-radius:8px; margin-top:8px; font-weight:600; color:#333;">
        💡 Tip of the Day: {tip_text}</div>
        """, unsafe_allow_html=True)

        # Downloadable summary
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
        Tip: {tip_text}
        """)
        b64 = base64.b64encode(summary_text.encode()).decode()
        download_href = f"""
        <a download="footfit_recommendation.txt" href="data:text/plain;base64,{b64}" style="background-color:#ff4da6; color:white; padding:10px 14px; border-radius:8px; text-decoration:none; font-weight:bold; display:inline-block;">
        📄 Download Recommendation (txt) </a>
        """
        st.markdown(download_href, unsafe_allow_html=True)

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
    # Multi-language Read Aloud (native greeting + recommend phrase)
    # ---------------------------
    if voice_enabled:
        if st.checkbox("🔊 Read recommendation aloud", key="read_aloud"):
            # Greetings and recommend phrase map
            greeting_map = {
                "English 🇬🇧": "",
                "Sinhala 🇱🇰": "ආයුබෝවන්! ",
                "Tamil 🇮🇳": "வணக்கம்! "
            }
            recommend_map = {
                "English 🇬🇧": "I recommend",
                "Sinhala 🇱🇰": "මම නිර්දේශ කරනවා",
                "Tamil 🇮🇳": "நான் பரிந்துரைக்கிறேன்"
            }
            greeting = greeting_map.get(language, "")
            recommend_phrase = recommend_map.get(language, "I recommend")

            full_text = f"{greeting}{recommend_phrase} {brand}. Material: {material}. Justification: {justification}. Tip: {tip_text}"

            played = False
            if gtts_code and GTTS_AVAILABLE:
                played = speak_server_gtts(full_text, gtts_code)
                if played:
                    st.audio(played, format="audio/mp3")
            if not played:
                speak_browser(full_text, browser_code)
            
            st.session_state["read_aloud"] = False
    else:
        st.info("🔇 Voice assistant is turned off. (Enable voice for read aloud.)")

    # Back button
    if st.button("← Back", key="back_to_step2"):
        st.session_state.step = 2
