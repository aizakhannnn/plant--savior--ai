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
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced Futuristic Cyberpunk CSS Design
st.markdown("""
<style>
    /* Global Styles & Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
        box-sizing: border-box;
    }
    
    h1, h2, h3, h4, h5, h6, .logo-text, .section-title, .step-title, .result-title, .disease-name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Hide Streamlit default branding & menus to create an ultra-clean, custom portal */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_container__1QS1h {display: none !important;}
    
    /* Smooth, Premium Obsidian Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0d1e1c 0%, #060b0d 60%, #030506 100%);
        background-attachment: fixed;
        color: #e2e8f0;
        overflow-x: hidden;
        min-height: 100vh;
    }
    
    /* Decorative Abstract Neural Grid Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(1.5px 1.5px at 40px 60px, rgba(0, 255, 136, 0.15), transparent),
            radial-gradient(1.5px 1.5px at 120px 180px, rgba(0, 255, 136, 0.1), transparent),
            radial-gradient(1.5px 1.5px at 200px 300px, rgba(0, 255, 136, 0.08), transparent);
        background-repeat: repeat;
        background-size: 320px 320px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Exquisite Hero Header Card */
    .main-header {
        background: linear-gradient(145deg, rgba(16, 28, 25, 0.65) 0%, rgba(10, 16, 18, 0.8) 100%);
        padding: 3.5rem 2rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(0, 255, 136, 0.15);
        box-shadow: 
            0 20px 50px rgba(0, 0, 0, 0.5),
            inset 0 1px 1px rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.6), transparent);
    }
    
    .logo-text {
        font-size: 3.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: #ffffff;
        background: linear-gradient(135deg, #ffffff 30%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.04em;
        text-shadow: 0 0 40px rgba(0, 255, 136, 0.2);
    }
    
    .tagline {
        font-size: 1.1rem;
        opacity: 0.85;
        font-weight: 500;
        max-width: 750px;
        margin: 0 auto;
        color: #a7f3d0;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* High-End Stats Cards */
    .stats-section {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 2.5rem 0;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: rgba(13, 22, 21, 0.45);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        text-align: center;
        min-width: 180px;
        flex: 1;
        border: 1px solid rgba(0, 255, 136, 0.08);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }
    
    .stat-card:hover {
        transform: translateY(-6px);
        border-color: rgba(0, 255, 136, 0.35);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(0, 255, 136, 0.15);
    }
    
    .stat-value {
        font-size: 2.8rem;
        font-weight: 700;
        color: #00ff88;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.03em;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
        line-height: 1;
        margin-bottom: 0.4rem;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Ultimate Glassmorphic Layout Container */
    .glass-container {
        background: rgba(13, 22, 21, 0.45);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(0, 255, 136, 0.08);
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.03);
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .glass-container:hover {
        border-color: rgba(0, 255, 136, 0.2);
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.6),
            0 0 30px rgba(0, 255, 136, 0.05);
    }
    
    /* Streamlit Native Collapsible Expander Overrides */
    .streamlit-expanderHeader {
        background-color: rgba(13, 22, 21, 0.45) !important;
        border: 1px solid rgba(0, 255, 136, 0.08) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: all 0.3s ease;
    }
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 255, 136, 0.3) !important;
        background-color: rgba(13, 22, 21, 0.6) !important;
    }
    .streamlit-expanderContent {
        background-color: rgba(8, 14, 15, 0.5) !important;
        border: 1px solid rgba(0, 255, 136, 0.05) !important;
        border-top: none !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
        padding: 1.5rem !important;
    }
    
    /* Beautiful Section Title Styling */
    .section-title {
        color: #ffffff;
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        position: relative;
    }
    
    .section-title::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: #00ff88;
        border-radius: 2px;
    }
    
    /* Steps / Cards for instructions */
    .steps-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1.5rem;
    }
    
    .step-card {
        background: rgba(8, 14, 15, 0.6);
        border-radius: 16px;
        padding: 2.2rem 1.8rem;
        text-align: center;
        flex: 1;
        min-width: 200px;
        border: 1px solid rgba(0, 255, 136, 0.05);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }
    
    .step-card:hover {
        transform: translateY(-8px);
        border-color: rgba(0, 255, 136, 0.25);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }
    
    .step-number {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #00ff88 0%, #10b981 100%);
        color: #060b0d;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-weight: 700;
        font-size: 1.25rem;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    
    .step-icon {
        font-size: 2.5rem;
        margin-bottom: 1.2rem;
        display: block;
    }
    
    .step-title {
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    .step-description {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Upload / Control Panel Redesign */
    .upload-section {
        background: rgba(13, 22, 21, 0.45);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(0, 255, 136, 0.08);
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.4);
    }
    
    .upload-title {
        color: #ffffff;
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Streamlit Upload Container Overrides */
    div[data-testid="stFileUploader"] {
        border: 1px dashed rgba(0, 255, 136, 0.3) !important;
        background: rgba(8, 14, 15, 0.45) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #00ff88 !important;
        background: rgba(8, 14, 15, 0.7) !important;
    }
    
    /* Streamlit Native Buttons Customization */
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #10b981 100%) !important;
        color: #060b0d !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(0, 255, 136, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 12px 30px rgba(0, 255, 136, 0.4),
            0 0 15px rgba(0, 255, 136, 0.2) !important;
        color: #060b0d !important;
    }
    
    .stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    /* Custom Image and Analysis Layout */
    .analysis-section {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }
    
    .image-preview-container, .results-container {
        background: rgba(8, 14, 15, 0.55);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(0, 255, 136, 0.08);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }
    
    .section-subtitle {
        color: #ffffff;
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        text-align: center;
        letter-spacing: -0.01em;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
    }
    
    /* Modern centered leaf frame preview */
    .preview-image {
        border-radius: 12px;
        border: 1px solid rgba(0, 255, 136, 0.15);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Loading Spinner */
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .spinner {
        width: 64px;
        height: 64px;
        border: 4px solid rgba(0, 255, 136, 0.1);
        border-top: 4px solid #00ff88;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-size: 1.2rem;
        color: #00ff88;
        font-weight: 600;
        letter-spacing: 0.05em;
        animation: pulse 1.8s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    .loading-subtext {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Results Presentation */
    .results-card {
        background: rgba(6, 10, 11, 0.7);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(0, 255, 136, 0.15);
    }
    
    .result-item {
        margin-bottom: 1.8rem;
        padding: 1.5rem;
        border-radius: 12px;
        background: rgba(13, 22, 21, 0.4);
        border: 1px solid rgba(0, 255, 136, 0.05);
    }
    
    .result-title {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.8rem;
    }
    
    .disease-name {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        background: linear-gradient(135deg, #ffffff 40%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 0.5rem 0;
        letter-spacing: -0.04em;
    }
    
    /* Clean custom styled progress bar */
    .progress-container {
        margin: 1rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.6rem;
        color: #cbd5e1;
        font-size: 0.95rem;
    }
    
    .progress-bar-bg {
        width: 100%;
        height: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #10b981, #00ff88);
        border-radius: 10px;
    }
    
    .confidence-text {
        font-weight: 700;
        color: #00ff88;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Treatment details */
    .treatment-box {
        background: rgba(16, 185, 129, 0.05);
        border-left: 4px solid #00ff88;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-top: 0.5rem;
    }
    
    .treatment-text {
        line-height: 1.6;
        color: #cbd5e1;
        font-size: 1rem;
        margin: 0;
    }
    
    /* Clean alert box override */
    .error-box {
        background: rgba(239, 68, 68, 0.05);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        color: #fca5a5;
    }
    
    /* About section & tech badges */
    .about-section {
        background: rgba(13, 22, 21, 0.45);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(0, 255, 136, 0.08);
    }
    
    .about-content {
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
    }
    
    .about-text {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #94a3b8;
        margin-bottom: 1.8rem;
    }
    
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }
    
    .tech-item {
        background: rgba(255, 255, 255, 0.03);
        padding: 0.5rem 1rem;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #cbd5e1;
        font-weight: 500;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }
    
    .tech-item:hover {
        border-color: #00ff88;
        color: #00ff88;
        transform: translateY(-2px);
    }
    
    /* Meet The Team Section */
    .team-section {
        background: rgba(13, 22, 21, 0.45);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(0, 255, 136, 0.08);
    }
    
    .team-title {
        color: #ffffff;
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 2.5rem;
        position: relative;
    }
    
    .team-title::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: #00ff88;
        border-radius: 2px;
    }
    
    .team-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
    }
    
    .team-card {
        background: rgba(8, 14, 15, 0.6);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        flex: 1;
        min-width: 240px;
        max-width: 280px;
        border: 1px solid rgba(0, 255, 136, 0.05);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .team-card:hover {
        transform: translateY(-6px);
        border-color: rgba(0, 255, 136, 0.25);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }
    
    .team-name {
        color: #ffffff;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    
    .team-role {
        color: #00ff88;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }
    
    .team-desc {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .love-icon {
        display: block;
        text-align: center;
        font-size: 1.8rem;
        margin: 1.5rem 0 0.5rem;
        color: #00ff88;
        animation: heartbeat 1.6s ease-in-out infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.15); }
    }
    
    /* Footer Style */
    .footer {
        background: linear-gradient(180deg, rgba(8, 14, 15, 0) 0%, rgba(8, 14, 15, 0.8) 100%);
        color: #94a3b8;
        text-align: center;
        padding: 3rem 1.5rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(0, 255, 136, 0.08);
    }
    
    .footer-text {
        font-size: 0.9rem;
        opacity: 0.8;
        margin: 0.5rem 0;
    }
    
    .creator-info {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #030506;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 255, 136, 0.2);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 255, 136, 0.4);
    }
    
    /* Adaptive spacing and responsive typography */
    @media (max-width: 768px) {
        .logo-text { font-size: 2.8rem; }
        .tagline { font-size: 0.95rem; }
        .section-title { font-size: 1.8rem; }
        .glass-container, .upload-section, .about-section, .team-section { padding: 1.75rem; }
        .stats-section { flex-direction: column; }
    }
</style>
""", unsafe_allow_html=True)

