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

# --- Configuration and Utility Functions ---

# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI - Instant Plant Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="auto"
)

# Nature-inspired color palette
PRIMARY_GREEN = "#2E8B57" # SeaGreen
ACCENT_ORANGE = "#FF6B35" # Burnt Orange
BACKGROUND_LIGHT = "#F8F8F8" # Light Grayish White
TEXT_DARK = "#333333"
TEXT_LIGHT = "#E0E0E0"
BORDER_GRAY = "#D0D0D0"

# Custom CSS for modern, nature-inspired design and responsiveness
st.markdown(f"""
<style>
    /* Google Fonts - Inter and Roboto for modern sans-serif */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');

    body {{
        font-family: 'Roboto', sans-serif;
        color: {TEXT_DARK};
        background-color: {BACKGROUND_LIGHT};
    }}
    
    .stApp {{
        background-color: {BACKGROUND_LIGHT};
    }}

    /* Typography */
    h1, .h1-font {{
        font-family: 'Inter', sans-serif;
        font-size: 32px; /* H1: 32px bold */
        font-weight: 700;
        color: {PRIMARY_GREEN};
        margin-bottom: 0.5em;
        line-height: 1.2;
    }}
    h2, .h2-font {{
        font-family: 'Inter', sans-serif;
        font-size: 24px; /* H2: 24px semi-bold */
        font-weight: 600;
        color: {PRIMARY_GREEN};
        margin-top: 1.5em;
        margin-bottom: 0.8em;
        line-height: 1.3;
    }}
    p, label, .stMarkdown, .stText, .stButton > button, .stFileUploader label, .stRadio > label, .stCheckbox > label {{
        font-family: 'Roboto', sans-serif;
        font-size: 16px; /* Body: 16px regular */
        font-weight: 400;
        line-height: 1.6; /* Proper line spacing */
        color: {TEXT_DARK};
    }}

    /* Custom Header Styles (Streamlit defaults) */
    .css-10trblm {{ /* Targeting Streamlit's default h1 */
        color: {PRIMARY_GREEN};
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        font-weight: 700;
    }}
    .css-qn80mc {{ /* Targeting Streamlit's default h2 */
        color: {PRIMARY_GREEN};
        font-family: 'Inter', sans-serif;
        font-size: 24px;
        font-weight: 600;
    }}

    /* Main Container Padding */
    .main .block-container {{
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px; /* Max width for content */
    }}

    /* Hero Section */
    .hero-section {{
        background: url("https://images.unsplash.com/photo-1510414777559-0a9117a7c5b6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1920&q=80") center center / cover no-repeat;
        color: white;
        text-align: center;
        padding: 80px 20px;
        border-radius: 15px;
        margin-bottom: 48px; /* xxl spacing */
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }}
    .hero-overlay {{
        background-color: rgba(46, 139, 87, 0.7); /* Primary green with transparency */
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 1;
    }}
    .hero-content {{
        position: relative;
        z-index: 2;
        max-width: 800px;
        margin: 0 auto;
    }}
    .hero-title {{
        font-family: 'Inter', sans-serif;
        font-size: 48px; /* Larger title for hero */
        font-weight: 700;
        margin-bottom: 24px; /* lg spacing */
        line-height: 1.2;
        color: white;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    }}
    .hero-subtitle {{
        font-size: 20px;
        font-weight: 400;
        margin-bottom: 32px; /* xl spacing */
        color: #E0E0E0;
    }}
    .stButton > button.hero-button {{
        background-color: {ACCENT_ORANGE};
        color: white;
        border-radius: 50px;
        padding: 16px 40px;
        font-size: 20px;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
        min-height: 44px; /* Tap target */
    }}
    .stButton > button.hero-button:hover {{
        background-color: #FF8855; /* Lighter orange on hover */
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.6);
    }}

    /* Section Styling */
    .st-emotion-cache-1gjn39h {{ /* Streamlit's column container */
        gap: 24px; /* xl spacing between columns */
    }}

    /* Card-like containers for sections */
    .card-container {{
        background-color: white;
        border-radius: 15px;
        padding: 32px; /* xl spacing */
        margin-bottom: 24px; /* lg spacing */
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid {BORDER_GRAY};
        transition: all 0.3s ease;
    }}
    .card-container:hover {{
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }}

    /* How It Works Section */
    .steps-container {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 32px; /* xl spacing */
        margin-bottom: 24px; /* lg spacing */
    }}
    .step-card {{
        background-color: #F0FBF0; /* Very light green background */
        border-radius: 10px;
        padding: 24px; /* lg spacing */
        text-align: center;
        flex: 1;
        min-width: 250px;
        max-width: 350px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        border: 1px solid #E0F0E0;
        transition: all 0.3s ease;
    }}
    .step-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }}
    .step-icon {{
        font-size: 48px;
        color: {PRIMARY_GREEN};
        margin-bottom: 16px; /* md spacing */
    }}
    .step-title {{
        font-size: 20px;
        font-weight: 600;
        color: {TEXT_DARK};
        margin-bottom: 8px; /* sm spacing */
    }}
    .step-description {{
        font-size: 14px;
        color: #555555;
    }}

    /* File Uploader Customization */
    .stFileUploader label {{
        font-size: 18px;
        font-weight: 500;
        color: {PRIMARY_GREEN};
    }}
    .stFileUploader > div > button {{ /* Browse button */
        background-color: {PRIMARY_GREEN};
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 500;
        border: none;
        transition: background-color 0.3s;
        min-height: 44px; /* Tap target */
    }}
    .stFileUploader > div > button:hover {{
        background-color: #3CB371; /* Darker green */
    }}

    /* Drag & Drop Zone Styling (Simulated with st.empty & st.markdown) */
    .drop-zone-area {{
        border: 2px dashed {PRIMARY_GREEN};
        border-radius: 15px;
        padding: 40px; /* A bit more padding */
        text-align: center;
        margin-bottom: 24px; /* lg spacing */
        background-color: #F5FFF5; /* Very light green background */
        transition: all 0.3s ease;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}
    .drop-zone-area.hover {{
        background-color: #E6FFE6; /* Lighter on hover */
        border-color: {ACCENT_ORANGE};
        box-shadow: 0 0 15px rgba(46, 139, 87, 0.2);
    }}
    .drop-zone-text {{
        font-size: 20px;
        font-weight: 500;
        color: {PRIMARY_GREEN};
        margin-bottom: 16px; /* md spacing */
    }}
    .drop-zone-icon {{
        font-size: 60px;
        color: {PRIMARY_GREEN};
        margin-bottom: 10px;
    }}
    .file-requirements {{
        font-size: 14px;
        color: #777777;
    }}

    /* Image Preview */
    .image-preview {{
        border-radius: 10px;
        max-width: 100%;
        height: auto;
        object-fit: contain;
        border: 1px solid {BORDER_GRAY};
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-top: 16px; /* md spacing */
        max-height: 300px; /* Limit height for better layout */
    }}

    /* Results Section */
    .results-section {{
        padding: 32px; /* xl spacing */
        background-color: #F8FFF8; /* Very light green */
        border-radius: 15px;
        border: 1px solid #E0F0E0;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
    }}
    .disease-name-display {{
        font-family: 'Inter', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: {ACCENT_ORANGE};
        text-align: center;
        margin-bottom: 16px; /* md spacing */
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Confidence Score */
    .confidence-gauge {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        position: relative;
        margin: 24px auto; /* lg spacing */
        background: conic-gradient(#3CB371 0% VAR(--percentage), #E0E0E0 VAR(--percentage) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: 700;
        color: {TEXT_DARK};
        border: 5px solid {PRIMARY_GREEN};
        box-shadow: 0 0 20px rgba(46, 139, 87, 0.2);
    }}
    .confidence-gauge::before {{
        content: "";
        position: absolute;
        top: 15px;
        left: 15px;
        right: 15px;
        bottom: 15px;
        background-color: white;
        border-radius: 50%;
        z-index: 1;
    }}
    .confidence-text-inside {{
        position: relative;
        z-index: 2;
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: {PRIMARY_GREEN};
    }}
    .confidence-label {{
        text-align: center;
        margin-top: 10px;
        font-size: 16px;
        font-weight: 500;
        color: {TEXT_DARK};
    }}
    
    /* Treatment Recommendations */
    .treatment-card {{
        background-color: white;
        border-radius: 10px;
        padding: 24px; /* lg spacing */
        margin-top: 24px; /* lg spacing */
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #E0F0E0;
    }}
    .treatment-title {{
        font-size: 20px;
        font-weight: 600;
        color: {PRIMARY_GREEN};
        margin-bottom: 16px; /* md spacing */
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .treatment-list ul {{
        list-style-type: '🌱 '; /* Custom bullet point */
        padding-left: 20px;
    }}
    .treatment-list li {{
        margin-bottom: 10px; /* sm spacing */
        color: {TEXT_DARK};
        font-size: 16px;
        line-height: 1.6;
    }}
    .treatment-list strong {{
        color: {PRIMARY_GREEN};
    }}
    .learn-more-button {{
        background-color: {ACCENT_ORANGE};
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 500;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 16px; /* md spacing */
        min-height: 44px; /* Tap target */
    }}
    .learn-more-button:hover {{
        background-color: #FF8855;
    }}

    /* Loading States */
    .loading-container {{
        text-align: center;
        padding: 40px; /* A bit more padding */
        background-color: #F8FFF8;
        border-radius: 15px;
        border: 1px solid #E0F0E0;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
    }}
    .spinner-grow {{
        display: inline-block;
        width: 60px;
        height: 60px;
        vertical-align: -0.125em;
        background-color: currentColor;
        border-radius: 50%;
        opacity: 0;
        animation: .75s linear infinite spinner-grow;
        color: {PRIMARY_GREEN};
    }}
    @keyframes spinner-grow {{
        0% {{
            transform: scale(0);
            opacity: 0;
        }}
        50% {{
            opacity: 1;
            transform: none;
        }}
    }}
    .loading-text {{
        font-size: 20px;
        font-weight: 500;
        color: {PRIMARY_GREEN};
        margin-top: 16px; /* md spacing */
    }}

    /* Error Messages */
    .error-container {{
        background-color: #FFF0F0; /* Light red background */
        border: 1px solid #FFCCCC; /* Light red border */
        color: #CC0000; /* Darker red text */
        border-radius: 10px;
        padding: 24px; /* lg spacing */
        margin-top: 24px; /* lg spacing */
        font-size: 16px;
        font-weight: 500;
        line-height: 1.6;
    }}
    .error-container strong {{
        color: #8B0000;
    }}
    .retry-button {{
        background-color: {ACCENT_ORANGE};
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 500;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 16px; /* md spacing */
        min-height: 44px; /* Tap target */
    }}
    .retry-button:hover {{
        background-color: #FF8855;
    }}

    /* Recent Diagnoses */
    .history-card {{
        background-color: white;
        border-radius: 15px;
        padding: 32px; /* xl spacing */
        margin-bottom: 24px; /* lg spacing */
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid {BORDER_GRAY};
    }}
    .history-item {{
        display: flex;
        align-items: center;
        gap: 16px; /* md spacing */
        padding: 12px 0; /* sm spacing */
        border-bottom: 1px dashed #EEEEEE;
    }}
    .history-item:last-child {{
        border-bottom: none;
    }}
    .history-image {{
        width: 60px;
        height: 60px;
        object-fit: cover;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
    }}
    .history-details strong {{
        color: {PRIMARY_GREEN};
        font-size: 16px;
    }}
    .history-details span {{
        font-size: 14px;
        color: #777777;
    }}

    /* About and Contact Sections */
    .about-contact-card {{
        background-color: white;
        border-radius: 15px;
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid {BORDER_GRAY};
    }}
    .about-contact-card p {{
        margin-bottom: 16px;
    }}
    .about-contact-card a {{
        color: {PRIMARY_GREEN};
        text-decoration: none;
        font-weight: 500;
    }}
    .about-contact-card a:hover {{
        text-decoration: underline;
    }}

    /* Streamlit overrides for better aesthetics */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid {BORDER_GRAY};
        padding: 10px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        min-height: 44px; /* Tap target */
    }}
    .stTextArea > div > div > textarea {{
        border-radius: 8px;
        border: 1px solid {BORDER_GRAY};
        padding: 10px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        min-height: 100px;
    }}
    .stButton > button {{
        min-height: 44px; /* Ensure all buttons meet tap target */
    }}

    /* Responsive Adjustments (Mobile-first approach) */
    @media (max-width: 768px) {{ /* Mobile to Tablet */
        .hero-title {{
            font-size: 36px;
        }}
        .hero-subtitle {{
            font-size: 18px;
        }}
        .hero-button {{
            padding: 12px 25px;
            font-size: 18px;
        }}
        h1, .h1-font {{ font-size: 28px; }}
        h2, .h2-font {{ font-size: 20px; }}
        p, label, .stMarkdown, .stText, .stButton > button, .stFileUploader label, .stRadio > label, .stCheckbox > label {{ font-size: 15px; }}
        .main .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        .drop-zone-area {{
            padding: 20px;
            min-height: 150px;
        }}
        .drop-zone-text {{
            font-size: 18px;
        }}
        .drop-zone-icon {{
            font-size: 40px;
        }}
        .steps-container {{
            flex-direction: column;
            align-items: center;
            gap: 16px;
        }}
        .step-card {{
            width: 100%;
            max-width: 90%;
            padding: 16px;
        }}
        .analysis-section {{
            flex-direction: column;
            gap: 16px;
        }}
        .image-preview-container, .results-container {{
            min-width: unset;
            width: 100%;
            padding: 20px;
        }}
        .disease-name-display {{
            font-size: 24px;
        }}
        .confidence-gauge {{
            width: 120px;
            height: 120px;
            font-size: 20px;
        }}
        .confidence-text-inside {{
            font-size: 24px;
        }}
        .treatment-list ul {{
            padding-left: 15px;
        }}
        .treatment-list li {{
            font-size: 15px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Placeholder for the ML model (replace with your actual model loading)
@st.cache_resource
def load_disease_model():
    # Simulate model loading time
    # time.sleep(3) 
    # Replace 'your_model.h5' with the actual path to your trained Keras model
    # model = tf.keras.models.load_model('your_model.h5')
    
    # For demonstration, creating a dummy model
    class DummyModel:
        def predict(self, image_array):
            # Simulate prediction
            num_classes = 39 # Based on typical plantvillage dataset
            probabilities = np.random.rand(1, num_classes)
            probabilities = probabilities / np.sum(probabilities) # Normalize
            return probabilities

    model = DummyModel()
    return model

# Placeholder for disease labels and recommendations (replace with your actual data)
@st.cache_data
def load_disease_info():
    # In a real application, load this from a JSON file or database
    # For now, a dummy dict
    disease_labels = [
        "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
        "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
        "Corn_(maize)___Cercospora_leaf_spot_Gray_leaf_spot", "Corn_(maize)___Common_rust",
        "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot",
        "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
        "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
        "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight",
        "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy", "Soybean___healthy",
        "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy",
        "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
        "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites_Two-spotted_spider_mite",
        "Tomato___Target_Spot", "Tomato___Tomato_mosaic_virus", "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___healthy", "Watermelon___healthy"
    ]
    
    # Dummy recommendations for demonstration
    recommendations = {}
    for label in disease_labels:
        if "healthy" in label:
            recommendations[label] = "Your plant looks healthy! Keep up the good work with regular watering and appropriate sunlight."
        else:
            disease_name = label.replace("___", " - ").replace("_", " ")
            recommendations[label] = f"""
            <strong>Disease: {disease_name}</strong>
            <ul>
                <li><strong>Identification:</strong> Look for specific symptoms like spots, discoloration, or wilting on the leaves.</li>
                <li><strong>Treatment:</strong>
                    <ul>
                        <li>Remove affected leaves or parts of the plant immediately to prevent spread.</li>
                        <li>Apply an appropriate fungicide or pesticide. Consult your local agricultural extension for specific product recommendations.</li>
                        <li>Ensure good air circulation around the plant.</li>
                        <li>Avoid overhead watering to keep leaves dry.</li>
                        <li>Improve soil drainage if necessary.</li>
                        <li>Consider crop rotation for future plantings.</li>
                    </ul>
                </li>
                <li><strong>Prevention:</strong>
                    <ul>
                        <li>Use disease-resistant varieties.</li>
                        <li>Practice good sanitation: clean tools, remove plant debris.</li>
                        <li>Monitor plants regularly for early signs of disease.</li>
                        <li>Maintain proper plant spacing.</li>
                    </ul>
                </li>
            </ul>
            """
    return disease_labels, recommendations

# Preprocess image for model prediction
def preprocess_image(image, target_size=(224, 224)):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = image_array / 255.0  # Normalize to [0,1]
    return image_array

# --- Load Model and Disease Info ---
model = load_disease_model()
disease_labels, disease_recommendations = load_disease_info()

# --- Custom Components (to simulate drag & drop and handle file input) ---
def render_file_uploader_area():
    # Streamlit's file uploader is the closest to native drag-and-drop
    uploaded_file = st.file_uploader(
        "Upload an image of a plant leaf for diagnosis",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
        key="file_uploader"
    )
    return uploaded_file

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def get_image_from_bytes(uploaded_file):
    if uploaded_file is not None:
        return Image.open(uploaded_file)
    return None

# --- Main Application Layout ---

# Hero Section
st.markdown(f"""
<div class="hero-section">
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <h1 class="hero-title">Plant Savior AI</h1>
        <p class="hero-subtitle">Instant Plant Disease Detection using AI</p>
        <div style="margin-top: 32px;">
            <a href="#disease-detection" style="text-decoration: none;">
                <button class="hero-button">Get Started</button>
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("") # Add some space

# How It Works Section
st.markdown(f'<div class="card-container">', unsafe_allow_html=True)
st.markdown(f'<h2 class="h2-font" style="text-align: center;">How It Works</h2>', unsafe_allow_html=True)
st.markdown(f'<div class="steps-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-icon">⬆️</div>
        <div class="step-title">1. Upload Image</div>
        <div class="step-description">Capture or upload a clear photo of your plant leaf.</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-icon">🧠</div>
        <div class="step-title">2. AI Analysis</div>
        <div class="step-description">Our advanced AI model processes your image for signs of disease.</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-icon">✔️</div>
        <div class="step-title">3. Get Results</div>
        <div class="step-description">Receive instant diagnosis and personalized treatment recommendations.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'</div></div>', unsafe_allow_html=True) # Close steps-container and card-container

st.write("") # Add some space

# Disease Detection Section
st.markdown(f'<a name="disease-detection"></a>', unsafe_allow_html=True) # Anchor for Get Started button
st.markdown(f'<div class="card-container">', unsafe_allow_html=True)
st.markdown(f'<h2 class="h2-font" style="text-align: center;">Diagnose Your Plant</h2>', unsafe_allow_html=True)

uploaded_file = render_file_uploader_area()

# Initialize session state for displaying results
if 'diagnosis_result' not in st.session_state:
    st.session_
