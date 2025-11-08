# app.py — FootFit Analyzer (light pastel violet navigation + white dropdowns + pastel rec boxes)
import streamlit as st
import random
from PIL import Image
import textwrap

# ----------------
# Page configuration
st.set_page_config(page_title="FootFit Analyzer", page_icon="👟", layout="wide")

# ----------------
# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #F9F7FF;
    }
    .stSelectbox, .stTextInput {
        background-color: white !important;
        border-radius: 10px;
    }
    .title {
        font-size: 40px;
        font-weight: 700;
        color: #7A4EB2;
        text-align: center;
    }
    .recommender-title {
        font-size: 26px;
        font-weight: bold;
        color: #4A3D8A;
        margin-bottom: 8px;
    }
    .pink-button button {
        background-color: #FF6FB0 !important;
        color: white !important;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
    }
    .rec-box {
        background-color: #EDE6FF;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0px 4px 10px rgba(122, 78, 178, 0.2);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------
# Title
st.markdown("<h1 class='title'>👟 FootFit Analyzer</h1>", unsafe_allow_html=True)
st.write("### Discover the perfect footwear for your biomechanics!")

# ----------------
# Sidebar inputs
st.sidebar.header("🔍 Enter Your Details")
age = st.sidebar.selectbox("Age Range", ["Under 18", "18–25", "26–35", "36–50", "51–65", "Over 65"])
gender = st.sidebar.








