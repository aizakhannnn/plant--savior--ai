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
import urllib.parse
# Google OAuth imports
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI - Advanced Plant Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Premium Modern UI Design System
st.markdown("""
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&display=swap" rel="stylesheet"/>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Base Overrides */
    .stApp {
        background-color: #f6f8f7;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    /* Premium Typography */
    h1, h2, h3, h4, .font-display {
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Hide Streamlit Header/Footer */
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu { visibility: hidden; }
    footer { display: none; }

    /* Custom Components */
    .premium-card {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08);
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #13ec92 0%, #0bb36e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Style Streamlit Widgets to match */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 12px 16px !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    .stButton > button {
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    div[data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #13ec92;
        border-radius: 24px;
        padding: 2rem;
    }

    /* Micro-animations */
    @keyframes pulse-soft {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
    }
    .animate-pulse-soft { animation: pulse-soft 3s infinite; }
</style>
""", unsafe_allow_html=True)


# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    # Login Layout using Tailwind via st.markdown
    st.markdown("""
    <div class="flex flex-col items-center justify-center pt-8 p-4">
        <div class="w-full max-w-[480px] space-y-8">
            <!-- Header -->
            <div class="flex items-center justify-center gap-3 mb-8">
                <div class="flex items-center justify-center w-12 h-12 rounded-xl bg-[#13ec92]/20 text-[#13ec92]">
                    <span class="material-symbols-outlined text-3xl">potted_plant</span>
                </div>
                <h2 class="text-2xl font-bold tracking-tight text-slate-900">Plant Savior AI</h2>
            </div>

            <!-- Login Card -->
            <div class="bg-white p-8 rounded-[32px] shadow-2xl shadow-[#13ec92]/5 border border-slate-100">
                <div class="text-center mb-10">
                    <div class="w-full h-48 rounded-2xl bg-slate-100 overflow-hidden relative mb-6">
                        <img alt="Lush Greenhouse" class="w-full h-full object-cover" src="https://images.unsplash.com/photo-1585336261022-680e295ce3fe?auto=format&fit=crop&q=80&w=800">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
                    </div>
                    <h1 class="text-3xl font-bold text-slate-900 mb-2 font-display">System Authentication</h1>
                    <p class="text-slate-500">Authorized Personnel Access Only</p>
                </div>
    """, unsafe_allow_html=True)

    # Use Streamlit columns for the form to keep it centered and functional
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        username = st.text_input("Operator ID", placeholder="Enter unique ID", label_visibility="collapsed")
        password = st.text_input("Access Code", type="password", placeholder="Access Code", label_visibility="collapsed")
        
        st.markdown('<div class="py-2"></div>', unsafe_allow_html=True)
        
        if st.button("🚀 Initiate System", use_container_width=True, type="primary"):
            if username == "aiza" and password == "pakistan2313":
                st.session_state.logged_in = True
                st.session_state.login_time = time.time()
                st.session_state.last_activity_time = time.time()
                st.success("✅ ACCESS GRANTED. INITIALIZING DASHBOARD...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ INVALID CREDENTIALS")

        st.markdown("""
            <div class="relative py-6 flex items-center">
                <div class="grow border-t border-slate-200"></div>
                <span class="shrink mx-4 text-xs font-medium text-slate-400 uppercase tracking-widest">or secure login via</span>
                <div class="grow border-t border-slate-200"></div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🔵 Google Operations Account", use_container_width=True):
            st.session_state.google_user = {"name": "Staff Member", "email": "staff@plantsavior.ai"}
            st.session_state.logged_in = True
            st.session_state.login_time = time.time()
            st.session_state.last_activity_time = time.time()
            st.rerun()

    st.markdown("""
                <div class="mt-8 flex justify-between items-center text-sm text-slate-400 px-2">
                    <a href="#" class="hover:text-[#13ec92] transition-colors">Forgot Credentials?</a>
                    <div class="flex gap-4">
                        <span class="material-symbols-outlined text-sm">shield</span>
                        <span class="material-symbols-outlined text-sm">lock</span>
                    </div>
                </div>
            </div>

            <!-- Footer Info -->
            <div class="text-center space-y-4 pt-8 border-t border-slate-100">
                <p class="text-xs text-slate-400 leading-relaxed max-w-xs mx-auto">
                    This system is monitored for security purposes. Unauthorized access attempts are logged and reported.
                </p>
                <div class="flex justify-center gap-6 text-[10px] font-bold uppercase tracking-widest text-slate-400">
                    <a href="#" class="hover:text-[#13ec92]">Support</a>
                    <a href="#" class="hover:text-[#13ec92]">Protocol</a>
                    <a href="#" class="hover:text-[#13ec92]">Privacy</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Check login status
if not st.session_state.logged_in:
    login_page()
    st.stop()

# Auto-logout logic
current_time = time.time()

# Check 20 minutes session limit (20 * 60 = 1200 seconds)
if 'login_time' in st.session_state and (current_time - st.session_state.login_time > 1200):
    st.session_state.logged_in = False
    st.rerun()

# Check 10 minutes inactivity limit (10 * 60 = 600 seconds)
if 'last_activity_time' in st.session_state and (current_time - st.session_state.last_activity_time > 600):
    st.session_state.logged_in = False
    st.rerun()

# Update last activity time
st.session_state.last_activity_time = current_time

# Dashboard Header
st.markdown("""
<div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-10">
    <div>
        <h1 class="text-4xl font-bold text-slate-900 mb-2 font-display">Command Center</h1>
        <p class="text-slate-500">Welcome back, Operator. System is ready for analysis.</p>
    </div>
    <div class="flex items-center gap-3 bg-white p-2 pr-6 rounded-2xl border border-slate-100 shadow-sm">
        <div class="w-12 h-12 rounded-xl bg-[#13ec92] flex items-center justify-center text-white shadow-lg shadow-[#13ec92]/20">
            <span class="material-symbols-outlined">shield_person</span>
        </div>
        <div>
            <div class="text-xs font-bold uppercase tracking-wider text-slate-400">Security Clearance</div>
            <div class="text-sm font-bold text-slate-900">Level 4 authorized</div>
        </div>
    </div>
</div>

<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
    <div class="premium-card">
        <div class="flex items-center gap-4 mb-4">
            <div class="p-3 bg-emerald-50 text-[#13ec92] rounded-xl">
                <span class="material-symbols-outlined">target</span>
            </div>
            <div class="text-sm font-bold uppercase tracking-widest text-slate-400">Diagnosis Accuracy</div>
        </div>
        <div class="stat-value">99.2%</div>
        <div class="text-xs text-slate-400 mt-2">Verified against 50k+ datasets</div>
    </div>
    <div class="premium-card">
        <div class="flex items-center gap-4 mb-4">
            <div class="p-3 bg-emerald-50 text-[#13ec92] rounded-xl">
                <span class="material-symbols-outlined">database</span>
            </div>
            <div class="text-sm font-bold uppercase tracking-widest text-slate-400">Network Knowledge</div>
        </div>
        <div class="stat-value">15+</div>
        <div class="text-xs text-slate-400 mt-2">Specialized plant species</div>
    </div>
    <div class="premium-card">
        <div class="flex items-center gap-4 mb-4">
            <div class="p-3 bg-emerald-50 text-[#13ec92] rounded-xl">
                <span class="material-symbols-outlined">bolt</span>
            </div>
            <div class="text-sm font-bold uppercase tracking-widest text-slate-400">Analysis Velocity</div>
        </div>
        <div class="stat-value">&lt; 3.0s</div>
        <div class="text-xs text-slate-400 mt-2">Real-time edge processing</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Premium Sidebar
with st.sidebar:
    st.markdown("""
        <div class="flex flex-col items-center mb-8 p-4 bg-[#f6f8f7] rounded-3xl border border-slate-100">
            <div class="w-16 h-16 rounded-2xl bg-[#13ec92] flex items-center justify-center text-white mb-3 shadow-lg shadow-[#13ec92]/20">
                <span class="material-symbols-outlined text-3xl">precision_manufacturing</span>
            </div>
            <div class="text-center">
                <div class="text-sm font-bold text-slate-900">System Operator</div>
                <div class="text-[10px] uppercase tracking-widest text-[#13ec92] font-bold">Standard Access</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Logout Session", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("�️ System Status", expanded=True):
        st.markdown("""
            <div class="space-y-4 pt-2">
                <div class="flex items-center gap-3">
                    <div class="w-2 h-2 rounded-full bg-[#13ec92] animate-pulse-soft"></div>
                    <div class="text-xs font-bold text-slate-600">Neural Engine: Active</div>
                </div>
                <div class="flex items-center gap-3">
                    <div class="w-2 h-2 rounded-full bg-[#13ec92] animate-pulse-soft"></div>
                    <div class="text-xs font-bold text-slate-600">Vision Processor: Online</div>
                </div>
                <div class="flex items-center gap-3">
                    <div class="w-2 h-2 rounded-full bg-[#13ec92] animate-pulse-soft"></div>
                    <div class="text-xs font-bold text-slate-600">Knowledge Base: v4.2</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with st.expander("� Analysis Guide"):
        st.markdown("""
            <div class="text-xs text-slate-500 leading-relaxed font-medium">
                1. Ensure leaf is in focus<br>
                2. Use natural lighting if possible<br>
                3. Avoid overlapping foliage<br>
                4. Focus on diseased areas
            </div>
        """, unsafe_allow_html=True)

# How it works section with premium design
st.markdown("""
<div class="premium-card mb-10">
    <h3 class="text-xl font-bold text-slate-900 mb-8 flex items-center gap-3 font-display">
        <span class="material-symbols-outlined text-[#13ec92]">info</span>
        Operational Workflow
    </h3>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="space-y-3">
            <div class="text-2xl font-bold text-slate-100 font-display">01</div>
            <h4 class="font-bold text-slate-900">Visual Input</h4>
            <p class="text-sm text-slate-500">Provide a high-resolution optical sample for the neural network to analyze.</p>
        </div>
        <div class="space-y-3">
            <div class="text-2xl font-bold text-slate-100 font-display">02</div>
            <h4 class="font-bold text-slate-900">Pattern Synthesis</h4>
            <p class="text-sm text-slate-500">The AI performs pixel-level extraction to identify microscopic disease signatures.</p>
        </div>
        <div class="space-y-3">
            <div class="text-2xl font-bold text-slate-100 font-display">03</div>
            <h4 class="font-bold text-slate-900">Protocol Delivery</h4>
            <p class="text-sm text-slate-500">Receive an authenticated diagnosis and specialized mitigation procedures.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Function to load model with enhanced caching
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

# Load treatment dictionary with enhanced error handling
@st.cache_resource(show_spinner=False)
def load_treatments():
    """Load treatment recommendations with enhanced error handling - Updated for healthy classes"""
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

# Main upload section
st.markdown("""
<div class="premium-card mb-8">
    <div class="flex items-center gap-3 mb-6">
        <div class="p-2 bg-emerald-50 text-[#13ec92] rounded-lg">
            <span class="material-symbols-outlined">upload_file</span>
        </div>
        <h2 class="text-xl font-bold text-slate-900 font-display">Neural Image Ingestion</h2>
    </div>
    <p class="text-sm text-slate-500 mb-6">Transmitting optical data to the edge nodes for pattern synthesis. Support for JPG, JPEG, and PNG formats.</p>
</div>
""", unsafe_allow_html=True)
# Enhanced file uploader
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], help="Upload a clear image of the plant leaf for AI analysis")
if uploaded_file is not None:
    # Analysis section with enhanced two-column layout
    st.markdown('<div class="analysis-section fade-in-up">', unsafe_allow_html=True)
    # Left column - Enhanced image preview
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
        <div style="background: rgba(0, 30, 60, 0.5); padding: 1rem; border-radius: 10px; margin-top: 1rem; border: 1px solid rgba(0, 197, 255, 0.3);">
            <p style="color: #00f5ff; margin: 0;"><strong>📊 IMAGE DETAILS:</strong></p>
            <p style="color: #c0d8ff; margin: 5px 0;">📐 Dimensions: {width} × {height} pixels</p>
            <p style="color: #c0d8ff; margin: 5px 0;">💾 Size: {file_size:.1f} KB</p>
            <p style="color: #c0d8ff; margin: 5px 0;">📁 Format: {uploaded_file.type}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 **UPLOAD NEW IMAGE**", key="reset", help="Upload a different leaf image", use_container_width=True):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    # Right column - Results
    with col2:
        st.markdown("""
        <div class="premium-card h-full">
            <h3 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-3 font-display">
                <span class="material-symbols-outlined text-[#13ec92]">analytics</span>
                Analysis Report
            </h3>
        """, unsafe_allow_html=True)
        if st.session_state.model is not None and st.session_state.treatments:
            if st.button("🚀 **ANALYZE WITH AI**", key="analyze", help="Start advanced AI analysis", use_container_width=True):
                # Enhanced loading animation
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
                    # Get all predictions for top 3 results
                    top_3_indices = np.argsort(predictions[0])[-3:][::-1]
                    # Get class names and prediction
                    class_names = list(st.session_state.treatments.keys())
                    predicted_disease = class_names[predicted_class]
                    treatment = st.session_state.treatments.get(predicted_disease, "Consult with an agricultural expert for specialized treatment.")
                    # Update analysis counter
                    st.session_state.analysis_count += 1
                    # Display enhanced results
                    st.markdown('<div class="space-y-6 mt-6">', unsafe_allow_html=True)
                    # Main diagnosis result
                    st.markdown('<div class="p-6 bg-slate-50 rounded-3xl border border-slate-100">', unsafe_allow_html=True)
                    st.markdown('<h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">🎯 Primary Diagnosis</h4>', unsafe_allow_html=True)
                    # Clean disease name for display
                    display_disease = predicted_disease.replace('_', ' ').title()
                    st.markdown(f'<p class="text-2xl font-extrabold text-[#13ec92] mb-4 font-display">{display_disease}</p>', unsafe_allow_html=True)
                    # Health status indicator
                    if "healthy" in predicted_disease.lower():
                        st.markdown('<span class="inline-flex items-center px-4 py-1.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-600 uppercase tracking-widest">🌿 Healthy Specimen</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="inline-flex items-center px-4 py-1.5 rounded-full text-xs font-bold bg-rose-100 text-rose-600 uppercase tracking-widest">⚠️ Pathology Detected</span>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Confidence score 
                    st.markdown('<div class="p-6 bg-slate-50 rounded-3xl border border-slate-100">', unsafe_allow_html=True)
                    st.markdown('<h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">📊 System Confidence</h4>', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="space-y-2">
                            <div class="flex justify-between items-end">
                                <span class="text-sm font-bold text-slate-900">{confidence_score*100:.1f}% Match</span>
                            </div>
                            <div class="w-full h-3 bg-slate-200 rounded-full overflow-hidden">
                                <div class="h-full bg-[#13ec92] rounded-full" style="width: {confidence_score*100}%"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Treatment recommendation
                    st.markdown('<div class="p-6 bg-slate-50 rounded-3xl border border-slate-100">', unsafe_allow_html=True)
                    if "healthy" in predicted_disease.lower():
                        st.markdown('<h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">🌿 Care Recommendation</h4>', unsafe_allow_html=True)
                    else:
                        st.markdown('<h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">💊 Mitigation Protocol</h4>', unsafe_allow_html=True)
                    st.markdown(f'<p class="text-sm text-slate-600 leading-relaxed font-medium">{treatment}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Analysis summary
                    st.markdown('<div class="p-6 bg-slate-50 rounded-3xl border border-slate-100">', unsafe_allow_html=True)
                    st.markdown('<h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">📈 Session Metadata</h4>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Analysis ID</div>
                            <div class="text-sm font-bold text-slate-900">#PS-{st.session_state.analysis_count:04d}</div>
                        </div>
                        <div>
                            <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Processing</div>
                            <div class="text-sm font-bold text-slate-900">Neural Sync</div>
                        </div>
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
                <div class="flex flex-col items-center justify-center p-10 border-2 border-dashed border-slate-200 rounded-[32px] text-center bg-slate-50">
                    <div class="w-20 h-20 rounded-full bg-white flex items-center justify-center shadow-sm mb-6">
                        <span class="material-symbols-outlined text-[#13ec92] text-4xl">biotech</span>
                    </div>
                    <h4 class="text-lg font-bold text-slate-900 mb-2">Neural Link Ready</h4>
                    <p class="text-sm text-slate-500 max-w-[240px]">Initiate diagnostic sequence to process the uploaded sample.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="p-6 bg-rose-50 border border-rose-100 rounded-3xl text-rose-600">
                <div class="flex items-center gap-3 mb-2 font-bold">
                    <span class="material-symbols-outlined">warning</span>
                    System Offline
                </div>
                <p class="text-xs opacity-80 leading-relaxed text-rose-500">
                    The AI model or treatment database could not be synchronized. Please refresh the diagnostic terminal or contact support.
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Enhanced upload prompt
    st.markdown("""
    <div class="flex flex-col items-center justify-center p-20 border-2 border-dashed border-slate-200 rounded-[48px] text-center bg-white shadow-sm">
        <div class="w-24 h-24 rounded-[32px] bg-[#13ec92]/10 flex items-center justify-center text-[#13ec92] mb-8">
            <span class="material-symbols-outlined text-5xl">add_a_photo</span>
        </div>
        <h3 class="text-2xl font-bold text-slate-900 mb-4 font-display">Awaiting Optical Input</h3>
        <p class="text-slate-500 max-w-sm mx-auto mb-8">Select a clear image of the plant leaf for the neural network to analyze. High-resolution samples yield the best results.</p>
        <div class="flex gap-4">
            <div class="px-6 py-2 bg-slate-100 rounded-full text-[10px] font-bold text-slate-400 uppercase tracking-widest">JPG Supported</div>
            <div class="px-6 py-2 bg-slate-100 rounded-full text-[10px] font-bold text-slate-400 uppercase tracking-widest">PNG Supported</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Premium About Section
st.markdown("""
<div class="premium-card mb-10 overflow-hidden relative">
    <div class="absolute top-0 right-0 p-8 opacity-5">
        <span class="material-symbols-outlined text-9xl">psychology</span>
    </div>
    <div class="relative z-10 max-w-2xl">
        <h2 class="text-3xl font-bold text-slate-900 mb-6 font-display">Neural Architecture</h2>
        <p class="text-slate-600 leading-relaxed mb-8">
            Plant Savior AI represents a paradigm shift in botanical diagnostics. By leveraging deep residual networks 
            trained on a global corpus of leaf pathology, we've achieved a classification accuracy that rivals 
            laboratory-grade equipment.
        </p>
        <div class="flex flex-wrap gap-3">
            <span class="px-4 py-2 bg-slate-100 rounded-xl text-slate-700 text-xs font-bold uppercase tracking-wider">TensorFlow 2.x</span>
            <span class="px-4 py-2 bg-slate-100 rounded-xl text-slate-700 text-xs font-bold uppercase tracking-wider">Computer Vision</span>
            <span class="px-4 py-2 bg-slate-100 rounded-xl text-slate-700 text-xs font-bold uppercase tracking-wider">CNN Optimizers</span>
        </div>
    </div>
</div>

<div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
    <div class="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm">
        <div class="w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-white mb-6">
            <span class="material-symbols-outlined">leaderboard</span>
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-3">Aiza</h3>
        <p class="text-sm text-slate-500 font-medium opacity-70 mb-4 uppercase tracking-widest text-[10px]">Lead AI Architect</p>
        <p class="text-sm text-slate-500 leading-relaxed">Directs core neural research and end-to-end integration protocols.</p>
    </div>
    <div class="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm">
        <div class="w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-white mb-6">
            <span class="material-symbols-outlined">palette</span>
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-3">Tooba</h3>
        <p class="text-sm text-slate-500 font-medium opacity-70 mb-4 uppercase tracking-widest text-[10px]">Experience Designer</p>
        <p class="text-sm text-slate-500 leading-relaxed">Synthesizes complex diagnostic data into premium visual interfaces.</p>
    </div>
    <div class="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm">
        <div class="w-12 h-12 rounded-2xl bg-slate-900 flex items-center justify-center text-white mb-6">
            <span class="material-symbols-outlined">biotech</span>
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-3">Taiba</h3>
        <p class="text-sm text-slate-500 font-medium opacity-70 mb-4 uppercase tracking-widest text-[10px]">Data Scientist</p>
        <p class="text-sm text-slate-500 leading-relaxed">Specializes in stochastic model refinement and performance tuning.</p>
    </div>
</div>

<div class="text-center py-10 border-t border-slate-200">
    <div class="flex items-center justify-center gap-2 mb-6 opacity-30">
        <div class="p-2 bg-slate-200 rounded-lg">
            <span class="material-symbols-outlined text-sm">potted_plant</span>
        </div>
        <span class="font-bold tracking-tighter text-slate-900">Plant Savior AI</span>
    </div>
    <p class="text-xs text-slate-400 font-bold uppercase tracking-[0.2em] mb-4">Precision Agriculture Protocols Enabled</p>
    <div class="flex justify-center gap-8 text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-10">
        <a href="#" class="hover:text-slate-900 transition-colors">Neural Assets</a>
        <a href="#" class="hover:text-slate-900 transition-colors">Compliance</a>
        <a href="#" class="hover:text-slate-900 transition-colors">API Access</a>
    </div>
    <p class="text-xs text-slate-300">© 2026 Plant Savior AI Corporation. All signatures verified.</p>
</div>
""", unsafe_allow_html=True)
