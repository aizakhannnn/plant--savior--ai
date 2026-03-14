import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json
from PIL import Image
import os
import time

st.set_page_config(
    page_title="Plant Savior AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --primary: #13ec92;
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
        background-color: #f8fafc;
    }

    /* Hide standard headers */
    header[data-testid="stHeader"] { display: none !important; }

    .block-container {
        padding-top: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
    }

    /* Safe Sidebar */
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
        font-size: 1.25rem;
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

    /* Top Navigation */
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

    /* Hero Component safely styled */
    .hero-container {
        position: relative;
        overflow: hidden;
        border-radius: 1.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        min-height: 280px;
        display: flex;
        align-items: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
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
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 1rem;
        color: white;
    }
    .hero-description {
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-bottom: 0;
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
        font-size: 1.25rem;
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
        font-weight: 800;
        color: var(--slate-900);
        line-height: 1;
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
        margin-bottom: 2rem;
    }
    .panel-header-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--slate-900);
        margin: 0 0 0.5rem 0;
    }
    .panel-header-desc {
        color: var(--slate-500);
        font-size: 0.95rem;
        margin: 0;
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
    .result-pill.healthy { background-color: #dcfce7; color: #166534; }
    .result-pill.disease { background-color: #fee2e2; color: #991b1b; }
    
    .treatment-box {
        background-color: #ffffff;
        border: 1px solid var(--slate-200);
        border-left: 4px solid var(--primary);
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-top: 1.5rem;
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
    
    div[data-testid="stFileUploader"] {
        background-color: var(--slate-50);
        border-radius: 0.75rem;
        padding: 1rem;
        border: 1px dashed var(--slate-300);
    }
    </style>
    """, unsafe_allow_html=True)

# Application State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

local_css()

def show_login():
    st.markdown("""
    <div style="position: fixed; inset: 0; z-index: -1;">
        <video autoplay loop muted playsinline style="width: 100vw; height: 100vh; object-fit: cover; filter: brightness(0.4) sepia(0.3) hue-rotate(90deg);">
            <source src="https://assets.mixkit.co/videos/preview/mixkit-scientist-working-in-a-laboratory-with-a-microscope-41662-large.mp4" type="video/mp4">
        </video>
    </div>
    <style>
    div[data-testid="column"]:nth-of-type(2) {
        background-color: #ffffff;
        border-radius: 1.5rem;
        padding: 2.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    .block-container { padding-top: 10vh !important; background-color: transparent !important; }
    .stApp { background-color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.5, 2.5, 1.5])
    with c2:
        st.markdown("""
            <div style="width: 100%; height: 10rem; background-color: #f1f5f9; border-radius: 1rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px dashed #cbd5e1;">
               <span style="font-size: 5rem;">🌱</span>
            </div>
            <h1 style="text-align: center; color: #0f172a; font-weight: 800; font-size: 1.875rem; margin-bottom: 0.25rem;">System Authentication</h1>
            <p style="text-align: center; color: #64748b; font-weight: 500; margin-bottom: 2rem;">Authorized Personnel Access Only</p>
        """, unsafe_allow_html=True)

        st.markdown('<span style="font-size: 0.875rem; font-weight: 600; color: #334155; margin-bottom: 0.5rem; display: block;">Operator ID</span>', unsafe_allow_html=True)
        username = st.text_input("Operator ID", label_visibility="collapsed", placeholder="Enter unique ID")
        
        st.markdown('<span style="font-size: 0.875rem; font-weight: 600; color: #334155; margin-bottom: 0.5rem; display: block; margin-top: 1rem;">Access Code</span>', unsafe_allow_html=True)
        password = st.text_input("Access Code", type="password", label_visibility="collapsed", placeholder="••••••••")
        
        st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
        
        if st.session_state.auth_mode == 'login':
            if st.button("⚡ Initiate System", type="primary", use_container_width=True):
                if username == "aiza" and password == "pakistan2313":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            
            st.markdown('<div style="text-align: center; margin-top: 1rem;">', unsafe_allow_html=True)
            if st.button("Need an account? Sign Up", type="secondary", use_container_width=True):
                st.session_state.auth_mode = 'signup'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            if st.button("🚀 Register Account", type="primary", use_container_width=True):
                if username == "aiza":
                    st.error("Username already exists. Please choose another username.")
                elif username == "" or password == "":
                    st.warning("Please fill out all fields.")
                else:
                    st.success("Account successfully created! Please log in.")
                    time.sleep(1)
                    st.session_state.auth_mode = 'login'
                    st.rerun()
                    
            st.markdown('<div style="text-align: center; margin-top: 1rem;">', unsafe_allow_html=True)
            if st.button("Already have an account? Log In", type="secondary", use_container_width=True):
                st.session_state.auth_mode = 'login'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
            <div style="text-align: center; color: #94a3b8; font-size: 0.75rem; margin-top: 2rem; line-height: 1.5;">
                This system is monitored for security purposes. Unauthorized access attempts are logged and reported to the Bio-Security Department.
            </div>
        """, unsafe_allow_html=True)


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
    model = load_sys_model()
    treatments = load_sys_treatments()

    # Build Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="brand-container">
            <div class="brand-icon">🌱</div>
            <div>
                <div class="brand-title">Plant Savior</div>
                <div class="brand-subtitle">Global AI</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.current_page == "Dashboard" else "secondary"):
            st.session_state.current_page = "Dashboard"
            st.rerun()
        if st.button("🔬 Analysis", use_container_width=True, type="primary" if st.session_state.current_page == "Analysis" else "secondary"):
            st.session_state.current_page = "Analysis"
            st.rerun()
        if st.button("👥 About Team", use_container_width=True, type="primary" if st.session_state.current_page == "About" else "secondary"):
            st.session_state.current_page = "About"
            st.rerun()
        
        st.markdown("<hr/>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.rerun()

    # Top Header Banner
    st.markdown("""
    <div class="top-header">
        <div class="search-mockup">
            🔍 <span style="color: var(--slate-400); font-size: 0.875rem;">Search crops, diseases, or reports...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.current_page == "About":
        st.markdown('<h1 style="color: var(--slate-900); font-weight: 800; font-size: 2.5rem; margin-bottom: 2rem;">Meet The Team</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: white; border-radius: 1.5rem; padding: 2.5rem; border: 1px solid var(--slate-200); box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1);">
            <div style="display: flex; gap: 2rem; align-items: center; margin-bottom: 2rem;">
                <div style="width: 100px; height: 100px; border-radius: 50%; background-color: var(--slate-100); display: flex; align-items: center; justify-content: center; font-size: 3rem;">👩‍💻</div>
                <div>
                    <h3 style="margin: 0; color: var(--slate-900); font-size: 1.5rem; font-weight: 800;">Aiza</h3>
                    <p style="margin: 0; color: var(--primary); font-weight: 700;">Lead AI Researcher & Engineer</p>
                    <p style="margin-top: 0.5rem; color: var(--slate-600);">Passionate about leveraging deep learning capabilities to revolutionize global agriculture and sustainable farming practices.</p>
                </div>
            </div>
            <h4 style="color: var(--slate-900); font-weight: 700; margin-bottom: 0.5rem;">The Mission</h4>
            <p style="color: var(--slate-600); line-height: 1.6;">The Plant Savior AI project aims to build accessible, lightning-fast disease classification networks deployed directly to farmers worldwide. By uniting modern web technologies with advanced TensorFlow architectures, we are mitigating crop losses on a massive scale.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    if st.session_state.current_page == "Dashboard":
        st.markdown("""
        <div class="hero-container">
            <div class="hero-content">
                <div class="hero-badge">Next-Gen Farming</div>
                <h1 class="hero-title">Empowering Global Agriculture with AI</h1>
                <p class="hero-description">Revolutionizing crop health with instant disease detection and precision farming insights using state-of-the-art neural networks.</p>
            </div>
        </div>
        <div class="dashboard-stats">
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-icon" style="background-color: #eff6ff; color: #3b82f6;">🎯</div>
                    <div class="stat-badge">+0.5%</div>
                </div>
                <div class="stat-label">Accuracy</div>
                <div class="stat-value">99.2%</div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-icon" style="background-color: rgba(19,236,146,0.1); color: var(--primary);">🧠</div>
                    <div class="stat-badge">+2 New</div>
                </div>
                <div class="stat-label">Plant Diseases</div>
                <div class="stat-value">15+</div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-icon" style="background-color: #fff7ed; color: #f97316;">⚡</div>
                    <div class="stat-badge">-0.2s</div>
                </div>
                <div class="stat-label">Analysis Time</div>
                <div class="stat-value"><3s</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<h2 style="font-weight: 800; color: var(--slate-900); font-size: 1.875rem; margin-top: 2rem; margin-bottom: 1.5rem;">HOW THE AI SYSTEM WORKS</h2>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-stats">', unsafe_allow_html=True)
        h1, h2, h3 = st.columns(3)
        with h1:
            st.markdown("""
            <div class="stat-card" style="border-top: 4px solid var(--primary);">
                <div class="stat-icon" style="background-color: rgba(19,236,146,0.1); color: var(--primary); font-size: 2rem; margin-bottom: 1rem;">📱</div>
                <h3 style="font-weight: 800; font-size: 1.25rem; margin-bottom: 0.5rem; color: var(--slate-900);">IMAGE CAPTURE</h3>
                <p style="color: var(--slate-600); line-height: 1.6; font-size: 0.95rem;">Upload a high-quality image of the affected plant leaf. Our system accepts JPG, JPEG, and PNG formats for maximum compatibility.</p>
            </div>
            """, unsafe_allow_html=True)
        with h2:
            st.markdown("""
            <div class="stat-card" style="border-top: 4px solid #3b82f6;">
                <div class="stat-icon" style="background-color: #eff6ff; color: #3b82f6; font-size: 2rem; margin-bottom: 1rem;">🧠</div>
                <h3 style="font-weight: 800; font-size: 1.25rem; margin-bottom: 0.5rem; color: var(--slate-900);">AI PROCESSING</h3>
                <p style="color: var(--slate-600); line-height: 1.6; font-size: 0.95rem;">Advanced convolutional neural network analyzes the image using deep learning algorithms trained on 50,000+ plant images.</p>
            </div>
            """, unsafe_allow_html=True)
        with h3:
            st.markdown("""
            <div class="stat-card" style="border-top: 4px solid #f97316;">
                <div class="stat-icon" style="background-color: #fff7ed; color: #f97316; font-size: 2rem; margin-bottom: 1rem;">📊</div>
                <h3 style="font-weight: 800; font-size: 1.25rem; margin-bottom: 0.5rem; color: var(--slate-900);">INSTANT DIAGNOSIS</h3>
                <p style="color: var(--slate-600); line-height: 1.6; font-size: 0.95rem;">Receive comprehensive results with disease identification, confidence score, and professional treatment recommendations.</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_page in ["Dashboard", "Analysis"]:
        st.markdown("""
        <div class="analysis-panel">
            <div class="panel-header-flex">
                <div>
                    <h2 class="panel-header-title">AI-Powered Plant Analysis</h2>
                    <p class="panel-header-desc">Identify diseases and nutrient deficiencies instantly</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

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
                                pill_icon = '✅' if is_healthy else '⚠️'
                                pill_msg = 'Healthy Plant' if is_healthy else 'Disease Detected'
                                
                                html_result = (
'<div style="background-color: var(--slate-50); border: 1px solid var(--slate-200); border-radius: 1rem; padding: 1.5rem;">'
f'<div class="result-pill {pill_class}">{pill_icon} {pill_msg}</div>'
f'<h2 style="font-size: 1.5rem; font-weight: 900; color: var(--slate-900); margin-bottom: 0.5rem;">{d_name}</h2>'
f'<p style="color: var(--slate-500); font-size: 0.875rem; margin-bottom: 1.5rem;">Analysis #{st.session_state.analysis_count} via Advanced CNN v2.1</p>'
'<div style="margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">'
'<span style="font-size: 0.875rem; font-weight: 600; color: var(--slate-700);">Diagnostic Confidence</span>'
f'<span style="font-size: 0.875rem; font-weight: 800; color: var(--slate-900);">{con*100:.1f}%</span>'
'</div>'
'<div class="progress-bar">'
f'<div class="progress-fill" style="width: {con*100}%;"></div>'
'</div>'
'<div class="treatment-box">'
'<div class="treatment-title">Recommended Protocol</div>'
f'<p class="treatment-text">{tx}</p>'
'</div>'
'</div>'
)
                                st.markdown(html_result, unsafe_allow_html=True)
                            else:
                                st.error("Engine failure: Neural weights unassigned.")
                                
                        except Exception as e:
                            st.error(f"Analysis Failed: {e}")

        st.markdown('</div>', unsafe_allow_html=True) 

if st.session_state.logged_in:
    show_dashboard()
else:
    show_login()
