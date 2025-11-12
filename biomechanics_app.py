# app.py — FootFit Analyzer (light pastel violet + Sinhala/Tamil voice assistant)
import streamlit as st
import random
import base64

st.set_page_config(page_title="FootFit Analyzer", layout="wide", page_icon="👟")

# ---------------------------------------
# Helper & Initialization
# ---------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'voice_lang' not in st.session_state:
    st.session_state.voice_lang = "English"

# ---------------------------------------
# Header and Language Selection
# ---------------------------------------
st.markdown(
    "<h1 style='text-align: center; color: #6a5acd;'>👣 FootFit Analyzer</h1>",
    unsafe_allow_html=True,
)
st.write("")
col1, col2, col3 = st.columns(3)
with col2:
    st.session_state.voice_lang = st.selectbox(
        "🌐 Voice Assistant Language",
        ["English", "Sinhala", "Tamil"],
        index=["English", "Sinhala", "Tamil"].index(st.session_state.voice_lang),
    )

# ---------------------------------------
# Voice Assistant (Sinhala/Tamil/English)
# ---------------------------------------
def speak_text():
    lang = st.session_state.get("voice_lang", "English")

    if lang == "Sinhala":
        greeting = "ආයුබෝවන්! ඔබේ නිර්දේශය මෙන්න."
        material_label = "ද්‍රව්‍යය"
        tip_label = "දින උපදෙස"
    elif lang == "Tamil":
        greeting = "வணக்கம்! உங்கள் பரிந்துரை இதோ."
        material_label = "பொருள்"
        tip_label = "நாள் குறிப்பு"
    else:
        greeting = "Hello! Here is your recommendation."
        material_label = "Material"
        tip_label = "Tip of the Day"

    brand = st.session_state.get("rec_brand", "Brand Name")
    material = st.session_state.get("rec_material", "Material info")
    justification = st.session_state.get("rec_justification", "Justification text")
    tip_text = st.session_state.get("rec_tip", "")

    sentence = f"{greeting} {brand} recommended. {material_label}: {material}. {justification}"
    if tip_text:
        sentence += f" {tip_label}: {tip_text}"

    html = f"""
    <script>
    const msg = new SpeechSynthesisUtterance({repr(sentence)});
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(html, height=0)

# ---------------------------------------
# Recommendation Logic
# ---------------------------------------
def recommend(foot_type, weight, activity, footwear_pref, age, gender):
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
            justification = "Dual-density EVA supports the medial arch."
        elif foot_type == "High Arch":
            material = "EVA midsole + Responsive gel insert"
            justification = "Gel insert disperses high-pressure points."
        else:
            material = "Lightweight mesh + Balanced foam"
            justification = "Balanced cushioning suits neutral feet."
    elif footwear_pref == "Cross-training shoes":
        material = "Dense EVA + Reinforced upper"
        justification = "Provides lateral stability for multi-directional movements."
    elif footwear_pref == "Casual/fashion sneakers":
        material = "Soft foam midsole + Textile upper"
        justification = "Comfortable for daily wear."
    else:
        material = "Soft EVA footbed + Contoured support"
        justification = "Comfortable for light activity."

    tip_list = [
        "Stretch your calves daily.",
        "Replace running shoes every 500–800 km.",
        "Use orthotic insoles if needed.",
        "Air-dry shoes after workouts.",
        "Perform ankle rotations to strengthen stabilizers."
    ]
    tip_text = random.choice(tip_list)
    return brand, material, justification, tip_text

# ---------------------------------------
# STEP 1: Personal Info
# ---------------------------------------
if st.session_state.step == 1:
    st.markdown("### 🧍 Step 1: Personal Information")

    age = st.selectbox("Age Group", ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"])
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    weight = st.selectbox("Weight Category", ["Under 50 kg", "50–70 kg", "71–90 kg", "Over 90 kg"])

    if st.button("Next ➜"):
        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.weight = weight
        st.session_state.step = 2

# ---------------------------------------
# STEP 2: Foot Type & Activity
# ---------------------------------------
elif st.session_state.step == 2:
    st.markdown("### 🦶 Step 2: Foot Type & Activity Level")

    activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])
    foot_type = st.selectbox("Foot Type", ["Flat Arch", "Normal Arch", "High Arch"])
    footwear_pref = st.selectbox(
        "Type of Footwear You Prefer",
        ["Running shoes", "Cross-training shoes", "Casual/fashion sneakers", "Sandals or slippers"],
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            st.session_state.step = 1
    with col2:
        if st.button("Next ➜"):
            st.session_state.activity = activity
            st.session_state.foot_type = foot_type
            st.session_state.footwear_pref = footwear_pref
            st.session_state.step = 3

# ---------------------------------------
# STEP 3: Recommendation
# ---------------------------------------
elif st.session_state.step == 3:
    st.markdown("### 🎯 Step 3: Your Footwear Recommendation")

    brand, material, justification, tip_text = recommend(
        st.session_state.foot_type,
        st.session_state.weight,
        st.session_state.activity,
        st.session_state.footwear_pref,
        st.session_state.age,
        st.session_state.gender,
    )

    # Save for voice assistant
    st.session_state.rec_brand = brand
    st.session_state.rec_material = material
    st.session_state.rec_justification = justification
    st.session_state.rec_tip = tip_text

    # Display results
    st.markdown(f"<div style='background-color:#f4e7fe;padding:20px;border-radius:15px;'><h3>👟 {brand}</h3></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#fff8dc;padding:15px;border-radius:10px;margin-top:10px;'><b>🧵 Material:</b> {material}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#e8f8f5;padding:15px;border-radius:10px;margin-top:10px;'><b>💬 Justification:</b> {justification}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#fffacd;padding:15px;border-radius:10px;margin-top:10px;'><b>💡 Tip of the Day:</b> {tip_text}</div>", unsafe_allow_html=True)

    st.write("")
    if st.checkbox("🔊 Read recommendation aloud"):
        speak_text()

    # Download button (pink)
    summary_text = f"""
    👟 FootFit Recommendation

    Age: {st.session_state.age}
    Gender: {st.session_state.gender}
    Weight: {st.session_state.weight}
    Activity: {st.session_state.activity}
    Foot Type: {st.session_state.foot_type}
    Footwear Preference: {st.session_state.footwear_pref}

    Recommended Shoe: {brand}
    Material: {material}
    Justification: {justification}
    Tip: {tip_text}
    """
    b64 = base64.b64encode(summary_text.encode()).decode()
    st.markdown(
        f'<a href="data:text/plain;base64,{b64}" download="recommendation.txt" style="background-color:#ff69b4;color:white;padding:10px 15px;border-radius:10px;text-decoration:none;">📄 Download Recommendation</a>',
        unsafe_allow_html=True,
    )

    st.write("")
    if st.button("🔁 Start Over"):
        st.session_state.step = 1