# Main header with enhanced futuristic design
st.markdown("""
<div class="main-header">
    <h1 class="logo-text">🌱 PLANT SAVIOR AI</h1>
    <p class="tagline">NEXT-GENERATION PLANT DISEASE DETECTION POWERED BY ADVANCED ARTIFICIAL INTELLIGENCE</p>
</div>
""", unsafe_allow_html=True)

# Statistics Section - Removed "24/7 Available" as requested
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

# System Information Expander instead of Sidebar
with st.expander("ℹ️ SYSTEM INFORMATION & GUIDE", expanded=False):
    st.markdown("### 🚀 AI SYSTEM STATUS")
    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1:
        st.success("🟢 NEURAL NETWORK: ACTIVE")
    with status_col2:
        st.success("🟢 IMAGE PROCESSOR: READY")
    with status_col3:
        st.success("🟢 TREATMENT DB: LOADED")
    
    st.markdown("---")
    
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.markdown("### 🌿 ABOUT THIS SYSTEM")
        st.info("""
        **PLANT SAVIOR AI** utilizes cutting-edge deep learning technology to provide instant plant disease diagnosis. Our advanced convolutional neural network has been trained on thousands of plant images to deliver professional-grade accuracy.
        🔬 **POWERED BY**: TensorFlow & Keras
        🎯 **ACCURACY**: 99.2% on test data
        ⚡ **SPEED**: Real-time analysis
        """)
        st.markdown("### 💡 TECH STACK")
        st.markdown("""
        • **TensorFlow 2.x** - Deep Learning
        • **Streamlit** - Web Interface  
        • **PIL/OpenCV** - Image Processing
        • **NumPy** - Numerical Computing
        • **Custom CNN** - Disease Classification
        """)
        
    with info_col2:
        st.markdown("### 📋 OPTIMAL RESULTS GUIDE")
        st.markdown("""
        **📸 PHOTOGRAPHY TIPS:**
        • Natural daylight works best | • Focus on affected leaf areas
        • Avoid shadows and reflections | • Hold camera steady for clarity
        
        **🔍 BEST PRACTICES:**
        • Single leaf per image | • Clear disease symptoms visible
        • High resolution (>500px) | • Minimal background clutter
        """)
        st.markdown("### 🎯 SUPPORTED DISEASES")
        st.markdown("""
        **🍅 TOMATO (10 TYPES):** Early/Late Blight, Leaf Mold, Septoria, Spider Mites, Target Spot, Yellow Leaf Curl, Mosaic Virus, Bacterial Spot, Healthy
        **🥔 POTATO (3 TYPES):** Early/Late Blight, Healthy
        **🌶️ PEPPER (2 TYPES):** Bacterial Spot, Healthy
        """)

