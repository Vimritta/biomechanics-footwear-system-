# app.py — reliable persistence + recommender fix
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
    # simple TTS via browser (works in Streamlit)
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
    if w < 50: return "Under 50 kg"
    if w < 71: return "50–70 kg"
    if w < 91: return "71–90 kg"
    return "Over 90 kg"

def map_activity_index(i):
    labels = ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (frequent walking/running)"]
    return labels[int(i)]

def map_gender_index(i):
    return ["Male", "Female"][int(i)]

# Recommender logic
def recommend(foot_type, weight_group, activity, footwear_pref, age_group, gender):
    brands = {
        "Running shoes": ["Nike Air Zoom", "ASICS Gel-Nimbus", "Adidas Ultraboost"],
        "Cross-training shoes": ["Nike Metcon", "Reebok Nano", "Under Armour TriBase"],
        "Casual/fashion sneakers": ["New Balance 574", "Vans Old Skool", "Converse Chuck Taylor"],
        "Sandals or slippers": ["Crocs Classic Clog", "Birkenstock Arizona", "Teva Original"]
    }
    brand = random.choice(brands.get(footwear_pref, ["Generic FootFit Shoe"]))

    # Material & justification
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
    else:
        material = "**Soft EVA footbed + contoured cork or foam support**"
        justification = "*Justification: Soft footbed for comfort and a contoured profile to support arches during light activity.*"

    # Weight
    if weight_group == "Over 90 kg":
        material = material.replace("EVA", "Thick EVA").replace("Dense EVA", "High-density EVA").replace("soft foam", "high-density foam")
        justification = justification.replace("provides", "provides extra").replace("comfortable", "more durable and comfortable")

    # Activity adaptation
    if "High" in activity:
        material += " **+ Breathable knit upper**"
        justification = justification[:-1] + " Ideal for frequent activity.*"
    elif "Low" in activity:
        material += " **+ Soft rubber outsole for comfort**"
        justification = justification[:-1] + " Better for low-activity comfort.*"

    # Gender nuance
    if gender == "Female":
        justification = "Designed for narrower heels and a more contoured fit. " + justification

    # Age nuance
    if "Under 18" in age_group:
        brand = brand + " (Youth Edition)"

    return brand, material, justification

