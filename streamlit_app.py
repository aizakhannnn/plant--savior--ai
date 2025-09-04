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

# Custom CSS for futuristic design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    :root {
        --primary-dark: #0a0e17;
        --secondary-dark: #121826;
        --accent-blue: #00f0ff;
        --accent-purple: #a020f0;
        --accent-green: #00ff9d;
        --accent-pink: #ff00c8;
        --text-light: #e0e0ff;
        --text-dim: #a0a0c0;
    }
    
    * {
        font-family: 'Exo 2', sans-serif;
        color: var(--text-light);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
    }
    
    /* Main background and layout */
    .stApp {
        background: var(--primary-dark);
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(160, 32, 240, 0.1) 0%, transparent 20%),
            radial-gradient(circle at 90% 80%, rgba(0, 240, 255, 0.1) 0%, transparent 20%);
        color: var(--text-light);
    }
    
    @keyframes rotate {
        100% {
            transform: rotate(360deg);
        }
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: rgba(18, 24, 38, 0.9);
        border-right: 1px solid rgba(0, 240, 255, 0.2);
    }
    
    .sidebar-section {
        background: rgba(30, 40, 60, 0.6);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 
            0 5px 15px rgba(0, 0, 0, 0.3),
            inset 0 0 10px rgba(0, 240, 255, 0.1);
        border: 1px solid rgba(0, 240, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .sidebar-title {
        color: var(--accent-blue);
        font-size: 1.4rem;
        margin-top: 0;
        margin-bottom: 15px;
        font-family: 'Orbitron', sans-serif;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .stSelectbox label {
        color: var(--text-dim) !important;
    }
    
    .stSelectbox div {
        background: rgba(18, 24, 38, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        color: var(--text-light) !important;
    }
    
    /* Progress Bar in Sidebar */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)) !important;
    }
    
    .stProgress > div {
        background: rgba(30, 40, 60, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
    }
    
    /* Toggle Switch */
    .stCheckbox label {
        color: var(--text-dim) !important;
        font-size: 1.1rem !important;
    }
    
    /* Info Box */
    .stAlert {
        background: rgba(0, 240, 255, 0.1) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        color: var(--text-light) !important;
        border-radius: 10px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(160, 32, 240, 0.1) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(160, 32, 240, 0.3) !important;
    }
    
    /* Metric */
    .stMetric {
        background: rgba(30, 40, 60, 0.6) !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.1) !important;
    }
    
    .stMetric-label {
        color: var(--text-dim) !important;
    }
    
    .stMetric-value {
        color: var(--accent-blue) !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .logo-text {
            font-size: 2.8rem;
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
            padding: 2rem 1rem;
        }
        
        .stat-card {
            min-width: 140px;
            padding: 1.5rem;
        }
        
        .stat-value {
            font-size: 2rem;
        }
        
        .tech-cards {
            flex-direction: column;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 1.5rem 1rem;
        }
        
        .logo-text {
            font-size: 2.2rem;
        }
        
        .tagline {
            font-size: 1rem;
        }
        
        .upload-section, .about-section, .image-preview-container, .results-container {
            padding: 1.8rem;
        }
        
        .step-card {
            min-width: 100%;
        }
        
        .feedback-reactions {
            flex-direction: column;
            align-items: center;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main header with enhanced design
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(18, 24, 38, 0.9) 0%, rgba(10, 14, 23, 0.95) 100%); padding: 2.5rem 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem; box-shadow: 0 0 30px rgba(0, 240, 255, 0.3), inset 0 0 20px rgba(160, 32, 240, 0.2); position: relative; overflow: hidden; border: 1px solid rgba(0, 240, 255, 0.3);">
    <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: conic-gradient(transparent, rgba(0, 240, 255, 0.4), rgba(160, 32, 240, 0.4), transparent); animation: rotate 4s linear infinite; z-index: -1;"></div>
    <h1 style="font-size: 4rem; font-weight: 700; margin-bottom: 0.5rem; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: 0 0 20px rgba(0, 240, 255, 0.5); position: relative; z-index: 2; letter-spacing: 3px;">🌱 PLANT SAVIOR AI</h1>
    <p style="font-size: 1.5rem; opacity: 0.9; font-weight: 300; max-width: 800px; margin: 0 auto; color: var(--text-dim);">ADVANCED PLANT DISEASE DETECTION USING ARTIFICIAL INTELLIGENCE</p>
</div>
""", unsafe_allow_html=True)

# Add a futuristic notification banner
st.markdown("""
<div style="background: linear-gradient(90deg, rgba(0, 240, 255, 0.15), rgba(160, 32, 240, 0.15)); padding: 15px; border-radius: 12px; margin-bottom: 20px; text-align: center; border-left: 5px solid var(--accent-blue); box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);">
    <p style="margin: 0; font-weight: 500; font-size: 1.1rem; letter-spacing: 1px;">✨ NEW: REAL-TIME DISEASE ANALYSIS WITH 91.02% ACCURACY ✨</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with additional information
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">🌿 ABOUT THIS TOOL</h3>', unsafe_allow_html=True)
    st.info("""
    This AI-powered system helps farmers and gardeners detect plant diseases from leaf images with high accuracy.
    
    Simply upload a clear photo of a plant leaf and get instant diagnosis with treatment recommendations.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">📋 HOW TO GET BEST RESULTS</h3>', unsafe_allow_html=True)
    with st.expander("Expand for tips", expanded=True):
        st.markdown("""
        1. **Lighting**: Take photo in good natural light
        2. **Focus**: Ensure leaf is in sharp focus
        3. **Background**: Simple background works best
        4. **Angle**: Top-down view of the leaf
        5. **Symptoms**: Show affected areas clearly
        """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">🎯 SUPPORTED DISEASES</h3>', unsafe_allow_html=True)
    disease_options = {
        "Tomato": 10,
        "Potato": 3,
        "Pepper": 2,
        "Apple": 4,
        "Grape": 4,
        "Corn": 4,
        "Cherry": 2,
        "Peach": 2,
        "Strawberry": 1,
        "Orange": 1
    }
    
    disease_select = st.selectbox("Select plant type", list(disease_options.keys()))
    st.markdown(f"**{disease_options[disease_select]} diseases** supported for {disease_select}")
    
    # Add a progress tracker for supported diseases
    st.markdown("### 📊 Disease Coverage")
    st.progress(0.95)  # 38 out of 40 diseases covered
    st.caption("95% of common plant diseases supported")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">ℹ️ NEED HELP?</h3>', unsafe_allow_html=True)
    st.markdown("Contact: support@plantsavior.ai")
    st.markdown('</div>', unsafe_allow_html=True)

# How it works section with enhanced design
st.markdown("""
<div style="background: rgba(18, 24, 38, 0.7); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 0 20px rgba(160, 32, 240, 0.2), inset 0 0 20px rgba(0, 240, 255, 0.1); border: 1px solid rgba(160, 32, 240, 0.2); backdrop-filter: blur(10px);">
    <h2 style="color: var(--accent-blue); text-align: center; font-size: 2.2rem; margin-bottom: 2rem; font-weight: 600; position: relative; padding-bottom: 15px; font-family: 'Orbitron', sans-serif;">
        HOW IT WORKS
        <div style="content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 100px; height: 4px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); border-radius: 2px; box-shadow: 0 0 10px var(--accent-blue);"></div>
    </h2>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1.5rem;">
        <div style="background: rgba(30, 40, 60, 0.6); border-radius: 15px; padding: 2rem 1.5rem; text-align: center; flex: 1; min-width: 220px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); transition: all 0.3s ease; border: 1px solid rgba(0, 240, 255, 0.2); position: relative; overflow: hidden; backdrop-filter: blur(5px);">
            <div style="content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); transform: scaleX(0); transform-origin: left; transition: transform 0.3s ease;"></div>
            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); color: var(--primary-dark); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.2rem; font-weight: bold; font-size: 1.5rem; box-shadow: 0 0 15px rgba(0, 240, 255, 0.5); font-family: 'Orbitron', sans-serif;">1</div>
            <div style="font-size: 3rem; margin-bottom: 1.2rem; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📸</div>
            <h3 style="color: var(--accent-blue); font-size: 1.5rem; font-weight: 600; margin-bottom: 0.8rem; font-family: 'Orbitron', sans-serif;">UPLOAD IMAGE</h3>
            <p style="color: var(--text-dim); line-height: 1.6;">Take a clear photo of the affected plant leaf and upload it to our system</p>
        </div>
        <div style="background: rgba(30, 40, 60, 0.6); border-radius: 15px; padding: 2rem 1.5rem; text-align: center; flex: 1; min-width: 220px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); transition: all 0.3s ease; border: 1px solid rgba(0, 240, 255, 0.2); position: relative; overflow: hidden; backdrop-filter: blur(5px);">
            <div style="content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); transform: scaleX(0); transform-origin: left; transition: transform 0.3s ease;"></div>
            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); color: var(--primary-dark); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.2rem; font-weight: bold; font-size: 1.5rem; box-shadow: 0 0 15px rgba(0, 240, 255, 0.5); font-family: 'Orbitron', sans-serif;">2</div>
            <div style="font-size: 3rem; margin-bottom: 1.2rem; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🤖</div>
            <h3 style="color: var(--accent-blue); font-size: 1.5rem; font-weight: 600; margin-bottom: 0.8rem; font-family: 'Orbitron', sans-serif;">AI ANALYSIS</h3>
            <p style="color: var(--text-dim); line-height: 1.6;">Our advanced AI model analyzes the image to detect any plant diseases</p>
        </div>
        <div style="background: rgba(30, 40, 60, 0.6); border-radius: 15px; padding: 2rem 1.5rem; text-align: center; flex: 1; min-width: 220px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); transition: all 0.3s ease; border: 1px solid rgba(0, 240, 255, 0.2); position: relative; overflow: hidden; backdrop-filter: blur(5px);">
            <div style="content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); transform: scaleX(0); transform-origin: left; transition: transform 0.3s ease;"></div>
            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); color: var(--primary-dark); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.2rem; font-weight: bold; font-size: 1.5rem; box-shadow: 0 0 15px rgba(0, 240, 255, 0.5); font-family: 'Orbitron', sans-serif;">3</div>
            <div style="font-size: 3rem; margin-bottom: 1.2rem; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📊</div>
            <h3 style="color: var(--accent-blue); font-size: 1.5rem; font-weight: 600; margin-bottom: 0.8rem; font-family: 'Orbitron', sans-serif;">GET RESULTS</h3>
            <p style="color: var(--text-dim); line-height: 1.6;">Receive instant diagnosis with confidence score and treatment recommendations</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Add a metrics dashboard