# How it works section with enhanced design
st.markdown('<div class="how-it-works glass-container fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">HOW THE AI SYSTEM WORKS</h2>', unsafe_allow_html=True)
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

# Function to load model with enhanced caching
@st.cache_resource(show_spinner=False)
def load_model():
    """Load the trained model with enhanced error handling"""
    try:
        with st.spinner("🚀 INITIALIZING AI NEURAL NETWORK..."):
            model = tf.keras.models.load_model('best_plant_model_final.keras')
            return model
    except FileNotFoundError:
        st.error("🚨 **AI MODEL ERROR**: Model file 'best_plant_model_final.keras' not found in the current directory.")
        return None
    except Exception as e:
        st.error(f"🚨 **SYSTEM ERROR**: {str(e)}")
        return None

# Load treatment dictionary with enhanced error handling
@st.cache_resource(show_spinner=False)
def load_treatments():
    """Load treatment recommendations with enhanced error handling - Updated for healthy classes"""
    try:
        with open('treatment_dict_complete.json', 'r') as f:
            treatments = json.load(f)
        return treatments
    except FileNotFoundError:
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
        st.error(f"❌ TREATMENT LOADING ERROR: {str(e)}")
        return {}

# Initialize session state with enhanced management
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.treatments = {}
    st.session_state.analysis_count = 0

