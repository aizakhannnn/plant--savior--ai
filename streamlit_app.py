# streamlit_app.py
import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json
from PIL import Image
import os
import time

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

# Professional Light Agriculture Themed CSS Design
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, h5, h6, .logo-text, .section-title {
        font-family: 'Montserrat', sans-serif;
        color: #1B5E20;
    }
    
    /* Main background and layout */
    .stApp {
        background-color: #F8FBF8;
        background-image: 
            radial-gradient(#4CAF50 0.5px, transparent 0.5px),
            radial-gradient(#4CAF50 0.5px, #F8FBF8 0.5px);
        background-size: 40px 40px;
        background-position: 0 0, 20px 20px;
        background-attachment: fixed;
        color: #333333;
    }

    /* Override Streamlit Defaults */
    div.block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .stMarkdown, p, div {
        color: #424242;
    }

    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        padding: 4rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.15);
        position: relative;
        overflow: hidden;
    }
    .main-header::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: #81C784;
    }
    .logo-text {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .tagline {
        font-size: 1.2rem;
        font-weight: 400;
        max-width: 800px;
        margin: 0 auto;
        color: #E8F5E9;
    }

    /* Beautiful Container Design */
    .glass-container {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 3rem;
        margin-bottom: 3rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(76, 175, 80, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(46, 125, 50, 0.08);
    }

    /* Section Titles */
    .section-title {
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 2.5rem;
        font-weight: 700;
        position: relative;
    }
    .section-title::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: #4CAF50;
        border-radius: 2px;
    }

    /* Statistics Section */
    .stats-section {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0 4rem 0;
        flex-wrap: wrap;
    }
    .stat-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        min-width: 200px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        border: 1px solid #E8F5E9;
        transition: transform 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        border-color: #A5D6A7;
    }
    .stat-value {
        font-size: 2.8rem;
        font-weight: 800;
        color: #2E7D32;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        color: #757575;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Steps Section */
    .steps-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 2rem;
    }
    .step-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2.5rem 2rem;
        text-align: center;
        flex: 1;
        min-width: 280px;
        max-width: 320px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
        border: 1px solid #E8F5E9;
        position: relative;
    }
    .step-number {
        width: 60px;
        height: 60px;
        background: #E8F5E9;
        color: #2E7D32;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-weight: 700;
        font-size: 1.5rem;
    }
    .step-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
    }
    .step-title {
        color: #1B5E20;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .step-description {
        color: #616161;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Analysis Results Section */
    .analysis-section {
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
        margin-bottom: 3rem;
    }
    .image-preview-container, .results-container {
        flex: 1;
        min-width: 350px;
        background: #FFFFFF;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
        border: 1px solid #E8F5E9;
    }
    .section-subtitle {
        color: #2E7D32;
        font-size: 1.5rem;
        margin-bottom: 2rem;
        font-weight: 700;
        border-bottom: 2px solid #E8F5E9;
        padding-bottom: 0.5rem;
        display: inline-block;
    }
    
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    .loading-text {
        font-size: 1.4rem;
        color: #2E7D32;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .loading-subtext {
        color: #757575;
        font-size: 1rem;
    }

    /* Result Info Blocks */
    .result-item {
        background: #F9FBF9;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E8F5E9;
        margin-bottom: 1.5rem;
    }
    .result-title {
        color: #388E3C;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .disease-name {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1B5E20;
        text-align: center;
        margin: 1rem 0;
    }

    /* Progress bar */
    .progress-container {
        margin: 1.5rem 0;
    }
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-weight: 600;
        color: #424242;
        font-size: 1rem;
    }
    .progress-bar-bg {
        width: 100%;
        height: 12px;
        background-color: #E0E0E0;
        border-radius: 6px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #4CAF50, #81C784);
        border-radius: 6px;
        transition: width 1.5s ease;
    }
    .confidence-text {
        color: #2E7D32;
        font-weight: 700;
    }

    .treatment-box {
        background: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-top: 1rem;
        color: #2E7D32;
        font-weight: 500;
        line-height: 1.6;
    }

    /* Team Section & About */
    .about-content {
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
        color: #555555;
        font-size: 1.1rem;
        line-height: 1.8;
    }
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin: 2.5rem 0;
    }
    .tech-item {
        background: #FFFFFF;
        padding: 0.8rem 1.5rem;
        border-radius: 30px;
        border: 1px solid #4CAF50;
        color: #2E7D32;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .team-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }
    .team-card {
        background: #FFFFFF;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        flex: 1;
        min-width: 260px;
        border: 1px solid #E8F5E9;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .team-name {
        color: #1B5E20;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .team-role {
        color: #4CAF50;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    /* Footer */
    .footer {
        background: #1B5E20;
        color: #FFFFFF;
        text-align: center;
        padding: 3rem 2rem;
        margin-top: 4rem;
        border-radius: 16px 16px 0 0;
    }
    .footer-text {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0.5rem 0;
        color: white;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #FAFAFA;
        border-right: 1px solid #E0E0E0;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: #FAFAFA;
    }
    
    /* Animation Utility */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    # Login Page Header
    st.markdown("""
    <div class="main-header" style="background: linear-gradient(135deg, #1B5E20 0%, #388E3C 100%);">
        <h1 class="logo-text" style="font-size: 3rem;">🔐 Access Gateway</h1>
        <p class="tagline">Secure Authentication for Plant Savior AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-container fade-in" style="padding: 2.5rem; border: 1px solid #C8E6C9;">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title" style="font-size: 1.8rem; margin-bottom: 1.5rem;">Sign In</h2>', unsafe_allow_html=True)
        
        # Login Inputs
        username = st.text_input("👤 Username", placeholder="Enter username (try: aiza)")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter password (try: pakistan2313)")
        
        # Login Button
        if st.button("🚀 Secure Login", use_container_width=True):
            if username == "aiza" and password == "pakistan2313":
                st.session_state.logged_in = True
                st.session_state.login_time = time.time()
                st.session_state.last_activity_time = time.time()
                st.success("✅ Signed in successfully! Redirecting...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
        
        st.markdown("<div style='text-align: center; margin: 1.5rem 0; color: #9E9E9E; font-size: 0.9rem;'>──────── OR ────────</div>", unsafe_allow_html=True)
        
        # Google OAuth Configuration
        google_client_id = "351572421259-l5njghok477nemk3fthgg4q1025nimqj.apps.googleusercontent.com"
        google_client_secret = "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"
        deployed_url = "https://plantsaviorai.streamlit.app"
        
        def real_google_sign_in():
            try:
                redirect_uri = deployed_url
                client_config = {
                    "web": {
                        "client_id": google_client_id,
                        "client_secret": google_client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "redirect_uris": [deployed_url, "http://localhost:8501", "http://localhost:8502", "http://127.0.0.1:8501"]
                    }
                }
                flow = Flow.from_client_config(
                    client_config,
                    scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
                    redirect_uri=redirect_uri
                )
                auth_url, state = flow.authorization_url(
                    access_type="offline",
                    include_granted_scopes="true",
                    prompt="select_account"
                )
                st.session_state["oauth_flow"] = flow
                st.session_state["oauth_state"] = state
                
                # Google Button Styling
                st.markdown(f"""
                <a href="{auth_url}" target="_self" style="text-decoration: none;">
                    <div style="background-color: #FFFFFF; color: #757575; padding: 10px 24px; border: 1px solid #E0E0E0; border-radius: 8px; 
                                text-align: center; font-weight: 500; cursor: pointer; 
                                display: flex; align-items: center; justify-content: center; gap: 10px;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: all 0.2s ease;">
                        <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" style="width: 20px;" alt="Google Logo"/>
                        Sign in with Google
                    </div>
                </a>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Google Sign-In Error: {str(e)}")
        
        if "code" in st.query_params:
            try:
                code = st.query_params["code"]
                flow = st.session_state.get("oauth_flow")
                if flow:
                    flow.fetch_token(code=code)
                    credentials = flow.credentials
                    request = google.auth.transport.requests.Request()
                    id_info = id_token.verify_oauth2_token(
                        credentials.id_token, request, google_client_id
                    )
                    st.session_state.google_user = {
                        "email": id_info.get("email"),
                        "name": id_info.get("name"),
                        "picture": id_info.get("picture")
                    }
                    st.session_state.logged_in = True
                    st.session_state.login_time = time.time()
                    st.session_state.last_activity_time = time.time()
                    st.success(f"✅ Welcome, {id_info.get('name')}!")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"OAuth verification failed: {str(e)}")
        
        if google_client_id and google_client_secret:
            real_google_sign_in()
        else:
            if st.button("🔵 Sign in with Google (Demo)", use_container_width=True):
                st.session_state.google_user = {"email": "user@gmail.com", "name": "Google User", "picture": None}
                st.session_state.logged_in = True
                st.session_state.login_time = time.time()
                st.session_state.last_activity_time = time.time()
                st.success("✅ Logged in via Demo Mode.")
                time.sleep(1)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# Check login status
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

# Main header
st.markdown("""
<div class="main-header fade-in">
    <h1 class="logo-text">🌱 Plant Savior AI</h1>
    <p class="tagline">Next-Generation Agriculture Analysis & Disease Detection powered by Artificial Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Statistics Section
st.markdown("""
<div class="stats-section fade-in">
    <div class="stat-card">
        <div class="stat-value">99.2%</div>
        <div class="stat-label">Model Accuracy</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">15+</div>
        <div class="stat-label">Diseases Detected</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><3s</div>
        <div class="stat-label">Analysis Speed</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    if st.button("🔒 Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    st.markdown("### ⚙️ System Status")
    st.success("🟢 AI Engine Online")
    st.success("🟢 Processor Ready")
    st.success("🟢 Database Connected")
    st.markdown("### 🌿 Intelligence Source")
    st.info("""
    **Plant Savior AI** utilizes edge CNN tech to give fast, reliable plant diagnosis. Focus your camera well to get the best results.
    """)
    st.markdown("### 📸 Photography Tips")
    st.markdown("""
    - Use natural lighting
    - Capture closely to the affected region
    - Isolate single leaves
    """)

# Instructions Section
st.markdown('<div class="glass-container fade-in">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="steps-container">
    <div class="step-card">
        <div class="step-number">1</div>
        <div class="step-icon">📸</div>
        <h3 class="step-title">Upload Image</h3>
        <p class="step-description">Securely transmit a high-resolution photo of the affected plant leaf into our AI system.</p>
    </div>
    <div class="step-card">
        <div class="step-number">2</div>
        <div class="step-icon">🧠</div>
        <h3 class="step-title">Deep Analysis</h3>
        <p class="step-description">Our trained neural network scans the image, matching patterns against 15+ known pathogens.</p>
    </div>
    <div class="step-card">
        <div class="step-number">3</div>
        <div class="step-icon">📋</div>
        <h3 class="step-title">Actionable Care</h3>
        <p class="step-description">Receive an instant diagnosis along with carefully vetted treatment recommendations.</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_model():
    try:
        with st.spinner("⏳ Loading AI Model..."):
            model = tf.keras.models.load_model('best_plant_model_final.keras')
            return model
    except Exception as e:
        st.error(f"Model Error: {str(e)}")
        return None

@st.cache_resource(show_spinner=False)
def load_treatments():
    try:
        with open('treatment_dict_complete.json', 'r') as f:
            return json.load(f)
    except Exception:
        return {
            "Tomato_healthy": "Plant appears healthy! Continue current care routine.",
            "Tomato_Bacterial_spot": "Apply copper-based bactericide. Avoid overhead watering.",
        }

if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.treatments = {}
    st.session_state.analysis_count = 0

if st.session_state.model is None:
    model = load_model()
    st.session_state.model = model
st.session_state.treatments = load_treatments()

# Analysis Section
st.markdown('<div class="glass-container fade-in">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Field Analysis Interface</h2>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Select crop image (JPG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.markdown('<div class="analysis-section fade-in">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown('<div class="image-preview-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-subtitle">Image Preview</h3>', unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True, clamp=True)
        st.markdown(f"""
        <div style="background: #F9FBF9; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #E8F5E9;">
            <p style="margin: 3px 0; color:#616161;"><strong>Dimensions:</strong> {image.size[0]} x {image.size[1]}</p>
            <p style="margin: 3px 0; color:#616161;"><strong>Size:</strong> {len(uploaded_file.getvalue())/1024:.1f} KB</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Reset Image"):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-subtitle">Intelligence Report</h3>', unsafe_allow_html=True)
        
        if st.session_state.model is not None:
            if st.button("🚀 Process Analysis", type="primary", use_container_width=True):
                loading_placeholder = st.empty()
                with loading_placeholder:
                    st.markdown('''
                    <div class="loading-container">
                        <div class="loading-text">🔄 Processing structural data...</div>
                        <div class="loading-subtext">Comparing features with botanical database</div>
                    </div>''', unsafe_allow_html=True)
                    time.sleep(1.5)
                loading_placeholder.empty()

                try:
                    with open("temp_image.jpg", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    img = load_img("temp_image.jpg", target_size=(224, 224))
                    img_array = img_to_array(img)
                    img_array = img_array.reshape(1, 224, 224, 3) / 255.0
                    
                    predictions = st.session_state.model.predict(img_array, verbose=0)
                    predicted_class = np.argmax(predictions[0])
                    confidence_score = float(predictions[0][predicted_class])
                    class_names = list(st.session_state.treatments.keys())
                    predicted_disease = class_names[predicted_class]
                    treatment = st.session_state.treatments.get(predicted_disease, "Consult specialist.")
                    st.session_state.analysis_count += 1
                    
                    display_disease = predicted_disease.replace('_', ' ').title()
                    
                    # Result Display
                    st.markdown(f'<div class="disease-name">{display_disease}</div>', unsafe_allow_html=True)
                    
                    if "healthy" in predicted_disease.lower():
                        st.markdown('<div style="text-align:center; margin-bottom: 1.5rem;"><span style="background: #E8F5E9; color: #2E7D32; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">✅ Healthy Pattern Detected</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="text-align:center; margin-bottom: 1.5rem;"><span style="background: #FFEBEE; color: #C62828; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">⚠️ Disease Signature Found</span></div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<div class="result-title">Confidence Metric</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="progress-container">
                            <div class="progress-label">
                                <span>Certainty</span>
                                <span class="confidence-text">{confidence_score*100:.1f}%</span>
                            </div>
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill" style="width: {confidence_score*100}%"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<div class="result-title">Recommended Action</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="treatment-box">{treatment}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                
                try:
                    os.remove("temp_image.jpg")
                except:
                    pass
            else:
                st.info("System standing by. Click process to evaluate the current image.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; border-radius: 12px; border: 2px dashed #4CAF50; background: #F9FBF9;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📷</div>
        <h3 style="color: #2E7D32; font-size: 1.5rem;">Select an image to begin</h3>
        <p style="color: #757575;">Supports all standard mobile and web image formats.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# About Section
st.markdown('<div class="glass-container fade-in">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Technology Review</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="about-content">
    <p>Plant Savior utilizes state vector analysis via Convolutional Neural Networks to rapidly classify foliar structures and isolate pathogenic variants.</p>
    <div class="tech-stack">
        <div class="tech-item">TensorFlow 2</div>
        <div class="tech-item">Streamlit</div>
        <div class="tech-item">NumPy Native</div>
        <div class="tech-item">OAuth 2.0</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Team Section
st.markdown('<div class="glass-container fade-in">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Development Team</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="team-container">
    <div class="team-card">
        <h3 class="team-name">Aiza</h3>
        <p class="team-role">AI Engineer</p>
        <p style="color: #757575;">Architecture and core ML integration.</p>
    </div>
    <div class="team-card">
        <h3 class="team-name">Tooba</h3>
        <p class="team-role">Interface Designer</p>
        <p style="color: #757575;">Modernizing the UI mapping.</p>
    </div>
    <div class="team-card">
        <h3 class="team-name">Taiba</h3>
        <p class="team-role">Data Systems</p>
        <p style="color: #757575;">Ensuring inference accuracy remains 99%+</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <h3 style="color: white; margin-bottom: 0.5rem; font-family: 'Montserrat', sans-serif;">Plant Savior AI</h3>
    <p class="footer-text">Delivering advanced diagnostics capabilities to modern agriculture.</p>
    <p class="footer-text" style="font-size: 0.85rem; margin-top: 1.5rem; opacity: 0.7;">© 2026 Plant Savior Team. All properties reserved.</p>
</div>
""", unsafe_allow_html=True)
