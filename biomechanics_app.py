# app.py
"""
FootFit Math Engine — Streamlit app (no datasets required)
A compact, self-contained biomechanics -> shoe recommendation engine.
Uses simple mathematical models to estimate arch index, pronation, pressure balance,
heel-to-toe drop needs, and recommended midsole stiffness & materials.

Run:
    pip install -r requirements.txt
    streamlit run app.py
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, radians

# ---------- App config ----------
st.set_page_config(page_title="FootFit Math Engine", layout="wide", page_icon="👟")

# ---------- Helper math & models ----------
def compute_bmi(weight_kg, height_cm):
    """Return BMI (kg/m^2)."""
    h_m = height_cm / 100.0
    if h_m <= 0:
        return None
    bmi = weight_kg / (h_m * h_m)
    return bmi

def arch_index_from_contact_ratio(heel_contact_pct, midfoot_contact_pct, forefoot_contact_pct):
    """
    Simple Arch Index proxy:
      arch_index = midfoot_contact / (heel + midfoot + forefoot)
    Values:
      low (<0.15) -> high arch
      normal (~0.15-0.28) -> normal arch
      high (>0.28) -> flat foot
    """
    total = heel_contact_pct + midfoot_contact_pct + forefoot_contact_pct
    if total <= 0:
        return 0.0
    ai = midfoot_contact_pct / total
    return ai

def pronation_angle_class(pronation_angle_deg):
    """
    Interpret subtalar/pronation angle (simple).
    Positive -> pronation (rolling in)
    Negative -> supination (rolling out)
    """
    a = pronation_angle_deg
    if a > 10:
        return "Overpronation"
    elif a > 4:
        return "Mild Pronation"
    elif a >= -4:
        return "Neutral"
    elif a >= -10:
        return "Mild Supination"
    else:
        return "Oversupination"

def heel_to_toe_drop_recommendation(ground_strike_location, activity_type):
    """
    Recommend heel-to-toe drop in mm based on strike and activity.
    ground_strike_location: 'Heel', 'Midfoot', 'Forefoot'
    activity_type: 'Walking', 'Running (short)', 'Running (long)', 'Training'
    """
    if ground_strike_location == "Heel":
        base = 10  # mm drop
    elif ground_strike_location == "Midfoot":
        base = 6
    else:  # Forefoot
        base = 0

    # activity tweak
    if activity_type == "Running (long)":
        base += 2
    elif activity_type == "Training":
        base += 4  # a little more heel for stability
    # clamp
    return int(max(0, min(14, base)))

def midsole_stiffness(arch_index, weight_kg, pronation_angle_deg):
    """
    Small rule to recommend midsole stiffness (Shore-A proxy / qualitative):
      returns one of: 'Soft', 'Medium', 'Firm', 'Very Firm'
    Heavier users and flat feet need firmer midsoles.
    Pronators may need firmer medial posting.
    """
    score = 0.0
    # arch influence: lower arch_index -> higher score -> firmer
    score += (0.30 - arch_index) * 10  # midfoot low -> positive
    # weight influence
    score += (weight_kg - 65) / 10.0
    # pronation influence
    if pronation_angle_deg > 8:
        score += 1.5
    elif pronation_angle_deg < -8:
        score -= 1.0

    # map to categories
    if score < -1.0:
        return "Soft"
    elif score < 2.5:
        return "Medium"
    elif score < 5.0:
        return "Firm"
    else:
        return "Very Firm"

def cushioning_level_by_bmi(bmi):
    """
    Suggest cushioning intensity from BMI:
      BMI < 22 -> Light
      22-27 -> Moderate
      >27 -> High
    """
    if bmi is None:
        return "Moderate"
    if bmi < 22:
        return "Light"
    elif bmi <= 27:
        return "Moderate"
    else:
        return "High"

def recommended_materials(midsole_stiff, cushioning_level, pronation_angle_deg):
    """
    Map the above to human-friendly material recommendations.
    """
    materials = []
    if midsole_stiff in ("Soft", "Medium"):
        materials.append("EVA foam (responsive, lightweight)")
    else:
        materials.append("High-density EVA or TPU plate (durable, firmer)")

    if cushioning_level == "High":
        materials.append("Layered responsive foam + additional heel foam")
    elif cushioning_level == "Light":
        materials.append("Low-profile PU/EVA for ground feel")
    else:
        materials.append("Balanced responsive foam")

    if pronation_angle_deg > 8:
        materials.append("Medial posting/arch support (denser medial foam)")
    elif pronation_angle_deg < -8:
        materials.append("Lateral support features or rocker sole")

    return materials

def symmetry_index(left_force, right_force):
    """
    Compute gait symmetry index (0 perfect, >0 increasing asymmetry).
    left_force, right_force are positive values (e.g., % or Newtons)
    SI = abs(L - R) / ((L + R)/2)
    """
    denom = (left_force + right_force) / 2.0
    if denom == 0:
        return 0.0
    return abs(left_force - right_force) / denom

# ---------- UI ----------
st.title("👟 FootFit — Mathematical Biomechanics Engine")
st.write("This web app uses small physics/math models (angles, contact ratios, BMI) to recommend shoe engineering parameters (drop, midsole stiffness, cushioning & materials). No dataset required.")

with st.expander("Quick notes — what this app models (human way):", expanded=True):
    st.markdown("""
    - We use **contact ratios** (heel/midfoot/forefoot) as a simple proxy for arch behavior.
    - **Pronation angle** (°) is interpreted as rolling-in (positive) or rolling-out (negative).
    - **Heel-to-toe drop** and **midsole stiffness** are engineering levers chosen to match mechanics and comfort.
    - This is educational / engineering-proxy level — not a clinical diagnosis.
    """)

# Left column for inputs
col1, col2 = st.columns([1,1])
with col1:
    st.header("Human inputs (measurements)")
    st.markdown("Provide simple biomechanical measurements — sliders use reasonable ranges.")
    weight_kg = st.slider("Weight (kg)", 30, 140, 68)
    height_cm = st.slider("Height (cm)", 120, 220, 170)
    age = st.slider("Age (years)", 8, 90, 30)

    st.markdown("---")
    st.subheader("Contact ratios (estimate % of plantar contact)")
    st.markdown("These three should sum roughly to 100 — they are a quick proxy for plantar pressure distribution.")
    heel_pct = st.slider("Heel contact (%)", 0, 100, 40)
    midfoot_pct = st.slider("Midfoot contact (%)", 0, 100, 20)
    forefoot_pct = st.slider("Forefoot contact (%)", 0, 100, 40)

    st.markdown("---")
    st.subheader("Gait & angle")
    pronation_deg = st.slider("Pronation / supination angle (°) — positive = pronation", -20, 30, 6)
    strike_location = st.selectbox("Ground strike location", ["Heel", "Midfoot", "Forefoot"])
    activity_type = st.selectbox("Primary activity", ["Walking", "Running (short)", "Running (long)", "Training"])

with col2:
    st.header("Engineering interpretation")
    st.markdown("These are derived values from your inputs.")
    bmi = compute_bmi(weight_kg, height_cm)
    st.metric("BMI", f"{bmi:.1f}" if bmi else "—")

    ai = arch_index_from_contact_ratio(heel_pct, midfoot_pct, forefoot_pct)
    if ai < 0.15:
        arch_type = "High Arch (cavus)"
    elif ai <= 0.28:
        arch_type = "Normal Arch"
    else:
        arch_type = "Flat Foot (pes planus)"
    st.metric("Arch Index (proxy)", f"{ai:.2f}")
    st.write("Interpreted arch type:", f"**{arch_type}**")

    pronation_class = pronation_angle_class(pronation_deg)
    st.metric("Pronation status", f"{pronation_class} ({pronation_deg}°)")

    drop_mm = heel_to_toe_drop_recommendation(strike_location, activity_type)
    st.metric("Recommended heel-to-toe drop (mm)", f"{drop_mm} mm")

    stiffness = midsole_stiffness(ai, weight_kg, pronation_deg)
    st.metric("Recommended midsole stiffness", stiffness)

    cushion = cushioning_level_by_bmi(bmi)
    st.metric("Cushioning intensity", cushion)

    materials = recommended_materials(stiffness, cushion, pronation_deg)
    st.write("Suggested materials / construction features:")
    for m in materials:
        st.write("•", m)

# ---------- visualizations ----------
st.markdown("---")
st.header("Visuals — pressure distribution & angle model (human-friendly)")

# Pressure distribution pie
fig1, ax1 = plt.subplots(figsize=(4,4))
parts = [heel_pct, midfoot_pct, forefoot_pct]
labels = [f"Heel ({heel_pct}%)", f"Midfoot ({midfoot_pct}%)", f"Forefoot ({forefoot_pct}%)"]
# Use matplotlib default colors (do not set colors per tool instructions)
ax1.pie(parts, labels=labels, autopct='%1.0f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Simple angle / roll visualization (2D stick foot)
fig2, ax2 = plt.subplots(figsize=(6,3))
# draw foot baseline
x = np.linspace(0, 1, 100)
y = np.zeros_like(x)
ax2.plot(x, y, linewidth=2)
# draw a representation of the foot as line rotated by pronation angle about heel (x=0.1)
theta = radians(pronation_deg)
heel_x = 0.1
foot_len = 0.8
toe_x = heel_x + foot_len * cos(theta)
toe_y = foot_len * sin(theta)
ax2.plot([heel_x, toe_x], [0, toe_y], linewidth=6, solid_capstyle='round')
ax2.scatter([heel_x, toe_x], [0, toe_y], s=40)
ax2.set_xlim(0, 1.05)
ax2.set_ylim(-0.2, 0.4)
ax2.set_title(f"Foot roll visualization — pronation {pronation_deg}° ({pronation_class})")
ax2.axis('off')
st.pyplot(fig2)

# Symmetry indicator (ask user for simple left/right force)
st.markdown("---")
st.subheader("Gait symmetry (simple) — optional inputs")
left_force = st.number_input("Left leg peak force (arbitrary units)", min_value=0.0, value=100.0, step=1.0, format="%.1f")
right_force = st.number_input("Right leg peak force (arbitrary units)", min_value=0.0, value=98.0, step=1.0, format="%.1f")

si = symmetry_index(left_force, right_force)
si_pct = si * 100
st.write(f"Gait symmetry index: **{si:.3f}**  — approximate asymmetry **{si_pct:.1f}%**")
if si_pct < 5:
    st.success("Symmetry is good (<5%).")
elif si_pct < 12:
    st.info("Mild asymmetry (5–12%). Consider minor balancing strategies.")
else:
    st.warning("Marked asymmetry (>12%). Consider professional gait assessment if persistent.")

# ---------- final recommendation block ----------
st.markdown("---")
st.header("Final human-friendly recommendation")

# Compose a short readable summary
summary_lines = []
summary_lines.append(f"Age: {age} yrs | Weight: {weight_kg} kg | Height: {height_cm} cm | BMI: {bmi:.1f}")
summary_lines.append(f"Arch proxy (AI): {ai:.2f} — {arch_type}")
summary_lines.append(f"Pronation: {pronation_deg}° → {pronation_class}")
summary_lines.append(f"Recommended heel-to-toe drop: {drop_mm} mm")
summary_lines.append(f"Midsole stiffness recommendation: {stiffness}")
summary_lines.append(f"Cushioning intensity: {cushion}")
summary_lines.append("Material & construction highlights: " + "; ".join(materials))
summary_lines.append(f"Gait asymmetry: {si_pct:.1f}%")

for s in summary_lines:
    st.write("•", s)

st.info("Engineering notes: firmer midsoles distribute load for heavier / flat-foot users; medial posting helps overpronation. Lower drop suits forefoot strikers; higher drop eases heel-strike impact.")

st.markdown("---")
st.caption("This tool provides engineering-level heuristics for shoe design and personal selection. It is not a medical diagnostic.")
