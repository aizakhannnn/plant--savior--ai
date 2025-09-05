import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json
from PIL import Image
import os

# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI - Plant Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for the professional design
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background and layout */
    .stApp {
        background: linear-gradient(135deg, #e0f7e0 0%, #c8f2d1 100%);
        color: #333333;
        overflow-x: hidden;
    }
    
    /* Interactive elements */
    .interactive-card {
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .interactive-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 24px rgba(46, 125, 50, 0.25) !important;
    }
    
    /* Animated badges */
    .badge {
        display: inline-block;
        padding: 0.25em 0.75em;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin: 0 0.25em;
        animation: pulse 2s infinite;
    }
    
    .badge-primary {
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        color: white;
    }
    
    .badge-secondary {
        background: linear-gradient(135deg, #2196F3, #0D47A1);
        color: white;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    
    /* Floating animation */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Bounce animation */
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-20px);}
        60% {transform: translateY(-10px);}
    }
    
    .bounce {
        animation: bounce 2s infinite;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        padding: 3rem 2rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border-radius: 0 0 20px 20px;
        position: relative;
        overflow: hidden;
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
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 2;
    }
    
    .tagline {
        font-size: 1.3rem;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto;
        opacity: 0.95;
        position: relative;
        z-index: 2;
    }
    
    /* Container Styles */
    .section-container {
        max-width: 1300px;
        margin: 0 auto 2rem;
        padding: 0 1.5rem;
    }
    
    /* Glass Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-container:hover {
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
        transform: translateY(-5px);
    }
    
    /* Section Title */
    .section-title {
        color: #2E7D32;
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 2.5rem;
        font-weight: 700;
        position: relative;
    }
    
    .section-title::after {
        content: "";
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #FF9800, #4CAF50);
        border-radius: 2px;
    }
    
    /* Steps Section */
    .steps-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 2rem;
        margin-top: 2.5rem;
    }
    
    .step-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 2rem 1.8rem;
        text-align: center;
        flex: 1;
        min-width: 250px;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        transition: all 0.4s ease;
        border: 1px solid rgba(46, 125, 50, 0.1);
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
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
    }
    
    .step-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 24px rgba(46, 125, 50, 0.2);
        border-color: rgba(46, 125, 50, 0.3);
    }
    
    .step-number {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.2rem;
        font-weight: 700;
        font-size: 1.3rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .step-icon {
        font-size: 3rem;
        margin-bottom: 1.2rem;
        color: #4CAF50;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    .step-title {
        color: #2E7D32;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .step-description {
        color: #555;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Upload Section */
    .upload-section {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
    }
    
    .upload-title {
        color: #2E7D32;
        text-align: center;
        font-size: 2rem;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    /* File Uploader */
    .file-uploader {
        border: 3px dashed #4CAF50;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(232, 245, 233, 0.5) 0%, rgba(200, 230, 201, 0.3) 100%);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .file-uploader:hover {
        background: linear-gradient(135deg, rgba(220, 237, 221, 0.7) 0%, rgba(185, 225, 187, 0.5) 100%);
        border-color: #2E7D32;
        transform: scale(1.02);
    }
    
    .file-uploader::before {
        content: "";
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: linear-gradient(45deg, transparent, rgba(76, 175, 80, 0.1), transparent);
        z-index: 0;
        animation: borderAnimation 3s linear infinite;
    }
    
    @keyframes borderAnimation {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .upload-icon {
        font-size: 4rem;
        color: #2E7D32;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .upload-text {
        font-size: 1.3rem;
        color: #2E7D32;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .file-types {
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.8rem;
    }
    
    /* Analysis Section */
    .analysis-section {
        display: flex;
        gap: 2.5rem;
        flex-wrap: wrap;
        margin-bottom: 2.5rem;
    }
    
    .image-preview-container {
        flex: 1;
        min-width: 350px;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .image-preview-container:hover {
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
    }
    
    .results-container {
        flex: 1;
        min-width: 350px;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .results-container:hover {
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
    }
    
    .section-subtitle {
        color: #2E7D32;
        font-size: 1.7rem;
        margin-bottom: 1.8rem;
        font-weight: 700;
        text-align: center;
    }
    
    .preview-image {
        width: 100%;
        max-height: 400px;
        object-fit: contain;
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(46, 125, 50, 0.1);
    }
    
    .reset-button {
        background: linear-gradient(135deg, #9E9E9E, #616161);
        color: white;
        border: none;
        padding: 1rem 1.8rem;
        border-radius: 12px;
        cursor: pointer;
        font-size: 1.05rem;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1.5rem;
        width: 100%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .reset-button:hover {
        background: linear-gradient(135deg, #757575, #424242);
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    }
    
    /* Loading State */
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .spinner {
        width: 60px;
        height: 60px;
        border: 5px solid rgba(46, 125, 50, 0.2);
        border-top: 5px solid #2E7D32;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-size: 1.3rem;
        color: #2E7D32;
        font-weight: 600;
    }
    
    .loading-subtext {
        color: #666;
        margin-top: 0.7rem;
        font-size: 1rem;
    }
    
    /* Results Card */
    .results-card {
        background: rgba(241, 248, 233, 0.7);
        border-radius: 14px;
        padding: 2rem;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 187, 106, 0.3);
        margin-bottom: 1.5rem;
    }
    
    .result-item {
        margin-bottom: 1.8rem;
    }
    
    .result-item:last-child {
        margin-bottom: 0;
    }
    
    .result-title {
        color: #2E7D32;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    
    .disease-name {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2E7D32;
        text-align: center;
        margin: 1rem 0;
        padding: 1.2rem;
        background: linear-gradient(135deg, rgba(232, 245, 233, 0.8) 0%, rgba(200, 230, 201, 0.6) 100%);
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* Progress Bar */
    .progress-container {
        margin: 1.2rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.7rem;
        font-weight: 600;
        font-size: 1.05rem;
    }
    
    .progress-bar-bg {
        width: 100%;
        height: 16px;
        background-color: #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        border-radius: 8px;
        transition: width 1.5s cubic-bezier(0.22, 0.61, 0.36, 1);
        position: relative;
    }
    
    .progress-bar-fill::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: progressGlow 2s infinite;
    }
    
    @keyframes progressGlow {
        0% { opacity: 0; }
        50% { opacity: 1; }
        100% { opacity: 0; }
    }
    
    .confidence-text {
        font-weight: 700;
        color: #2E7D32;
        font-size: 1.1rem;
    }
    
    /* Treatment Box */
    .treatment-box {
        background: linear-gradient(135deg, rgba(232, 245, 233, 0.9) 0%, rgba(200, 230, 201, 0.7) 100%);
        border-left: 5px solid #4CAF50;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 0.7rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .treatment-text {
        line-height: 1.7;
        color: #333;
        font-size: 1.05rem;
        font-weight: 500;
    }
    
    /* Analyze Button */
    .analyze-button {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        color: white;
        border: none;
        padding: 1.2rem;
        border-radius: 12px;
        cursor: pointer;
        font-size: 1.2rem;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 6px 16px rgba(46, 125, 50, 0.4);
        margin-top: 1.2rem;
        letter-spacing: 0.5px;
    }
    
    .analyze-button:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 24px rgba(46, 125, 50, 0.5);
        background: linear-gradient(135deg, #1B5E20 0%, #388E3C 100%);
    }
    
    .analyze-button:disabled {
        background: #BDBDBD;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    /* Error Message */
    .error-box {
        background: linear-gradient(135deg, rgba(255, 235, 238, 0.9) 0%, rgba(248, 220, 222, 0.7) 100%);
        border-left: 5px solid #F44336;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        color: #B71C1C;
        font-size: 1.05rem;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* About Section */
    .about-section {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 3rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .about-section:hover {
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
    }
    
    .about-content {
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
    }
    
    .about-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #444;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white;
        text-align: center;
        padding: 2.5rem;
        margin-top: 2.5rem;
        border-radius: 20px 20px 0 0;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
    }
    
    .footer-text {
        font-size: 1.1rem;
        opacity: 0.95;
        margin: 0.3rem 0;
        font-weight: 400;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, rgba(224, 247, 250, 0.9) 0%, rgba(178, 235, 242, 0.7) 100%);
        border-left: 5px solid #00BCD4;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        color: #006064;
        font-size: 1.05rem;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-right: 1px solid rgba(46, 125, 50, 0.2);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #2E7D32 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: #333 !important;
        font-weight: 500;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .logo-text {
            font-size: 2.2rem;
        }
        
        .tagline {
            font-size: 1.1rem;
        }
        
        .steps-container {
            flex-direction: column;
        }
        
        .analysis-section {
            flex-direction: column;
        }
        
        .file-uploader {
            padding: 2rem 1.2rem;
        }
        
        .section-title {
            font-size: 1.8rem;
        }
        
        .upload-title {
            font-size: 1.7rem;
        }
        
        .upload-section, .about-section, .image-preview-container, .results-container {
            padding: 1.8rem;
        }
        
        .step-card {
            min-width: 100%;
        }
        
        .section-subtitle {
            font-size: 1.4rem;
        }
        
        .disease-name {
            font-size: 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 1.8rem 1rem;
        }
        
        .logo-text {
            font-size: 1.8rem;
        }
        
        .tagline {
            font-size: 1rem;
        }
        
        .upload-section, .about-section, .image-preview-container, .results-container {
            padding: 1.5rem;
        }
        
        .section-subtitle {
            font-size: 1.3rem;
        }
        
        .upload-text {
            font-size: 1.1rem;
        }
        
        .step-icon {
            font-size: 2.5rem;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #e8f5e9;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #388E3C, #1B5E20);
    }
    
    /* Animation for results */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)

# Main header with enhanced professional design
st.markdown("""
<div class="main-header">
    <h1 class="logo-text floating">🌱 Plant Savior AI</h1>
    <p class="tagline">Advanced AI for Instant Plant Disease Detection & Treatment Recommendations</p>
</div>
""", unsafe_allow_html=True)

# Enhanced sidebar with additional information
with st.sidebar:
    st.markdown("### 🌿 About This Tool")
    st.info("""
    This AI-powered system helps farmers and gardeners detect plant diseases from leaf images with high accuracy.
    
    Simply upload a clear photo of a plant leaf and get instant diagnosis with treatment recommendations.
    """)
    
    st.markdown("### 📋 How to Get Best Results <span class='badge badge-secondary'>TIPS</span>", unsafe_allow_html=True)
    st.markdown("""
    1. **Lighting**: Take photo in good natural light
    2. **Focus**: Ensure leaf is in sharp focus
    3. **Background**: Simple background works best
    4. **Angle**: Top-down view of the leaf
    5. **Symptoms**: Show affected areas clearly
    """)
    
    st.markdown("### 🎯 Supported Diseases <span class='badge badge-primary'>38 TYPES</span>", unsafe_allow_html=True)
    st.markdown("""
    - Apple diseases (4 types)
    - Blueberry healthy
    - Cherry diseases (2 types)
    - Corn diseases (4 types)
    - Grape diseases (4 types)
    - Orange disease (1 type)
    - Peach disease (1 type)
    - Pepper diseases (2 types)
    - Potato diseases (3 types)
    - Raspberry healthy
    - Soybean healthy
    - Squash Powdery mildew
    - Strawberry diseases (2 types)
    - Tomato diseases (10 types)
    """)
    
    st.markdown("### ℹ️ Need Help?")
    st.markdown("Contact: support@plantsavior.ai")

# How it works section with enhanced professional design
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="steps-container">
    <div class="step-card interactive-card">
        <div class="step-number">1</div>
        <div class="step-icon">📸</div>
        <h3 class="step-title">Upload Image</h3>
        <p class="step-description">Take a clear photo of the affected plant leaf and upload it to our system</p>
    </div>
    <div class="step-card interactive-card">
        <div class="step-number">2</div>
        <div class="step-icon bounce">🤖</div>
        <h3 class="step-title">AI Analysis</h3>
        <p class="step-description">Our advanced AI model analyzes the image to detect any plant diseases</p>
    </div>
    <div class="step-card interactive-card">
        <div class="step-number">3</div>
        <div class="step-icon">📊</div>
        <h3 class="step-title">Get Results</h3>
        <p class="step-description">Receive instant diagnosis with confidence score and treatment recommendations</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Function to load model directly
@st.cache_resource
def load_model():
    """Load the trained model directly"""
    try:
        st.sidebar.info("📥 Loading AI model...")
        model = tf.keras.models.load_model('best_plant_model_final.keras')
        st.sidebar.success("✅ AI Model ready!")
        return model
    except Exception as e:
        st.sidebar.error(f"❌ Error loading model: {str(e)}")
        return None

# Load treatment dictionary
@st.cache_resource
def load_treatments():
    """Load treatment recommendations"""
    try:
        with open('treatment_dict_complete.json', 'r') as f:
            treatments = json.load(f)
        st.sidebar.success("✅ Treatment database ready!")
        return treatments
    except Exception as e:
        st.sidebar.error(f"❌ Error loading treatments: {str(e)}")
        return {}

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.treatments = {}

# Load model and treatments
if st.session_state.model is None:
    with st.spinner("🚀 Initializing Plant Savior AI System..."):
        model = load_model()
        treatments = load_treatments()
        st.session_state.model = model
        st.session_state.treatments = treatments

# Main content area with enhanced design
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown('<h2 class="upload-title">Upload Plant Leaf Image <span class="badge badge-primary">NEW</span></h2>', unsafe_allow_html=True)

# File uploader with enhanced UI
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Analysis section with two columns
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    
    # Left column - Image preview
    st.markdown('<div class="image-preview-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-subtitle">Uploaded Image</h3>', unsafe_allow_html=True)
    
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Leaf Image", use_column_width=True, clamp=True)
    
    if st.button("📤 Upload Different Image", key="reset", help="Upload a different image"):
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Right column - Results
    st.markdown('<div class="results-container interactive-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-subtitle">Analysis Results</h3>', unsafe_allow_html=True)
    
    if st.session_state.model is not None and st.session_state.treatments:
        if st.button("🔍 Analyze Leaf", key="analyze", help="Start AI analysis of the uploaded image", 
                     type="primary"):
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
                    treatment = st.session_state.treatments.get(predicted_disease, "Consult agricultural expert.")
                    
                    # Display results in enhanced card with animation
                    st.markdown('<div class="results-card fade-in">', unsafe_allow_html=True)
                    
                    # Disease prediction
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">🪴 Predicted Disease</h4>', unsafe_allow_html=True)
                    st.markdown(f'<p class="disease-name">{predicted_disease}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Confidence score with enhanced progress bar
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">📊 Confidence Score</h4>', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="progress-container">
                            <div class="progress-label">
                                <span>Confidence Level</span>
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
                    st.markdown('<h4 class="result-title">🌿 Treatment Recommendation</h4>', unsafe_allow_html=True)
                    st.markdown(f'<div class="treatment-box"><p class="treatment-text">{treatment}</p></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Error during prediction: {str(e)}</div>', unsafe_allow_html=True)
                
                # Clean up temporary file
                try:
                    os.remove("temp_image.jpg")
                except:
                    pass
        else:
            st.info("👆 Click 'Analyze Leaf' to start the AI diagnosis")
    else:
        st.markdown('<div class="error-box">❌ AI system not initialized. Please check the sidebar for error messages.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Enhanced upload interface
    st.markdown("""
    <div class="file-uploader">
        <div class="upload-icon floating">📁</div>
        <p class="upload-text">Drag & Drop your image here</p>
        <p class="file-types">Supported formats: JPG, PNG, JPEG (Max 200MB)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">💡 <strong>Tip:</strong> For best results, take a clear photo of the affected leaf with good lighting and upload in JPG or PNG format.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# About section with enhanced professional design
st.markdown('<div class="about-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">About Plant Savior AI <span class="badge badge-primary">AI POWERED</span></h2>', unsafe_allow_html=True)
st.markdown("""
<div class="about-content">
    <p class="about-text">
        Plant Savior AI is an advanced artificial intelligence system designed to help farmers, gardeners, 
        and agricultural professionals quickly identify plant diseases from leaf images. Our system uses 
        deep learning technology trained on thousands of plant images to provide accurate diagnoses with 
        treatment recommendations, helping to save crops and reduce the use of unnecessary pesticides.
    </p>
    <p class="about-text">
        Our AI model can detect over 30 different plant diseases across various crops including tomatoes, 
        potatoes, peppers, apples, and more. With an accuracy rate exceeding 95%, Plant Savior AI is a 
        trusted tool for rapid disease identification in agricultural settings.
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer with enhanced professional design
st.markdown("""
<div class="footer">
    <p class="footer-text">🌱 Plant Savior AI - Making agriculture smarter with AI technology</p>
    <p class="footer-text">© 2025 Plant Savior AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)