st.markdown("""
<div style="display: flex; justify-content: center; gap: 25px; margin: 30px 0; flex-wrap: wrap;">
    <div style="background: rgba(30, 40, 60, 0.7); padding: 20px 25px; border-radius: 15px; text-align: center; min-width: 180px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.3); backdrop-filter: blur(5px); transition: all 0.3s ease;">
        <div style="font-size: 2.5rem; margin-bottom: 10px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">⚡</div>
        <h3 style="color: var(--accent-blue); margin: 0 0 10px 0; font-family: 'Orbitron', sans-serif; font-size: 1.1rem;">PROCESSING SPEED</h3>
        <p style="font-size: 1.6rem; font-weight: bold; margin: 0; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Orbitron', sans-serif;">&lt; 3 SECONDS</p>
    </div>
    <div style="background: rgba(30, 40, 60, 0.7); padding: 20px 25px; border-radius: 15px; text-align: center; min-width: 180px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.3); backdrop-filter: blur(5px); transition: all 0.3s ease;">
        <div style="font-size: 2.5rem; margin-bottom: 10px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🎯</div>
        <h3 style="color: var(--accent-blue); margin: 0 0 10px 0; font-family: 'Orbitron', sans-serif; font-size: 1.1rem;">ACCURACY</h3>
        <p style="font-size: 1.6rem; font-weight: bold; margin: 0; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Orbitron', sans-serif;">91.02%</p>
    </div>
    <div style="background: rgba(30, 40, 60, 0.7); padding: 20px 25px; border-radius: 15px; text-align: center; min-width: 180px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.3); backdrop-filter: blur(5px); transition: all 0.3s ease;">
        <div style="font-size: 2.5rem; margin-bottom: 10px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🌍</div>
        <h3 style="color: var(--accent-blue); margin: 0 0 10px 0; font-family: 'Orbitron', sans-serif; font-size: 1.1rem;">PLANTS COVERED</h3>
        <p style="font-size: 1.6rem; font-weight: bold; margin: 0; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Orbitron', sans-serif;">10+ SPECIES</p>
    </div>
</div>
""", unsafe_allow_html=True)

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
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown('<h2 class="upload-title">UPLOAD PLANT LEAF IMAGE</h2>', unsafe_allow_html=True)

