# app.py (fixed persistence for foot type & footwear preference)
import streamlit as st
import os
from PIL import Image
import random
import textwrap

st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")
IMAGE_DIR = "images"

# ---------- Helpers ----------
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

    if weight_group == "Over 90 kg":
        material = material.replace("EVA", "Thick EVA").replace("Dense EVA", "High-density EVA").replace("soft foam", "high-density foam")
        justification = justification.replace("provides", "provides extra").replace("comfortable", "more durable and comfortable")

    if "High" in activity:
        material += " **+ Breathable knit upper**"
        justification = justification[:-1] + " Ideal for frequent activity.*"
    elif "Low" in activity:
        material += " **+ Soft rubber outsole for comfort**"
        justification = justification[:-1] + " Better for low-activity comfort.*"

    if gender == "Female":
        justification = "Designed for narrower heels and a more contoured fit. " + justification
    if "Under 18" in age_group:
        brand = brand + " (Youth Edition)"

    return brand, material, justification

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
    .shoe-wall img {{ max-width:120px; margin:6px; border-radius:8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    .foot-type-selected {{ border: 3px solid {accent}; border-radius:8px; padding:4px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------- Session init ----------
if 'step' not in st.session_state: st.session_state.step = 1
if 'inputs' not in st.session_state: st.session_state.inputs = {}
if 'analyze_clicked' not in st.session_state: st.session_state.analyze_clicked = False

# Initialize persistent controls (safe defaults)
if 'foot_type' not in st.session_state: st.session_state.foot_type = st.session_state.inputs.get("foot_type", "Normal Arch")
if 'footwear_pref' not in st.session_state: st.session_state.footwear_pref = st.session_state.inputs.get("footwear_pref", "Running shoes")

# ---------- Header ----------
col1, col2 = st.columns([1, 8])
with col1:
    logo = load_image("logo.png")
    if logo: st.image(logo, width=110)
    else: st.markdown("<h3>👟 FootFit Analyzer</h3>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 style='margin-top:8px'>FootFit Analyzer — Biomechanics Footwear Profiler</h1>", unsafe_allow_html=True)
st.write("A biomechanics-informed recommender that suggests **shoe brand**, **materials** and explains *why*.")
st.markdown("---")

# ---------- STEP 1 ----------
if st.session_state.step == 1:
    st.header("Step 1 — Personal Info")
    st.write("Use sliders for a modern interactive feel.")

    age_i = st.slider("Age group", min_value=0, max_value=5, value=1, format="%d", key="age_i")
    age_label = map_age_index(age_i)
    st.caption(f"Selected age group: **{age_label}**")

    gender_i = st.slider("Gender (0 = Male, 1 = Female)", min_value=0, max_value=1, value=0, step=1, key="gender_i")
    gender_label = map_gender_index(gender_i)
    st.caption(f"Selected gender: **{gender_label}**")

    weight_val = st.slider("Weight (kg)", min_value=30, max_value=120, value=68, step=1, key="weight_val")
    weight_label = map_weight_val(weight_val)
    st.caption(f"Weight category: **{weight_label}**")

    next_col1, next_col2 = st.columns([1,1])
    with next_col2:
        if st.button("Next →", key="to_step2"):
            st.session_state.inputs.update({
                "age_group": age_label,
                "gender": gender_label,
                "weight_val": weight_val,
                "weight_group": weight_label
            })
            st.session_state.step = 2
            st.experimental_rerun()

# ---------- STEP 2 (FIXED) ----------
# ---------- STEP 2 (FINAL FIXED) ----------
elif st.session_state.step == 2:
    st.header("Step 2 — Foot & Activity Details")

    # Activity
    activity_i = st.slider("Daily activity level (0=Low,1=Moderate,2=High)", 0, 2, 1, step=1)
    activity_label = map_activity_index(activity_i)
    st.caption(f"Selected: **{activity_label}**")

    # Foot type
    st.subheader("👣 Foot Type — choose one")
    foot_options = {
        "Flat Arch": "flat.png",
        "Normal Arch": "normal.png",
        "High Arch": "high_arch.png"
    }

    # Initialize stored value if missing
    if "foot_type" not in st.session_state:
        st.session_state.foot_type = "Normal Arch"

    cols = st.columns(len(foot_options))
    for (label, img_file), col in zip(foot_options.items(), cols):
        with col:
            img = load_image(img_file)
            if img:
                st.image(img, caption=label, width=140)
            selected = st.session_state.foot_type == label
            if st.button(f"{'✅ ' if selected else ''}{label}", key=f"ft_{label}"):
                st.session_state.foot_type = label

    st.write(f"👉 Currently selected foot type: **{st.session_state.foot_type}**")

    # Footwear preference (selectbox with direct session binding)
    st.subheader("👟 Type of footwear you prefer")
    options = ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"]

    if "footwear_pref" not in st.session_state:
        st.session_state.footwear_pref = "Running shoes"

    st.session_state.footwear_pref = st.selectbox(
        "Select your preferred footwear type",
        options,
        index=options.index(st.session_state.footwear_pref)
        if st.session_state.footwear_pref in options else 0,
        key="footwear_pref"
    )

    st.write(f"👉 Currently selected footwear: **{st.session_state.footwear_pref}**")

    # Navigation
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 1
    with col2:
        if st.button("Next →"):
            st.session_state.inputs.update({
                "activity_label": activity_label,
                "activity_key": "Low" if "Low" in activity_label else ("Moderate" if "Moderate" in activity_label else "High"),
                "foot_type": st.session_state.foot_type,
                "footwear_pref": st.session_state.footwear_pref
            })
            st.session_state.step = 3


# ---------- STEP 3 ----------
elif st.session_state.step == 3:
    st.header("Step 3 — Recommendation & Biomechanics Summary")

    set_activity_theme = lambda k: None  # no-op if you don't need theme here
    set_activity_theme(st.session_state.inputs.get("activity_key", "Moderate"))

    age_group = st.session_state.inputs.get("age_group", "18–25")
    gender = st.session_state.inputs.get("gender", "Male")
    weight_group = st.session_state.inputs.get("weight_group", "50–70 kg")
    activity_label = st.session_state.inputs.get("activity_label", "Moderate (walking/standing sometimes)")
    foot_type = st.session_state.inputs.get("foot_type", "Normal Arch")
    footwear_pref = st.session_state.inputs.get("footwear_pref", "Running shoes")

    analyze_col1, analyze_col2, analyze_col3 = st.columns([1,1,2])
    with analyze_col1:
        if st.button("Analyze", key="analyze_btn"):
            st.session_state.analyze_clicked = True

    with analyze_col3:
        if st.button("🔁 Start Over", key="start_over"):
            st.session_state.step = 1
            st.session_state.inputs = {}
            st.session_state.foot_type = "Normal Arch"
            st.session_state.footwear_pref = "Running shoes"
            st.session_state.analyze_clicked = False
            st.experimental_rerun()

    brand, material, justification = recommend(foot_type, weight_group, activity_label, footwear_pref, age_group, gender)

    if st.session_state.analyze_clicked:
        gif_path = os.path.join(IMAGE_DIR, "walking.gif")
        if os.path.exists(gif_path):
            st.markdown(f"<img src='{gif_path}' width='220' style='border-radius:8px;'/>", unsafe_allow_html=True)
        speak_text(f"Recommendation ready. {brand} recommended.")

    # Summary card
    summary_md = f"""
    <div class="summary-card">
      <h3>🧠 Biomechanics Summary</h3>
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
        st.experimental_rerun()





