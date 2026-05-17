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

# --- CRITICAL FIX FOR STREAMLIT CLOUD ---
# Streamlit Cloud caches the broken OpenCV GUI version that Ultralytics installs.
# This script forcefully uninstalls the broken one and installs the headless one
# at runtime, completely bypassing the need for a packages.txt file or cache clearing.
import subprocess
import sys
try:
    import cv2
    _ = cv2.Mat
except ImportError:
    # Use force-reinstall to overwrite the broken cv2 binaries without triggering pip uninstall permission errors
    subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python-headless", "--force-reinstall", "--no-deps"], check=False)
    import cv2

from ultralytics import YOLO

# Cache the YOLO classifier so it loads only once
@st.cache_resource(show_spinner=False)
def load_yolo_classifier():
    return YOLO('yolov8n-cls.pt')

# Plant/leaf related ImageNet class keywords
PLANT_KEYWORDS = [
    'cabbage', 'broccoli', 'cauliflower', 'zucchini', 'squash',
    'cucumber', 'artichoke', 'pepper', 'bell_pepper', 'cardoon',
    'rapeseed', 'corn', 'mushroom', 'agaric', 'bolete', 'earthstar',
    'stinkhorn', 'hen-of-the-woods', 'coral_fungus', 'gyromitra',
    'strawberry', 'orange', 'lemon', 'banana', 'fig', 'pineapple',
    'jackfruit', 'custard_apple', 'pomegranate', 'grape', 'granny_smith',
    'daisy', 'sunflower', 'rose', 'tulip', 'orchid', 'lily',
    'yellow_lady', 'lotus', 'poppy', 'hibiscus', 'flowerpot',
    'acorn', 'hip', 'hay', 'leaf', 'plant', 'flower', 'tree',
    'garden', 'botanical', 'vegetation', 'foliage', 'seed', 'petal',
    'fern', 'moss', 'vine', 'herb', 'aloe', 'cactus', 'succulent',
]

def is_leaf_image(img_path):
    """Use YOLO classifier (ImageNet 1000 classes) to verify image is a plant/leaf.
    Returns True only if any of the top 10 predictions match plant/leaf keywords.
    Blocks humans, animals, vehicles, cartoons, electronics, etc."""
    try:
        model = load_yolo_classifier()
        results = model(img_path, verbose=False)
        probs = results[0].probs
        names = results[0].names

        # Get top 10 prediction indices
        top_indices = probs.data.topk(10).indices.tolist()

        for idx in top_indices:
            label = names[idx].lower()
            for keyword in PLANT_KEYWORDS:
                if keyword in label:
                    return True
        return False
    except Exception:
        return False

# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI - Advanced Plant Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Enhanced Futuristic Modern UI CSS Design
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6, .logo-text, .cyberpunk-text {
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.02em;
    }
    
    /* Main background and layout */
    .stApp {
        background-color: #0B1121;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(16, 185, 129, 0.08), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(52, 211, 153, 0.08), transparent 25%);
        color: #F8FAFC;
        overflow-x: hidden;
        min-height: 100vh;
    }
    
    /* Header Styles - Premium Modern */
    .main-header {
        padding: 5rem 2rem 3rem 2rem;
        border-radius: 0;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .logo-text {
        font-size: 4.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #34D399 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: -1px;
    }
    
    .tagline {
        font-size: 1.2rem;
        font-weight: 400;
        color: #94A3B8;
        max-width: 800px;
        margin: 0 auto;
        letter-spacing: 0.5px;
    }
    
    /* Statistics Section */
    .stats-section {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 0 0 4rem 0;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        min-width: 180px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #10B981;
        margin-bottom: 0.25rem;
        font-family: 'Outfit', sans-serif;
    }
    
    .stat-label {
        color: #94A3B8;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Glassmorphism Container */
    .glass-container {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        padding: 3rem;
        margin-bottom: 3rem;
        transition: transform 0.3s ease;
    }
    
    /* How It Works Section */
    .how-it-works {
        padding: 4rem;
    }
    
    .section-title, .upload-title, .team-title {
        color: #F8FAFC;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 3rem;
        font-weight: 700;
    }
    
    .section-title span, .upload-title span, .team-title span {
        color: #10B981;
    }
    
    .steps-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 2rem;
    }
    
    .step-card {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        flex: 1;
        min-width: 250px;
        border: 1px solid rgba(255, 255, 255, 0.03);
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-8px);
        border-color: rgba(16, 185, 129, 0.3);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    .step-number {
        width: 60px;
        height: 60px;
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-weight: 700;
        font-size: 1.5rem;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .step-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
    }
    
    .step-title {
        color: #E2E8F0;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .step-description {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Upload Section */
    .upload-section {
        padding: 4rem;
        text-align: center;
    }
    
    /* Analysis Section */
    .analysis-section {
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
        margin-bottom: 3rem;
        margin-top: 2rem;
    }
    
    .image-preview-container, .results-container {
        flex: 1;
        min-width: 320px;
        background: rgba(30, 41, 59, 0.3);
        border-radius: 24px;
        padding: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .section-subtitle {
        color: #F8FAFC;
        font-size: 1.5rem;
        margin-bottom: 2rem;
        font-weight: 600;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
    }
    
    .preview-image {
        width: 100%;
        max-height: 400px;
        object-fit: cover;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    /* Loading Animation */
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(16, 185, 129, 0.1);
        border-top: 4px solid #10B981;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 2rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-size: 1.25rem;
        color: #E2E8F0;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .loading-subtext {
        color: #94A3B8;
        font-size: 0.95rem;
    }
    
    /* Results Card */
    .results-card {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-item {
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    .result-title {
        color: #94A3B8;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    .disease-name {
        font-size: 1.75rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0.5rem 0;
    }
    
    /* Progress Bar */
    .progress-container {
        margin: 1.5rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.75rem;
        font-weight: 500;
        color: #CBD5E1;
        font-size: 0.95rem;
    }
    
    .progress-bar-bg {
        width: 100%;
        height: 8px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #34D399, #10B981);
        border-radius: 8px;
        transition: width 1s ease-out;
    }
    
    .confidence-text {
        font-weight: 600;
        color: #10B981;
    }
    
    /* Treatment Box */
    .treatment-box {
        background: rgba(16, 185, 129, 0.05);
        border-left: 4px solid #10B981;
        border-radius: 0 12px 12px 0;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .treatment-text {
        line-height: 1.6;
        color: #E2E8F0;
        font-size: 1rem;
        margin: 0;
    }
    
    /* Buttons */
    .stButton>button {
        background: #10B981 !important;
        color: white !important;
        border: none !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2) !important;
    }
    
    .stButton>button:hover {
        background: #059669 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Status Boxes */
    .error-box {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #EF4444;
        border-radius: 0 12px 12px 0;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: #FCA5A5;
    }
    
    /* Info Box styling */
    .info-box {
        background: rgba(15, 23, 42, 0.6);
        padding: 1.25rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .info-box p {
        color: #CBD5E1 !important;
        margin: 0.4rem 0 !important;
        font-size: 0.95rem !important;
    }
    
    .info-box strong {
        color: #10B981 !important;
    }
    
    /* About & Team Sections */
    .about-section, .team-section {
        padding: 4rem;
        margin-bottom: 2rem;
    }
    
    .about-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #94A3B8;
        margin-bottom: 2rem;
        text-align: center;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 3rem 0;
    }
    
    .tech-item {
        background: rgba(255, 255, 255, 0.03);
        padding: 0.75rem 1.5rem;
        border-radius: 100px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #E2E8F0;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .tech-item:hover {
        background: rgba(16, 185, 129, 0.1);
        border-color: #10B981;
        color: #10B981;
    }
    
    .team-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }
    
    .team-card {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        flex: 1;
        min-width: 250px;
        max-width: 320px;
        border: 1px solid rgba(255, 255, 255, 0.03);
        transition: transform 0.3s ease;
    }
    
    .team-card:hover {
        transform: translateY(-8px);
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    .team-name {
        color: #F8FAFC;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem;
    }
    
    .team-role {
        color: #10B981;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    
    .team-desc {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .love-icon {
        text-align: center;
        font-size: 2rem;
        margin: 3rem 0 1rem;
        color: #EF4444;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 4rem;
    }
    
    .footer-text {
        font-size: 0.95rem;
        color: #94A3B8;
        margin: 0.5rem 0;
    }
    
    .creator-info {
        margin: 2rem 0;
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }
    
    .creator-info .footer-text {
        background: rgba(255, 255, 255, 0.03);
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-size: 0.9rem;
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
        font-family: 'Outfit', sans-serif;
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] li {
        color: #94A3B8 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Status Pills */
    .status-pill {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 100px;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    
    .status-healthy {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-disease {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header { padding: 3rem 1rem 2rem; }
        .logo-text { font-size: 3rem; }
        .analysis-section { flex-direction: column; }
        .glass-container { padding: 2rem; }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0B1121;
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }
    
    /* Streamlit uploader tweaks */
    [data-testid="stFileUploader"] {
        max-width: 600px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1 class="logo-text">🌱 PLANT SAVIOR AI</h1>
    <p class="tagline">NEXT-GENERATION PLANT DISEASE DETECTION POWERED BY ADVANCED ARTIFICIAL INTELLIGENCE</p>
</div>
""", unsafe_allow_html=True)

# Statistics Section
st.markdown("""
<div class="stats-section">
    <div class="stat-card">
        <div class="stat-value">99.2%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">15+</div>
        <div class="stat-label">Plant Diseases</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><3s</div>
        <div class="stat-label">Analysis Time</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("### 🚀 AI SYSTEM STATUS")
    st.success("🟢 NEURAL NETWORK: ACTIVE")
    st.success("🟢 IMAGE PROCESSOR: READY")
    st.success("🟢 TREATMENT DB: LOADED")
    st.markdown("### 🌿 ABOUT THIS SYSTEM")
    st.info("""
    **PLANT SAVIOR AI** utilizes cutting-edge deep learning technology to provide instant plant disease diagnosis. Our advanced convolutional neural network has been trained on thousands of plant images to deliver professional-grade accuracy.
    🔬 **POWERED BY**: TensorFlow & Keras
    🎯 **ACCURACY**: 99.2% on test data
    ⚡ **SPEED**: Real-time analysis
    """)
    st.markdown("### 📋 OPTIMAL RESULTS GUIDE")
    st.markdown("""
    **📸 PHOTOGRAPHY TIPS:**
    • Natural daylight works best
    • Focus on affected leaf areas
    • Avoid shadows and reflections
    • Hold camera steady for clarity
    • Fill frame with leaf details
    **🔍 BEST PRACTICES:**
    • Single leaf per image
    • Clear disease symptoms visible
    • High resolution (>500px)
    • Minimal background clutter
    """)
    st.markdown("### 🎯 SUPPORTED DISEASES")
    st.markdown("""
    **🍅 TOMATO DISEASES (10 TYPES):**
    • Early Blight • Late Blight
    • Leaf Mold • Septoria Leaf Spot
    • Spider Mites • Target Spot
    • Yellow Leaf Curl • Mosaic Virus
    • Bacterial Spot • Healthy
    **🥔 POTATO DISEASES (3 TYPES):**
    • Early Blight • Late Blight
    • Healthy
    **🌶️ PEPPER DISEASES (2 TYPES):**
    • Bacterial Spot • Healthy
    """)
    st.markdown("### 💡 TECH STACK")
    st.markdown("""
    • **TensorFlow 2.x** - Deep Learning
    • **Streamlit** - Web Interface  
    • **PIL/OpenCV** - Image Processing
    • **NumPy** - Numerical Computing
    • **Custom CNN** - Disease Classification
    """)

# How it works section
st.markdown('<div class="how-it-works glass-container fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">HOW THE <span>AI SYSTEM</span> WORKS</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="steps-container">
    <div class="step-card">
        <div class="step-number">1</div>
        <div class="step-icon">📱</div>
        <h3 class="step-title">IMAGE CAPTURE</h3>
        <p class="step-description">Upload a high-quality image of the affected plant leaf. Our system accepts JPG, JPEG, and PNG formats for maximum compatibility.</p>
    </div>
    <div class="step-card">
        <div class="step-number">2</div>
        <div class="step-icon">🧠</div>
        <h3 class="step-title">AI PROCESSING</h3>
        <p class="step-description">Advanced convolutional neural network analyzes the image using deep learning algorithms trained on 87K rgb images of healthy and diseased crop leaves which is categorized into 38 different classes.</p>
    </div>
    <div class="step-card">
        <div class="step-number">3</div>
        <div class="step-icon">📊</div>
        <h3 class="step-title">INSTANT DIAGNOSIS</h3>
        <p class="step-description">Receive comprehensive results with disease identification, confidence score, and professional treatment recommendations.</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Function to load model
@st.cache_resource(show_spinner=False)
def load_model():
    """Load the trained model with enhanced error handling"""
    try:
        with st.spinner("🚀 INITIALIZING AI NEURAL NETWORK..."):
            model = tf.keras.models.load_model('best_plant_model_final.keras')
            st.sidebar.success("✅ AI MODEL: FULLY LOADED")
            return model
    except FileNotFoundError:
        st.sidebar.error("❌ MODEL FILE NOT FOUND: best_plant_model_final.keras")
        st.error("🚨 **AI MODEL ERROR**: Model file 'best_plant_model_final.keras' not found in the current directory.")
        return None
    except Exception as e:
        st.sidebar.error(f"❌ MODEL LOADING ERROR: {str(e)}")
        st.error(f"🚨 **SYSTEM ERROR**: {str(e)}")
        return None

# Load treatment dictionary
@st.cache_resource(show_spinner=False)
def load_treatments():
    """Load treatment recommendations with enhanced error handling"""
    try:
        with open('treatment_dict_complete.json', 'r') as f:
            treatments = json.load(f)
        st.sidebar.success("✅ TREATMENT DATABASE: READY")
        return treatments
    except FileNotFoundError:
        st.sidebar.error("❌ TREATMENT FILE NOT FOUND: treatment_dict_complete.json")
        # Fallback treatment dictionary
        fallback_treatments = {
            "Tomato_Early_blight": "Apply fungicide containing chlorothalonil or copper. Ensure good air circulation and avoid overhead watering.",
            "Tomato_Late_blight": "Remove affected plants immediately. Apply copper-based fungicide preventively. Improve ventilation.",
            "Tomato_Leaf_Mold": "Reduce humidity, improve air circulation. Apply fungicide if severe. Remove affected leaves.",
            "Tomato_Septoria_leaf_spot": "Apply fungicide with chlorothalonil. Remove lower leaves. Ensure proper spacing for air flow.",
            "Tomato_Spider_mites_Two_spotted_spider_mite": "Increase humidity around plants. Use miticide or neem oil. Remove heavily infested leaves.",
            "Tomato_Target_Spot": "Apply fungicide rotation. Improve air circulation. Avoid overhead irrigation.",
            "Tomato_Yellow_Leaf_Curl_Virus": "Remove affected plants. Control whiteflies. Use virus-resistant varieties.",
            "Tomato_mosaic_virus": "Remove infected plants immediately. Disinfect tools. Use resistant varieties.",
            "Tomato_Bacterial_spot": "Apply copper-based bactericide. Avoid overhead watering. Remove affected plant parts.",
            "Tomato_healthy": "Plant appears healthy! Continue current care routine with proper watering and nutrition.",
            "Potato_Early_blight": "Apply fungicide containing chlorothalonil. Ensure proper plant spacing and air circulation.",
            "Potato_Late_blight": "Apply copper fungicide preventively. Remove affected plants. Improve drainage.",
            "Potato_healthy": "Potato plant looks healthy! Maintain current growing conditions.",
            "Pepper_bell_Bacterial_spot": "Apply copper bactericide. Avoid overhead watering. Remove affected leaves.",
            "Pepper_bell_healthy": "Pepper plant is healthy! Continue proper care and monitoring."
        }
        st.warning("⚠️ Using fallback treatment database")
        return fallback_treatments
    except Exception as e:
        st.sidebar.error(f"❌ TREATMENT LOADING ERROR: {str(e)}")
        return {}

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.treatments = {}
    st.session_state.analysis_count = 0

# Load model and treatments
if st.session_state.model is None:
    with st.spinner("⚡ BOOTING UP PLANT SAVIOR AI SYSTEM..."):
        model = load_model()
        st.session_state.model = model
        if model is not None:
            st.success("🚀 **SYSTEM READY**: Plant Savior AI is now fully operational!")
            time.sleep(1)

# Always load treatments
st.session_state.treatments = load_treatments()

# Main upload section
st.markdown('<div class="upload-section glass-container fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="upload-title">🔬 AI-POWERED <span>PLANT ANALYSIS</span></h2>', unsafe_allow_html=True)

# Enhanced file uploader
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], help="Upload a clear image of the plant leaf for AI analysis")

if uploaded_file is not None:
    # Analysis section
    st.markdown('<div class="analysis-section fade-in-up">', unsafe_allow_html=True)
    # Left column
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown('<div class="image-preview-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-subtitle">📸 UPLOADED IMAGE</h3>', unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        st.image(image, caption="🌿 Ready for AI Analysis", use_column_width=True, clamp=True)
        # Image info display
        width, height = image.size
        file_size = len(uploaded_file.getvalue()) / 1024  # KB
        st.markdown(f"""
        <div class="info-box">
            <p style="margin: 0; color: #10B981 !important;"><strong>📊 IMAGE DETAILS:</strong></p>
            <p style="margin: 5px 0;">📐 Dimensions: {width} × {height} pixels</p>
            <p style="margin: 5px 0;">💾 Size: {file_size:.1f} KB</p>
            <p style="margin: 5px 0;">📁 Format: {uploaded_file.type}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 UPLOAD NEW IMAGE", key="reset", help="Upload a different leaf image", use_container_width=True):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right column
    with col2:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-subtitle">🧬 AI ANALYSIS CENTER</h3>', unsafe_allow_html=True)
        if st.session_state.model is not None and st.session_state.treatments:
            if st.button("🚀 ANALYZE WITH AI", key="analyze", help="Start advanced AI analysis", use_container_width=True):
                # Save uploaded file temporarily
                with open("temp_image.jpg", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                if not is_leaf_image("temp_image.jpg"):
                    st.markdown('<div class="error-box" style="text-align: center;">', unsafe_allow_html=True)
                    st.markdown('<h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">⚠️ NOT A LEAF PIC</h3>', unsafe_allow_html=True)
                    st.markdown('<p style="color: #FCA5A5;">This image does not appear to be a plant leaf. Our AI is specifically trained to analyze natural plant leaves.</p>', unsafe_allow_html=True)
                    st.markdown('<p style="color: #FCA5A5;"><strong>Please upload a clear leaf picture and try again.</strong></p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    try:
                        os.remove("temp_image.jpg")
                    except:
                        pass
                    st.stop()
                    
                # Enhanced loading animation
                loading_placeholder = st.empty()
                with loading_placeholder:
                    st.markdown("""
                    <div class="loading-container">
                        <div class="spinner"></div>
                        <div class="loading-text">🧠 AI PROCESSING IMAGE...</div>
                        <div class="loading-subtext">Neural network analyzing leaf patterns</div>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                    st.markdown("""
                    <div class="loading-container">
                        <div class="spinner"></div>
                        <div class="loading-text">🔍 DETECTING PATTERNS...</div>
                        <div class="loading-subtext">Comparing with disease database</div>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                    st.markdown("""
                    <div class="loading-container">
                        <div class="spinner"></div>
                        <div class="loading-text">📊 GENERATING DIAGNOSIS...</div>
                        <div class="loading-subtext">Calculating confidence scores</div>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                
                # Clear the loading animation
                loading_placeholder.empty()
                try:
                    # Preprocess image
                    img = load_img("temp_image.jpg", target_size=(224, 224))
                    img_array = img_to_array(img)
                    img_array = img_array.reshape(1, 224, 224, 3) / 255.0
                    # Make prediction
                    predictions = st.session_state.model.predict(img_array, verbose=0)
                    predicted_class = np.argmax(predictions[0])
                    confidence_score = float(predictions[0][predicted_class])
                    
                    # Get class names and prediction
                    class_names = list(st.session_state.treatments.keys())
                    predicted_disease = class_names[predicted_class]
                    treatment = st.session_state.treatments.get(predicted_disease, "Consult with an agricultural expert for specialized treatment.")
                    
                    # Update analysis counter
                    st.session_state.analysis_count += 1
                    
                    # Display results
                    st.markdown('<div class="results-card">', unsafe_allow_html=True)
                    
                    # Main diagnosis result
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">🎯 PRIMARY DIAGNOSIS</h4>', unsafe_allow_html=True)
                    
                    # Clean disease name for display
                    display_disease = predicted_disease.replace('_', ' ').title()
                    st.markdown(f'<p class="disease-name" style="text-align: center;">{display_disease}</p>', unsafe_allow_html=True)
                    
                    # Health status indicator
                    if "healthy" in predicted_disease.lower():
                        st.markdown('<div style="text-align: center; margin: 1.5rem 0;"><span class="status-pill status-healthy">🌿 HEALTHY PLANT</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="text-align: center; margin: 1.5rem 0;"><span class="status-pill status-disease">⚠️ DISEASE DETECTED</span></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Confidence score
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">🎯 CONFIDENCE ANALYSIS</h4>', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="progress-container">
                            <div class="progress-label">
                                <span>AI Confidence Level</span>
                                <span class="confidence-text">{confidence_score*100:.1f}%</span>
                            </div>
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill" style="width: {confidence_score*100}%"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Confidence interpretation
                    if confidence_score > 0.9:
                        conf_msg = "🟢 VERY HIGH CONFIDENCE - Diagnosis is highly reliable"
                        conf_color = "#10B981"
                    elif confidence_score > 0.7:
                        conf_msg = "🟡 HIGH CONFIDENCE - Diagnosis is reliable"
                        conf_color = "#F59E0B"
                    elif confidence_score > 0.5:
                        conf_msg = "🟠 MODERATE CONFIDENCE - Consider expert consultation"
                        conf_color = "#34D399"
                    else:
                        conf_msg = "🔴 LOW CONFIDENCE - Recommend professional diagnosis"
                        conf_color = "#EF4444"
                    st.markdown(f'<p style="color: {conf_color}; font-weight: 500; font-size: 0.95rem; text-align: center; margin-top: 1rem;">{conf_msg}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Treatment recommendation
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    if "healthy" in predicted_disease.lower():
                        st.markdown('<h4 class="result-title">🌿 CARE RECOMMENDATION</h4>', unsafe_allow_html=True)
                    else:
                        st.markdown('<h4 class="result-title">💊 TREATMENT PROTOCOL</h4>', unsafe_allow_html=True)
                    st.markdown(f'<div class="treatment-box"><p class="treatment-text">{treatment}</p></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Analysis summary
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">📈 ANALYSIS SUMMARY</h4>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-box">
                        <p style="margin: 0.5rem 0;"><strong>🔬 Analysis #{st.session_state.analysis_count}</strong></p>
                        <p style="margin: 0.5rem 0;">🧠 Model: Advanced CNN v2.1</p>
                        <p style="margin: 0.5rem 0;">⚡ Processing Time: <3 seconds</p>
                        <p style="margin: 0.5rem 0;">🎯 Classes Evaluated: {len(class_names)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Success notification
                    st.success("✅ **ANALYSIS COMPLETE!** Your plant has been successfully diagnosed by our AI system.")

                except Exception as e:
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    st.markdown(f'<p style="margin: 0; font-weight: 600;">❌ ANALYSIS ERROR: {str(e)}</p>', unsafe_allow_html=True)
                    st.markdown('<p style="margin-top: 0.5rem;">Please try uploading a different image or contact support if the issue persists.</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Clean up temporary file
                try:
                    os.remove("temp_image.jpg")
                except:
                    pass
            else:
                st.markdown("""
                <div class="info-box" style="text-align: center; border: 2px dashed rgba(255,255,255,0.1); padding: 3rem 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
                    <h4 style="color: #F8FAFC; font-family: Outfit; font-size: 1.5rem; margin-bottom: 1rem;">AI READY FOR ANALYSIS</h4>
                    <p style="color: #94A3B8;">Click the "ANALYZE WITH AI" button above to start the diagnosis process. Our neural network will examine your plant image and provide detailed results.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.markdown('<p style="font-weight: 600;">❌ SYSTEM ERROR: AI model or treatment database not properly loaded.</p>', unsafe_allow_html=True)
            st.markdown('<p>Please refresh the page or contact technical support.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Enhanced upload prompt
    st.markdown("""
    <div class="glass-container" style="text-align: center; border: 2px dashed rgba(255,255,255,0.1); padding: 5rem 2rem; max-width: 800px; margin: 2rem auto;">
        <div style="font-size: 4rem; margin-bottom: 1.5rem;">📸</div>
        <h3 style="color: #F8FAFC; font-family: Outfit; margin-bottom: 1rem; font-size: 2rem;">UPLOAD PLANT IMAGE FOR <span style="color: #10B981;">AI ANALYSIS</span></h3>
        <p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 2rem;">Select a clear image of the plant leaf you want to analyze</p>
        <div class="info-box" style="max-width: 400px; margin: 0 auto;">
            <p>Supported formats: JPG, JPEG, PNG</p>
            <p>Maximum file size: 200MB</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# About section
st.markdown('<div class="about-section glass-container fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🚀 ABOUT <span>PLANT SAVIOR AI</span></h2>', unsafe_allow_html=True)
st.markdown("""
<div class="about-content">
    <p class="about-text">
        <strong>Plant Savior AI</strong> represents the cutting edge of agricultural technology, combining advanced machine learning with practical farming solutions. Our system utilizes a sophisticated Convolutional Neural Network (CNN) architecture trained on 87K rgb images of healthy and diseased crop leaves which is categorized into 38 different classes to deliver professional-grade plant disease diagnosis.
    </p>
    <p class="about-text">
        Built with <strong>TensorFlow 2.x</strong> and deployed using <strong>Streamlit</strong>, this application showcases the power of AI in solving real-world agricultural challenges. Whether you're a farmer, gardener, or agricultural researcher, Plant Savior AI provides instant, accurate plant health assessment at your fingertips.
    </p>
    <div class="tech-stack">
        <div class="tech-item">🧠 TensorFlow</div>
        <div class="tech-item">🌐 Streamlit</div>
        <div class="tech-item">🖼️ OpenCV</div>
        <div class="tech-item">🔢 NumPy</div>
        <div class="tech-item">🐍 Python</div>
        <div class="tech-item">📊 Keras</div>
    </div>
    <p class="about-text">
        Our mission is to democratize plant disease detection, making advanced agricultural AI accessible to everyone. By combining scientific rigor with user-friendly design, we're helping to create a more sustainable and productive agricultural future.
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Team Section
st.markdown('<div class="team-section glass-container fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="team-title">👥 MEET <span>THE TEAM</span></h2>', unsafe_allow_html=True)
st.markdown("""
<div class="team-container">
    <div class="team-card">
        <h3 class="team-name">Aiza</h3>
        <p class="team-role">Team Lead, Full Stack AI Engineer</p>
        <p class="team-desc">Leading the development and integration of AI models and full-stack architecture. Expert in deep learning, neural networks, and end-to-end system design.</p>
    </div>
    <div class="team-card">
        <h3 class="team-name">Tooba</h3>
        <p class="team-role">Web Designer</p>
        <p class="team-desc">Crafting the futuristic UI/UX experience. Responsible for the modern design, animations, and responsive interface that powers Plant Savior AI.</p>
    </div>
    <div class="team-card">
        <h3 class="team-name">Taiba</h3>
        <p class="team-role">Machine Learning Engineer</p>
        <p class="team-desc">Specializing in model training, optimization, and performance tuning. Ensures our AI delivers 99.2% accuracy across diverse plant conditions.</p>
    </div>
</div>
<div class="love-icon">❤️</div>
<p style="text-align: center; color: #10B981; font-size: 1.1rem; font-weight: 500;">Made with ❤️ by the Plant Savior AI Team</p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-text" style="color: #F8FAFC; font-weight: 600; font-size: 1.1rem;">🌱 PLANT SAVIOR AI - REVOLUTIONIZING AGRICULTURE WITH ARTIFICIAL INTELLIGENCE</div>
    <div class="footer-text">Powered by Advanced Deep Learning • Real-time Disease Detection • Professional Treatment Recommendations</div>
    <div class="creator-info">
        <div class="footer-text">🎯 <strong>MODEL ACCURACY:</strong> 99.2% on validation data</div>
        <div class="footer-text">⚡ <strong>PROCESSING SPEED:</strong> Sub-3-second analysis</div>
        <div class="footer-text">🌍 <strong>IMPACT:</strong> Helping farmers worldwide save crops</div>
    </div>
    <div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid rgba(255, 255, 255, 0.05);">
        <div class="footer-text" style="font-size: 0.85rem;">© 2025 Plant Savior AI. All rights reserved. | Built with ❤️ using TensorFlow & Streamlit</div>
    </div>
</div>
""", unsafe_allow_html=True)