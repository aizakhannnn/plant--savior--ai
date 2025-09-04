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

# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI - Plant Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Cyberpunk CSS Design
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Exo 2', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6, .logo-text, .cyberpunk-text {
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
    }
    
    /* Main background and layout */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0ff;
        overflow-x: hidden;
    }
    
    /* Header Styles - Futuristic Cyberpunk */
    .main-header {
        background: linear-gradient(135deg, #00c9ff 0%, #1e60c4 100%);
        padding: 3rem 2rem;
        border-radius: 0;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(30, 96, 196, 0.7);
        position: relative;
        overflow: hidden;
        border-bottom: 3px solid #00f5ff;
        animation: pulse-border 3s infinite;
    }
    
    @keyframes pulse-border {
        0% { box-shadow: 0 0 5px rgba(0, 245, 255, 0.5); }
        50% { box-shadow: 0 0 25px rgba(0, 245, 255, 0.9); }
        100% { box-shadow: 0 0 5px rgba(0, 245, 255, 0.5); }
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
        transform: rotate(30deg);
    }
    
    .logo-text {
        font-size: 4.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.7);
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 2s infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #00dbde, 0 0 20px #00dbde; }
        to { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fc00ff, 0 0 40px #fc00ff; }
    }
    
    .tagline {
        font-size: 1.5rem;
        opacity: 0.95;
        font-weight: 300;
        max-width: 900px;
        margin: 0 auto;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
        color: #e0f7ff;
    }
    
    /* Glassmorphism Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
        padding: 2rem;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .glass-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 197, 255, 0.3);
        border: 1px solid rgba(0, 197, 255, 0.3);
    }
    
    /* How It Works Section - Futuristic */
    .how-it-works {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 197, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .section-title {
        color: #00f5ff;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2.5rem;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.7);
        position: relative;
        display: inline-block;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .section-title::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #00f5ff, transparent);
    }
    
    .steps-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 2rem;
    }
    
    .step-card {
        background: rgba(0, 30, 60, 0.6);
        border-radius: 15px;
        padding: 2rem 1.8rem;
        text-align: center;
        flex: 1;
        min-width: 250px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
        border: 1px solid rgba(0, 197, 255, 0.3);
        backdrop-filter: blur(5px);
        position: relative;
        overflow: hidden;
    }
    
    .step-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #00c9ff, #1e60c4);
    }
    
    .step-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 12px 40px rgba(0, 197, 255, 0.4);
        border: 1px solid rgba(0, 245, 255, 0.6);
    }
    
    .step-number {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #00c9ff 0%, #1e60c4 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-weight: bold;
        font-size: 1.5rem;
        box-shadow: 0 0 15px rgba(0, 197, 255, 0.5);
        border: 2px solid #00f5ff;
    }
    
    .step-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        color: #00f5ff;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.7);
    }
    
    .step-title {
        color: #00f5ff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-shadow: 0 0 5px rgba(0, 245, 255, 0.5);
    }
    
    /* Upload Section - Futuristic */
    .upload-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 197, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .upload-title {
        color: #00f5ff;
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.7);
    }
    
    /* Drop Zone - Futuristic */
    .drop-zone {
        border: 3px dashed #00f5ff;
        border-radius: 20px;
        padding: 3.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s ease;
        background: rgba(0, 30, 60, 0.3);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 197, 255, 0.2);
    }
    
    .drop-zone::before {
        content: "";
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: linear-gradient(45deg, #00c9ff, #1e60c4, #fc00ff, #00c9ff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        z-index: -1;
        border-radius: 25px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .drop-zone:hover {
        background: rgba(0, 50, 100, 0.4);
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(0, 197, 255, 0.4);
    }
    
    .drop-zone.active {
        background: rgba(0, 50, 100, 0.6);
        border-color: #ff2d95;
        box-shadow: 0 0 30px rgba(255, 45, 149, 0.6);
    }
    
    .upload-icon {
        font-size: 5rem;
        color: #00f5ff;
        margin-bottom: 1.8rem;
        text-shadow: 0 0 15px rgba(0, 245, 255, 0.8);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    
    .drop-text {
        font-size: 1.5rem;
        color: #e0f7ff;
        margin-bottom: 1rem;
        font-weight: 500;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    }
    
    .file-types {
        color: #a0d0ff;
        font-size: 1.1rem;
        margin-bottom: 1.8rem;
    }
    
    .browse-button {
        background: linear-gradient(135deg, #00c9ff 0%, #1e60c4 100%);
        color: white;
        border: none;
        padding: 1.2rem 2.5rem;
        border-radius: 50px;
        cursor: pointer;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 197, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 2px solid #00f5ff;
    }
    
    .browse-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 197, 255, 0.8);
        background: linear-gradient(135deg, #1e60c4 0%, #00c9ff 100%);
    }
    
    .file-input {
        display: none;
    }
    
    /* Analysis Section - Futuristic */
    .analysis-section {
        display: flex;
        gap: 2.5rem;
        flex-wrap: wrap;
        margin-bottom: 2.5rem;
    }
    
    .image-preview-container {
        flex: 1;
        min-width: 300px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 197, 255, 0.2);
    }
    
    .results-container {
        flex: 1;
        min-width: 300px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 197, 255, 0.2);
    }
    
    .section-subtitle {
        color: #00f5ff;
        font-size: 1.8rem;
        margin-bottom: 2rem;
        font-weight: 700;
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.7);
    }
    
    .preview-image {
        width: 100%;
        max-height: 400px;
        object-fit: contain;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0, 197, 255, 0.3);
        border: 2px solid rgba(0, 245, 255, 0.3);
    }
    
    .reset-button {
        background: linear-gradient(135deg, #ff2d95 0%, #b30062 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 2rem;
        width: 100%;
        box-shadow: 0 0 15px rgba(255, 45, 149, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 2px solid #ff2d95;
    }
    
    .reset-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(255, 45, 149, 0.7);
        background: linear-gradient(135deg, #b30062 0%, #ff2d95 100%);
    }
    
    /* Loading State - Futuristic */
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .spinner {
        width: 80px;
        height: 80px;
        border: 5px solid rgba(0, 197, 255, 0.3);
        border-top: 5px solid #00f5ff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 2rem;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-size: 1.5rem;
        color: #00f5ff;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.7);
    }
    
    .loading-subtext {
        color: #a0d0ff;
        margin-top: 0.8rem;
        font-size: 1.1rem;
    }
    
    /* Results Card - Futuristic */
    .results-card {
        background: rgba(0, 30, 60, 0.6);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 197, 255, 0.3);
    }
    
    .result-item {
        margin-bottom: 2rem;
        padding: 1.5rem;
        border-radius: 12px;
        background: rgba(0, 20, 40, 0.4);
        border: 1px solid rgba(0, 197, 255, 0.2);
    }
    
    .result-title {
        color: #00f5ff;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        text-shadow: 0 0 5px rgba(0, 245, 255, 0.5);
    }
    
    .disease-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.7);
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Progress Bar - Futuristic */
    .progress-container {
        margin: 1.5rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.8rem;
        font-weight: 500;
        color: #e0f7ff;
    }
    
    .progress-bar-bg {
        width: 100%;
        height: 16px;
        background-color: rgba(0, 30, 60, 0.6);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(0, 197, 255, 0.3);
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #00c9ff, #00f5ff);
        border-radius: 10px;
        transition: width 1.5s ease-in-out;
        box-shadow: 0 0 15px rgba(0, 245, 255, 0.7);
        position: relative;
    }
    
    .progress-bar-fill::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shine 2s infinite;
    }
    
    @keyframes shine {
        0% { background-position: -100% 0; }
        100% { background-position: 100% 0; }
    }
    
    .confidence-text {
        font-weight: 700;
        color: #00f5ff;
        text-shadow: 0 0 5px rgba(0, 245, 255, 0.7);
        font-size: 1.2rem;
    }
    
    /* Treatment Box - Futuristic */
    .treatment-box {
        background: rgba(0, 40, 80, 0.5);
        border-left: 4px solid #00f5ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 0.8rem;
        box-shadow: 0 0 15px rgba(0, 197, 255, 0.3);
        border: 1px solid rgba(0, 197, 255, 0.2);
    }
    
    .treatment-text {
        line-height: 1.7;
        color: #e0f7ff;
        font-size: 1.1rem;
    }
    
    /* Analyze Button - Futuristic */
    .analyze-button {
        background: linear-gradient(135deg, #00c9ff 0%, #1e60c4 100%);
        color: white;
        border: none;
        padding: 1.5rem;
        border-radius: 15px;
        cursor: pointer;
        font-size: 1.3rem;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 0 25px rgba(0, 197, 255, 0.6);
        margin-top: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        border: 2px solid #00f5ff;
    }
    
    .analyze-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 197, 255, 0.8);
        background: linear-gradient(135deg, #1e60c4 0%, #00c9ff 100%);
    }
    
    .analyze-button:disabled {
        background: #2a2a4a;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
        border: 1px solid #444466;
    }
    
    /* Error Message - Futuristic */
    .error-box {
        background: rgba(100, 0, 40, 0.3);
        border-left: 4px solid #ff2d95;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        color: #ff7eb9;
        box-shadow: 0 0 15px rgba(255, 45, 149, 0.3);
        border: 1px solid rgba(255, 45, 149, 0.2);
    }
    
    /* About Section - Futuristic */
    .about-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 197, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .about-content {
        max-width: 1000px;
        margin: 0 auto;
        text-align: center;
    }
    
    .about-text {
        font-size: 1.2rem;
        line-height: 1.8;
        color: #c0d8ff;
        margin-bottom: 2.5rem;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
    }
    
    .stats-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 2.5rem;
        margin-top: 2rem;
    }
    
    .stat-card {
        background: rgba(0, 30, 60, 0.6);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        min-width: 200px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 197, 255, 0.3);
        backdrop-filter: blur(5px);
    }
    
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0, 197, 255, 0.4);
        border: 1px solid rgba(0, 245, 255, 0.6);
    }
    
    .stat-value {
        font-size: 2.8rem;
        font-weight: 700;
        color: #00f5ff;
        margin-bottom: 0.8rem;
        text-shadow: 0 0 15px rgba(0, 245, 255, 0.7);
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #a0d0ff;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Footer - Futuristic */
    .footer {
        background: linear-gradient(135deg, #00c9ff 0%, #1e60c4 100%);
        color: white;
        text-align: center;
        padding: 2.5rem;
        border-radius: 0;
        margin-top: 2.5rem;
        box-shadow: 0 0 30px rgba(30, 96, 196, 0.7);
        border-top: 3px solid #00f5ff;
    }
    
    .footer-text {
        font-size: 1.2rem;
        opacity: 0.95;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.7);
        margin: 0.5rem 0;
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: rgba(10, 15, 40, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 197, 255, 0.3);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #00f5ff !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #c0d8ff !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .logo-text {
            font-size: 3rem;
        }
        
        .tagline {
            font-size: 1.2rem;
        }
        
        .steps-container {
            flex-direction: column;
        }
        
        .analysis-section {
            flex-direction: column;
        }
        
        .drop-zone {
            padding: 2.5rem 1.5rem;
        }
        
        .stat-card {
            min-width: 150px;
            padding: 1.5rem;
        }
        
        .stat-value {
            font-size: 2.2rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 2rem 1rem;
        }
        
        .logo-text {
            font-size: 2.5rem;
        }
        
        .tagline {
            font-size: 1.1rem;
        }
        
        .upload-section, .about-section, .image-preview-container, .results-container {
            padding: 1.8rem;
        }
        
        .step-card {
            min-width: 100%;
        }
        
        .upload-icon {
            font-size: 3.5rem;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(10, 15, 40, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00c9ff, #1e60c4);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #1e60c4, #00c9ff);
    }
</style>
""", unsafe_allow_html=True)

# Main header with futuristic design
st.markdown("""
<div class="main-header">
    <h1 class="logo-text">🌱 PLANT SAVIOR AI</h1>
    <p class="tagline">INSTANT PLANT DISEASE DETECTION USING ADVANCED ARTIFICIAL INTELLIGENCE</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with futuristic design
with st.sidebar:
    st.markdown("### 🌿 ABOUT THIS TOOL")
    st.info("""
    THIS CYBERPUNK AI SYSTEM HELPS FARMERS AND GARDENERS DETECT PLANT DISEASES 
    FROM LEAF IMAGES WITH HIGH ACCURACY.
    
    UPLOAD A CLEAR PHOTO OF A PLANT LEAF AND GET INSTANT DIAGNOSIS WITH 
    TREATMENT RECOMMENDATIONS.
    """)
    
    st.markdown("### 📋 HOW TO GET BEST RESULTS")
    st.markdown("""
    1. **LIGHTING**: TAKE PHOTO IN GOOD NATURAL LIGHT
    2. **FOCUS**: ENSURE LEAF IS IN SHARP FOCUS
    3. **BACKGROUND**: SIMPLE BACKGROUND WORKS BEST
    4. **ANGLE**: TOP-DOWN VIEW OF THE LEAF
    5. **SYMPTOMS**: SHOW AFFECTED AREAS CLEARLY
    """)
    
    st.markdown("### 🎯 SUPPORTED DISEASES")
    st.markdown("""
    - TOMATO DISEASES (10 TYPES)
    - POTATO DISEASES (3 TYPES)
    - PEPPER DISEASES (2 TYPES)
    """)
    
    st.markdown("### ℹ️ NEED HELP?")
    st.markdown("CONTACT: SUPPORT@PLANTSAVIOR.AI")

# How it works section with futuristic design
st.markdown('<div class="how-it-works glass-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">HOW IT WORKS</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="steps-container">
    <div class="step-card">
        <div class="step-number">1</div>
        <div class="step-icon">📸</div>
        <h3 class="step-title">UPLOAD IMAGE</h3>
        <p>TAKE A CLEAR PHOTO OF THE AFFECTED PLANT LEAF AND UPLOAD IT TO OUR SYSTEM</p>
    </div>
    <div class="step-card">
        <div class="step-number">2</div>
        <div class="step-icon">🤖</div>
        <h3 class="step-title">AI ANALYSIS</h3>
        <p>OUR ADVANCED AI MODEL ANALYZES THE IMAGE TO DETECT ANY PLANT DISEASES</p>
    </div>
    <div class="step-card">
        <div class="step-number">3</div>
        <div class="step-icon">📊</div>
        <h3 class="step-title">GET RESULTS</h3>
        <p>RECEIVE INSTANT DIAGNOSIS WITH CONFIDENCE SCORE AND TREATMENT RECOMMENDATIONS</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Function to load model directly
@st.cache_resource
def load_model():
    """Load the trained model directly"""
    try:
        st.sidebar.info("📥 LOADING AI MODEL...")
        model = tf.keras.models.load_model('best_plant_model_final.keras')
        st.sidebar.success("✅ AI MODEL READY!")
        return model
    except Exception as e:
        st.sidebar.error(f"❌ ERROR LOADING MODEL: {str(e)}")
        return None

# Load treatment dictionary
@st.cache_resource
def load_treatments():
    """Load treatment recommendations"""
    try:
        with open('treatment_dict_complete.json', 'r') as f:
            treatments = json.load(f)
        st.sidebar.success("✅ TREATMENT DATABASE READY!")
        return treatments
    except Exception as e:
        st.sidebar.error(f"❌ ERROR LOADING TREATMENTS: {str(e)}")
        return {}

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.treatments = {}

# Load model and treatments
if st.session_state.model is None:
    with st.spinner("INITIALIZING PLANT SAVIOR AI SYSTEM..."):
        model = load_model()
        treatments = load_treatments()
        st.session_state.model = model
        st.session_state.treatments = treatments

# Main content area
st.markdown('<div class="upload-section glass-container">', unsafe_allow_html=True)
st.markdown('<h2 class="upload-title">UPLOAD PLANT LEAF IMAGE</h2>', unsafe_allow_html=True)

# File uploader with enhanced UI
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Analysis section with two columns
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    
    # Left column - Image preview
    st.markdown('<div class="image-preview-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-subtitle">UPLOADED IMAGE</h3>', unsafe_allow_html=True)
    
    image = Image.open(uploaded_file)
    st.image(image, caption="UPLOADED LEAF IMAGE", use_column_width=True, clamp=True)
    
    if st.button("📤 UPLOAD DIFFERENT IMAGE", key="reset", help="UPLOAD A DIFFERENT IMAGE"):
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Right column - Results
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-subtitle">ANALYSIS RESULTS</h3>', unsafe_allow_html=True)
    
    if st.session_state.model is not None and st.session_state.treatments:
        if st.button("🔍 ANALYZE LEAF", key="analyze", help="START AI ANALYSIS OF THE UPLOADED IMAGE"):
            with st.spinner(""):
                try:
                    # Save uploaded file temporarily
                    with open("temp_image.jpg", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
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
                    treatment = st.session_state.treatments.get(predicted_disease, "CONSULT AGRICULTURAL EXPERT.")
                    
                    # Display results in enhanced card
                    st.markdown('<div class="results-card">', unsafe_allow_html=True)
                    
                    # Disease prediction
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">🪴 PREDICTED DISEASE</h4>', unsafe_allow_html=True)
                    st.markdown(f'<p class="disease-name">{predicted_disease}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Confidence score with enhanced progress bar
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">📊 CONFIDENCE SCORE</h4>', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="progress-container">
                            <div class="progress-label">
                                <span>CONFIDENCE LEVEL</span>
                                <span class="confidence-text">{confidence_score*100:.1f}%</span>
                            </div>
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill" style="width: {confidence_score*100}%"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Treatment recommendation
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">🌿 TREATMENT RECOMMENDATION</h4>', unsafe_allow_html=True)
                    st.markdown(f'<div class="treatment-box"><p class="treatment-text">{treatment}</p></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ ERROR DURING PREDICTION: {str(e)}</div>', unsafe_allow_html=True)
                
                # Clean up temporary file
                try:
                    os.remove("temp_image.jpg")
                except:
                    pass
        else:
            st.info("👆 CLICK 'ANALYZE LEAF' TO START THE AI DIAGNOSIS")
    else:
        st.markdown('<div class="error-box">❌ AI SYSTEM NOT INITIALIZED. PLEASE CHECK THE SIDEBAR FOR ERROR MESSAGES.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Enhanced upload interface
    st.markdown("""
    <div class="drop-zone" id="dropZone">
        <div class="upload-icon">📁</div>
        <p class="drop-text">DRAG & DROP YOUR IMAGE HERE</p>
        <p class="file-types">SUPPORTED FORMATS: JPG, PNG, JPEG (MAX 200MB)</p>
        <button class="browse-button" onclick="document.getElementById('fileInput').click()">BROWSE FILES</button>
        <input type="file" id="fileInput" class="file-input" accept="image/jpeg,image/png,image/jpg">
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **TIP**: FOR BEST RESULTS, TAKE A CLEAR PHOTO OF THE AFFECTED LEAF WITH GOOD LIGHTING AND UPLOAD IN JPG OR PNG FORMAT.")

st.markdown('</div>', unsafe_allow_html=True)

# About section with futuristic design
st.markdown('<div class="about-section glass-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">ABOUT PLANT SAVIOR AI</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="about-content">
    <p class="about-text">
        PLANT SAVIOR AI IS AN ADVANCED ARTIFICIAL INTELLIGENCE SYSTEM DESIGNED TO HELP FARMERS, GARDENERS, 
        AND AGRICULTURAL PROFESSIONALS QUICKLY IDENTIFY PLANT DISEASES FROM LEAF IMAGES. OUR SYSTEM USES 
        DEEP LEARNING TECHNOLOGY TRAINED ON THOUSANDS OF PLANT IMAGES TO PROVIDE ACCURATE DIAGNOSES WITH 
        TREATMENT RECOMMENDATIONS, HELPING TO SAVE CROPS AND REDUCE THE USE OF UNNECESSARY PESTICIDES.
    </p>
    
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-value">91.02%</div>
            <div class="stat-label">ACCURACY RATE</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">38</div>
            <div class="stat-label">DISEASE TYPES</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">224×224</div>
            <div class="stat-label">IMAGE RESOLUTION</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">24/7</div>
            <div class="stat-label">AVAILABILITY</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer with futuristic design
st.markdown("""
<div class="footer">
    <p class="footer-text">🌱 PLANT SAVIOR AI - MAKING AGRICULTURE SMARTER WITH AI TECHNOLOGY</p>
    <p class="footer-text">© 2025 PLANT SAVIOR AI. ALL RIGHTS RESERVED.</p>
</div>
""", unsafe_allow_html=True)