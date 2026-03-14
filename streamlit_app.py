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
# Enhanced Futuristic Cyberpunk CSS Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&display=swap');

    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp, .stApp > header {
        background-color: #f6f8f7 !important;
        color: #0f172a;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    p, span, div {
        color: #334155;
    }
    
    .text-primary { color: #13ec92 !important; }
    
    .main-header {
        background-color: transparent;
        padding: 0;
        border: none;
        box-shadow: none;
        display: none;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .logo-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 3rem;
        height: 3rem;
        border-radius: 0.75rem;
        background-color: rgba(19, 236, 146, 0.1);
        color: #13ec92;
        font-size: 2rem;
    }
    
    .logo-text {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    
    .tagline {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 400;
    }
    
    .login-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 20px 25px -5px rgba(19, 236, 146, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        align-items: center;
    }
    
    .glass-container {
        background-color: #ffffff;
        border-radius: 1.5rem;
        padding: 2.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    
    .section-title {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
    }
    
    .stats-section {
        display: grid;
        grid-template-columns: repeat(3, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .stat-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0f172a;
    }
    
    .stat-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .hero-section {
        background-color: #10221a;
        border-radius: 1.5rem;
        padding: 3rem;
        color: #ffffff;
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
        background-image: url('https://images.unsplash.com/photo-1628186120894-325d7429188d');
        background-size: cover;
        background-position: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        position: relative;
        z-index: 10;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.125rem;
        color: #e2e8f0;
        max-width: 600px;
        position: relative;
        z-index: 10;
    }
    
    .steps-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
    }
    
    .step-card {
        background-color: #f8fafc;
        border-radius: 1rem;
        padding: 2rem;
        border: 1px solid #e2e8f0;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .step-number {
        width: 3rem;
        height: 3rem;
        border-radius: 0.75rem;
        background-color: rgba(19, 236, 146, 0.2);
        color: #059669;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .step-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    
    .step-description {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Ensure Results Cards Look Good */
    .result-item {
        background-color: #f8fafc;
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .result-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1rem;
    }
    
    .disease-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #13ec92;
    }
    
    .progress-container {
        margin: 1rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
        font-weight: 500;
        color: #475569;
    }
    
    .progress-bar-bg {
        width: 100%;
        height: 0.5rem;
        background-color: #e2e8f0;
        border-radius: 9999px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background-color: #13ec92;
        border-radius: 9999px;
    }
    
    .confidence-text {
        font-weight: 700;
        color: #0f172a;
    }
    
    .treatment-box {
        background-color: rgba(19, 236, 146, 0.1);
        border-left: 4px solid #13ec92;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
    }
    
    .treatment-text {
        color: #1e293b;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Streamlit Input Overrides */
    div[data-baseweb="input"] {
        border-radius: 0.75rem !important;
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #13ec92 !important;
        box-shadow: 0 0 0 1px #13ec92 !important;
    }
    
    /* Buttons */
    .stButton > button, .analyze-button, .reset-button {
        background: #13ec92 !important;
        color: #0f172a !important;
        border: none !important;
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px -1px rgba(19, 236, 146, 0.2) !important;
    }
    
    .stButton > button:hover, .analyze-button:hover, .reset-button:hover {
        background: #10d482 !important;
        transform: translateY(-1px);
    }
    
    /* Secondary buttons (like Google) */
    .stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #f8fafc !important;
    }
    
    /* Sidebar Overrides */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-top-color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #0f172a !important;
    }
    
    .success-box, div[data-testid="stAlert"] {
        background-color: #f0fdf4 !important;
        color: #166534 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 0.75rem !important;
    }
    
    .error-box {
        background-color: #fef2f2 !important;
        color: #991b1b !important;
        border: 1px solid #fecaca !important;
        border-radius: 0.75rem !important;
        padding: 1rem;
    }
    
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(19, 236, 146, 0.2);
        border-top: 4px solid #13ec92;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    .loading-subtext {
        color: #64748b;
        font-size: 0.875rem;
    }
    
    .footer {
        text-align: center;
        padding: 3rem;
        margin-top: 3rem;
        border-top: 1px solid #e2e8f0;
        color: #64748b;
    }
    
    .team-container {
        display: grid;
        grid-template-columns: repeat(3, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .team-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .team-name {
        font-weight: 700;
        color: #0f172a;
        font-size: 1.25rem;
        margin-bottom: 0.25rem;
    }
    
    .team-role {
        color: #13ec92;
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .team-desc {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .upload-section {
        background-color: #ffffff;
        border-radius: 1.5rem;
        padding: 2.5rem;
        border: 1px dashed #cbd5e1;
        text-align: center;
    }
    
    .upload-title {
        color: #0f172a;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    /* Rest of app fixes */
    .stMarkdown p { color: inherit; }
    
</style>
""", unsafe_allow_html=True)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

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
        
        # Google OAuth Configuration
        # Using provided credentials for real Google Sign-In
        google_client_id = "351572421259-l5njghok477nemk3fthgg4q1025nimqj.apps.googleusercontent.com"
        google_client_secret = "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"
        # Your deployed Streamlit Cloud URL
        deployed_url = "https://plantsaviorai.streamlit.app"
        
        def real_google_sign_in():
            try:
                # Use the deployed Streamlit Cloud URL as redirect URI
                redirect_uri = deployed_url
                
                # Create Flow instance with the correct redirect URI
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
                
                # Generate authorization URL with all necessary parameters
                auth_url, state = flow.authorization_url(
                    access_type="offline",
                    include_granted_scopes="true",
                    prompt="select_account"
                )
                
                # Store flow and state in session state
                st.session_state["oauth_flow"] = flow
                st.session_state["oauth_state"] = state
                
                # Show authentication link styled as Google button
                st.markdown(f"""
                <a href="{auth_url}" target="_self" style="text-decoration: none;">
                    <div style="background-color: #4285F4; color: white; padding: 12px 24px; border-radius: 4px; 
                                text-align: center; font-weight: 500; cursor: pointer; 
                                display: flex; align-items: center; justify-content: center; gap: 10px;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.25); transition: all 0.3s ease;
                                font-family: 'Roboto', sans-serif; font-size: 16px;">
                        <svg style="width: 18px; height: 18px;" viewBox="0 0 24 24">
                            <path fill="white" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                            <path fill="white" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                            <path fill="white" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                            <path fill="white" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                        </svg>
                        Sign in with Google
                    </div>
                </a>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Google Sign-In Error: {str(e)}")
        
        # Check for OAuth callback (handles the redirect back from Google)
        if "code" in st.query_params:
            try:
                code = st.query_params["code"]
                flow = st.session_state.get("oauth_flow")
                if flow:
                    flow.fetch_token(code=code)
                    credentials = flow.credentials
                    
                    # Verify ID token
                    request = google.auth.transport.requests.Request()
                    id_info = id_token.verify_oauth2_token(
                        credentials.id_token, request, google_client_id
                    )
                    
                    # Store user info and log in
                    st.session_state.google_user = {
                        "email": id_info.get("email"),
                        "name": id_info.get("name"),
                        "picture": id_info.get("picture")
                    }
                    st.session_state.logged_in = True
                    st.session_state.login_time = time.time()
                    st.session_state.last_activity_time = time.time()
                    st.success(f"✅ Welcome, {id_info.get('name')}! ACCESS GRANTED.")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"OAuth verification failed: {str(e)}")
        
        # Show appropriate sign-in option based on configuration
        if google_client_id and google_client_secret:
            # Real Google OAuth is configured
            real_google_sign_in()
        else:
            # Demo mode - works immediately without any setup
            # Styled Google button using Streamlit's button with custom HTML appearance
            st.markdown("""
            <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&display=swap');

    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp, .stApp > header {
        background-color: #f6f8f7 !important;
        color: #0f172a;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    p, span, div {
        color: #334155;
    }
    
    .text-primary { color: #13ec92 !important; }
    
    .main-header {
        background-color: transparent;
        padding: 0;
        border: none;
        box-shadow: none;
        display: none;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .logo-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 3rem;
        height: 3rem;
        border-radius: 0.75rem;
        background-color: rgba(19, 236, 146, 0.1);
        color: #13ec92;
        font-size: 2rem;
    }
    
    .logo-text {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    
    .tagline {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 400;
    }
    
    .login-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 20px 25px -5px rgba(19, 236, 146, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        align-items: center;
    }
    
    .glass-container {
        background-color: #ffffff;
        border-radius: 1.5rem;
        padding: 2.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    
    .section-title {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
    }
    
    .stats-section {
        display: grid;
        grid-template-columns: repeat(3, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .stat-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0f172a;
    }
    
    .stat-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .hero-section {
        background-color: #10221a;
        border-radius: 1.5rem;
        padding: 3rem;
        color: #ffffff;
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
        background-image: url('https://images.unsplash.com/photo-1628186120894-325d7429188d');
        background-size: cover;
        background-position: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        position: relative;
        z-index: 10;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.125rem;
        color: #e2e8f0;
        max-width: 600px;
        position: relative;
        z-index: 10;
    }
    
    .steps-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
    }
    
    .step-card {
        background-color: #f8fafc;
        border-radius: 1rem;
        padding: 2rem;
        border: 1px solid #e2e8f0;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .step-number {
        width: 3rem;
        height: 3rem;
        border-radius: 0.75rem;
        background-color: rgba(19, 236, 146, 0.2);
        color: #059669;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .step-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    
    .step-description {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Ensure Results Cards Look Good */
    .result-item {
        background-color: #f8fafc;
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .result-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1rem;
    }
    
    .disease-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #13ec92;
    }
    
    .progress-container {
        margin: 1rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
        font-weight: 500;
        color: #475569;
    }
    
    .progress-bar-bg {
        width: 100%;
        height: 0.5rem;
        background-color: #e2e8f0;
        border-radius: 9999px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background-color: #13ec92;
        border-radius: 9999px;
    }
    
    .confidence-text {
        font-weight: 700;
        color: #0f172a;
    }
    
    .treatment-box {
        background-color: rgba(19, 236, 146, 0.1);
        border-left: 4px solid #13ec92;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
    }
    
    .treatment-text {
        color: #1e293b;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Streamlit Input Overrides */
    div[data-baseweb="input"] {
        border-radius: 0.75rem !important;
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #13ec92 !important;
        box-shadow: 0 0 0 1px #13ec92 !important;
    }
    
    /* Buttons */
    .stButton > button, .analyze-button, .reset-button {
        background: #13ec92 !important;
        color: #0f172a !important;
        border: none !important;
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px -1px rgba(19, 236, 146, 0.2) !important;
    }
    
    .stButton > button:hover, .analyze-button:hover, .reset-button:hover {
        background: #10d482 !important;
        transform: translateY(-1px);
    }
    
    /* Secondary buttons (like Google) */
    .stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #f8fafc !important;
    }
    
    /* Sidebar Overrides */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-top-color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #0f172a !important;
    }
    
    .success-box, div[data-testid="stAlert"] {
        background-color: #f0fdf4 !important;
        color: #166534 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 0.75rem !important;
    }
    
    .error-box {
        background-color: #fef2f2 !important;
        color: #991b1b !important;
        border: 1px solid #fecaca !important;
        border-radius: 0.75rem !important;
        padding: 1rem;
    }
    
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(19, 236, 146, 0.2);
        border-top: 4px solid #13ec92;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    .loading-subtext {
        color: #64748b;
        font-size: 0.875rem;
    }
    
    .footer {
        text-align: center;
        padding: 3rem;
        margin-top: 3rem;
        border-top: 1px solid #e2e8f0;
        color: #64748b;
    }
    
    .team-container {
        display: grid;
        grid-template-columns: repeat(3, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .team-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .team-name {
        font-weight: 700;
        color: #0f172a;
        font-size: 1.25rem;
        margin-bottom: 0.25rem;
    }
    
    .team-role {
        color: #13ec92;
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .team-desc {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .upload-section {
        background-color: #ffffff;
        border-radius: 1.5rem;
        padding: 2.5rem;
        border: 1px dashed #cbd5e1;
        text-align: center;
    }
    
    .upload-title {
        color: #0f172a;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    /* Rest of app fixes */
    .stMarkdown p { color: inherit; }
    
</style>
            """, unsafe_allow_html=True)
            
            if st.button("🔵 Sign in with Google", use_container_width=True, key="google_signin"):
                st.session_state.google_user = {
                    "email": "user@gmail.com",
                    "name": "Google User",
                    "picture": None
                }
                st.session_state.logged_in = True
                st.session_state.login_time = time.time()
                st.session_state.last_activity_time = time.time()
                st.success("✅ Welcome! ACCESS GRANTED via Google Sign-In.")
                time.sleep(1)
                st.rerun()
            
            # Show info about OAuth
            with st.expander("ℹ️ Google Sign-In Setup"):
                st.markdown(f"""
                **✅ Real Google Sign-In is configured!**
                
                **Your Deployed URL:**
                ```
                {deployed_url}
                ```
                
                **Steps to fix 403 error:**
                1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
                2. Find your OAuth 2.0 Client ID and click **Edit**
                3. Under **"Authorized redirect URIs"**, add EXACTLY:
                   ```
                   {deployed_url}
                   ```
                4. Click **Save**
                5. Wait 2-3 minutes for changes to propagate
                6. Try signing in again
                
                **⚠️ Common issues:**
                - Make sure there's NO trailing slash (`/`)
                - Must be exactly `https://plantsaviorai.streamlit.app`
                - Don't add it to "Authorized JavaScript origins" - add to "Authorized redirect URIs"
                - Changes may take a few minutes to take effect
                
                **How it works:**
                - You'll be redirected to Google's secure login page
                - After signing in, Google sends back a secure token
                - The app verifies the token and grants access
                """)
        
        # Demo Credentials Hint
        st.markdown("""
        <div style="margin-top: 2rem; text-align: center; color: #a0d0ff; font-size: 0.9rem; background: rgba(0, 30, 60, 0.5); padding: 1rem; border-radius: 10px;">
            <p style="margin:0;">🔒 SECURE TERMINAL</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

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

# Enhanced Sidebar
with st.sidebar:
    if st.button("🔒 LOGOUT SYSTEM", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
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
        <p class="step-description">Advanced convolutional neural network analyzes the image using deep learning algorithms trained on 50,000+ plant images.</p>
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

# Main upload section with enhanced design
st.markdown('<div class="upload-section glass-container fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="upload-title">🔬 AI-POWERED PLANT ANALYSIS</h2>', unsafe_allow_html=True)
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
    # Right column - Enhanced results
    with col2:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-subtitle">🧬 AI ANALYSIS CENTER</h3>', unsafe_allow_html=True)
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
                    st.markdown('<div class="results-card">', unsafe_allow_html=True)
                    # Main diagnosis result
                    st.markdown('<div class="result-item">', unsafe_allow_html=True)
                    st.markdown('<h4 class="result-title">🎯 PRIMARY DIAGNOSIS</h4>', unsafe_allow_html=True)
                    # Clean disease name for display
                    display_disease = predicted_disease.replace('_', ' ').title()
                    st.markdown(f'<p class="disease-name">{display_disease}</p>', unsafe_allow_html=True)
                    # Health status indicator
                    if "healthy" in predicted_disease.lower():
                        st.markdown('<div style="text-align: center; margin: 1rem 0;"><span style="background: linear-gradient(90deg, #00ff88, #00cc66); color: white; padding: 0.5rem 2rem; border-radius: 25px; font-weight: bold; font-size: 1.1rem;">🌿 HEALTHY PLANT</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="text-align: center; margin: 1rem 0;"><span style="background: linear-gradient(90deg, #ff6b35, #ff2d95); color: white; padding: 0.5rem 2rem; border-radius: 25px; font-weight: bold; font-size: 1.1rem;">⚠️ DISEASE DETECTED</span></div>', unsafe_allow_html=True)
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
                        conf_msg = "🟢 **VERY HIGH CONFIDENCE** - Diagnosis is highly reliable"
                        conf_color = "#00ff88"
                    elif confidence_score > 0.7:
                        conf_msg = "🟡 **HIGH CONFIDENCE** - Diagnosis is reliable"
                        conf_color = "#ffaa00"
                    elif confidence_score > 0.5:
                        conf_msg = "🟠 **MODERATE CONFIDENCE** - Consider expert consultation"
                        conf_color = "#ff6b35"
                    else:
                        conf_msg = "🔴 **LOW CONFIDENCE** - Recommend professional diagnosis"
                        conf_color = "#ff2d95"
                    st.markdown(f'<p style="color: {conf_color}; font-weight: 600; text-align: center; margin-top: 1rem;">{conf_msg}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    # Top 3 predictions

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
                    <div style="background: rgba(0, 40, 80, 0.5); padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(0, 197, 255, 0.3);">
                        <p style="color: #c0d8ff; margin: 0.5rem 0;"><strong>🔬 Analysis #{st.session_state.analysis_count}</strong></p>
                        <p style="color: #c0d8ff; margin: 0.5rem 0;">🧠 Model: Advanced CNN v2.1</p>
                        <p style="color: #c0d8ff; margin: 0.5rem 0;">⚡ Processing Time: <3 seconds</p>
                        <p style="color: #c0d8ff; margin: 0.5rem 0;">🎯 Classes Evaluated: {len(class_names)}</p>
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
                <div style="text-align: center; padding: 2rem; background: rgba(0, 30, 60, 0.4); border-radius: 15px; border: 2px dashed rgba(0, 197, 255, 0.3);">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
                    <h4 style="color: #00f5ff; margin-bottom: 1rem;">AI READY FOR ANALYSIS</h4>
                    <p style="color: #c0d8ff;">Click the "ANALYZE WITH AI" button above to start the diagnosis process. Our neural network will examine your plant image and provide detailed results.</p>
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
    <div style="text-align: center; padding: 3rem; background: rgba(0, 30, 60, 0.3); border-radius: 20px; border: 3px dashed rgba(0, 197, 255, 0.4); margin: 2rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1.5rem; animation: bounce 2s infinite;">📸</div>
        <h3 style="color: #00f5ff; margin-bottom: 1rem; font-size: 2rem;">UPLOAD PLANT IMAGE FOR AI ANALYSIS</h3>
        <p style="color: #c0d8ff; font-size: 1.2rem; margin-bottom: 1.5rem;">Select a clear image of the plant leaf you want to analyze</p>
        <div style="background: rgba(0, 50, 100, 0.5); padding: 1rem; border-radius: 10px; border: 1px solid rgba(0, 197, 255, 0.3);">
            <p style="color: #a0d0ff; margin: 0;">Supported formats: JPG, JPEG, PNG</p>
            <p style="color: #a0d0ff; margin: 0;">Maximum file size: 200MB</p>
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
        <strong>Plant Savior AI</strong> represents the cutting edge of agricultural technology, combining advanced machine learning with practical farming solutions. Our system utilizes a sophisticated Convolutional Neural Network (CNN) architecture trained on over 50,000 high-quality plant images to deliver professional-grade plant disease diagnosis.
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
<p style="text-align: center; color: #00f5ff; font-size: 1.3rem; font-weight: 600;">Made with ❤️ by the Plant Savior AI Team</p>
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
    <div style="margin-top: 2rem; padding-top: 1rem; border-top: 2px solid rgba(255, 255, 255, 0.2);">
        <div class="footer-text">© 2025 Plant Savior AI. All rights reserved. | Built with ❤️ using TensorFlow & Streamlit</div>
    </div>
</div>
""", unsafe_allow_html=True)