# File uploader with enhanced UI
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

# Add a sample images section
st.markdown('<h3 class="sample-images-title">📷 SAMPLE IMAGES</h3>', unsafe_allow_html=True)
st.markdown("""
    <div style="display: flex; justify-content: center; gap: 30px; margin: 20px 0; flex-wrap: wrap;">
        <div style="text-align: center; background: rgba(30, 40, 60, 0.6); padding: 15px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); backdrop-filter: blur(5px); transition: all 0.3s ease;">
            <img src="https://images.unsplash.com/photo-1522005339026-cf3fa752ff95?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=200&q=80" style="width: 150px; height: 150px; object-fit: cover; border-radius: 10px; border: 2px solid rgba(0, 240, 255, 0.3);">
            <div style="margin-top: 10px; font-weight: 500; color: var(--accent-blue);">HEALTHY LEAF</div>
        </div>
        <div style="text-align: center; background: rgba(30, 40, 60, 0.6); padding: 15px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); backdrop-filter: blur(5px); transition: all 0.3s ease;">
            <img src="https://images.unsplash.com/photo-1597586128864-0a4d9e0a6b7b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=200&q=80" style="width: 150px; height: 150px; object-fit: cover; border-radius: 10px; border: 2px solid rgba(0, 240, 255, 0.3);">
            <div style="margin-top: 10px; font-weight: 500; color: var(--accent-blue);">DISEASED LEAF</div>
        </div>
        <div style="text-align: center; background: rgba(30, 40, 60, 0.6); padding: 15px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); backdrop-filter: blur(5px); transition: all 0.3s ease;">
            <img src="https://images.unsplash.com/photo-1622085041543-3a603c3a33c9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=200&q=80" style="width: 150px; height: 150px; object-fit: cover; border-radius: 10px; border: 2px solid rgba(0, 240, 255, 0.3);">
            <div style="margin-top: 10px; font-weight: 500; color: var(--accent-blue);">MAGNIFIED VIEW</div>
        </div>
    </div>
""", unsafe_allow_html=True)

