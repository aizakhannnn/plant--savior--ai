# streamlit_app.py
import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json
from PIL import Image
import os

# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .confidence-high { color: #28a745; font-weight: bold; font-size: 1.2em; }
    .confidence-medium { color: #ffc107; font-weight: bold; font-size: 1.2em; }
    .confidence-low { color: #dc3545; font-weight: bold; font-size: 1.2em; }
    .step-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    .treatment-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🌱 Plant Savior AI</h1>
    <p>Instant Plant Disease Detection using Artificial Intelligence</p>
</div>
""", unsafe_allow_html=True)

# How it works section
st.subheader("How It Works")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="step-card"><h2>1</h2><p>Upload Image</p><p>📸</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="step-card"><h2>2</h2><p>AI Analysis</p><p>🤖</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="step-card"><h2>3</h2><p>Get Results</p><p>📊</p></div>', unsafe_allow_html=True)

# Function to recreate model architecture
@st.cache_resource
def recreate_model():
    """Recreate the exact model architecture used during training"""
    st.info("🔧 Recreating model architecture...")
    
    try:
        # Recreate the exact same MobileNetV2 architecture
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze the base model
        base_model.trainable = False
        
        # Recreate the custom top layers exactly as trained
        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(15, activation='softmax')  # 15 classes from your training
        ])
        
        # Compile with exact same settings
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        st.success("✅ Model architecture recreated successfully!")
        return model
    except Exception as e:
        st.error(f"❌ Error recreating model: {str(e)}")
        return None

# Function to load weights
@st.cache_resource
def load_model_weights():
    """Load model weights from .keras file"""
    try:
        st.info("📥 Loading model weights...")
        
        # Recreate model first
        model = recreate_model()
        
        if model is None:
            return None
            
        # Load the weights (this is more compatible than loading the full model)
        model.load_weights('best_plant_model_final.keras')
        st.success("✅ Model weights loaded successfully!")
        
        return model
    except Exception as e:
        st.error(f"❌ Error loading weights: {str(e)}")
        return None

# Load treatment dictionary
@st.cache_resource
def load_treatments():
    """Load treatment recommendations"""
    try:
        with open('treatment_dict_complete.json', 'r') as f:
            treatments = json.load(f)
        st.success("✅ Treatment dictionary loaded!")
        return treatments
    except Exception as e:
        st.error(f"❌ Error loading treatments: {str(e)}")
        return {}

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.treatments = {}

# Load model and treatments
if st.session_state.model is None:
    with st.spinner("Initializing AI system..."):
        model = load_model_weights()
        treatments = load_treatments()
        st.session_state.model = model
        st.session_state.treatments = treatments

# File uploader
st.subheader("Upload Plant Leaf Image")
uploaded_file = st.file_uploader("Choose a plant leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Uploaded Image")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Leaf Image", use_column_width=True)
    
    with col2:
        if st.session_state.model is not None and st.session_state.treatments:
            with st.spinner("Analyzing image..."):
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
                    
                    # Display results
                    st.subheader("Analysis Results")
                    st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
                    st.markdown(f"<h3>🪴 Predicted Disease</h3><p><strong>{predicted_disease}</strong></p>", unsafe_allow_html=True)
                    
                    # Confidence with color coding
                    if confidence_score > 0.8:
                        confidence_class = "confidence-high"
                        confidence_text = "High"
                    elif confidence_score > 0.6:
                        confidence_class = "confidence-medium"
                        confidence_text = "Medium"
                    else:
                        confidence_class = "confidence-low"
                        confidence_text = "Low"
                    
                    st.markdown(f"<h3>📊 Confidence Score</h3>", unsafe_allow_html=True)
                    st.progress(confidence_score)
                    st.markdown(f"<p class='{confidence_class}'>{confidence_score*100:.2f}% ({confidence_text} confidence)</p>", unsafe_allow_html=True)
                    
                    st.markdown(f"<h3>🌿 Treatment Recommendation</h3>", unsafe_allow_html=True)
                    st.markdown(f'<div class="treatment-box"><p>{treatment}</p></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error during prediction: {str(e)}")
                    st.markdown(f'<div class="error-box"><p>Technical details: {str(e)}</p></div>', unsafe_allow_html=True)
                
                # Clean up temporary file
                try:
                    os.remove("temp_image.jpg")
                except:
                    pass
        else:
            st.error("❌ AI system not initialized. Please check the error messages above.")

# Information section
st.subheader("About Plant Savior AI")
st.info("""
This AI-powered tool helps farmers and gardeners detect plant diseases from leaf images.
Using deep learning technology, it can identify common plant diseases and provide
treatment recommendations to help save crops and plants.

**Model Performance:** 91.02% validation accuracy on 15 plant disease classes
""")

# Troubleshooting section
with st.expander("⚠️ Troubleshooting"):
    st.write("""
    **If you're seeing model loading errors:**
    
    1. **Version Compatibility**: This app now recreates the model architecture and loads weights separately
    2. **File Issues**: Ensure all required files are present in the project directory
    3. **Memory**: Try refreshing the page if you see memory errors
    
    **Required Files:**
    - `best_plant_model_final.keras` (model weights)
    - `treatment_dict_complete.json` (treatment recommendations)
    """)

# Technical details
with st.expander("Technical Details"):
    st.write("""
    **Model Architecture:** MobileNetV2 with transfer learning
    **Input Size:** 224×224 RGB images
    **Classes:** 15 plant disease categories
    **Training Data:** PlantVillage dataset with class balancing
    **Framework:** TensorFlow/Keras
    """)

# Footer
st.markdown("---")
st.caption("🌱 Plant Savior AI - Making agriculture smarter with AI technology")