# ---------------------------
# UI theme (basic)
# ---------------------------
def set_activity_theme(activity_key):
    if activity_key == "Low":
        color = "#d8ecff"; accent = "#3478b6"
    elif activity_key == "Moderate":
        color = "#e8f9e9"; accent = "#2e8b57"
    else:
        color = "#ffe9d6"; accent = "#e55300"
    css = f"""
    <style>
    .stApp {{ background: {color}; }}
    .summary-card {{ background: white; border-radius: 10px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }}
    .highlight-box {{ border-left: 6px solid {accent}; padding:12px; border-radius:8px; background: rgba(255,255,255,0.6); }}
    .foot-type-selected {{ border: 3px solid {accent}; border-radius:8px; padding:4px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------------------------
# Session init
# ---------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'inputs' not in st.session_state:
    st.session_state.inputs = {}
if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False

# persistent individual keys (keep in session_state so UI binds to them)
if 'foot_type' not in st.session_state:
    st.session_state.foot_type = st.session_state.inputs.get("foot_type", "Normal Arch")
if 'footwear_pref' not in st.session_state:
    st.session_state.footwear_pref = st.session_state.inputs.get("footwear_pref", "Running shoes")

# ---------------------------
# Header / logo
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
st.write("A biomechanics-informed recommender that suggests **shoe brand**, **materials** and explains *why*.")
st.markdown("---")

# ---------------------------
# STEP 1: Personal info
# ---------------------------
if st.session_state.step == 1:
    st.header("Step 1 — Personal Info")
    st.write("Use sliders for a modern interactive feel.")

    age_i = st.slider("Age group", 0, 5, 1, key="age_i")
    age_label = map_age_index(age_i)
    st.caption(f"Selected age group: **{age_label}**")

    gender_i = st.slider("Gender (0 = Male, 1 = Female)", 0, 1, 0, key="gender_i")
    gender_label = map_gender_index(gender_i)
    st.caption(f"Selected gender: **{gender_label}**")

    weight_val = st.slider("Weight (kg)", 30, 120, 68, key="weight_val")
    weight_label = map_weight_val(weight_val)
    st.caption(f"Weight category: **{weight_label}**")

    next_col1, next_col2 = st.columns([1,1])
    with next_col2:
        if st.button("Next →", key="to_step2"):
            # always write into inputs at transition
            st.session_state.inputs.update({
                "age_group": age_label,
                "gender": gender_label,
                "weight_val": weight_val,
                "weight_group": weight_label
            })
            st.session_state.step = 2
            # do not use experimental_rerun here; next render will show step 2

# ---------------------------
# STEP 2: Foot & activity
# ---------------------------
elif st.session_state.step == 2:
    st.header("Step 2 — Foot & Activity Details")

    # Activity slider
    activity_i = st.slider("Daily activity level (0=Low,1=Moderate,2=High)", 0, 2, 1, key="activity_i")
    activity_label = map_activity_index(activity_i)
    st.caption(f"Selected: **{activity_label}**")
    # store activity live (so if user hits Next later it's there)
    st.session_state.inputs["activity_label"] = activity_label
    st.session_state.inputs["activity_key"] = "Low" if "Low" in activity_label else ("Moderate" if "Moderate" in activity_label else "High")

    # Foot type (images + buttons) — update st.session_state.foot_type
    st.subheader("👣 Foot Type — choose one")
    foot_options = [("Flat Arch","flat.png"), ("Normal Arch","normal.png"), ("High Arch","high_arch.png")]
    cols = st.columns(len(foot_options))
    for (label, imgfile), col in zip(foot_options, cols):
        with col:
            img = load_image(imgfile)
            selected = (st.session_state.foot_type == label)
            if img:
                if selected:
                    # visually mark selected
                    st.markdown(f"<div class='foot-type-selected'>{st.image(img, caption=label, width=140) or ''}</div>", unsafe_allow_html=True)
                else:
                    st.image(img, caption=label, width=140)
            else:
                st.write(label)

            # clicking a button sets session_state.foot_type
            if st.button(label, key=f"ftbtn_{label}"):
                st.session_state.foot_type = label
                # also reflect into inputs so Step3 always finds it
                st.session_state.inputs["foot_type"] = label

    # show current picked foot type
    st.write(f"👉 Currently selected foot type: **{st.session_state.foot_type}**")
    # ensure inputs has foot_type even if user didn't click the button (use default)
    st.session_state.inputs["foot_type"] = st.session_state.get("foot_type", st.session_state.inputs.get("foot_type", "Normal Arch"))

    # Footwear preference (selectbox) — bind to st.session_state.footwear_pref
    st.subheader("👟 Type of footwear you prefer")
    options = ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"]
    # ensure a sensible default
    if st.session_state.get("footwear_pref") is None:
        st.session_state.footwear_pref = st.session_state.inputs.get("footwear_pref", "Running shoes")
    # compute index safely
    try:
        idx = options.index(st.session_state.footwear_pref)
    except Exception:
        idx = 0
    # show selectbox and write the chosen value into session_state immediately
    new_pref = st.selectbox("Select your preferred footwear type", options, index=idx, key="footwear_select")
    st.session_state.footwear_pref = new_pref
    st.session_state.inputs["footwear_pref"] = new_pref

    st.write(f"👉 Currently selected footwear: **{st.session_state.footwear_pref}**")

    # Navigation
    back_col, next_col = st.columns([1,1])
    with back_col:
        if st.button("← Back", key="back_step1"):
            st.session_state.step = 1
    with next_col:
        if st.button("Next →", key="to_step3"):
            # ensure all inputs are present before leaving
            st.session_state.inputs["age_group"] = st.session_state.inputs.get("age_group", map_age_index(st.session_state.get("age_i",1)))
            st.session_state.inputs["gender"] = st.session_state.inputs.get("gender", map_gender_index(st.session_state.get("gender_i",0)))
            st.session_state.inputs["weight_val"] = st.session_state.inputs.get("weight_val", st.session_state.get("weight_val",68))
            st.session_state.inputs["weight_group"] = st.session_state.inputs.get("weight_group", map_weight_val(st.session_state.inputs.get("weight_val",68)))
            st.session_state.inputs["activity_label"] = st.session_state.inputs.get("activity_label", map_activity_index(st.session_state.get("activity_i",1)))
            st.session_state.inputs["activity_key"] = st.session_state.inputs.get("activity_key", "Moderate")
            st.session_state.inputs["foot_type"] = st.session_state.inputs.get("foot_type", st.session_state.get("foot_type", "Normal Arch"))
            st.session_state.inputs["footwear_pref"] = st.session_state.inputs.get("footwear_pref", st.session_state.get("footwear_pref", "Running shoes"))
            st.session_state.step = 3

# ---------------------------
# STEP 3: Recommendation
# ---------------------------
elif st.session_state.step == 3:
    st.header("Step 3 — Recommendation & Biomechanics Summary")

    # Get values robustly: prefer inputs dict, fallback to session_state individual keys, fallback defaults
    def get_val(key, default):
        return st.session_state.inputs.get(key, st.session_state.get(key, default))

    age_group = get_val("age_group", "18–25")
    gender = get_val("gender", "Male")
    weight_group = get_val("weight_group", "50–70 kg")
    activity_label = get_val("activity_label", "Moderate (walking/standing sometimes)")
    activity_key = get_val("activity_key", "Moderate")
    foot_type = get_val("foot_type", "Normal Arch")
    footwear_pref = get_val("footwear_pref", "Running shoes")

    # apply theme
    set_activity_theme(activity_key)

    # analyze / start over
    col_a1, col_a2, col_a3 = st.columns([1,1,2])
    with col_a1:
        if st.button("Analyze", key="analyze_btn"):
            st.session_state.analyze_clicked = True
    with col_a3:
        if st.button("🔁 Start Over", key="start_over"):
            # reset everything
            st.session_state.step = 1
            st.session_state.inputs = {}
            st.session_state.foot_type = "Normal Arch"
            st.session_state.footwear_pref = "Running shoes"
            st.session_state.analyze_clicked = False

    # compute recommendation using robust values
    brand, material, justification = recommend(foot_type, weight_group, activity_label, footwear_pref, age_group, gender)

    # animated gif if clicked
    if st.session_state.analyze_clicked:
        gif_path = os.path.join(IMAGE_DIR, "walking.gif")
        if os.path.exists(gif_path):
            st.markdown(f"<img src='{gif_path}' width='220' style='border-radius:8px;'/>", unsafe_allow_html=True)
        # speak concise result
        speak_text(f"Recommendation ready. {brand} recommended.")

    # summary card
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

    st.markdown("---")
    rec_col1, rec_col2 = st.columns([2,1])
    with rec_col1:
        st.success(f"👟 **Recommended Shoe:** {brand}")
        st.info(f"🧵 **Material:** {material}")
        st.write(f"💬 {justification}")

        tips = [
            "Stretch your calves daily to reduce heel strain.",
            "Replace running shoes every 500–800 km.",
            "Use orthotic insoles when experiencing arch pain.",
            "Air-dry shoes after workouts to prevent odor and damage.",
            "Perform ankle rotations to strengthen stabilizers."
        ]
        st.markdown(f"💡 **Tip of the Day:** *{random.choice(tips)}*")

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

    if st.checkbox("🔊 Read recommendation aloud", key="read_aloud"):
        speak_text(f"I recommend {brand}. Material: {material}. {justification}")

    if st.button("← Back", key="back_to_step2"):
        st.session_state.step = 2

    # ---- DEBUG (development only) ----
    st.markdown("---")
    st.caption("DEBUG — session_state values (for troubleshooting):")
    debug_vals = {
        "step": st.session_state.step,
        "inputs": st.session_state.inputs,
        "foot_type": st.session_state.get("foot_type"),
        "footwear_pref": st.session_state.get("footwear_pref"),
        "analyze_clicked": st.session_state.analyze_clicked
    }
    st.text(debug_vals)





