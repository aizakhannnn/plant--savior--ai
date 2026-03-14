code = """import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json
from PIL import Image
import os
import base64
from io import BytesIO
import time
import urllib.parse
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests

st.set_page_config(
    page_title="Plant Savior AI - Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css():
    st.markdown(\"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

    :root {
        --primary: #13ec92;
        --background-light: #f6f8f7;
        --background-dark: #10221a;
        --slate-900: #0f172a;
        --slate-800: #1e293b;
        --slate-700: #334155;
        --slate-500: #64748b;
        --slate-400: #94a3b8;
        --slate-300: #cbd5e1;
        --slate-200: #e2e8f0;
        --slate-100: #f1f5f9;
        --slate-50: #f8fafc;
    }

    * {
        font-family: 'Space Grotesk', sans-serif !important;
    }

    .stApp {
        background-color: var(--background-light);
    }

    /* Hide standard headers */
    header[data-testid="stHeader"] { display: none !important; }

    .block-container {
        padding-top: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1400px !important;
    }

    /* Base Typography and Element setup */
    p, span, div { color: var(--slate-800); }
    h1, h2, h3, h4, h5, h6 { color: var(--slate-900); }
    
    /* Clean Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid var(--slate-200);
    }
    
    [data-testid="stSidebar"] hr {
        border-color: var(--slate-200);
        margin: 1.5rem 0;
    }

    .brand-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1.5rem;
    }

    .brand-icon {
        width: 2.5rem;
        height: 2.5rem;
        background-color: var(--primary);
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px 0 rgba(19, 236, 146, 0.3);
    }

    .brand-icon span {
        color: var(--slate-900);
        font-weight: bold;
        font-size: 1.5rem;
    }

    .brand-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: var(--slate-900);
        line-height: 1.2;
    }

    .brand-subtitle {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Top Navigation Search / Profile Header styling */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2.5rem;
    }
    .search-mockup {
        background-color: #fff;
        border: 1px solid var(--slate-200);
        border-radius: 9999px;
        padding: 0.5rem 1.25rem;
        display: flex;
        align-items: center;
        width: 400px;
        gap: 0.75rem;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
    }
    .profile-icons {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .notification-btn {
        height: 2.5rem;
        width: 2.5rem;
        border-radius: 9999px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--slate-500);
        border: 1px solid var(--slate-200);
        background: #fff;
    }
    .avatar-mockup {
        height: 2.5rem;
        width: 2.5rem;
        border-radius: 9999px;
        border: 2px solid var(--primary);
        background-color: var(--slate-200);
        background-image: url('https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=250&auto=format&fit=crop');
        background-size: cover;
    }

    /* Hero Component matching Google Stitch */
    .hero-container {
        position: relative;
        overflow: hidden;
        border-radius: 1.5rem;
        background-color: var(--slate-900);
        color: white;
        min-height: 320px;
        display: flex;
        align-items: center;
        margin-bottom: 2.5rem;
    }
    .hero-bg-img {
        position: absolute;
        inset: 0;
        background-image: url('https://images.unsplash.com/photo-1628186120894-325d7429188d?q=80&w=2670&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        opacity: 0.4;
        mix-blend-mode: overlay;
    }
    .hero-gradient {
        position: absolute;
        inset: 0;
        background: linear-gradient(to right, var(--slate-900) 0%, rgba(15,23,42,0.85) 50%, transparent 100%);
    }
    .hero-content {
        position: relative;
        z-index: 10;
        padding: 3rem 4rem;
        max-width: 50rem;
    }
    .hero-badge {
        background-color: rgba(19, 236, 146, 0.2);
        color: var(--primary);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
        display: inline-flex;
        border: 1px solid rgba(19, 236, 146, 0.3);
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 1rem;
        letter-spacing: -0.025em;
        color: white;
    }
    .hero-description {
        color: #cbd5e1;
        font-size: 1.125rem;
        margin-bottom: 2rem;
        line-height: 1.6;
        max-width: 40rem;
    }
    
    /* Stats Layout */
    .dashboard-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-bottom: 2.5rem;
    }
    .stat-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid var(--slate-200);
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
    }
    .stat-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    .stat-icon {
        padding: 0.75rem;
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stat-badge {
        background-color: #dcfce7;
        color: #10b981;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .stat-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--slate-500);
        margin-bottom: 0.25rem;
    }
    .stat-value {
        font-size: 1.875rem;
        font-weight: 900;
        color: var(--slate-900);
        line-height: 1;
        letter-spacing: -0.025em;
    }

    /* Analysis Section */
    .analysis-panel {
        background-color: #ffffff;
        border-radius: 1.5rem;
        border: 1px solid var(--slate-200);
        padding: 2.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 2.5rem;
    }
    .panel-header-flex {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2.5rem;
    }
    .panel-header-title {
        font-size: 1.5rem;
        font-weight: 900;
        letter-spacing: -0.025em;
        margin-bottom: 0.25rem;
        color: var(--slate-900);
    }
    .panel-header-desc {
        color: var(--slate-500);
        margin: 0;
    }
    .system-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .ping-dot {
        position: relative;
        display: flex;
        height: 0.75rem;
        width: 0.75rem;
    }
    .ping-dot .pulse {
        animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
        position: absolute;
        height: 100%;
        width: 100%;
        border-radius: 9999px;
        background-color: var(--primary);
        opacity: 0.75;
    }
    .ping-dot .core {
        position: relative;
        border-radius: 9999px;
        height: 0.75rem;
        width: 0.75rem;
        background-color: var(--primary);
    }
    .system-text {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--slate-400);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    @keyframes ping {
      75%, 100% {
        transform: scale(2);
        opacity: 0;
      }
    }

    /* Auth Screen CSS */
    .auth-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 80vh;
        width: 100%;
    }
    .auth-card {
        background-color: #ffffff;
        border-radius: 1.5rem;
        padding: 0;
        border: 1px solid var(--slate-200);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        width: 100%;
        max-width: 480px;
        overflow: hidden;
    }
    .auth-header {
        width: 100%;
        height: 12rem;
        background-image: url('https://images.unsplash.com/photo-1530836369250-ef71a3fb90e6?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        position: relative;
    }
    .auth-header::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(to bottom right, rgba(19, 236, 146, 0.2), transparent);
    }
    .auth-body {
        padding: 2.5rem;
        text-align: center;
    }
    .auth-title {
        font-size: 1.875rem;
        font-weight: 800;
        color: var(--slate-900);
        margin-bottom: 0.25rem;
        letter-spacing: -0.025em;
    }
    .auth-subtitle {
        color: var(--slate-500);
        font-weight: 500;
        margin-bottom: 2rem;
    }
    .auth-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--slate-700);
        margin-bottom: 0.5rem;
        display: block;
        text-align: left;
    }

    /* Streamlit overrides for better inputs */
    [data-baseweb="input"] {
        border-radius: 0.75rem !important;
        background-color: var(--slate-50) !important;
        border: 1px solid var(--slate-200) !important;
        transition: all 0.2s;
    }
    [data-baseweb="input"]:focus-within {
        border-color: var(--primary) !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }
    [data-baseweb="input"] input {
        color: var(--slate-900) !important;
        font-weight: 500 !important;
    }

    /* Primary and Secondary Custom Buttons */
    .stButton > button {
        border-radius: 0.75rem !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.2s !important;
        width: 100% !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: var(--primary) !important;
        color: var(--slate-900) !important;
        box-shadow: 0 4px 6px -1px rgba(19, 236, 146, 0.2) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(19, 236, 146, 0.3) !important;
        background-color: #10d482 !important;
    }

    .stButton > button[kind="secondary"] {
        background-color: var(--slate-900) !important;
        color: #ffffff !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: var(--slate-800) !important;
        transform: translateY(-2px);
    }
    
    .stButton > button.google-btn {
        background-color: #ffffff !important;
        color: var(--slate-700) !important;
        border: 1px solid var(--slate-200) !important;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05) !important;
    }
    .stButton > button.google-btn:hover {
        background-color: var(--slate-50) !important;
        border-color: var(--slate-300) !important;
        transform: none;
    }

    /* Uploader Overrides */
    [data-testid="stFileUploader"] {
        margin-top: 2rem;
    }
    [data-testid="stFileUploader"] section {
        padding: 4rem 2rem !important;
        border-radius: 1.5rem !important;
        border: 2px dashed var(--slate-300) !important;
        background-color: var(--slate-50) !important;
        transition: all 0.2s ease;
    }
    [data-testid="stFileUploader"] section:hover {
        border-color: var(--primary) !important;
        background-color: rgba(19, 236, 146, 0.05) !important;
    }
    .stFileUploaderDropzoneInstructions {
        color: var(--slate-900) !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
    }
    [data-testid="stFileUploader"] small {
        color: var(--slate-500) !important;
        font-size: 1rem !important;
    }
    
    /* Result styling */
    .result-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.875rem;
        margin-bottom: 1rem;
    }
    .result-pill.healthy {
        background-color: #dcfce7;
        color: #166534;
    }
    .result-pill.disease {
        background-color: #fee2e2;
        color: #991b1b;
    }
    .treatment-box {
        background-color: #ffffff;
        border: 1px solid var(--slate-200);
        border-left: 4px solid var(--primary);
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-top: 1rem;
    }
    .treatment-title {
        font-size: 0.875rem;
        font-weight: 700;
        color: var(--slate-900);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }
    .treatment-text {
        font-size: 0.95rem;
        color: var(--slate-600);
        line-height: 1.6;
        margin: 0;
    }
    
    /* Progress layout */
    .progress-bar {
        width: 100%;
        height: 0.5rem;
        background-color: var(--slate-200);
        border-radius: 9999px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background-color: var(--primary);
        border-radius: 9999px;
        transition: width 1s ease-in-out;
    }
    </style>
    \"\"\", unsafe_allow_html=True)

# Main Authentication and Routing Logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0

local_css()

def show_login():
    st.markdown(\"\"\"
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="auth-header"></div>
            <div class="auth-body">
                <h1 class="auth-title">System Authentication</h1>
                <p class="auth-subtitle">Authorized Personnel Access Only</p>
    \"\"\", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown('<span class="auth-label">Operator ID</span>', unsafe_allow_html=True)
        username = st.text_input("Operator ID", label_visibility="collapsed", placeholder="Enter unique ID")
        
        st.markdown('<span class="auth-label" style="margin-top: 1rem;">Access Code</span>', unsafe_allow_html=True)
        password = st.text_input("Access Code", type="password", label_visibility="collapsed", placeholder="••••••••")
        
        st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
        
        if st.button("⚡ Initiate System", type="primary"):
            if username == "aiza" and password == "pakistan2313":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials.")
                
        st.markdown(\"\"\"
            <div style="display: flex; align-items: center; justify-content: center; margin: 1.5rem 0;">
                <div style="height: 1px; flex-grow: 1; background-color: #e2e8f0;"></div>
                <span style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 1rem; font-weight: 600;">or secure login via</span>
                <div style="height: 1px; flex-grow: 1; background-color: #e2e8f0;"></div>
            </div>
        \"\"\", unsafe_allow_html=True)
        
        st.markdown("""<style>div:has(> button[key="google"]) > button { background-color: #fff !important; color: #334155 !important; border: 1px solid #e2e8f0 !important; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05) !important; }</style>""", unsafe_allow_html=True)
        
        if st.button("Google Operations Account", key="google", type="secondary"):
            st.session_state.logged_in = True
            st.rerun()

    st.markdown(\"\"\"
            </div>
        </div>
        <div style="text-align: center; color: #94a3b8; font-size: 0.75rem; margin-top: 1.5rem; max-width: 400px; line-height: 1.5;">
            This system is monitored for security purposes. Unauthorized access attempts are logged and reported to the Bio-Security Department.
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_sys_model():
    try:
        model = tf.keras.models.load_model('best_plant_model_final.keras')
        return model
    except:
        return None

@st.cache_resource(show_spinner=False)
def load_sys_treatments():
    try:
        with open('treatment_dict_complete.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "Tomato_healthy": "Plant appears healthy! Continue current care routine with proper watering and nutrition.",
            "Tomato_Early_blight": "Apply fungicide containing chlorothalonil or copper. Ensure good air circulation.",
            "Potato_Late_blight": "Remove affected plants immediately. Apply copper-based fungicide preventively. Improve ventilation."
        }

def show_dashboard():
    # Load requirements silently
    model = load_sys_model()
    treatments = load_sys_treatments()

    # Build Sidebar
    with st.sidebar:
        st.markdown(\"\"\"
        <div class="brand-container">
            <div class="brand-icon">
                <span class="material-symbols-outlined" style="color:var(--slate-900);">potted_plant</span>
            </div>
            <div>
                <div class="brand-title">Plant Savior</div>
                <div class="brand-subtitle">Global AI</div>
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)
        
        st.button("📊 Dashboard", use_container_width=True, type="secondary")
        st.button("🔬 Analysis", use_container_width=True, type="secondary")
        st.button("👥 About Team", use_container_width=True, type="secondary")
        
        st.markdown("<hr/>", unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.markdown(\"\"\"
        <div style="margin-top: 2rem; padding: 1.5rem; background-color: var(--slate-50); border: 1px solid var(--slate-200); border-radius: 1rem;">
            <p style="font-size: 0.75rem; font-weight: 700; color: var(--slate-400); text-transform: uppercase; margin-bottom: 0.75rem; letter-spacing: 0.05em;">Current Plan</p>
            <p style="font-size: 0.875rem; font-weight: 700; color: var(--slate-900); margin-bottom: 0.75rem;">Enterprise Pro</p>
            <div style="width: 100%; height: 0.375rem; background-color: var(--slate-200); border-radius: 9999px; overflow: hidden;">
                <div style="width: 75%; height: 100%; background-color: var(--primary); border-radius: 9999px;"></div>
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)

    # Top Header Banner
    st.markdown(\"\"\"
    <div class="top-header">
        <div class="search-mockup">
            <span class="material-symbols-outlined" style="color: var(--slate-400); font-size: 1.25rem;">search</span>
            <span style="color: var(--slate-400); font-size: 0.875rem;">Search crops, diseases, or reports...</span>
        </div>
        <div class="profile-icons">
            <div class="notification-btn">
                <span class="material-symbols-outlined" style="font-size: 1.25rem;">notifications</span>
            </div>
            <div class="avatar-mockup"></div>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)

    # Hero Banner Container
    st.markdown(\"\"\"
    <div class="hero-container">
        <div class="hero-bg-img"></div>
        <div class="hero-gradient"></div>
        <div class="hero-content">
            <div class="hero-badge">Next-Gen Farming</div>
            <h1 class="hero-title">Empowering Global Agriculture with AI</h1>
            <p class="hero-description">Revolutionizing crop health with instant disease detection and precision farming insights using state-of-the-art neural networks.</p>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)

    # Stats Summary
    st.markdown('<div class="dashboard-stats">', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown(\"\"\"
        <div class="stat-card">
            <div class="stat-header">
                <div class="stat-icon" style="background-color: #eff6ff; color: #3b82f6;"><span class="material-symbols-outlined">verified</span></div>
                <div class="stat-badge">+0.5%</div>
            </div>
            <div class="stat-label">Accuracy</div>
            <div class="stat-value">99.2%</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with sc2:
        st.markdown(\"\"\"
        <div class="stat-card">
            <div class="stat-header">
                <div class="stat-icon" style="background-color: rgba(19,236,146,0.1); color: var(--primary);"><span class="material-symbols-outlined">psychology</span></div>
                <div class="stat-badge">+2 New</div>
            </div>
            <div class="stat-label">Plant Diseases</div>
            <div class="stat-value">15+</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with sc3:
        st.markdown(\"\"\"
        <div class="stat-card">
            <div class="stat-header">
                <div class="stat-icon" style="background-color: #fff7ed; color: #f97316;"><span class="material-symbols-outlined">speed</span></div>
                <div class="stat-badge">-0.2s</div>
            </div>
            <div class="stat-label">Analysis Time</div>
            <div class="stat-value"><3s</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Engine Core Container
    st.markdown(\"\"\"
    <div class="analysis-panel">
        <div class="panel-header-flex">
            <div>
                <h2 class="panel-header-title">AI-Powered Plant Analysis</h2>
                <p class="panel-header-desc">Identify diseases and nutrient deficiencies instantly</p>
            </div>
            <div class="system-status">
                <div class="ping-dot">
                    <span class="pulse"></span>
                    <span class="core"></span>
                </div>
                <span class="system-text">System Active</span>
            </div>
        </div>
    \"\"\", unsafe_allow_html=True)

    img_file = st.file_uploader("Upload Plant Image to Analyze", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    
    if img_file is not None:
        st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
        img_col, info_col = st.columns([1, 1], gap="large")
        with img_col:
            st.markdown('<p style="font-weight:700; color:var(--slate-900); font-size:1.125rem; margin-bottom:1rem;">Source Image</p>', unsafe_allow_html=True)
            image = Image.open(img_file)
            st.image(image, use_column_width=True, clamp=True)
            
        with info_col:
            st.markdown('<p style="font-weight:700; color:var(--slate-900); font-size:1.125rem; margin-bottom:1rem;">Neural Diagnostics</p>', unsafe_allow_html=True)
            
            if st.button("Run Global Analysis", use_container_width=True, type="primary"):
                with st.spinner("Processing structural geometry with Vision AI..."):
                    time.sleep(1)
                    try:
                        with open("temp.jpg", "wb") as f: f.write(img_file.getbuffer())
                        
                        if model:
                            loaded_img = load_img("temp.jpg", target_size=(224, 224))
                            arr = img_to_array(loaded_img)
                            arr = arr.reshape(1, 224, 224, 3) / 255.0
                            preds = model.predict(arr, verbose=0)
                            cls = np.argmax(preds[0])
                            con = float(preds[0][cls])
                            keys = list(treatments.keys())
                            disease = keys[cls]
                            tx = treatments.get(disease, "Consult with an agricultural expert.")
                            st.session_state.analysis_count += 1
                            os.remove("temp.jpg")
                            
                            is_healthy = "healthy" in disease.lower()
                            d_name = disease.replace('_', ' ').title()
                            
                            pill_class = 'healthy' if is_healthy else 'disease'
                            pill_icon = 'check_circle' if is_healthy else 'warning'
                            pill_msg = 'Healthy Plant' if is_healthy else 'Disease Detected'
                            
                            st.markdown(f\"\"\"
                            <div style="background-color: var(--slate-50); border: 1px solid var(--slate-200); border-radius: 1rem; padding: 1.5rem;">
                                <div class="result-pill {pill_class}">
                                    <span class="material-symbols-outlined" style="font-size: 1.125rem;">{pill_icon}</span>
                                    {pill_msg}
                                </div>
                                <h2 style="font-size: 1.5rem; font-weight: 900; color: var(--slate-900); margin-bottom: 0.5rem;">{d_name}</h2>
                                <p style="color: var(--slate-500); font-size: 0.875rem; margin-bottom: 1.5rem;">Analysis #{st.session_state.analysis_count} via Advanced CNN v2.1</p>
                                
                                <div style="margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 0.875rem; font-weight: 600; color: var(--slate-700);">Diagnostic Confidence</span>
                                    <span style="font-size: 0.875rem; font-weight: 800; color: var(--slate-900);">{con*100:.1f}%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {con*100}%;"></div>
                                </div>
                                
                                <div class="treatment-box">
                                    <div class="treatment-title">Recommended Protocol</div>
                                    <p class="treatment-text">{tx}</p>
                                </div>
                            </div>
                            \"\"\", unsafe_allow_html=True)
                            
                        else:
                            st.error("Engine failure: Neural weights unassigned.")
                            
                    except Exception as e:
                        st.error(f"Analysis Failed: {e}")

    st.markdown('</div>', unsafe_allow_html=True) 

if st.session_state.logged_in:
    show_dashboard()
else:
    show_login()
"""

with open("c:/Users/hp/Documents/GitHub/plant--savior--ai/replace_app.py", "w", encoding="utf-8") as f:
    f.write(code)