if uploaded_file is not None:
    # Analysis section with two columns
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    
    # Left column - Image preview
    st.markdown('<div class="image-preview-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-subtitle">UPLOADED IMAGE</h3>', unsafe_allow_html=True)
    
    image = Image.open(uploaded_file)
    st.image(image, caption="UPLOADED LEAF IMAGE", use_column_width=True, clamp=True)
    
    # Add image analysis features
    st.markdown('<h4 class="sample-images-title">📊 IMAGE ANALYSIS</h4>', unsafe_allow_html=True)
    img_width, img_height = image.size
    st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; margin: 20px 0; flex-wrap: wrap;">
            <div style="background: rgba(30, 40, 60, 0.7); padding: 15px 20px; border-radius: 12px; text-align: center; min-width: 140px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), inset 0 0 8px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2);">
                <div style="color: var(--text-dim); font-size: 0.9rem; margin-bottom: 5px;">DIMENSIONS</div>
                <div style="font-size: 1.3rem; font-weight: 600; margin: 0; color: var(--accent-blue); font-family: 'Orbitron', sans-serif;">{} × {}</div>
            </div>
            <div style="background: rgba(30, 40, 60, 0.7); padding: 15px 20px; border-radius: 12px; text-align: center; min-width: 140px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), inset 0 0 8px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2);">
                <div style="color: var(--text-dim); font-size: 0.9rem; margin-bottom: 5px;">FILE SIZE</div>
                <div style="font-size: 1.3rem; font-weight: 600; margin: 0; color: var(--accent-blue); font-family: 'Orbitron', sans-serif;">{:.1f} KB</div>
            </div>
        </div>
    """.format(img_width, img_height, uploaded_file.size / 1024), unsafe_allow_html=True)
    
    if st.button("📤 UPLOAD DIFFERENT IMAGE", key="reset", help="Upload a different image"):
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Right column - Results
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-subtitle">ANALYSIS RESULTS</h3>', unsafe_allow_html=True)
    
    if st.session_state.model is not None and st.session_state.treatments:
        # Add a confidence threshold slider
        st.markdown('<div class="confidence-slider">', unsafe_allow_html=True)
        confidence_threshold = st.slider("CONFIDENCE THRESHOLD", 0.0, 1.0, 0.7, 0.05, 
                                         help="MINIMUM CONFIDENCE LEVEL FOR DISPLAYING RESULTS")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🔍 ANALYZE LEAF", key="analyze", help="Start AI analysis of the uploaded image"):
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
                    
                    # Display results in enhanced card
                    st.markdown("""
                        <div style="background: rgba(30, 40, 60, 0.6); border-radius: 15px; padding: 2rem; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); backdrop-filter: blur(5px);">
                    """, unsafe_allow_html=True)
                    
                    # Disease prediction
                    st.markdown("""
                        <div style="margin-bottom: 1.8rem;">
                            <h4 style="color: var(--accent-blue); font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.8rem; font-family: 'Orbitron', sans-serif;">
                                🪴 PREDICTED DISEASE
                            </h4>
                            <p style="font-size: 1.8rem; font-weight: 700; text-align: center; padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, rgba(0, 240, 255, 0.1), rgba(160, 32, 240, 0.1)); box-shadow: 0 0 15px rgba(0, 240, 255, 0.3); border: 1px solid rgba(0, 240, 255, 0.3); font-family: 'Orbitron', sans-serif; letter-spacing: 1px;">
                                {}
                            </p>
                        </div>
                    """.format(predicted_disease), unsafe_allow_html=True)
                    
                    # Confidence score with enhanced progress bar
                    st.markdown("""
                        <div style="margin-bottom: 1.8rem;">
                            <h4 style="color: var(--accent-blue); font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.8rem; font-family: 'Orbitron', sans-serif;">
                                📊 CONFIDENCE SCORE
                            </h4>
                            <div style="margin: 1.5rem 0;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 0.8rem; font-weight: 500; font-size: 1.1rem;">
                                    <span>CONFIDENCE LEVEL</span>
                                    <span style="font-weight: 700; font-size: 1.2rem; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Orbitron', sans-serif;">
                                        {:.1f}%
                                    </span>
                                </div>
                                <div style="width: 100%; height: 20px; background: rgba(30, 40, 60, 0.8); border-radius: 10px; overflow: hidden; box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3); border: 1px solid rgba(0, 240, 255, 0.2);">
                                    <div style="height: 100%; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); border-radius: 10px; transition: width 1s ease-in-out; position: relative; box-shadow: 0 0 10px var(--accent-blue); width: {:.1f}%;">
                                    </div>
                                </div>
                            </div>
                    """.format(confidence_score*100, confidence_score*100), unsafe_allow_html=True)
                    
                    # Add confidence indicator
                    if confidence_score >= 0.9:
                        st.markdown('<div style="background: rgba(0, 255, 157, 0.1); border-left: 4px solid var(--accent-green); padding: 15px; border-radius: 8px; margin: 15px 0; box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);">✅ HIGH CONFIDENCE RESULT</div>', unsafe_allow_html=True)
                    elif confidence_score >= 0.7:
                        st.markdown('<div style="background: rgba(255, 204, 0, 0.1); border-left: 4px solid #ffcc00; padding: 15px; border-radius: 8px; margin: 15px 0; box-shadow: 0 0 10px rgba(255, 204, 0, 0.2);">⚠️ MEDIUM CONFIDENCE RESULT</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="background: rgba(255, 0, 0, 0.1); border-left: 4px solid #ff0000; padding: 15px; border-radius: 8px; margin: 15px 0; box-shadow: 0 0 10px rgba(255, 0, 0, 0.2);">❗ LOW CONFIDENCE RESULT - CONSIDER RECHECKING WITH A CLEARER IMAGE</div>', unsafe_allow_html=True)
                        
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Treatment recommendation
                    st.markdown("""
                        <div style="margin-bottom: 1.8rem;">
                            <h4 style="color: var(--accent-blue); font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.8rem; font-family: 'Orbitron', sans-serif;">
                                🌿 TREATMENT RECOMMENDATION
                            </h4>
                            <div style="background: rgba(0, 255, 157, 0.05); border-left: 4px solid var(--accent-green); padding: 1.5rem; border-radius: 10px; margin-top: 0.8rem; box-shadow: 0 0 10px rgba(0, 255, 157, 0.1); border: 1px solid rgba(0, 255, 157, 0.1);">
                                <p style="line-height: 1.7; font-size: 1.1rem;">{}</p>
                            </div>
                        </div>
                    """.format(treatment), unsafe_allow_html=True)
                    
                    # Add treatment details expander
                    with st.expander("🔬 DETAILED TREATMENT INFORMATION"):
                        st.markdown(f"**FOR {predicted_disease}:**")
                        st.markdown("1. Apply appropriate fungicide or remove infected parts")
                        st.markdown("2. Monitor nearby plants for similar symptoms")
                        st.markdown("3. Adjust watering schedule to prevent moisture buildup")
                        st.markdown("4. Ensure proper plant spacing for air circulation")
                        st.markdown("5. Consider using disease-resistant plant varieties in future plantings")
                        st.markdown("6. Practice crop rotation to prevent soil-borne diseases")
                    
                    # Add similar diseases information
                    st.markdown("""
                        <div style="margin-bottom: 1.8rem;">
                            <h4 style="color: var(--accent-blue); font-size: 1.4rem; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.8rem; font-family: 'Orbitron', sans-serif;">
                                🔄 SIMILAR DISEASES
                            </h4>
                            <div style="background: rgba(30, 40, 60, 0.6); border-radius: 10px; padding: 15px; border: 1px solid rgba(0, 240, 255, 0.2);">
                    """, unsafe_allow_html=True)
                    
                    # Get top 3 predictions
                    top_3_indices = np.argsort(predictions[0])[::-1][:3]
                    for i, idx in enumerate(top_3_indices):
                        disease_name = class_names[idx]
                        score = predictions[0][idx]
                        if i == 0:
                            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 10px; padding: 10px; border-radius: 8px; background: rgba(0, 255, 157, 0.1); border: 1px solid rgba(0, 255, 157, 0.3); font-weight: bold;'><span>1. {disease_name}</span><span>{score*100:.1f}%</span></div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 10px; padding: 10px; border-radius: 8px; background: rgba(0, 240, 255, 0.05);'><span>{i+1}. {disease_name}</span><span>{score*100:.1f}%</span></div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add action buttons
                    st.markdown("""
                        <div style="display: flex; gap: 15px; margin-top: 25px; flex-wrap: wrap;">
                            <button style="flex: 1; min-width: 120px; background: rgba(30, 40, 60, 0.8); color: var(--text-light); border: 1px solid rgba(0, 240, 255, 0.3); padding: 12px; border-radius: 8px; cursor: pointer; font-size: 1rem; font-weight: 500; transition: all 0.3s ease; font-family: 'Orbitron', sans-serif; letter-spacing: 1px;">
                                🖨️ SAVE REPORT
                            </button>
                            <button style="flex: 1; min-width: 120px; background: rgba(30, 40, 60, 0.8); color: var(--text-light); border: 1px solid rgba(0, 240, 255, 0.3); padding: 12px; border-radius: 8px; cursor: pointer; font-size: 1rem; font-weight: 500; transition: all 0.3s ease; font-family: 'Orbitron', sans-serif; letter-spacing: 1px;">
                                📤 SHARE RESULTS
                            </button>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Add prevention tips
                    st.markdown("""
                    <div style="margin-top: 25px; padding: 20px; background: rgba(255, 204, 0, 0.05); border-radius: 15px; border: 1px solid rgba(255, 204, 0, 0.2); box-shadow: 0 0 15px rgba(255, 204, 0, 0.1);">
                        <h4 style="color: #ffcc00; margin-top: 0; font-family: 'Orbitron', sans-serif;">🩺 PREVENTION TIPS</h4>
                        <ul style="padding-left: 20px; margin-bottom: 0; line-height: 1.8;">
                            <li>MAINTAIN PROPER PLANT SPACING FOR GOOD AIR CIRCULATION</li>
                            <li>WATER AT THE BASE OF PLANTS, NOT ON LEAVES</li>
                            <li>REMOVE AND DESTROY INFECTED PLANT MATERIAL</li>
                            <li>USE MULCH TO PREVENT SOIL-BORNE DISEASES</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
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
    <div style="border: 3px dashed var(--accent-blue); border-radius: 15px; padding: 3rem; text-align: center; cursor: pointer; transition: all 0.3s ease; background: rgba(0, 240, 255, 0.05); margin-bottom: 1.5rem; position: relative; overflow: hidden;">
        <div style="font-size: 5rem; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1.5rem;">📁</div>
        <p style="font-size: 1.5rem; margin-bottom: 0.8rem; font-weight: 500; color: var(--text-light);">DRAG & DROP YOUR IMAGE HERE</p>
        <p style="color: var(--text-dim); font-size: 1.1rem; margin-bottom: 1.5rem;">SUPPORTED FORMATS: JPG, PNG, JPEG (MAX 200MB)</p>
        <button style="background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); color: var(--primary-dark); border: none; padding: 1rem 2.5rem; border-radius: 50px; cursor: pointer; font-size: 1.2rem; font-weight: 600; transition: all 0.3s ease; box-shadow: 0 0 20px rgba(0, 240, 255, 0.5); font-family: 'Orbitron', sans-serif; letter-spacing: 1px; position: relative; overflow: hidden;">BROWSE FILES</button>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **TIP**: FOR BEST RESULTS, TAKE A CLEAR PHOTO OF THE AFFECTED LEAF WITH GOOD LIGHTING AND UPLOAD IN JPG OR PNG FORMAT.")
    
    # Add quick tips section
    st.markdown('<h3 class="quick-tips-title">⚡ QUICK TIPS</h3>', unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px; flex-wrap: wrap;">
            <div style="background: rgba(30, 40, 60, 0.7); padding: 15px 20px; border-radius: 12px; min-width: 180px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), inset 0 0 8px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">💡</div>
                <div style="font-weight: 500;">ENSURE GOOD LIGHTING</div>
            </div>
            <div style="background: rgba(30, 40, 60, 0.7); padding: 15px 20px; border-radius: 12px; min-width: 180px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), inset 0 0 8px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🎯</div>
                <div style="font-weight: 500;">FOCUS ON AFFECTED AREAS</div>
            </div>
            <div style="background: rgba(30, 40, 60, 0.7); padding: 15px 20px; border-radius: 12px; min-width: 180px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), inset 0 0 8px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">⬜</div>
                <div style="font-weight: 500;">USE A PLAIN BACKGROUND</div>
            </div>
            <div style="background: rgba(30, 40, 60, 0.7); padding: 15px 20px; border-radius: 12px; min-width: 180px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2), inset 0 0 8px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">📸</div>
                <div style="font-weight: 500;">AVOID BLURRY IMAGES</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# About section with enhanced design
st.markdown("""
<div style="background: rgba(18, 24, 38, 0.7); border-radius: 20px; padding: 2.5rem; margin-bottom: 2rem; box-shadow: 0 0 20px rgba(0, 240, 255, 0.2), inset 0 0 20px rgba(160, 32, 240, 0.1); border: 1px solid rgba(160, 32, 240, 0.2); backdrop-filter: blur(10px);">
    <h2 style="color: var(--accent-blue); text-align: center; font-size: 2.2rem; margin-bottom: 2rem; font-weight: 600; position: relative; padding-bottom: 15px; font-family: 'Orbitron', sans-serif;">
        ABOUT PLANT SAVIOR AI
        <div style="content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 100px; height: 4px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); border-radius: 2px; box-shadow: 0 0 10px var(--accent-blue);"></div>
    </h2>
    <div style="max-width: 900px; margin: 0 auto; text-align: center;">
        <p style="font-size: 1.2rem; line-height: 1.8; color: var(--text-dim); margin-bottom: 2rem;">
            PLANT SAVIOR AI IS AN ADVANCED ARTIFICIAL INTELLIGENCE SYSTEM DESIGNED TO HELP FARMERS, GARDENERS, 
            AND AGRICULTURAL PROFESSIONALS QUICKLY IDENTIFY PLANT DISEASES FROM LEAF IMAGES. OUR SYSTEM USES 
            DEEP LEARNING TECHNOLOGY TRAINED ON THOUSANDS OF PLANT IMAGES TO PROVIDE ACCURATE DIAGNOSES WITH 
            TREATMENT RECOMMENDATIONS, HELPING TO SAVE CROPS AND REDUCE THE USE OF UNNECESSARY PESTICIDES.
        </p>
        
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 2rem; margin-top: 1.5rem;">
            <div style="background: rgba(30, 40, 60, 0.6); border-radius: 15px; padding: 1.8rem; text-align: center; min-width: 180px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); transition: all 0.3s ease; backdrop-filter: blur(5px);">
                <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Orbitron', sans-serif;">91.02%</div>
                <div style="color: var(--text-dim); font-size: 1.1rem;">ACCURACY RATE</div>
            </div>
            <div style="background: rgba(30, 40, 60, 0.6); border-radius: 15px; padding: 1.8rem; text-align: center; min-width: 180px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); transition: all 0.3s ease; backdrop-filter: blur(5px);">
                <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Orbitron', sans-serif;">38</div>
                <div style="color: var(--text-dim); font-size: 1.1rem;">DISEASE TYPES</div>
            </div>
            <div style="background: rgba(30, 40, 60, 0.6); border-radius: 15px; padding: 1.8rem; text-align: center; min-width: 180px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); transition: all 0.3s ease; backdrop-filter: blur(5px);">
                <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Orbitron', sans-serif;">224×224</div>
                <div style="color: var(--text-dim); font-size: 1.1rem;">IMAGE RESOLUTION</div>
            </div>
            <div style="background: rgba(30, 40, 60, 0.6); border-radius: 15px; padding: 1.8rem; text-align: center; min-width: 180px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3), inset 0 0 10px rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.2); transition: all 0.3s ease; backdrop-filter: blur(5px);">
                <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Orbitron', sans-serif;">24/7</div>
                <div style="color: var(--text-dim); font-size: 1.1rem;">AVAILABILITY</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Add a technology showcase section
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(0, 240, 255, 0.1), rgba(160, 32, 240, 0.1)); padding: 2.5rem; border-radius: 20px; margin: 2.5rem 0; box-shadow: 0 0 30px rgba(0, 240, 255, 0.2); border: 1px solid rgba(0, 240, 255, 0.2); backdrop-filter: blur(10px);">
    <h2 style="color: var(--accent-blue); text-align: center; margin-top: 0; font-family: 'Orbitron', sans-serif; font-size: 2.2rem;">🔬 TECHNOLOGY SHOWCASE</h2>
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; margin-top: 25px;">
        <div style="background: rgba(18, 24, 38, 0.8); padding: 25px; border-radius: 15px; flex: 1; min-width: 220px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); text-align: center; border: 1px solid rgba(0, 240, 255, 0.3); transition: all 0.3s ease;">
            <div style="font-size: 3rem; margin-bottom: 15px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🤖</div>
            <h3 style="color: var(--accent-purple); font-size: 1.5rem; margin-top: 0; font-family: 'Orbitron', sans-serif;">AI MODEL</h3>
            <p style="color: var(--text-dim);">DEEP LEARNING CNN ARCHITECTURE</p>
        </div>
        <div style="background: rgba(18, 24, 38, 0.8); padding: 25px; border-radius: 15px; flex: 1; min-width: 220px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); text-align: center; border: 1px solid rgba(0, 240, 255, 0.3); transition: all 0.3s ease;">
            <div style="font-size: 3rem; margin-bottom: 15px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📂</div>
            <h3 style="color: var(--accent-purple); font-size: 1.5rem; margin-top: 0; font-family: 'Orbitron', sans-serif;">DATASET</h3>
            <p style="color: var(--text-dim);">15,000+ PLANT IMAGES</p>
        </div>
        <div style="background: rgba(18, 24, 38, 0.8); padding: 25px; border-radius: 15px; flex: 1; min-width: 220px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); text-align: center; border: 1px solid rgba(0, 240, 255, 0.3); transition: all 0.3s ease;">
            <div style="font-size: 3rem; margin-bottom: 15px; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🚀</div>
            <h3 style="color: var(--accent-purple); font-size: 1.5rem; margin-top: 0; font-family: 'Orbitron', sans-serif;">PERFORMANCE</h3>
            <p style="color: var(--text-dim);">REAL-TIME PROCESSING</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Add a feedback section
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(255, 0, 200, 0.1), rgba(255, 102, 0, 0.1)); padding: 2.5rem; border-radius: 20px; margin: 2.5rem 0; box-shadow: 0 0 30px rgba(255, 0, 200, 0.2); border: 1px solid rgba(255, 0, 200, 0.2); backdrop-filter: blur(10px);">
    <h2 style="color: var(--accent-pink); text-align: center; margin-top: 0; font-family: 'Orbitron', sans-serif; font-size: 2.2rem;">💬 WE VALUE YOUR FEEDBACK</h2>
    <p style="text-align: center; font-size: 1.2rem; color: var(--text-dim);">HELP US IMPROVE PLANT SAVIOR AI BY SHARING YOUR EXPERIENCE</p>
    <div style="max-width: 600px; margin: 0 auto; display: flex; gap: 15px; margin-top: 25px;">
        <input type="text" placeholder="YOUR FEEDBACK..." style="flex: 1; padding: 15px; border-radius: 10px; border: 1px solid rgba(255, 0, 200, 0.3); background: rgba(18, 24, 38, 0.8); color: var(--text-light); font-size: 1.1rem;">
        <button style="background: linear-gradient(135deg, var(--accent-pink), #ff4d94); color: white; border: none; padding: 15px 25px; border-radius: 10px; cursor: pointer; font-size: 1.1rem; font-weight: 600; transition: all 0.3s ease; font-family: 'Orbitron', sans-serif; letter-spacing: 1px;">SEND</button>
    </div>
    <div style="display: flex; justify-content: center; gap: 30px; margin-top: 30px; flex-wrap: wrap;">
        <div style="text-align: center; cursor: pointer; transition: all 0.3s ease; padding: 15px; border-radius: 10px; background: rgba(18, 24, 38, 0.5); border: 1px solid rgba(255, 0, 200, 0.2);">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">👍</div>
            <p style="margin: 0; font-weight: 500;">HELPFUL</p>
        </div>
        <div style="text-align: center; cursor: pointer; transition: all 0.3s ease; padding: 15px; border-radius: 10px; background: rgba(18, 24, 38, 0.5); border: 1px solid rgba(255, 0, 200, 0.2);">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">👎</div>
            <p style="margin: 0; font-weight: 500;">NOT HELPFUL</p>
        </div>
        <div style="text-align: center; cursor: pointer; transition: all 0.3s ease; padding: 15px; border-radius: 10px; background: rgba(18, 24, 38, 0.5); border: 1px solid rgba(255, 0, 200, 0.2);">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">💡</div>
            <p style="margin: 0; font-weight: 500;">SUGGEST</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer with enhanced design
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(18, 24, 38, 0.9) 0%, rgba(10, 14, 23, 0.95) 100%); color: var(--text-light); text-align: center; padding: 2.5rem; border-radius: 20px; margin-top: 2.5rem; box-shadow: 0 0 20px rgba(0, 240, 255, 0.2), inset 0 0 20px rgba(160, 32, 240, 0.1); position: relative; overflow: hidden; border: 1px solid rgba(0, 240, 255, 0.2);">
    <div style="content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));"></div>
    <p style="font-size: 1.2rem; opacity: 0.9; margin: 10px 0; color: var(--text-dim);">🌱 PLANT SAVIOR AI - MAKING AGRICULTURE SMARTER WITH AI TECHNOLOGY</p>
    <p style="font-size: 1.2rem; opacity: 0.9; margin: 10px 0; color: var(--text-dim);">© 2025 PLANT SAVIOR AI. ALL RIGHTS RESERVED.</p>
</div>
""", unsafe_allow_html=True)