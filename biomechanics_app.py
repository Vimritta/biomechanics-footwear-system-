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
    css = """
    <style>
    .stApp { background-color: white; color: black; }
    .stMarkdown, .stText, .stSelectbox, .stRadio, label, div, p, h1, h2, h3, h4, h5, h6 { color: black !important; }
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
    if activity_key == "Low": color = "#d8ecff"; accent = "#3478b6"
    elif activity_key == "Moderate": color = "#e8f9e9"; accent = "#2e8b57"
    else: color = "#ffe9d6"; accent = "#e55300"
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
if 'step' not in st.session_state: st.session_state.step = 1
if 'inputs' not in st.session_state: st.session_state.inputs = {}
if 'analyze_clicked' not in st.session_state: st.session_state.analyze_clicked = False
if 'foot_type' not in st.session_state: st.session_state.foot_type = "Normal Arch"
if 'footwear_pref' not in st.session_state: st.session_state.footwear_pref = "Running shoes"
if 'greeting_done' not in st.session_state: st.session_state.greeting_done = False  # NEW

# ---------------------------
# Header
# ---------------------------
col1, col2 = st.columns([1, 8])
with col1:
    logo = load_image("logo.png")
    if logo: st.image(logo, width=100)
    else: st.markdown("<h3>👟 FootFit Analyzer</h3>", unsafe_allow_html=True)
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
            st.session_state.inputs.update({"age_group": age_label, "gender": gender_label, "weight_group": weight_label})
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
    st.session_state.inputs["activity_key"] = ("Low" if "Low" in activity_label else ("Moderate" if "Moderate" in activity_label else "High"))

    st.subheader("👣 Foot Type — choose one")
    foot_options = [("Flat Arch","flat.png"), ("Normal Arch","normal.png"), ("High Arch","high_arch.png")]
    cols = st.columns(len(foot_options))
    for (label, imgfile), col in zip(foot_options, cols):
        with col:
            img = load_image(imgfile)
            if img: st.image(img, caption=label, width=140)
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
        if st.button("← Back", key="back_step1"): st.session_state.step = 1
    with next_col:
        if st.button("Next →", key="to_step3"): st.session_state.step = 3
# ---------------------------
# STEP 3: Recommendations
# ---------------------------
elif step == "Step 3: Recommendations":
    st.markdown("### 🧠 Step 3: Personalized Footwear Recommendations")

    # ---------------------------
    # Unique Age + Gender Greeting
    # ---------------------------
    def get_unique_greeting(age_group, gender):
        if age_group == "Under 18":
            if gender == "Male":
                return "Hey young champ! Ready to rule the track today? 💪"
            elif gender == "Female":
                return "Hey superstar! Ready to shine with every step? 🌟"
            else:
                return "Hey there, rising star! Let’s get you moving! ✨"
        elif age_group == "18–25":
            if gender == "Male":
                return "Yo, trailblazer! Time to sprint towards style and comfort! 🏃‍♂️"
            elif gender == "Female":
                return "Hey energetic soul! Let’s find the kicks that match your vibe! 💃"
            else:
                return "Hey go-getter! Your perfect fit is waiting to keep you active! 🔥"
        elif age_group == "26–40":
            if gender == "Male":
                return "Hello, active pro! Let’s balance performance with comfort today. ⚡"
            elif gender == "Female":
                return "Hello, multitasking marvel! Comfort meets class in your next step. 👟"
            else:
                return "Hello there! Let’s discover your ideal shoe for work and play! ✨"
        elif age_group == "41–60":
            if gender == "Male":
                return "Good day, sir! Let’s find a shoe that moves as smart as you do. 👞"
            elif gender == "Female":
                return "Good day, ma’am! Let’s choose footwear that pampers your every step. 👠"
            else:
                return "Good day! Let’s blend comfort and confidence in each step you take. 💫"
        else:
            if gender == "Male":
                return "Welcome, wise walker! Let’s make each stride effortless and light. 👟"
            elif gender == "Female":
                return "Welcome, graceful walker! Let’s make every step a soft breeze. 🌸"
            else:
                return "Welcome! Let’s choose shoes that make walking feel like floating. ☁️"

    # Example inputs from previous steps (replace these variables accordingly)
    age_group = st.session_state.get("age_group", "18–25")
    gender = st.session_state.get("gender", "Male")

    greeting = get_unique_greeting(age_group, gender)
    st.markdown(f"<h3 style='color:#8B5CF6; font-weight:600;'>{greeting}</h3>", unsafe_allow_html=True)

    # Voice assistant plays greeting
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.say(greeting)
    engine.runAndWait()

    # Walking GIF display (based on your provided URL)
    st.markdown(
        f"<div style='text-align:center;'><img src='https://i.pinimg.com/originals/e8/ef/28/e8ef28560911f51810df9b0581819650.gif' width='240'></div>",
        unsafe_allow_html=True,
    )

    st.write("")

    # ---------------------------
    # Rest of Step 3 features (original from your perfect version)
    # ---------------------------

    # Biomechanics Summary Box
    st.markdown(
        "<div style='background-color:#EDE9FE;padding:15px;border-radius:12px;'><b>👣 Biomechanics Summary:</b><br>Age, Gender, Foot Type, Activity Level, and Weight all influence the ideal footwear for you.</div>",
        unsafe_allow_html=True,
    )

    st.write("")

    # Recommendation Box
    st.markdown(
        "<div style='background-color:#E0F2FE;padding:15px;border-radius:12px;'><b>👟 Shoe Recommender:</b><br>Based on your biomechanics, we suggest lightweight running shoes with arch support.</div>",
        unsafe_allow_html=True,
    )

    st.write("")

    # Material Box
    st.markdown(
        "<div style='background-color:#F0FDF4;padding:15px;border-radius:12px;'><b>🧵 Material Suggestion:</b><br>Breathable mesh upper with memory foam cushioning for flexibility and comfort.</div>",
        unsafe_allow_html=True,
    )

    st.write("")

    # Justification Box
    st.markdown(
        "<div style='background-color:#FEF3C7;padding:15px;border-radius:12px;'><b>📖 Justification:</b><br>This material helps maintain airflow and reduce fatigue during prolonged activity.</div>",
        unsafe_allow_html=True,
    )

    st.write("")

    # Tip of the Day Box
    st.markdown(
        "<div style='background-color:#FFF7ED;padding:15px;border-radius:12px;'><b>💡 Tip of the Day:</b><br>Always wear socks that match your activity type to prevent blisters and discomfort.</div>",
        unsafe_allow_html=True,
    )

    st.write("")

    # Virtual Shoe Wall
    st.markdown("### 🧱 Virtual Shoe Wall")
    st.image(
        [
            "https://cdn.pixabay.com/photo/2017/02/13/16/38/shoes-2060900_1280.jpg",
            "https://cdn.pixabay.com/photo/2016/11/21/16/30/shoes-1846124_1280.jpg",
            "https://cdn.pixabay.com/photo/2015/10/13/15/16/shoes-986295_1280.jpg",
        ],
        width=180,
    )

    st.write("")

    # Read Aloud Option (Orange Checkbox)
    read_aloud = st.checkbox("🔊 Read recommendation aloud")
    if read_aloud:
        engine.say("We recommend lightweight running shoes with breathable mesh material.")
        engine.runAndWait()

    # Download Option
    st.download_button(
        label="⬇️ Download Your Recommendation",
        data="Lightweight running shoes with arch support and breathable mesh material.",
        file_name="footwear_recommendation.txt",
        mime="text/plain",
        key="download_btn",
        use_container_width=True,
    )




