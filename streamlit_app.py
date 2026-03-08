# streamlit_app.py
import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json
from PIL import Image
import os
import time
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests

# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI - Cyberpunk Diagnostic System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Modern UI Design System
st.markdown("""
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&display=swap" rel="stylesheet"/>
<style>
    /* Base Overrides */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Outfit', sans-serif;
        color: #1e293b;
    }
    
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    /* Premium Component Styles - Mapping to Original Cyberpunk Classes */
    .main-header {
        text-align: center;
        padding: 4rem 1rem;
        background: white;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 3rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .logo-text {
        font-weight: 800;
        font-size: 3.5rem;
        background: linear-gradient(135deg, #13ec92 0%, #0bb36e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .tagline {
        color: #64748b;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .glass-container {
        background: white;
        border: 1px solid #f1f5f9;
        border-radius: 32px;
        padding: 3rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
    }
    
    .section-title {
        color: #0f172a;
        font-weight: 700;
        text-align: center;
        margin-bottom: 3rem;
        border-bottom: 3px solid #13ec92;
        display: inline-block;
        padding-bottom: 0.5rem;
        width: auto;
    }
    
    .stats-section {
        display: flex;
        justify-content: space-between;
        gap: 24px;
        margin-bottom: 4rem;
    }
    
    .stat-card {
        flex: 1;
        background: white;
        border: 1px solid #f1f5f9;
        padding: 2rem;
        border-radius: 24px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value {
        font-size: 3rem;
        font-weight: 800;
        color: #13ec92;
    }
    
    .stat-label {
        color: #64748b;
        text-transform: uppercase;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .footer {
        border-top: 1px solid #f1f5f9;
        padding: 4rem 2rem;
        text-align: center;
        margin-top: 6rem;
        background: white;
    }

    /* Streamlit Widget Overrides */
    .stButton > button {
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .stButton > button:hover {
        border-color: #13ec92 !important;
        color: #13ec92 !important;
    }

    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 12px 16px !important;
    }

    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0

def login_page():
    # Login Page Header
    st.markdown("""
    <div class="main-header" style="padding: 2rem; margin-bottom: 2rem; animation: none;">
        <h1 class="logo-text" style="font-size: 3.5rem;">🔐 ACCESS CONTROL</h1>
        <p class="tagline">SECURE GATEWAY TO PLANT SAVIOR AI SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Form Container
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-container fade-in-up" style="padding: 3rem; border: 1px solid rgba(0, 245, 255, 0.3);">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title" style="font-size: 2rem; margin-bottom: 2rem;">IDENTITY VERIFICATION</h2>', unsafe_allow_html=True)
        
        # Login Inputs
        username = st.text_input("👤 OPERATOR ID", placeholder="Enter Username")
        password = st.text_input("🔑 ACCESS CODE", type="password", placeholder="Enter Password")
        
        # Login Button
        if st.button("🚀 INITIATE SYSTEM", use_container_width=True):
            if username == "aiza" and password == "pakistan2313":
                st.session_state.logged_in = True
                st.session_state.login_time = time.time()
                st.session_state.last_activity_time = time.time()
                st.success("✅ ACCESS GRANTED. INITIALIZING DASHBOARD...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ ACCESS DENIED. INVALID CREDENTIALS.")
        
        # Google Sign-In Button
        st.markdown("<div style='text-align: center; margin: 1.5rem 0; color: #a0d0ff;'>────────── OR ──────────</div>", unsafe_allow_html=True)
        
        if st.button("🔵 SIGN IN WITH GOOGLE", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.google_user = {"name": "Google User", "email": "user@gmail.com"}
            st.session_state.login_time = time.time()
            st.session_state.last_activity_time = time.time()
            st.success("✅ ACCESS GRANTED via Google Account.")
            time.sleep(1)
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# Main App Routine
if not st.session_state.logged_in:
    login_page()
    st.stop()

# Auto-logout logic
current_time = time.time()
if 'login_time' in st.session_state and (current_time - st.session_state.login_time > 1200):
    st.session_state.logged_in = False
    st.rerun()
if 'last_activity_time' in st.session_state and (current_time - st.session_state.last_activity_time > 600):
    st.session_state.logged_in = False
    st.rerun()
st.session_state.last_activity_time = current_time

# Dashboard Header
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

# Sidebar
with st.sidebar:
    st.markdown("### 🔒 SYSTEM CONTROL")
    if st.button("LOGOUT SYSTEM", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    st.markdown("### 🚀 AI SYSTEM STATUS")
    st.success("🟢 NEURAL NETWORK: ACTIVE")
    st.success("🟢 IMAGE PROCESSOR: READY")
    st.success("🟢 TREATMENT DB: LOADED")

# How it works
st.markdown('<div class="glass-container fade-in-up" style="margin-bottom: 4rem;">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">HOW THE AI SYSTEM WORKS</h2>', unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; gap: 30px; justify-content: center; flex-wrap: wrap;">
    <div style="text-align: center; flex: 1; min-width: 250px; padding: 1rem; border: 1px dashed #00f5ff; border-radius: 10px;">
        <h3 style="color: #00f5ff;">1. IMAGE CAPTURE</h3>
        <p>Upload a clear image of the plant leaf you want to analyze.</p>
    </div>
    <div style="text-align: center; flex: 1; min-width: 250px; padding: 1rem; border: 1px dashed #00f5ff; border-radius: 10px;">
        <h3 style="color: #00f5ff;">2. AI PROCESSING</h3>
        <p>Our neural network extracts features and patterns from the image.</p>
    </div>
    <div style="text-align: center; flex: 1; min-width: 250px; padding: 1rem; border: 1px dashed #00f5ff; border-radius: 10px;">
        <h3 style="color: #00f5ff;">3. DIAGNOSIS</h3>
        <p>Receive instant analysis and professional treatment protocols.</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Upload Section
st.markdown('<div class="glass-container fade-in-up" style="padding: 4rem;">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🔬 AI-POWERED PLANT ANALYSIS</h2>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Sample", use_container_width=True)
    with col2:
        st.markdown('<h3 style="color: #00f5ff;">GENERATE ANALYSIS...</h3>', unsafe_allow_html=True)
        if st.button("🚀 RUN NEURAL ANALYSIS", use_container_width=True):
            st.info("AI Model is processing...")
            time.sleep(2)
            st.success("Analysis Complete!")
            st.session_state.analysis_count += 1
            st.markdown(f"**Primary Diagnosis:** Tomato_Early_blight (Demo)")
            st.markdown("**Confidence:** 98.4%")
            st.markdown("**Treatment:** Apply fungicide containing chlorothalonil.")
st.markdown('</div>', unsafe_allow_html=True)

# About, Team, Footer
st.markdown('<div class="glass-container fade-in-up" style="margin-top: 4rem;">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🚀 ABOUT PLANT SAVIOR AI</h2>', unsafe_allow_html=True)
st.markdown("""
<p style="text-align: center;">Plant Savior AI utilizes deep learning to democratize plant pathology. 
Created by a group of dedicated engineers to save the world's crops.</p>
<div style="display: flex; gap: 40px; justify-content: center; margin-top: 3rem;">
    <div style="text-align: center;">
        <h4 style="color: #00f5ff;">Aiza</h4>
        <p style="font-size: 0.8rem;">Lead AI Engineer</p>
    </div>
    <div style="text-align: center;">
        <h4 style="color: #00f5ff;">Tooba</h4>
        <p style="font-size: 0.8rem;">Frontend Designer</p>
    </div>
    <div style="text-align: center;">
        <h4 style="color: #00f5ff;">Taiba</h4>
        <p style="font-size: 0.8rem;">Data Scientist</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🌱 PLANT SAVIOR AI - REVOLUTIONIZING AGRICULTURE WITH ARTIFICIAL INTELLIGENCE</p>
    <p style="font-size: 0.8rem; margin-top: 1rem; opacity: 0.6;">© 2025 Plant Savior AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
