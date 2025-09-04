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

# Custom CSS for the best frontend design
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background and layout */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        padding: 2.5rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(46, 139, 87, 0.3);
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
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .tagline {
        font-size: 1.4rem;
        opacity: 0.95;
        font-weight: 300;
        max-width: 800px;
        margin: 0 auto;
        color: var(--text-secondary);
    }
    
    /* How It Works Section */
    .how-it-works {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    .section-title {
        color: #2E8B57;
        text-align: center;
        font-size: 2rem;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    .steps-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 1.5rem;
    }
    
    .step-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        flex: 1;
        min-width: 220px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 2px solid #e9ecef;
    }
    
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(46, 139, 87, 0.2);
        border-color: #3CB371;
    }
    
    .step-number {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.2rem;
        font-weight: bold;
        font-size: 1.2rem;
        box-shadow: 0 4px 8px rgba(46, 139, 87, 0.3);
    }
    
    .step-icon {
        font-size: 2.5rem;
        margin-bottom: 1.2rem;
        color: #2E8B57;
    }
    
    .step-title {
        color: #2E8B57;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    /* Upload Section */
    .upload-section {
        background: white;
        border-radius: 15px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .upload-title {
        color: #2E8B57;
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    
    /* Drop Zone */
    .drop-zone {
        border: 3px dashed #3CB371;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        background-color: #f8fff8;
        margin-bottom: 1.5rem;
    }
    
    .drop-zone:hover {
        background-color: #e8f5e9;
        border-color: #2E8B57;
        transform: scale(1.02);
    }
    
    .drop-zone.active {
        background-color: #e8f5e9;
        border-color: #FF6B35;
    }
    
    .upload-icon {
        font-size: 4rem;
        color: #2E8B57;
        margin-bottom: 1.5rem;
    }
    
    .drop-text {
        font-size: 1.3rem;
        color: #333;
        margin-bottom: 0.8rem;
        font-weight: 500;
    }
    
    .file-types {
        color: #6c757d;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .browse-button {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        border: none;
        padding: 0.9rem 2rem;
        border-radius: 50px;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);
    }
    
    .browse-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(46, 139, 87, 0.4);
    }
    
    .file-input {
        display: none;
    }
    
    /* Analysis Section */
    .analysis-section {
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }
    
    .image-preview-container {
        flex: 1;
        min-width: 300px;
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .results-container {
        flex: 1;
        min-width: 300px;
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .section-subtitle {
        color: #2E8B57;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        text-align: center;
    }
    
    .preview-image {
        width: 100%;
        max-height: 400px;
        object-fit: contain;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .reset-button {
        background: linear-gradient(135deg, #FF6B35 0%, #ff8c5a 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.8rem;
        border-radius: 50px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        margin-top: 1.5rem;
        width: 100%;
        box-shadow: 0 4px 10px rgba(255, 107, 53, 0.3);
    }
    
    .reset-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255, 107, 53, 0.4);
    }
    
    /* Loading State */
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    .spinner {
        width: 60px;
        height: 60px;
        border: 5px solid rgba(46, 139, 87, 0.3);
        border-top: 5px solid #2E8B57;
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
        color: #2E8B57;
        font-weight: 500;
    }
    
    .loading-subtext {
        color: #6c757d;
        margin-top: 0.5rem;
    }
    
    /* Results Card */
    .results-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .result-item {
        margin-bottom: 1.5rem;
    }
    
    .result-title {
        color: #2E8B57;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .disease-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Progress Bar */
    .progress-container {
        margin: 1rem 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .progress-bar-bg {
        width: 100%;
        height: 12px;
        background-color: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #4CAF50, #2E8B57);
        border-radius: 10px;
        transition: width 1s ease-in-out;
    }
    
    .confidence-text {
        font-weight: 600;
        color: #333;
    }
    
    /* Treatment Box */
    .treatment-box {
        background: #e8f5e9;
        border-left: 4px solid #4CAF50;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 0.5rem;
    }
    
    .treatment-text {
        line-height: 1.6;
        color: #333;
    }
    
    /* Analyze Button */
    .analyze-button {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        border: none;
        padding: 1.2rem;
        border-radius: 12px;
        cursor: pointer;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 6px 20px rgba(46, 139, 87, 0.4);
        margin-top: 1rem;
    }
    
    .analyze-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(46, 139, 87, 0.5);
    }
    
    .analyze-button:disabled {
        background: #cccccc;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    /* Error Message */
    .error-box {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #c62828;
    }
    
    /* About Section */
    .about-section {
        background: white;
        border-radius: 15px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .about-content {
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
    }
    
    .about-text {
        font-size: 1.1rem;
        line-height: 1.7;
        color: #555;
        margin-bottom: 2rem;
    }
    
    .stats-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 2rem;
        margin-top: 1.5rem;
    }
    
    .stat-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        min-width: 180px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2E8B57;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #6c757d;
        font-size: 1rem;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
    }
    
    .footer-text {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .logo-text {
            font-size: 2.5rem;
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
        
        .drop-zone {
            padding: 2rem 1rem;
        }
        
        .stat-card {
            min-width: 140px;
            padding: 1.2rem;
        }
        
        .stat-value {
            font-size: 1.8rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 1.5rem 1rem;
        }
        
        .logo-text {
            font-size: 2rem;
        }
        
        .tagline {
            font-size: 1rem;
        }
        
        .upload-section, .about-section, .image-preview-container, .results-container {
            padding: 1.5rem;
        }
        
        .step-card {
            min-width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main header with enhanced design
st.markdown("""
<div class="main-header">
    <h1 class="logo-text">🌱 Plant Savior AI</h1>
    <p class="tagline">Instant Plant Disease Detection using Advanced Artificial Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with additional information
with st.sidebar:
    st.markdown("### 🌿 About This Tool")
    st.info("""
    This AI-powered system helps farmers and gardeners detect plant diseases from leaf images with high accuracy.
    
    Simply upload a clear photo of a plant leaf and get instant diagnosis with treatment recommendations.
    """)
    
    st.markdown("### 📋 How to Get Best Results")
    st.markdown("""
    1. **Lighting**: Take photo in good natural light
    2. **Focus**: Ensure leaf is in sharp focus
    3. **Background**: Simple background works best
    4. **Angle**: Top-down view of the leaf
    5. **Symptoms**: Show affected areas clearly
    """)
    
    st.markdown("### 🎯 Supported Diseases")
    st.markdown("""
    - Tomato diseases (10 types)
    - Potato diseases (3 types)
    - Pepper diseases (2 types)
    """)
    
    st.markdown("### ℹ️ Need Help?")
    st.markdown("Contact: support@plantsavior.ai")

# How it works section with enhanced design
st.markdown('<div class="how-it-works">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="steps-container">
    <div class="step-card">
        <div class="step-number">1</div>
        <div class="step-icon">📸</div>
        <h3 class="step-title">Upload Image</h3>
        <p>Take a clear photo of the affected plant leaf and upload it to our system</p>
    </div>
    <div class="step-card">
        <div class="step-number">2</div>
        <div class="step-icon">🤖</div>
        <h3 class="step-title">AI Analysis</h3>
        <p>Our advanced AI model analyzes the image to detect any plant diseases</p>
    </div>
    <div class="step-card">
        <div class="step-number">3</div>
        <div class="step-icon">📊</div>
        <h3 class="step-title">Get Results</h3>
        <p>Receive instant diagnosis with confidence score and treatment recommendations</p>
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
    with st.spinner("Initializing Plant Savior AI System..."):
        model = load_model()
        treatments = load_treatments()
        st.session_state.model = model
        st.session_state.treatments = treatments

# Main content area
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown('<h2 class="upload-title">Upload Plant Leaf Image</h2>', unsafe_allow_html=True)

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
    
    # File preview
    file_size = len(uploaded_file.getvalue())
    size_mb = file_size / (1024 * 1024)
    st.markdown(f"""
    <div class="file-preview">
        <div class="file-info">
            <div class="file-icon">📄</div>
            <div>
                <div class="file-name">{uploaded_file.name}</div>
                <div class="file-size">{size_mb:.2f} MB</div>
            </div>
        </div>
        <div class="remove-file" onclick="document.getElementById('fileInput').value = '';">×</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📤 Upload Different Image", key="reset", help="Upload a different image"):
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Right column - Results
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-subtitle">Analysis Results</h3>', unsafe_allow_html=True)
    
    if st.session_state.model is not None and st.session_state.treatments:
        if st.button("🔍 Analyze Leaf", key="analyze", help="Start AI analysis of the uploaded image"):
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
                    st.markdown('<div class="results-card">', unsafe_allow_html=True)
                    
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
    # Enhanced upload interface with drag and drop
    st.markdown("""
    <div class="drop-zone" id="dropZone">
        <div class="upload-icon">📁</div>
        <p class="drop-text">Drag & Drop your image here</p>
        <p class="file-types">Supported formats: JPG, PNG, JPEG (Max 200MB)</p>
        <button class="browse-button" onclick="document.getElementById('fileInput').click()">Browse Files</button>
        <input type="file" id="fileInput" class="file-input" accept="image/jpeg,image/png,image/jpg">
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Tip**: For best results, take a clear photo of the affected leaf with good lighting and upload in JPG or PNG format.")

st.markdown('</div>', unsafe_allow_html=True)

# About section with enhanced design
st.markdown('<div class="about-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">About Plant Savior AI</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="about-content">
    <p class="about-text">
        Plant Savior AI is an advanced artificial intelligence system designed to help farmers, gardeners, 
        and agricultural professionals quickly identify plant diseases from leaf images. Our system uses 
        deep learning technology trained on thousands of plant images to provide accurate diagnoses with 
        treatment recommendations, helping to save crops and reduce the use of unnecessary pesticides.
    </p>
    
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-value">91.02%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">38</div>
            <div class="stat-label">Disease Types</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">224×224</div>
            <div class="stat-label">Image Resolution</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">24/7</div>
            <div class="stat-label">Availability</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer with enhanced design
st.markdown("""
<div class="footer">
    <p class="footer-text">🌱 Plant Savior AI - Making agriculture smarter with AI technology</p>
    <p class="footer-text">© 2025 Plant Savior AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)