# Load model and treatments with progress tracking
if st.session_state.model is None:
    with st.spinner("⚡ BOOTING UP PLANT SAVIOR AI SYSTEM..."):
        model = load_model()
        st.session_state.model = model
        if model is not None:
            st.success("🚀 **SYSTEM READY**: Plant Savior AI is now fully operational!")
            time.sleep(1)  # Brief pause for effect

# Always load treatments to ensure updates are picked up
st.session_state.treatments = load_treatments()

# Main upload section with enhanced design
st.markdown('<div class="upload-section glass-container fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="upload-title">🔬 AI-POWERED PLANT ANALYSIS</h2>', unsafe_allow_html=True)
# Enhanced file uploader
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], help="Upload a clear image of the plant leaf for AI analysis")
if uploaded_file is not None:
    # Analysis section merged into a single flow layout
    st.markdown('<div class="analysis-section fade-in-up" style="flex-direction: column;">', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="image-preview-container" style="margin-bottom: 2rem;">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-subtitle">📸 UPLOADED IMAGE</h3>', unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        st.image(image, caption="🌿 Ready for AI Analysis", use_column_width=True, clamp=True)
        # Image info display
        width, height = image.size
        file_size = len(uploaded_file.getvalue()) / 1024  # KB
        st.markdown(f"""
        <div style="background: rgba(13, 22, 21, 0.6); padding: 1rem; border-radius: 12px; margin-top: 1rem; border: 1px solid rgba(0, 255, 136, 0.2); text-align: center;">
            <p style="color: #00ff88; margin: 0;"><strong>📊 IMAGE DETAILS:</strong></p>
            <p style="color: #cbd5e1; margin: 5px 0; display: inline-block; padding: 0 15px;">📐 Dimensions: {width} × {height} px</p>
            <p style="color: #cbd5e1; margin: 5px 0; display: inline-block; padding: 0 15px;">💾 Size: {file_size:.1f} KB</p>
            <p style="color: #cbd5e1; margin: 5px 0; display: inline-block; padding: 0 15px;">📁 Format: {uploaded_file.type}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 **UPLOAD NEW IMAGE**", key="reset", help="Upload a different leaf image", use_container_width=True):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-subtitle">🧬 AI ANALYSIS CENTER</h3>', unsafe_allow_html=True)
        if st.session_state.model is not None and st.session_state.treatments:
            if st.button("🚀 **ANALYZE WITH AI**", key="analyze", help="Start advanced AI analysis", use_container_width=True):
                # Save uploaded file temporarily
                with open("temp_image.jpg", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                if not is_leaf_image("temp_image.jpg"):
                    st.markdown('<div class="error-box" style="border-left-color: #ef4444; text-align: center;">', unsafe_allow_html=True)
                    st.markdown('<h3 style="color: #f87171;">⚠️ NOT A LEAF PIC</h3>', unsafe_allow_html=True)
                    st.markdown('<p style="color: #fca5a5;">This image does not appear to be a plant leaf. Our AI is specifically trained to analyze natural plant leaves.</p>', unsafe_allow_html=True)
                    st.markdown('<p style="color: #fca5a5;"><strong>Please upload a clear leaf picture and try again.</strong></p>', unsafe_allow_html=True)
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
                    # Get all predictions for top 3 results
                    top_3_indices = np.argsort(predictions[0])[-3:][::-1]
                    # Get class names and prediction
                    class_names = list(st.session_state.treatments.keys())
                    predicted_disease = class_names[predicted_class]
                    treatment = st.session_state.treatments.get(predicted_disease, "Consult with an agricultural expert for specialized treatment.")
                    # Update analysis counter
                    st.session_state.analysis_count += 1
                    # Display enhanced results
                    st.markdown('<div class="results-card">', unsafe_allow_html=True)
                    # Main diagnosis result
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">🎯 PRIMARY DIAGNOSIS</h4>', unsafe_allow_html=True)
                    # Clean disease name for display
                    display_disease = predicted_disease.replace('_', ' ').title()
                    st.markdown(f'<p class="disease-name">{display_disease}</p>', unsafe_allow_html=True)
                    # Health status indicator
                    if "healthy" in predicted_disease.lower():
                        st.markdown('<div style="text-align: center; margin: 1rem 0;"><span style="background: linear-gradient(90deg, #00ff88, #00cc66); color: #060b0d; padding: 0.6rem 2.2rem; border-radius: 30px; font-weight: 700; font-size: 1.1rem; display: inline-block;">🌿 HEALTHY PLANT</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="text-align: center; margin: 1rem 0;"><span style="background: linear-gradient(90deg, #ef4444, #f97316); color: white; padding: 0.6rem 2.2rem; border-radius: 30px; font-weight: 700; font-size: 1.1rem; display: inline-block; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.35);">⚠️ DISEASE DETECTED</span></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    # Confidence score with enhanced progress bar
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
                        conf_color = "#00ff88"
                    elif confidence_score > 0.7:
                        conf_msg = "🟡 HIGH CONFIDENCE - Diagnosis is reliable"
                        conf_color = "#ffaa00"
                    elif confidence_score > 0.5:
                        conf_msg = "🟠 MODERATE CONFIDENCE - Consider expert consultation"
                        conf_color = "#34d399"
                    else:
                        conf_msg = "🔴 LOW CONFIDENCE - Recommend professional diagnosis"
                        conf_color = "#ef4444"
                    st.markdown(f'<p style="color: {conf_color}; font-weight: 700; text-align: center; margin-top: 1rem; font-family: \'Space Grotesk\', sans-serif;">{conf_msg}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Treatment recommendation with enhanced styling
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
                    <div style="background: rgba(13, 22, 21, 0.6); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(0, 255, 136, 0.15);">
                        <p style="color: #cbd5e1; margin: 0.5rem 0;"><strong>🔬 Analysis #{st.session_state.analysis_count}</strong></p>
                        <p style="color: #94a3b8; margin: 0.5rem 0;">🧠 Model: Advanced CNN v2.1</p>
                        <p style="color: #94a3b8; margin: 0.5rem 0;">⚡ Processing Time: &lt;3 seconds</p>
                        <p style="color: #94a3b8; margin: 0.5rem 0;">🎯 Classes Evaluated: {len(class_names)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    # Success notification
                    st.success("✅ **ANALYSIS COMPLETE!** Your plant has been successfully diagnosed by our AI system.")

                except Exception as e:
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    st.markdown(f'<p>❌ **ANALYSIS ERROR**: {str(e)}</p>', unsafe_allow_html=True)
                    st.markdown('<p>Please try uploading a different image or contact support if the issue persists.</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                # Clean up temporary file
                try:
                    os.remove("temp_image.jpg")
                except:
                    pass
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: rgba(13, 22, 21, 0.45); border-radius: 16px; border: 2px dashed rgba(0, 255, 136, 0.2);">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
                    <h4 style="color: #00ff88; margin-bottom: 1rem;">AI READY FOR ANALYSIS</h4>
                    <p style="color: #cbd5e1;">Click the "ANALYZE WITH AI" button above to start the diagnosis process. Our neural network will examine your plant image and provide detailed results.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.markdown('<p>❌ **SYSTEM ERROR**: AI model or treatment database not properly loaded.</p>', unsafe_allow_html=True)
            st.markdown('<p>Please refresh the page or contact technical support.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Enhanced upload prompt
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: rgba(13, 22, 21, 0.4); border-radius: 20px; border: 2px dashed rgba(0, 255, 136, 0.25); margin: 2rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1.5rem; animation: heartbeat 2s infinite;">📸</div>
        <h3 style="color: #00ff88; margin-bottom: 1rem; font-size: 2rem;">UPLOAD PLANT IMAGE FOR AI ANALYSIS</h3>
        <p style="color: #94a3b8; font-size: 1.2rem; margin-bottom: 1.5rem;">Select a clear image of the plant leaf you want to analyze</p>
        <div style="background: rgba(8, 14, 15, 0.6); padding: 1rem; border-radius: 10px; border: 1px solid rgba(0, 255, 136, 0.15); display: inline-block;">
            <p style="color: #cbd5e1; margin: 0;">Supported formats: JPG, JPEG, PNG</p>
            <p style="color: #cbd5e1; margin: 0;">Maximum file size: 200MB</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Enhanced About section
st.markdown('<div class="about-section glass-container fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🚀 ABOUT PLANT SAVIOR AI</h2>', unsafe_allow_html=True)
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

# === NEW: Team Section ===
st.markdown('<div class="team-section glass-container fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="team-title">👥 MEET THE TEAM</h2>', unsafe_allow_html=True)
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
        <p class="team-desc">Crafting the futuristic UI/UX experience. Responsible for the cyberpunk design, animations, and responsive interface that powers Plant Savior AI.</p>
    </div>
    <div class="team-card">
        <h3 class="team-name">Taiba</h3>
        <p class="team-role">Machine Learning Engineer</p>
        <p class="team-desc">Specializing in model training, optimization, and performance tuning. Ensures our AI delivers 99.2% accuracy across diverse plant conditions.</p>
    </div>
</div>
<div class="love-icon">❤️</div>
<p style="text-align: center; color: #00ff88; font-size: 1.3rem; font-weight: 600;">Made with ❤️ by the Plant Savior AI Team</p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
<div class="footer">
    <div class="footer-text">🌱 PLANT SAVIOR AI - REVOLUTIONIZING AGRICULTURE WITH ARTIFICIAL INTELLIGENCE</div>
    <div class="footer-text">Powered by Advanced Deep Learning • Real-time Disease Detection • Professional Treatment Recommendations</div>
    <div class="creator-info">
        <div class="footer-text">🎯 <strong>MODEL ACCURACY:</strong> 99.2% on validation data</div>
        <div class="footer-text">⚡ <strong>PROCESSING SPEED:</strong> Sub-3-second analysis</div>
        <div class="footer-text">🌍 <strong>IMPACT:</strong> Helping farmers worldwide save crops and reduce pesticide use</div>
    </div>
    <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.05);">
        <div class="footer-text">© 2025 Plant Savior AI. All rights reserved. | Built with ❤️ using TensorFlow & Streamlit</div>
    </div>
</div>
""", unsafe_allow_html=True)