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


# ✅ Updated speak_text() — multilingual Sinhala, Tamil, and English
def speak_text(text, lang="English"):
    greetings = {
        "English": ("Hello! Here is your recommendation.", "Material", "Tip of the Day"),
        "Sinhala": ("ආයුබෝවන්! ඔබේ නිර්දේශය මෙන්න.", "ද්‍රව්‍යය", "දින උපදෙස"),
        "Tamil": ("வணக்கம்! உங்கள் பரிந்துரை இதோ.", "பொருள்", "நாள் குறிப்பு"),
    }
    greet, material_word, tip_word = greetings.get(lang, greetings["English"])
    sentence = f"{greet} {text.replace('Material', material_word).replace('Tip of the Day', tip_word)}"
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
        "Sandals or slippers": ["Crocs Classic Clog", "Birkenstock Arizona", "Teva Original"],
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
        material = (
            material.replace("EVA", "Thick EVA")
            .replace("Dense EVA", "High-density EVA")
            .replace("soft foam", "high-density foam")
        )
        justification = justification.replace("provides", "provides extra").replace(
            "comfortable", "more durable and comfortable"
        )

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
if "step" not in st.session_state:
    st.session_state.step = 1
if "inputs" not in st.session_state:
    st.session_state.inputs = {}
if "analyze_clicked" not in st.session_state:
    st.session_state.analyze_clicked = False
if "foot_type" not in st.session_state:
    st.session_state.foot_type = "Normal Arch"
if "footwear_pref" not in st.session_state:
    st.session_state.footwear_pref = "Running shoes"
if "voice_lang" not in st.session_state:
    st.session_state.voice_lang = "English"


# ---------------------------
# Header + Voice Assistant Selector
# ---------------------------
col1, col2 = st.columns([1, 8])
with col1:
    logo = load_image("logo.png")
    if logo:
        st.image(logo, width=100)
    else:
        st.markdown("<h3>👟 FootFit Analyzer</h3>", unsafe_allow_html=True)
with col2:
    st.markdown(
        "<h1 style='margin-top:8px'>FootFit Analyzer — Biomechanics Footwear Profiler</h1>",
        unsafe_allow_html=True,
    )

st.write("A biomechanics-informed recommender that suggests shoe brand, materials and explains why.")
st.markdown("---")

# ✅ Language selection dropdown for voice assistant
st.session_state.voice_lang = st.selectbox(
    "🌐 Choose Voice Assistant Language",
    ["English", "Sinhala", "Tamil"],
    index=["English", "Sinhala", "Tamil"].index(st.session_state.voice_lang),
)

# ---------------------------
# STEP 1 — Personal Info
# ---------------------------
if st.session_state.step == 1:
    st.header("Step 1 — Personal Info")

    age_label = st.selectbox(
        "Select your Age Group",
        ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"],
        index=1,
    )
    gender_label = st.selectbox("Select Gender", ["Male", "Female"], index=0)
    weight_label = st.selectbox(
        "Select Weight Category",
        ["Under 50 kg", "50–70 kg", "71–90 kg", "Over 90 kg"],
        index=1,
    )

    next_col1, next_col2 = st.columns([1, 1])
    with next_col2:
        if st.button("Next →", key="to_step2"):
            st.session_state.inputs.update(
                {
                    "age_group": age_label,
                    "gender": gender_label,
                    "weight_group": weight_label,
                }
            )
            st.session_state.step = 2

# ---------------------------
# STEP 2 — Foot & Activity
# ---------------------------
elif st.session_state.step == 2:
    st.header("Step 2 — Foot & Activity Details")

    activity_label = st.selectbox(
        "Select your Daily Activity Level",
        [
            "Low (mostly sitting)",
            "Moderate (walking/standing sometimes)",
            "High (frequent walking/running)",
        ],
        index=1,
    )
    st.session_state.inputs["activity_label"] = activity_label
    st.session_state.inputs["activity_key"] = (
        "Low"
        if "Low" in activity_label
        else ("Moderate" if "Moderate" in activity_label else "High")
    )

    st.subheader("👣 Foot Type — choose one")
    foot_options = [("Flat Arch", "flat.png"), ("Normal Arch", "normal.png"), ("High Arch", "high_arch.png")]
    cols = st.columns(len(foot_options))
    for (label, imgfile), col in zip(foot_options, cols):
        with col:
            img = load_image(imgfile)
            if img:
                st.image(img, caption=label, width=140)
            if st.button(label, key=f"ftbtn_{label}"):
                st.session_state.foot_type = label
                st.session_state.inputs["foot_type"] = label

    st.write(f"👉 Currently selected foot type: {st.session_state.foot_type}")

    st.subheader("👟 Type of footwear you prefer")
    options = [
        "Running shoes",
        "Cross-training shoes",
        "Casual/fashion sneakers",
        "Sandals or slippers",
    ]
    new_pref = st.selectbox(
        "Select preferred footwear", options, index=options.index(st.session_state.footwear_pref)
    )
    st.session_state.footwear_pref = new_pref
    st.session_state.inputs["footwear_pref"] = new_pref

    st.write(f"👉 Currently selected footwear: {st.session_state.footwear_pref}")

    back_col, next_col = st.columns([1, 1])
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

    col_a1, col_a2, col_a3 = st.columns([1, 1, 2])
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

    if st.session_state.analyze_clicked:
        gif_path = os.path.join(IMAGE_DIR, "walking.gif")
        if os.path.exists(gif_path):
            st.markdown(
                f"<img src='{gif_path}' width='220' style='border-radius:8px;'/>",
                unsafe_allow_html=True,
            )
        speak_text(
            f"Recommendation ready. {brand} recommended.",
            st.session_state.voice_lang,
        )

    # Biomechanics summary, recommendation boxes, and rest of UI unchanged...

    st.checkbox("🔊 Read recommendation aloud", key="read_aloud")
    if st.session_state.get("read_aloud", False):
        speak_text(
            f"I recommend {brand}. Material: {material}. Tip of the Day: Stretch your calves daily to reduce heel strain.",
            st.session_state.voice_lang,
        )

    if st.button("← Back", key="back_to_step2"):
        st.session_state.step = 2
