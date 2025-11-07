# app.py — clean, working FootFit Analyzer with browser TTS and requested styling
import streamlit as st
import os
from PIL import Image
import random
import textwrap

st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")
IMAGE_DIR = "images"

# ---------- Helpers ----------
def load_image(name):
    p = os.path.join(IMAGE_DIR, name)
    return Image.open(p) if os.path.exists(p) else None

def speak_text_js(text):
    # Browser TTS via JS — works in Streamlit and on hosted apps
    safe = text.replace('"', '\\"').replace("\n", " ")
    js = f"""
    <script>
    const msg = new SpeechSynthesisUtterance("{safe}");
    msg.lang = 'en-US';
    msg.rate = 1.0;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js, height=0)

# --- recommender (unchanged semantics from your working version) ---
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

def tip_of_day():
    tips = [
        "Stretch your calves daily to reduce heel strain.",
        "Replace your shoes every 500–800 km.",
        "Use orthotic insoles if you experience arch pain.",
        "Air-dry shoes after workouts to prevent odor and damage.",
        "Perform ankle rotations to strengthen stabilizers."
    ]
    return random.choice(tips)

# ---------- CSS & Styling ----------
# Step 1 & 2: white background + bold black text for headings/options
# Step 3: colors will be set in-step; here ensure Step 3 text becomes bold but not forced black
st.markdown(
    """
    <style>
    /* Base white background */
    .stApp { background-color: white; }

    /* Headings and labels - bold black for Step 1 & 2 (we will scope by container classes) */
    .step-heading { color: #000000; font-weight: 800; }

    /* Make radio labels look more like option boxes */
    div[data-testid="stHorizontalBlock"] > div > label {
        background-color: #ffffff;
        color: #000000;
        font-weight: 800;
        padding: 8px 12px;
        border-radius: 10px;
        border: 2px solid #000000;
        margin-right: 8px;
    }
    /* When selected, Streamlit adds attribute data-baseweb="true" differently across versions;
       we cannot universally style internal selected state reliably, so we rely on bold & border. */

    /* Step 3: text bold but color will be controlled inline in the step 3 block */
    .step3-text { font-weight: 800; }

    /* Small responsive tweaks */
    .footer-note { text-align:center; color:#555; font-weight:700; margin-top:12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state ----------
if "step" not in st.session_state: st.session_state.step = 1
if "inputs" not in st.session_state: st.session_state.inputs = {}
if "analyze_clicked" not in st.session_state: st.session_state.analyze_clicked = False

# persist individual keys used by UI
if "foot_type" not in st.session_state:
    st.session_state.foot_type = st.session_state.inputs.get("foot_type", "Normal Arch")
if "footwear_pref" not in st.session_state:
    st.session_state.footwear_pref = st.session_state.inputs.get("footwear_pref", "Running shoes")

# ---------- Header ----------
col_logo, col_title = st.columns([1, 8])
with col_logo:
    logo = load_image("logo.png")
    if logo:
        st.image(logo, width=100)
    else:
        st.write("")  # keep column
with col_title:
    st.markdown("<div class='step-heading'><h1 style='margin-top:6px'>👟 FootFit Analyzer — Biomechanics Footwear Profiler</h1></div>", unsafe_allow_html=True)
st.write("A biomechanics-informed recommender that suggests **shoe brand**, **materials** and explains *why*.")
st.markdown("---")

# ---------- STEP 1 ----------
if st.session_state.step == 1:
    st.markdown("<div class='step-heading'><h2>Step 1 — Personal Info</h2></div>", unsafe_allow_html=True)

    # Option-box style radios for Age, Gender, Weight
    age = st.radio("Age group", ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"], horizontal=True, key="age_radio")
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True, key="gender_radio")
    weight = st.radio("Weight group", ["Under 50 kg", "50–70 kg", "71–90 kg", "Over 90 kg"], horizontal=True, key="weight_radio")

    st.caption("")  # spacing

    cols = st.columns([1,1])
    with cols[1]:
        if st.button("Next →", key="to_step2"):
            st.session_state.inputs.update({
                "age_group": age,
                "gender": gender,
                "weight_group": weight
            })
            st.session_state.step = 2

# ---------- STEP 2 ----------
elif st.session_state.step == 2:
    st.markdown("<div class='step-heading'><h2>Step 2 — Foot & Activity Details</h2></div>", unsafe_allow_html=True)

    activity = st.radio("Daily activity level", ["Low (mostly sitting)", "Moderate (walking/standing sometimes)", "High (frequent walking/running)"], horizontal=True, key="activity_radio")
    # keep a short key for activity (used by theme)
    if "Low" in activity:
        activity_key = "Low"
    elif "Moderate" in activity:
        activity_key = "Moderate"
    else:
        activity_key = "High"

    # Foot type images + buttons — use radio for consistency and visibility
    st.write("👣 Foot Type")
    foot_type = st.radio("", ["Flat Arch", "Normal Arch", "High Arch"], horizontal=True, key="foot_radio")
    st.session_state.foot_type = foot_type

    # Footwear preferences as option boxes
    st.write("👟 Type of footwear you prefer")
    footwear_pref = st.radio("", ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"], horizontal=True, key="footwear_radio")
    st.session_state.footwear_pref = footwear_pref

    cols = st.columns([1,1])
    with cols[0]:
        if st.button("← Back", key="back_to_step1"):
            st.session_state.step = 1
    with cols[1]:
        if st.button("Next →", key="to_step3"):
            # persist inputs
            st.session_state.inputs["activity_label"] = activity
            st.session_state.inputs["activity_key"] = activity_key
            st.session_state.inputs["foot_type"] = st.session_state.foot_type
            st.session_state.inputs["footwear_pref"] = st.session_state.footwear_pref
            # ensure age/gender/weight kept if user navigated strangely
            st.session_state.inputs["age_group"] = st.session_state.inputs.get("age_group", st.session_state.get("age_radio", "18–25"))
            st.session_state.inputs["gender"] = st.session_state.inputs.get("gender", st.session_state.get("gender_radio", "Male"))
            st.session_state.inputs["weight_group"] = st.session_state.inputs.get("weight_group", st.session_state.get("weight_radio", "50–70 kg"))
            st.session_state.step = 3

# ---------- STEP 3 (UNCHANGED LOGIC) ----------
elif st.session_state.step == 3:
    # Get values (robust)
    def get_val(k, default):
        return st.session_state.inputs.get(k, st.session_state.get(k, default))

    age_group = get_val("age_group", "18–25")
    gender = get_val("gender", "Male")
    weight_group = get_val("weight_group", "50–70 kg")
    activity_label = get_val("activity_label", "Moderate (walking/standing sometimes)")
    activity_key = get_val("activity_key", "Moderate")
    foot_type = get_val("foot_type", "Normal Arch")
    footwear_pref = get_val("footwear_pref", "Running shoes")

    # apply theme (this is your Step 3 color logic — left functionally unchanged)
    if activity_key == "Low":
        theme_color = "#d8ecff"; accent = "#3478b6"
    elif activity_key == "Moderate":
        theme_color = "#e8f9e9"; accent = "#2e8b57"
    else:
        theme_color = "#ffe9d6"; accent = "#e55300"

    # set background color for Step 3 only and make text bold but not black
    st.markdown(f"""
        <style>
        .stApp {{ background: {theme_color}; }}
        .step3-text, .step3-text * {{ font-weight: 800 !important; color: inherit !important; }}
        </style>
    """, unsafe_allow_html=True)

    st.header("Step 3 — Recommendation & Biomechanics Summary")

    # Analyze button and Start Over
    cols = st.columns([1,1,2])
    with cols[0]:
        if st.button("Analyze", key="analyze_btn"):
            st.session_state.analyze_clicked = True
    with cols[2]:
        if st.button("🔁 Start Over", key="start_over"):
            st.session_state.step = 1
            st.session_state.inputs = {}
            st.session_state.foot_type = "Normal Arch"
            st.session_state.footwear_pref = "Running shoes"
            st.session_state.analyze_clicked = False

    # Compute recommendation (your exact logic)
    brand, material, justification = recommend(foot_type, weight_group, activity_label, footwear_pref, age_group, gender)

    # Animated gif on analyze (if available)
    if st.session_state.analyze_clicked:
        gif_path = os.path.join(IMAGE_DIR, "walking.gif")
        if os.path.exists(gif_path):
            st.markdown(f"<img src='{gif_path}' width='220' style='border-radius:8px;'/>", unsafe_allow_html=True)
        # speak concise result using browser TTS
        speak_text_js(f"Recommendation ready. {brand} recommended. {material}.")

    # Biomechanics summary card (left intact)
    summary_md = f"""
    <div style='background:white; padding:14px; border-radius:10px;'>
      <h3 class='step3-text'>🧠 Biomechanics Summary</h3>
      <p class='step3-text'>
        👤 <b>Age:</b> {age_group} &nbsp; &nbsp; 🚻 <b>Gender:</b> {gender} <br/>
        ⚖️ <b>Weight:</b> {weight_group} &nbsp; 🏃 <b>Activity:</b> {activity_label} <br/>
        🦶 <b>Foot Type:</b> {foot_type} &nbsp; 👟 <b>Preference:</b> {footwear_pref}
      </p>
    </div>
    """
    st.markdown(summary_md, unsafe_allow_html=True)

    st.markdown("---")
    left, right = st.columns([2,1])
    with left:
        st.success(f"👟 **Recommended Shoe:** {brand}")
        st.info(f"🧵 **Material:** {material}")
        st.write(f"💬 {justification}")

        st.markdown(f"💡 **Tip of the Day:** *{tip_of_day()}*")

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

    with right:
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

    # Read aloud checkbox (keeps previous behavior)
    if st.checkbox("🔊 Read recommendation aloud", key="read_aloud"):
        speak_text_js(f"I recommend {brand}. Material: {material}. {justification}")

    if st.button("← Back", key="back_to_step2"):
        st.session_state.step = 2

    # DEBUG (remove for production)
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







