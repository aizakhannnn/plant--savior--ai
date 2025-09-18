# streamlit_app.py

import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import Image
import time

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Plant Savior AI - Instant Plant Disease Detection",
    page_icon="🌱",
    layout="wide"
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background-color: #f8f9f9;
    color: #2E2E2E;
}

/* Headings */
h1 {
    font-size: 32px !important;
    font-weight: 700 !important;
    color: #2E8B57;
}
h2 {
    font-size: 24px !important;
    font-weight: 600 !important;
    color: #2E8B57;
}
p, li {
    font-size: 16px !important;
    line-height: 1.6;
}

/* Hero Section */
.hero {
    background: linear-gradient(rgba(46, 139, 87, 0.85), rgba(46, 139, 87, 0.85)), 
                url('https://images.unsplash.com/photo-1501004318641-b39e6451bec6') center/cover;
    color: white;
    text-align: center;
    padding: 4rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
}
.hero h1 {
    color: white;
    font-size: 40px !important;
}
.hero p {
    font-size: 18px;
    margin-top: 1rem;
}

/* CTA Button */
.stButton>button {
    background-color: #FF6B35;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 0.8rem 1.5rem;
    font-size: 16px;
    transition: 0.3s ease;
}
.stButton>button:hover {
    background-color: #e85a27;
    transform: translateY(-2px);
}

/* Step Cards */
.step-container {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    margin: 2rem 0;
}
.step-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 2rem;
    flex: 1;
    margin: 0.5rem;
    min-width: 250px;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
    transition: 0.3s ease;
}
.step-card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 6px 20px rgba(0,0,0,0.1);
}
.step-number {
    font-size: 24px;
    font-weight: 700;
    color: #2E8B57;
    margin-bottom: 0.5rem;
}

/* Upload Box */
.upload-box {
    border: 2px dashed #2E8B57;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    background: #ffffff;
    transition: 0.3s ease;
}
.upload-box:hover {
    background: #f1fdf4;
    border-color: #FF6B35;
}

/* Results Section */
.results-box {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Confidence Bar */
.conf-bar {
    height: 20px;
    background: #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
    margin: 1rem 0;
}
.conf-fill {
    height: 100%;
    background: #2E8B57;
    text-align: center;
    color: white;
    font-size: 14px;
    line-height: 20px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ----------------- HERO SECTION -----------------
st.markdown("""
<div class="hero">
    <h1>🌱 Plant Savior AI</h1>
    <p>Instant Plant Disease Detection using AI</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### How It Works")
st.markdown("""
<div class="step-container">
    <div class="step-card">
        <div class="step-number">1</div>
        <p><b>Upload Image</b><br>Choose or drag a plant leaf photo</p>
    </div>
    <div class="step-card">
        <div class="step-number">2</div>
        <p><b>AI Analysis</b><br>Our model analyzes the image</p>
    </div>
    <div class="step-card">
        <div class="step-number">3</div>
        <p><b>Get Results</b><br>Diagnosis & treatment instantly</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- FILE UPLOAD -----------------
st.markdown("### Upload a Plant Leaf Image")
uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"], label_visibility="collapsed")

if uploaded_file is not None:
    # Preview
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Image"):
        with st.spinner("Analyzing image..."):
            time.sleep(2)  # simulate loading

            # Dummy results (replace with model prediction)
            disease_name = "Powdery Mildew"
            confidence = 87
            recommendations = [
                "Remove and destroy infected leaves.",
                "Improve air circulation around plants.",
                "Apply fungicidal sprays if necessary."
            ]

        # ----------------- RESULTS -----------------
        st.markdown("### Results")
        st.markdown(f"<div class='results-box'><h2>{disease_name}</h2>", unsafe_allow_html=True)

        # Confidence bar
        st.markdown(f"""
        <div class="conf-bar">
            <div class="conf-fill" style="width:{confidence}%">{confidence}%</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("**Recommended Treatment:**")
        for rec in recommendations:
            st.write(f"- {rec}")
        st.markdown("</div>", unsafe_allow_html=True)
