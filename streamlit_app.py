# streamlit_app.py

import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json
from PIL import Image
import os
import base64
from io import BytesIO
import time

# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI - Instant Plant Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load the model (assuming model_path is correct; keep as is)
@st.cache_resource
def load_model(model_path="path/to/your/model.h5"):  # Replace with actual path
    model = tf.keras.models.load_model(model_path)
    return model

model = load_model()

# Class names (assuming from model; keep as is)
class_names = ['Healthy', 'Disease1', 'Disease2']  # Replace with actual classes

# Nature-inspired CSS Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        line-height: 1.2;
    }
    
    /* Spacing Scale */
    .spacing-xs { margin: 4px; }
    .spacing-sm { margin: 8px; }
    .spacing-md { margin: 16px; }
    .spacing-lg { margin: 24px; }
    .spacing-xl { margin: 32px; }
    .spacing-xxl { margin: 48px; }
    
    /* Color Palette */
    :root {
        --primary-green: #2E8B57;
        --accent-orange: #FF6B35;
        --bg-white: #FFFFFF;
        --bg-light-gray: #F8F9FA;
        --text-dark: #2C3E50;
        --text-light: #7F8C8D;
    }
    
    /* Global Styles */
    .stApp {
        background-color: var(--bg-white);
        color: var(--text-dark);
    }
    
    /* Hero Section */
    .hero-section {
        background-image: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        height: 60vh;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white;
        position: relative;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(46, 139, 87, 0.7);
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 800px;
        padding: 0 1rem;
    }
    
    .hero-title {
        font-size: 3.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .hero-subtitle {
        font-size: 1.6rem;
        font-weight: 400;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    .cta-button {
        background: var(--accent-orange);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
    }
    
    .cta-button:hover {
        background: #E55A2B;
        transform: translateY(-2px);
    }
    
    /* Three-Step Process */
    .steps-section {
        padding: 4rem 2rem;
        background: var(--bg-light-gray);
        text-align: center;
    }
    
    .steps-title {
        font-size: 2.4rem;
        color: var(--primary-green);
        margin-bottom: 3rem;
    }
    
    .steps-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .step-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .step-icon {
        font-size: 3rem;
        color: var(--primary-green);
        margin-bottom: 1rem;
    }
    
    .step-number {
        background: var(--primary-green);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .step-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 0.5rem;
    }
    
    .step-desc {
        color: var(--text-light);
        font-size: 1rem;
    }
    
    /* Upload Section */
    .upload-section {
        padding: 4rem 2rem;
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
    }
    
    .upload-title {
        font-size: 2.4rem;
        color: var(--primary-green);
        margin-bottom: 2rem;
    }
    
    /* Drag and Drop Zone */
    .drop-zone {
        border: 2px dashed var(--primary-green);
        border-radius: 12px;
        padding: 3rem;
        margin: 2rem 0;
        cursor: pointer;
        transition: border-color 0.3s ease, background 0.3s ease;
        background: var(--bg-light-gray);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .drop-zone:hover, .drop-zone.dragover {
        border-color: var(--accent-orange);
        background: rgba(255, 107, 53, 0.05);
    }
    
    .upload-icon {
        font-size: 4rem;
        color: var(--primary-green);
        margin-bottom: 1rem;
    }
    
    .drop-text {
        font-size: 1.4rem;
        color: var(--text-dark);
        margin-bottom: 0.5rem;
    }
    
    .file-info {
        color: var(--text-light);
        font-size: 1rem;
    }
    
    /* Image Preview and Results */
    .analysis-section {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        padding: 2rem;
        max-width: 1200px;
        margin: 2rem auto;
    }
    
    @media (max-width: 768px) {
        .analysis-section {
            grid-template-columns: 1fr;
        }
    }
    
    .preview-container, .results-container {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .preview-title, .results-title {
        font-size: 1.8rem;
        color: var(--primary-green);
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .preview-image {
        width: 100%;
        max-height: 400px;
        object-fit: contain;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Confidence Gauge (Progress Bar) */
    .confidence-gauge {
        margin: 1.5rem 0;
    }
    
    .confidence-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .progress-bg {
        width: 100%;
        height: 20px;
        background: var(--bg-light-gray);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-green), var(--accent-orange));
        border-radius: 10px;
        transition: width 1s ease;
        box-shadow: 0 0 10px rgba(46, 139, 87, 0.3);
    }
    
    .confidence-value {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-green);
        margin-top: 0.5rem;
    }
    
    /* Disease Name */
    .disease-name {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-green);
        text-align: center;
        margin: 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Treatment Recommendations */
    .treatment-section {
        margin-top: 2rem;
    }
    
    .treatment-title {
        font-size: 1.6rem;
        color: var(--text-dark);
        margin-bottom: 1rem;
    }
    
    .treatment-list {
        list-style: none;
        padding: 0;
    }
    
    .treatment-item {
        background: var(--bg-light-gray);
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-radius: 6px;
        border-left: 4px solid var(--accent-orange);
    }
    
    .learn-more {
        background: none;
        border: none;
        color: var(--accent-orange);
        cursor: pointer;
        font-size: 1rem;
        margin-top: 0.5rem;
        transition: color 0.3s ease;
    }
    
    .learn-more:hover {
        color: #E55A2B;
    }
    
    .details {
        display: none;
        margin-top: 1rem;
        padding: 1rem;
        background: white;
        border-radius: 6px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    /* Loading State */
    .loading {
        text-align: center;
        padding: 4rem;
    }
    
    .spinner {
        border: 4px solid var(--bg-light-gray);
        border-top: 4px solid var(--primary-green);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        color: var(--primary-green);
        font-size: 1.2rem;
    }
    
    /* Error Handling */
    .error-message {
        background: #FFF5F5;
        border: 1px solid #FED7D7;
        color: #C53030;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* History Section */
    .history-section {
        padding: 4rem 2rem;
        background: var(--bg-light-gray);
    }
    
    .history-title {
        font-size: 2.4rem;
        color: var(--primary-green);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .history-item {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* About Section */
    .about-section {
        padding: 4rem 2rem;
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
    }
    
    .about-title {
        font-size: 2.4rem;
        color: var(--primary-green);
        margin-bottom: 2rem;
    }
    
    .about-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: var(--text-light);
        margin-bottom: 2rem;
    }
    
    /* Contact Section */
    .contact-section {
        padding: 4rem 2rem;
        background: var(--bg-light-gray);
        text-align: center;
    }
    
    .contact-title {
        font-size: 2.4rem;
        color: var(--primary-green);
        margin-bottom: 2rem;
    }
    
    .contact-form {
        max-width: 600px;
        margin: 0 auto;
    }
    
    .form-group {
        margin-bottom: 1rem;
        text-align: left;
    }
    
    .form-group label {
        display: block;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--text-dark);
    }
    
    .form-group input, .form-group textarea {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #DDD;
        border-radius: 6px;
        font-family: inherit;
    }
    
    .submit-button {
        background: var(--primary-green);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 6px;
        font-size: 1.1rem;
        cursor: pointer;
        transition: background 0.3s ease;
    }
    
    .submit-button:hover {
        background: #1F6B3A;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.4rem; }
        .hero-subtitle { font-size: 1.2rem; }
        .steps-container { grid-template-columns: 1fr; }
        .upload-section, .analysis-section { padding: 2rem 1rem; }
        .steps-section, .history-section, .contact-section { padding: 2rem 1rem; }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        .steps-container { grid-template-columns: repeat(2, 1fr); }
    }
    
    /* Accessibility */
    :focus {
        outline: 2px solid var(--accent-orange);
        outline-offset: 2px;
    }
    
    /* Micro-interactions */
    button:hover, .step-card:hover, .drop-zone:hover {
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Session State for History
if 'history' not in st.session_state:
    st.session_state.history = []

# Main App
def main():
    # Hero Section
    st.markdown('<div class="hero-section"><div class="hero-content"><h1 class="hero-title">Plant Savior AI</h1><p class="hero-subtitle">Instant Plant Disease Detection using AI</p><button class="cta-button" onclick="document.querySelector(\'#upload\').scrollIntoView({behavior: \'smooth\'});">Get Started</button></div></div>', unsafe_allow_html=True)
    
    # Three-Step Process
    st.markdown('<div class="steps-section"><h2 class="steps-title">How It Works</h2><div class="steps-container">', unsafe_allow_html=True)
    steps = [
        ("<div class='step-number'>1</div><div class='step-icon'>📁</div><h3 class='step-title'>Upload Image</h3><p class='step-desc'>Drag & drop or select a photo of your plant leaf.</p>",
         "step-card"),
        ("<div class='step-number'>2</div><div class='step-icon'>🔍</div><h3 class='step-title'>AI Analysis</h3><p class='step-desc'>Our AI model analyzes the image for diseases in seconds.</p>",
         "step-card"),
        ("<div class='step-number'>3</div><div class='step-icon'>✅</div><h3 class='step-title'>Get Results</h3><p class='step-desc'>Receive diagnosis and treatment recommendations instantly.</p>",
         "step-card")
    ]
    for step in steps:
        st.markdown(f'<div class="{step[1]}">{step[0]}</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Upload Section
    st.markdown('<div class="upload-section" id="upload">', unsafe_allow_html=True)
    st.markdown('<h2 class="upload-title">Upload Your Plant Image</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], help="Supported formats: JPG, PNG, JPEG. Max size: 5MB.")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Analyze", key="analyze", help="Click to start AI analysis"):
            with st.spinner("Analyzing your image..."):
                time.sleep(2)  # Simulate processing
                # Preprocess image
                img_array = img_to_array(image.resize((224, 224)))
                img_array = np.expand_dims(img_array / 255.0, axis=0)
                
                # Predict
                predictions = model.predict(img_array)
                predicted_class = np.argmax(predictions[0])
                confidence = np.max(predictions[0]) * 100
                
                disease = class_names[predicted_class]
                treatment = f"Treatment for {disease}: Apply fungicide, ensure proper watering."  # Dummy; replace with real logic
                details = f"Detailed info on {disease}: Caused by fungi, affects leaves..."  # Expandable
                
                # Store in history
                st.session_state.history.append({
                    'image': uploaded_file.name,
                    'disease': disease,
                    'confidence': confidence,
                    'treatment': treatment
                })
                
                # Display Results
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="preview-container"><h3 class="preview-title">Image Preview</h3>', unsafe_allow_html=True)
                    st.image(image, use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="results-container"><h3 class="results-title">Analysis Results</h3>', unsafe_allow_html=True)
                    st.markdown(f'<h2 class="disease-name">{disease}</h2>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="confidence-gauge">', unsafe_allow_html=True)
                    st.markdown('<div class="confidence-label"><span>Confidence Score</span><span>{confidence:.1f}%</span></div>', unsafe_allow_html=True)
                    progress = st.markdown('<div class="progress-bg"><div class="progress-fill" style="width: 0%;"></div></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="confidence-value">{confidence:.1f}%</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Animate progress
                    st.markdown(f'<script>document.querySelector(".progress-fill").style.width = "{confidence}%";</script>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="treatment-section">', unsafe_allow_html=True)
                    st.markdown('<h4 class="treatment-title">Treatment Recommendations</h4>', unsafe_allow_html=True)
                    for item in treatment.split('. '):
                        if item:
                            st.markdown(f'<div class="treatment-item">• {item}</div>', unsafe_allow_html=True)
                    
                    if st.button("Learn More", key="learn_more"):
                        st.markdown(f'<div class="details">{details}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Reset", key="reset"):
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Loading State (handled in button)
    
    # Error Handling Example
    if 'error' in st.session_state:
        st.error(st.session_state.error)
        if st.button("Retry"):
            del st.session_state.error
    
    # History Section
    if st.session_state.history:
        st.markdown('<div class="history-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="history-title">Recent Diagnoses</h2>', unsafe_allow_html=True)
        for item in st.session_state.history[-5:]:  # Last 5
            st.markdown(f'<div class="history-item"><strong>{item["disease"]}</strong> - {item["confidence"]:.1f}% <small>{item["image"]}</small></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # About Section
    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="about-title">About Plant Savior AI</h2>', unsafe_allow_html=True)
    st.markdown('<p class="about-text">Plant Savior AI is an innovative tool powered by advanced machine learning to help farmers and gardeners detect plant diseases early. Our mission is to promote sustainable agriculture through accessible technology.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Contact Section
    st.markdown('<div class="contact-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="contact-title">Contact & Feedback</h2>', unsafe_allow_html=True)
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send", type="primary")
        if submitted:
            st.success("Thank you for your feedback!")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
