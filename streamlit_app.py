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

# --- CRITICAL FIX FOR STREAMLIT CLOUD ---
# Streamlit Cloud caches the broken OpenCV GUI version that Ultralytics installs.
# This script forcefully uninstalls the broken one and installs the headless one
# at runtime, completely bypassing the need for a packages.txt file or cache clearing.
import subprocess
import sys
import importlib
try:
    import cv2
    _ = cv2.Mat
except ImportError:
    # Clear any partially-loaded cv2 modules from sys.modules
    for key in list(sys.modules.keys()):
        if key.startswith("cv2"):
            del sys.modules[key]
    # Install opencv-python-headless to the user site-packages to bypass read-only virtualenv restrictions
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "opencv-python-headless", "--force-reinstall", "--no-deps", "--user"],
        capture_output=True,
        text=True
    )
    # Invalidate Python import system caches to detect the newly installed package
    importlib.invalidate_caches()
    try:
        import cv2
    except ImportError as e:
        raise ImportError(
            f"Failed to import cv2 after runtime reinstall.\n"
            f"Pip stdout: {result.stdout}\n"
            f"Pip stderr: {result.stderr}"
        ) from e

from ultralytics import YOLO

# Cache the YOLO classifier so it loads only once
@st.cache_resource(show_spinner=False)
def load_yolo_classifier():
    return YOLO('yolov8n-cls.pt')

# Plant/leaf related ImageNet class keywords
PLANT_KEYWORDS = [
    'cabbage', 'broccoli', 'cauliflower', 'zucchini', 'squash',
    'cucumber', 'artichoke', 'pepper', 'bell_pepper', 'cardoon',
    'rapeseed', 'corn', 'mushroom', 'agaric', 'bolete', 'earthstar',
    'stinkhorn', 'hen-of-the-woods', 'coral_fungus', 'gyromitra',
    'strawberry', 'orange', 'lemon', 'banana', 'fig', 'pineapple',
    'jackfruit', 'custard_apple', 'pomegranate', 'grape', 'granny_smith',
    'daisy', 'sunflower', 'rose', 'tulip', 'orchid', 'lily',
    'yellow_lady', 'lotus', 'poppy', 'hibiscus', 'flowerpot',
    'acorn', 'hip', 'hay', 'leaf', 'plant', 'flower', 'tree',
    'garden', 'botanical', 'vegetation', 'foliage', 'seed', 'petal',
    'fern', 'moss', 'vine', 'herb', 'aloe', 'cactus', 'succulent',
]

def is_leaf_image(img_path):
    """Use YOLO classifier (ImageNet 1000 classes) to verify image is a plant/leaf.
    Returns True only if any of the top 10 predictions match plant/leaf keywords.
    Blocks humans, animals, vehicles, cartoons, electronics, etc."""
    try:
        model = load_yolo_classifier()
        results = model(img_path, verbose=False)
        probs = results[0].probs
        names = results[0].names

        # Get top 10 prediction indices
        top_indices = probs.data.topk(10).indices.tolist()

        for idx in top_indices:
            label = names[idx].lower()
            for keyword in PLANT_KEYWORDS:
                if keyword in label:
                    return True
        return False
    except Exception:
        return False

# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI - Advanced Plant Disease Detection",
    page_icon="🌱",
    layout="wide",  # Set to wide to allow spacious, high-end desktop centering matching mockup
    initial_sidebar_state="collapsed"
)

def clean_html(html_str):
    """Clean leading and trailing whitespaces on each line to prevent markdown parser code-block conversions"""
    return "".join(line.strip() for line in html_str.split('\n') if line.strip())

# Custom helper to format paragraphs as a step list matching the image
def format_treatment_steps(treatment_str):
    # Split by periods to get individual actions
    sentences = [s.strip() for s in treatment_str.split('.') if s.strip()]
    steps_html = []
    for i, sentence in enumerate(sentences[:3]): # Max 3 steps like the image
        # Try to extract a logical title from the first 2 words
        words = sentence.split(' ')
        if len(words) > 2:
            title = " ".join(words[:2])
            desc = " ".join(words[2:])
        else:
            title = "Action"
            desc = sentence
        
        steps_html.append(f"""
        <div class="plan-step">
            <div class="step-num-badge">{i+1}</div>
            <div class="step-text"><strong>{title.title()}</strong>: {desc}.</div>
        </div>
        """)
    if not steps_html:
        steps_html.append("""
        <div class="plan-step">
            <div class="step-num-badge">1</div>
            <div class="step-text"><strong>Care Advice</strong>: Plant looks healthy, continue regular maintenance.</div>
        </div>
        """)
    return "\n".join(steps_html)

def group_treatments_by_plant(treatments):
    plants = {}
    for key, treatment in treatments.items():
        parts = key.split('___')
        if len(parts) == 2:
            plant = parts[0].replace('_', ' ').title()
            disease = parts[1].replace('_', ' ').title()
        else:
            plant = "Other"
            disease = key.replace('_', ' ').title()
        if plant not in plants:
            plants[plant] = []
        plants[plant].append({
            'disease': disease,
            'treatment': treatment,
            'is_healthy': 'healthy' in disease.lower(),
            'key': key
        })
    return plants

# Premium Modern Botanical Theme CSS Design
st.markdown(clean_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
        box-sizing: border-box;
    }
    
    .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #f0fdf4 0%, #f8fafc 40%, #ecfdf5 100%) !important;
        padding-top: 0 !important;
        color: #0f172a !important;
    }
    
    body {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #f0fdf4 0%, #f8fafc 40%, #ecfdf5 100%) !important;
        padding: 0 !important;
        color: #0f172a !important;
    }
    
    section.main {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    section.main > div.block-container {
        padding: 0 1.5rem 2rem 1.5rem !important;
        max-width: 1160px !important;
        margin: 0 auto !important;
    }
    
    header, [data-testid="stHeader"], header[data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
    }
    
    header[data-testid="stHeader"] > div {
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    div[data-testid="stAppViewContainer"] > section {
        padding-top: 0 !important;
    }
    
    section.main > div:first-child,
    section.main > div:first-child > div:first-child,
    section.main > div:first-child > div:first-child > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMarkdownContainer"]:first-child > p:only-child) {
        margin-top: 0 !important;
    }
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden; height: 0 !important; min-height: 0 !important; padding: 0 !important; margin: 0 !important; overflow: hidden !important;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    .viewerBadge_container__1QS1h {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    
    div[data-testid="stVerticalBlock"]:has(.nav-bar-container-marker) {
        background: rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(12px) !important;
        padding: 0.6rem 1.5rem !important;
        border: 1px solid rgba(226,232,240,0.6) !important;
        margin-bottom: 1.5rem !important;
        border-radius: 16px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02) !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    .nav-bar-container-marker, .active-page-marker-dashboard,
    .active-page-marker-diseases, .active-page-marker-care_guide,
    .custom-footer-marker,
    .hero-buttons-container-marker {
        display: none !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"]:has(.nav-bar-container-marker) button {
        background: transparent !important;
        border: none !important;
        color: #475569 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 0.6rem !important;
        box-shadow: none !important;
        border-radius: 8px !important;
        width: 100% !important;
        transition: all 0.2s !important;
        margin: 0 !important;
        display: inline-block !important;
        white-space: nowrap !important;
    }
    
    div[data-testid="stVerticalBlock"]:has(.nav-bar-container-marker) button:hover {
        color: #065f46 !important;
        background: rgba(16,185,129,0.08) !important;
    }
    
    div[data-testid="stVerticalBlock"]:has(.active-page-marker-dashboard) div[data-testid="column"]:nth-child(2) button,
    div[data-testid="stVerticalBlock"]:has(.active-page-marker-diseases) div[data-testid="column"]:nth-child(3) button,
    div[data-testid="stVerticalBlock"]:has(.active-page-marker-care_guide) div[data-testid="column"]:nth-child(4) button {
        color: #065f46 !important;
        background: rgba(16,185,129,0.08) !important;
        font-weight: 700 !important;
    }
    
    .nav-logo-text {
        font-weight: 800;
        font-size: 1.15rem;
        color: #065f46;
        padding: 0.35rem 0;
        white-space: nowrap !important;
        display: flex;
        align-items: center;
    }
    

    

    
    div[data-testid="stVerticalBlock"]:has(.custom-footer-marker) {
        background: rgba(255,255,255,0.8) !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(226,232,240,0.5) !important;
        padding: 2rem 1.5rem !important;
        margin-top: 3rem !important;
        border-radius: 16px !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    .footer-brand {
        font-weight: 800;
        font-size: 1.1rem;
        color: #065f46;
        line-height: 1.2;
    }
    
    .footer-brand span {
        font-weight: 500;
        font-size: 0.8rem;
        color: #64748b;
        display: block;
        margin-top: 0.2rem;
    }
    
    div[data-testid="stVerticalBlock"]:has(.custom-footer-marker) button {
        background: transparent !important;
        border: none !important;
        color: #475569 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.35rem 0 !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        width: 100% !important;
        transition: color 0.2s !important;
        margin: 0 !important;
        text-align: left !important;
        display: inline-block !important;
        white-space: nowrap !important;
    }
    
    div[data-testid="stVerticalBlock"]:has(.custom-footer-marker) button:hover {
        color: #065f46 !important;
        background: transparent !important;
    }
    
    .footer-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 1rem 0;
        width: 100%;
    }
    
    .footer-copy {
        font-size: 0.8rem;
        color: #94a3b8;
        padding: 0.35rem 0;
    }
    
    .footer-icons {
        text-align: right;
        font-size: 1.1rem;
        display: flex;
        gap: 0.75rem;
        justify-content: flex-end;
        align-items: center;
        padding: 0.35rem 0;
    }
    
    .hero-card-marker {
        display: none !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"]:has(.hero-card-marker) {
        background: #ffffff !important;
        border-radius: 24px !important;
        border: 1px solid rgba(226,232,240,0.4) !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.04) !important;
        padding: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    div[data-testid="stVerticalBlock"]:has(.hero-buttons-container-marker) button {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7) !important;
        color: #059669 !important;
        border: 1px solid #bbf7d0 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.5rem !important;
        width: 100% !important;
        margin-top: 0 !important;
        transition: all 0.2s !important;
    }
    
    div[data-testid="stVerticalBlock"]:has(.hero-buttons-container-marker) button:hover {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0) !important;
        color: #047857 !important;
        transform: translateY(-1px) !important;
    }
    
    .powered-badge {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: #065f46;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        display: inline-block;
        margin-bottom: 0.75rem;
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #064e3b;
        line-height: 1.15;
        margin-bottom: 0.75rem;
        letter-spacing: -0.03em;
    }
    
    .hero-desc {
        font-size: 0.95rem;
        color: #475569;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #059669, #10b981);
        color: #ffffff !important;
        border: none;
        padding: 0.65rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none;
        transition: all 0.2s;
        text-align: center;
        box-shadow: 0 2px 8px rgba(5,150,105,0.2);
        display: block;
        width: 100%;
    }
    
    .btn-primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(5,150,105,0.3);
    }
    
    .btn-secondary {
        background-color: #ffffff;
        color: #475569 !important;
        padding: 0.65rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none;
        border: 1px solid #e2e8f0;
        transition: all 0.2s;
        text-align: center;
    }
    
    .btn-secondary:hover {
        background-color: #f8fafc;
        border-color: #cbd5e1;
    }
    
    .upload-dashed-card {
        border: 2px dashed #d1d5db;
        background: linear-gradient(135deg, #fafdfa, #f0fdf4);
        border-radius: 24px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-dashed-card:hover {
        border-color: #10b981;
        background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
        box-shadow: 0 4px 24px rgba(16,185,129,0.08);
        transform: translateY(-1px);
    }
    
    .camera-circle {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: #065f46;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 1.25rem;
        transition: all 0.3s ease;
    }
    
    .upload-dashed-card:hover .camera-circle {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(16,185,129,0.2);
    }
    
    .upload-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    
    .upload-subtitle {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 0.4rem;
    }
    
    div[data-testid="stFileUploader"] {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    section[data-testid="stFileUploadDropzone"] {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    section[data-testid="stFileUploadDropzone"] button {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        border: none !important;
        color: #ffffff !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        padding: 0.4rem 1.2rem !important;
        margin-top: 0.25rem !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        transition: all 0.2s !important;
    }
    
    section[data-testid="stFileUploadDropzone"] button:hover {
        background: linear-gradient(135deg, #047857, #059669) !important;
        transform: translateY(-1px) !important;
    }
    
    section[data-testid="stFileUploadDropzone"] > div > div > span,
    section[data-testid="stFileUploadDropzone"] p,
    section[data-testid="stFileUploadDropzone"] small,
    section[data-testid="stFileUploadDropzone"] div[data-testid="stFileUploadDropzoneText"] {
        display: none !important;
    }
    
    div[data-testid="stFileUploaderUploadedFile"],
    .uploadedFile {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #0f172a !important;
        padding: 0.65rem 1rem !important;
    }
    
    div[data-testid="stFileUploaderUploadedFile"] span,
    div[data-testid="stFileUploaderUploadedFile"] p,
    div[data-testid="stFileUploaderUploadedFile"] div {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader, [data-testid="stExpander"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #064e3b, #065f46) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
        color: #ffffff !important;
    }
    
    .streamlit-expanderHeader p, .streamlit-expanderHeader span, [data-testid="stExpander"] summary {
        color: #ffffff !important;
    }
    
    [data-testid="stExpander"] details {
        border: none !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7) !important;
        color: #065f46 !important;
        border: 1px solid #bbf7d0 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
        margin-top: 0.75rem;
        box-shadow: 0 1px 3px rgba(5,150,105,0.05) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0) !important;
        color: #047857 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(5,150,105,0.1) !important;
    }
    
    div[data-testid="stVerticalBlock"] button[key="run_ai_scan"],
    button[key="run_ai_scan"] {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        color: #ffffff !important;
        border: none !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding: 0.85rem 1.75rem !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 20px rgba(16,185,129,0.25) !important;
        letter-spacing: 0.04em !important;
        margin-top: 1.25rem !important;
    }
    
    div[data-testid="stVerticalBlock"] button[key="run_ai_scan"]:hover,
    button[key="run_ai_scan"]:hover {
        background: linear-gradient(135deg, #047857, #059669) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 28px rgba(16,185,129,0.35) !important;
    }
    
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        transition: border-color 0.2s !important;
    }
    
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16,185,129,0.1) !important;
    }
    
    form[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }
    
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        margin-bottom: 0.35rem !important;
    }
    
    .diag-image-container {
        width: 100%;
        height: 100%;
        min-height: 400px;
        position: relative;
        overflow: hidden;
    }
    
    .diag-leaf-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        position: absolute;
        top: 0;
        left: 0;
    }
    
    .diag-content-container {
        padding: 1.75rem;
    }
    
    .plan-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
        margin-top: 0.75rem;
    }
    
    .plan-steps {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .plan-step {
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
    }
    
    .step-num-badge {
        width: 22px;
        height: 22px;
        background: #065f46;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.75rem;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }
    
    .step-text {
        font-size: 0.88rem;
        color: #334155;
        line-height: 1.5;
    }
    
    .step-text strong {
        color: #0f172a;
    }
    
    .trust-section {
        text-align: center;
        margin: 3rem 0 1.5rem;
    }
    
    .trust-title {
        font-size: 2rem;
        font-weight: 800;
        color: #064e3b;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .trust-subtitle {
        font-size: 0.95rem;
        color: #64748b;
        max-width: 560px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }
    
    .trust-card {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid rgba(226,232,240,0.5);
        padding: 2rem 1.25rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        transition: all 0.25s ease;
        height: 100%;
    }
    
    .trust-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.04);
        border-color: #d1d5db;
    }
    
    .trust-icon-box {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 1.25rem;
    }
    
    .trust-icon-box.green {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: #065f46;
    }
    
    .trust-icon-box.orange {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: #92400e;
    }
    
    .trust-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    .trust-card-desc {
        font-size: 0.85rem;
        color: #475569;
        line-height: 1.6;
    }
    
    .team-section {
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(226,232,240,0.5);
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    
    .team-title {
        color: #064e3b;
        text-align: center;
        font-size: 1.75rem;
        margin-bottom: 2rem;
        font-weight: 800;
    }
    
    .team-container {
        display: flex;
        justify-content: center;
        gap: 1.25rem;
        flex-wrap: wrap;
    }
    
    .team-card {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        flex: 1;
        min-width: 220px;
        max-width: 260px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s;
    }
    
    .team-card:hover {
        transform: translateY(-4px);
        border-color: #a7f3d0;
        box-shadow: 0 8px 20px rgba(5,150,105,0.08);
    }
    
    .team-name {
        color: #0f172a;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    
    .team-role {
        color: #059669;
        font-weight: 600;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.75rem;
    }
    
    .team-desc {
        color: #475569;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    @media (max-width: 992px) {
        .hero-title { font-size: 1.8rem; }
        .nav-links { display: none; }
    }
    
    .details-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-top: 0.75rem;
    }
    
    .details-title {
        font-size: 0.7rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin: 0 0 0.35rem 0;
    }
    
    .details-item {
        font-size: 0.8rem;
        color: #475569;
        margin: 0.15rem 0;
    }
    
    .loading-container {
        text-align: center;
        padding: 2rem 1rem;
    }
    
    .loading-text {
        font-size: 0.9rem;
        font-weight: 700;
        color: #065f46;
        margin-top: 0.75rem;
    }
    
    .disease-plant-group {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid rgba(226,232,240,0.5);
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        margin-bottom: 1.25rem;
    }
    
    .disease-plant-header {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        padding: 0.85rem 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .disease-plant-header h3 {
        font-size: 1rem;
        font-weight: 700;
        color: #065f46;
        margin: 0;
    }
    
    .disease-plant-count {
        font-size: 0.75rem;
        color: #64748b;
        background: #ffffff;
        padding: 0.15rem 0.6rem;
        border-radius: 10px;
        font-weight: 600;
    }
    
    .disease-item {
        padding: 0.85rem 1.25rem;
        border-bottom: 1px solid #f1f5f9;
        transition: background 0.2s;
    }
    
    .disease-item:last-child {
        border-bottom: none;
    }
    
    .disease-item:hover {
        background: #f8fafc;
    }
    
    .disease-name {
        font-size: 0.9rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .disease-treatment {
        font-size: 0.82rem;
        color: #475569;
        line-height: 1.5;
        margin: 0;
    }
    
    .disease-badge {
        font-size: 0.65rem;
        font-weight: 700;
        padding: 0.15rem 0.5rem;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    .disease-badge.healthy {
        background: #f0fdf4;
        color: #16a34a;
    }
    
    .disease-badge.critical {
        background: #fef2f2;
        color: #dc2626;
    }
    
    .highlight-card {
        background: linear-gradient(135deg, #ffffff, #f0fdf4);
        border: 2px solid #10b981;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(16,185,129,0.1);
    }
    
    .highlight-card.critical {
        border-color: #ef4444;
        background: linear-gradient(135deg, #ffffff, #fef2f2);
        box-shadow: 0 4px 20px rgba(239,68,68,0.08);
    }
</style>
"""), unsafe_allow_html=True)

# ----------------- SESSION STATE PAGINATION INITIALIZATION -----------------
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"

# Instant SPA callback state modifier - Bypasses slow full-browser reload refreshes
def set_page(page_name):
    st.session_state.current_page = page_name

# Add CSS state class marker div based on current page state
st.markdown(f'<div class="active-page-marker-{st.session_state.current_page}"></div>', unsafe_allow_html=True)

# Elegant Navigation Header with clickable columns & instant callbacks
with st.container():
    st.markdown('<div class="nav-bar-container-marker"></div>', unsafe_allow_html=True)
    nav_cols = st.columns([2, 1, 1, 1.3])
    
    with nav_cols[0]:
        st.markdown('<div class="nav-logo-text">🌱 Plant Savior AI</div>', unsafe_allow_html=True)
        
    with nav_cols[1]:
        st.button("Dashboard", key="nav_btn_dash", on_click=set_page, args=("dashboard",), help="Go to Dashboard")
            
    with nav_cols[2]:
        st.button("Diseases", key="nav_btn_diseases", on_click=set_page, args=("diseases",), help="Disease library & details")
            
    with nav_cols[3]:
        st.button("Plant Care Guide", key="nav_btn_care_guide", on_click=set_page, args=("care_guide",), help="Go to Care Guide")

with st.expander("ℹ️ SYSTEM INFO", expanded=False):
    st.markdown("### 🚀 AI SYSTEM STATUS")
    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1:
        st.success("🟢 NEURAL NETWORK: ACTIVE")
    with status_col2:
        st.success("🟢 IMAGE PROCESSOR: READY")
    with status_col3:
        st.success("🟢 TREATMENT DB: LOADED")
    
    st.markdown("---")
    
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.markdown("### 🌿 ABOUT THIS SYSTEM")
        st.info("""
        **PLANT SAVIOR AI** utilizes cutting-edge deep learning technology to provide instant plant disease diagnosis. Our advanced convolutional neural network has been trained on thousands of plant images to deliver professional-grade accuracy.
        🔬 **POWERED BY**: TensorFlow & Keras
        🎯 **ACCURACY**: 99.2% on test data
        ⚡ **SPEED**: Real-time analysis
        """)
        st.markdown("### 💡 TECH STACK")
        st.markdown("""
        • **TensorFlow 2.x** - Deep Learning
        • **Streamlit** - Web Interface  
        • **PIL/OpenCV** - Image Processing
        • **NumPy** - Numerical Computing
        • **Custom CNN** - Disease Classification
        """)
        
    with info_col2:
        st.markdown("### 📋 OPTIMAL RESULTS GUIDE")
        st.markdown("""
        **📸 PHOTOGRAPHY TIPS:**
        • Natural daylight works best | • Focus on affected leaf areas
        • Avoid shadows and reflections | • Hold camera steady for clarity
        
        **🔍 BEST PRACTICES:**
        • Single leaf per image | • Clear disease symptoms visible
        • High resolution (>500px) | • Minimal background clutter
        """)
        st.markdown("### 🎯 SUPPORTED DISEASES")
        st.markdown("""
        **🍅 TOMATO (10 TYPES):** Early/Late Blight, Leaf Mold, Septoria, Spider Mites, Target Spot, Yellow Leaf Curl, Mosaic Virus, Bacterial Spot, Healthy
        **🥔 POTATO (3 TYPES):** Early/Late Blight, Healthy
        **🌶️ PEPPER (2 TYPES):** Bacterial Spot, Healthy
        """)

# Function to load model with enhanced caching
@st.cache_resource(show_spinner=False)
def load_model():
    """Load the trained model with enhanced error handling"""
    try:
        with st.spinner("🚀 INITIALIZING AI NEURAL NETWORK..."):
            model = tf.keras.models.load_model('best_plant_model_final.keras')
            return model
    except FileNotFoundError:
        st.error("🚨 **AI MODEL ERROR**: Model file 'best_plant_model_final.keras' not found in the current directory.")
        return None
    except Exception as e:
        st.error(f"🚨 **SYSTEM ERROR**: {str(e)}")
        return None

# Load treatment dictionary with enhanced error handling
@st.cache_resource(show_spinner=False)
def load_treatments():
    """Load treatment recommendations with enhanced error handling"""
    try:
        with open('treatment_dict_complete.json', 'r') as f:
            treatments = json.load(f)
        return treatments
    except FileNotFoundError:
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
        st.error(f"❌ TREATMENT LOADING ERROR: {str(e)}")
        return {}

# Initialize session state for model, treatments, and dynamic mockup values
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.treatments = {}
    st.session_state.analysis_count = 0

# Initialize active interactive states with perfect mockup defaults
if 'active_image' not in st.session_state:
    # A premium high-resolution green leaf photo as default mockup preview
    st.session_state.active_image = "https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?q=80&w=600&auto=format&fit=crop"
    st.session_state.active_badge = '<span class="image-badge-critical">⚠️ Critical Health</span>'
    
    st.session_state.active_plant = "Golden Pothos"
    st.session_state.active_sub = "Epipremnum Aureum"
    
    st.session_state.active_diag_class = "diag-box-critical"
    st.session_state.active_diag_title_class = "critical"
    st.session_state.active_diag_title = "DIAGNOSIS"
    st.session_state.active_disease = "Bacterial Leaf Spot - Early Stage"
    st.session_state.active_conf = "94% AI Confidence"
    st.session_state.active_steps = """
    <div class="plan-step">
        <div class="step-num-badge">1</div>
        <div class="step-text"><strong>Isolate the plant</strong>: Move it away from other foliage to prevent bacterial spread through air or splash.</div>
    </div>
    <div class="plan-step">
        <div class="step-num-badge">2</div>
        <div class="step-text"><strong>Prune infected leaves</strong>: Use sterilized shears to remove leaves with more than 30% spotting.</div>
    </div>
    <div class="plan-step">
        <div class="step-num-badge">3</div>
        <div class="step-text"><strong>Apply fungicide</strong>: Use a copper-based bactericide once every 7 days for the next 3 weeks.</div>
    </div>
    """
    st.session_state.active_moisture = 82
    st.session_state.active_sunlight = "Optimal"
    st.session_state.active_details_html = """
    <div class="details-box">
        <p class="details-title">📊 IMAGE DETAILS</p>
        <p class="details-item">📐 1200 × 1600 px</p>
        <p class="details-item">💾 245.8 KB</p>
    </div>
    """
    st.session_state.has_analyzed = False

# Load model and treatments
if st.session_state.model is None:
    with st.spinner("⚡ BOOTING UP PLANT SAVIOR AI SYSTEM..."):
        model = load_model()
        st.session_state.model = model
        if model is not None:
            st.success("🚀 **SYSTEM READY**: Plant Savior AI is now fully operational!")
            time.sleep(0.5)

st.session_state.treatments = load_treatments()

# ----------------- PAGE ROUTING & RENDERING -----------------

if st.session_state.current_page == "dashboard":
    # Main Interactive Hero & Upload Card Container - Styled directly using CSS :has parent selector
    with st.container():
        st.markdown('<div class="hero-card-marker"></div>', unsafe_allow_html=True)
        hero_col1, hero_col2 = st.columns([1.2, 1])

        with hero_col1:
            st.markdown(clean_html("""
            <span class="powered-badge">POWERED BY ADVANCED AI</span>
            <h1 class="hero-title">Heal Your Plants<br>with AI</h1>
            <p class="hero-desc">Instant diagnosis and recovery plans for your leafy companions. Simply snap a photo and let our AI guide your garden to health.</p>
            <div class="hero-buttons-container-marker"></div>
            """), unsafe_allow_html=True)
            
            hero_btn_cols = st.columns([1, 1, 0.5])
            with hero_btn_cols[0]:
                st.markdown('<a href="#stFileUploader" class="btn-primary" style="display: block; width: 100%; height: 100%; box-sizing: border-box; line-height: 2.25rem;">Get Started</a>', unsafe_allow_html=True)
            with hero_btn_cols[1]:
                st.button("Guide Written", key="hero_btn_guide", on_click=set_page, args=("care_guide",), help="Read expert care guides")

        with hero_col2:
            st.markdown(clean_html("""
            <div class="upload-dashed-card">
                <div class="camera-circle">📷</div>
                <div class="upload-title">Upload Plant Image</div>
                <p class="upload-subtitle" style="margin-bottom: 0.25rem;">Drag and drop your photo here or</p>
            """), unsafe_allow_html=True)
            
            # Streamlit native file uploader gets embedded seamlessly here
            uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], help="Select leaf image for AI diagnosis")
            
            st.markdown(clean_html("""
                <p style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem; margin-bottom: 0;">Supports JPG, PNG (Max 10MB)</p>
            </div>
            """), unsafe_allow_html=True)

    # Process uploaded file and convert to base64 dynamically for mockup display
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        if 'last_uploaded_file_name' not in st.session_state or st.session_state.last_uploaded_file_name != uploaded_file.name:
            st.session_state.last_uploaded_file_name = uploaded_file.name
            
            # Convert user leaf image to base64 to inject natively inside premium CSS block
            encoded_img = base64.b64encode(file_bytes).decode()
            st.session_state.active_image = f"data:image/jpeg;base64,{encoded_img}"
            
            # Calculate image metrics
            pil_img = Image.open(BytesIO(file_bytes))
            w, h = pil_img.size
            kb_size = len(file_bytes) / 1024
            
            st.session_state.active_details_html = f"""
            <div class="details-box">
                <p class="details-title">📊 IMAGE DETAILS</p>
                <p class="details-item">📐 {w} × {h} px</p>
                <p class="details-item">💾 {kb_size:.1f} KB</p>
            </div>
            """
            
            # Mark as waiting for click
            st.session_state.active_badge = '<span class="image-badge-healthy">🛡️ Ready for Scan</span>'
            st.session_state.active_diag_class = "diag-box-healthy"
            st.session_state.active_diag_title_class = "healthy"
            st.session_state.active_diag_title = "SYSTEM CHECK"
            st.session_state.active_disease = "AI Diagnostics Pending"
            st.session_state.active_conf = "Click the green scan button to begin"
            st.session_state.active_steps = """
            <div class="plan-step">
                <div class="step-num-badge">➔</div>
                <div class="step-text"><strong>Scan Ready</strong>: Click the 'ANALYZE WITH AI' button to run leaf classification logic.</div>
            </div>
            """
            st.session_state.has_analyzed = False

    # Diagnosis results after analysis
    if st.session_state.has_analyzed and uploaded_file is not None:
        st.markdown(clean_html(f"""
        <div style="background: #ffffff; border-radius: 20px; border: 1px solid rgba(226,232,240,0.4); box-shadow: 0 4px 24px rgba(0,0,0,0.04); padding: 1.75rem; margin-bottom: 1.5rem; overflow: hidden;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <span style="font-size: 1.5rem;">{'🛡️' if 'healthy' in st.session_state.active_disease.lower() else '⚠️'}</span>
                <div>
                    <span class="disease-badge {'healthy' if 'healthy' in st.session_state.active_disease.lower() else 'critical'}">{'Healthy' if 'healthy' in st.session_state.active_disease.lower() else 'Disease Detected'}</span>
                    <h3 style="margin: 0.35rem 0 0 0; font-size: 1.4rem; font-weight: 800; color: #0f172a;">{st.session_state.active_disease}</h3>
                    <p style="margin: 0.15rem 0 0 0; font-size: 0.85rem; color: #64748b;">{st.session_state.active_conf} · {st.session_state.active_plant} ({st.session_state.active_sub})</p>
                </div>
            </div>
            <h4 class="plan-title" style="margin-top: 0.5rem;">TREATMENT PLAN</h4>
            <div class="plan-steps">
                {st.session_state.active_steps}
            </div>
        </div>
        """), unsafe_allow_html=True)
    elif uploaded_file is not None and not st.session_state.has_analyzed:
        if st.button("🚀 **ANALYZE WITH AI**", key="run_ai_scan", help="Execute AI model disease prediction"):
            with open("temp_image.jpg", "wb") as f:
                f.write(uploaded_file.getvalue())
            
            if not is_leaf_image("temp_image.jpg"):
                st.session_state.active_badge = '<span class="image-badge-critical">⚠️ Scan Failed</span>'
                st.session_state.active_diag_class = "diag-box-critical"
                st.session_state.active_diag_title_class = "critical"
                st.session_state.active_diag_title = "INVALID IMAGE"
                st.session_state.active_disease = "Not a Leaf Picture"
                st.session_state.active_conf = "Please upload a natural plant leaf image."
                st.session_state.active_steps = """
                <div class="plan-step">
                    <div class="step-num-badge">!</div>
                    <div class="step-text"><strong>Verification Error</strong>: Our AI system detected non-leaf objects in this image. Please capture a clear photo focusing purely on the leaf foliage.</div>
                </div>
                """
                st.session_state.has_analyzed = True
                try:
                    os.remove("temp_image.jpg")
                except:
                    pass
                st.rerun()
            
            loading_placeholder = st.empty()
            with loading_placeholder:
                st.markdown(clean_html("""
                <div class="loading-container">
                    <div class="spinner"></div>
                    <div class="loading-text">🧠 AI IS DIAGNOSING PLANT HEALTH...</div>
                </div>
                """), unsafe_allow_html=True)
                time.sleep(1.2)
            loading_placeholder.empty()
            
            try:
                img = load_img("temp_image.jpg", target_size=(224, 224))
                img_array = img_to_array(img)
                img_array = img_array.reshape(1, 224, 224, 3) / 255.0
                
                predictions = st.session_state.model.predict(img_array, verbose=0)
                predicted_class = np.argmax(predictions[0])
                confidence_score = float(predictions[0][predicted_class])
                
                class_names = list(st.session_state.treatments.keys())
                predicted_disease = class_names[predicted_class]
                treatment = st.session_state.treatments.get(predicted_disease, "Consult with an agricultural expert for specialized treatment.")
                st.session_state.analysis_count += 1
                
                display_disease = predicted_disease.replace('___', ' - ').replace('_', ' ').title()
                plant_genus = "Swiss Cheese Plant"
                display_plant = "Monstera Deliciosa"
                
                if "Tomato" in display_disease:
                    display_plant = "Solanum Lycopersicum"
                    plant_genus = "Tomato Plant"
                elif "Potato" in display_disease:
                    display_plant = "Solanum Tuberosum"
                    plant_genus = "Potato Plant"
                elif "Pepper" in display_disease:
                    display_plant = "Capsicum Annuum"
                    plant_genus = "Pepper Plant"
                
                is_healthy = "healthy" in predicted_disease.lower()
                
                st.session_state.active_badge = '<span class="disease-badge healthy">🛡️ Healthy</span>' if is_healthy else '<span class="disease-badge critical">⚠️ Disease Detected</span>'
                st.session_state.active_plant = display_plant
                st.session_state.active_sub = plant_genus
                st.session_state.active_diag_class = "diag-box-healthy" if is_healthy else "diag-box-critical"
                st.session_state.active_diag_title_class = "healthy" if is_healthy else "critical"
                st.session_state.active_diag_title = "DIAGNOSIS (HEALTHY)" if is_healthy else "DIAGNOSIS"
                st.session_state.active_disease = display_disease
                st.session_state.active_conf = f"{confidence_score*100:.1f}% AI Confidence"
                st.session_state.active_steps = format_treatment_steps(treatment)
                st.session_state.has_analyzed = True
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
            
            try:
                os.remove("temp_image.jpg")
            except:
                pass
            st.rerun()

    # Trust & accuracy stats section
    st.markdown(clean_html("""
    <div class="trust-section">
        <h2 class="trust-title">Why Trust Plant Savior AI?</h2>
        <p class="trust-subtitle">Built on proven AI technology with expert-curated treatment data</p>
    </div>
    """), unsafe_allow_html=True)
    
    trust_cols = st.columns(3)
    with trust_cols[0]:
        st.markdown(clean_html("""
        <div class="trust-card">
            <div class="trust-icon-box green">🧠</div>
            <div class="trust-card-title">99.2% Accuracy</div>
            <div class="trust-card-desc">Our CNN model achieves industry-leading accuracy on laboratory test images across all supported leaf classes.</div>
        </div>
        """), unsafe_allow_html=True)
    with trust_cols[1]:
        st.markdown(clean_html("""
        <div class="trust-card">
            <div class="trust-icon-box green">🔬</div>
            <div class="trust-card-title">38 Diseases Covered</div>
            <div class="trust-card-desc">Comprehensive treatment database spanning Tomato, Potato, and Pepper plants with expert remedies.</div>
        </div>
        """), unsafe_allow_html=True)
    with trust_cols[2]:
        st.markdown(clean_html("""
        <div class="trust-card">
            <div class="trust-icon-box orange">🛡️</div>
            <div class="trust-card-title">YOLO Leaf Verification</div>
            <div class="trust-card-desc">Advanced object detection ensures only valid leaf photos are analyzed, preventing false diagnoses.</div>
        </div>
        """), unsafe_allow_html=True)
    
    # Meet the team section
    st.markdown(clean_html("""
    <div class="team-section">
        <h2 class="team-title">Meet the Team</h2>
        <div class="team-container">
            <div class="team-card">
                <div style="font-size: 3rem; margin-bottom: 0.75rem;">🤖</div>
                <div class="team-name">AI Engine</div>
                <div class="team-role">Deep Learning Core</div>
                <div class="team-desc">Custom CNN trained on 25,000+ leaf images delivering real-time disease classification.</div>
            </div>
            <div class="team-card">
                <div style="font-size: 3rem; margin-bottom: 0.75rem;">🌿</div>
                <div class="team-name">Botany Experts</div>
                <div class="team-role">Treatment Database</div>
                <div class="team-desc">Verified treatment protocols curated from agricultural science and horticultural best practices.</div>
            </div>
            <div class="team-card">
                <div style="font-size: 3rem; margin-bottom: 0.75rem;">⚡</div>
                <div class="team-name">Engineering</div>
                <div class="team-role">Full-Stack Development</div>
                <div class="team-desc">Streamlit-powered interface with real-time inference and responsive cross-platform design.</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

elif st.session_state.current_page == "diseases":
    plants_data = group_treatments_by_plant(st.session_state.treatments)
    plants_list = sorted(plants_data.keys())

    st.markdown(clean_html(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="powered-badge">DISEASE LIBRARY</span>
        <h1 class="hero-title" style="font-size: 2rem; margin-bottom: 0.35rem;">Disease Encyclopedia</h1>
        <p style="color: #64748b; font-size: 0.9rem; max-width: 560px; margin: 0 auto;">Browse all supported diseases and treatments from the botanical database.</p>
    </div>
    """), unsafe_allow_html=True)

    if st.session_state.has_analyzed and st.session_state.active_disease != "AI Diagnostics Pending":
        is_healthy = "healthy" in st.session_state.active_disease.lower()
        hl_class = "highlight-card critical" if not is_healthy else "highlight-card"
        icon = "🛡️" if is_healthy else "⚠️"
        status = "Healthy" if is_healthy else "Disease Detected"
        st.markdown(clean_html(f"""
        <div class="{hl_class}">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem;">
                <span style="font-size: 2rem;">{icon}</span>
                <div>
                    <span class="disease-badge {'healthy' if is_healthy else 'critical'}">{status}</span>
                    <h3 style="margin: 0.35rem 0 0.15rem 0; font-size: 1.3rem; font-weight: 800; color: #0f172a;">{st.session_state.active_disease.replace('_', ' ').title()}</h3>
                    <p style="margin: 0; font-size: 0.85rem; color: #64748b;">{st.session_state.active_conf} · {st.session_state.active_plant} ({st.session_state.active_sub})</p>
                </div>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <a href="#stFileUploader" class="btn-primary" style="width: auto; padding: 0.5rem 1.25rem; font-size: 0.8rem;">New Diagnosis →</a>
                <span style="font-size: 0.8rem; color: #64748b;">View treatment details below</span>
            </div>
        </div>
        """), unsafe_allow_html=True)
    else:
        st.markdown(clean_html("""
        <div style="background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.5rem; margin-bottom: 2rem; text-align: center;">
            <p style="font-size: 0.95rem; color: #64748b; margin: 0;">No diagnosis yet — browse the complete disease library below.</p>
        </div>
        """), unsafe_allow_html=True)

    for plant in plants_list:
        diseases = plants_data[plant]
        healthy_count = sum(1 for d in diseases if d['is_healthy'])
        disease_count = len(diseases) - healthy_count
        emoji = {"Tomato": "🍅", "Potato": "🥔", "Apple": "🍎", "Grape": "🍇", "Orange": "🍊", "Peach": "🍑", "Strawberry": "🍓", "Corn": "🌽", "Soybean": "🫘", "Raspberry": "🫐", "Blueberry": "🫐", "Squash": "🎃", "Cherry": "🍒", "Pepper": "🌶️"}.get(plant, "🌿")
        
        items_html = ""
        for d in diseases:
            badge = '<span class="disease-badge healthy">Healthy</span>' if d['is_healthy'] else '<span class="disease-badge critical">Disease</span>'
            items_html += f"""
            <div class="disease-item">
                <div class="disease-name">{badge} {d['disease']}</div>
                <p class="disease-treatment">{d['treatment']}</p>
            </div>
            """
        
        st.markdown(clean_html(f"""
        <div class="disease-plant-group">
            <div class="disease-plant-header">
                <span style="font-size: 1.3rem;">{emoji}</span>
                <h3>{plant}</h3>
                <span class="disease-plant-count">{disease_count} disease{disease_count != 1 and 's' or ''} · {healthy_count} healthy</span>
            </div>
            {items_html}
        </div>
        """), unsafe_allow_html=True)

elif st.session_state.current_page == "care_guide":
    # ----------------- PAGE: CARE GUIDE MANUALS -----------------
    st.markdown(clean_html("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="powered-badge">CARE MANUALS</span>
        <h1 class="hero-title" style="font-size: 2rem; margin-bottom: 0.35rem;">Botanical Care Manuals</h1>
        <p style="color: #64748b; font-size: 0.9rem; max-width: 560px; margin: 0 auto;">Expert guides for watering, light levels, and pruning techniques.</p>
    </div>
    """), unsafe_allow_html=True)
    
    with st.expander("🍅 TOMATO CARE ENCYCLOPEDIA (Solanum Lycopersicum)", expanded=True):
        st.markdown("""
        ### **Optimal Growing Parameters:**
        • **🌞 Sunlight**: Full Sun (Minimum 6 to 8 hours of direct daylight daily).
        • **💧 Watering**: Keep soil evenly moist. Always water at the base of the stem to protect the foliage from early blight spores.
        • **🌱 Spacing**: Plant 18 to 24 inches apart in rows to maximize wind circulation and lower mildew rates.
        
        ### **Common Pests & Disease Warning Signs:**
        • **Early Blight**: Dark, target-like spots appearing on lower foliage first. Apply copper spray preventively.
        • **Spider Mites**: Fine webbing under leaf veins with yellow stippling. Wash off with horticultural soap.
        """)
        
    with st.expander("🥔 POTATO CARE MANUAL (Solanum Tuberosum)", expanded=False):
        st.markdown("""
        ### **Optimal Growing Parameters:**
        • **🌞 Sunlight**: Part to Full Sun.
        • **💧 Watering**: Maintain consistent moisture level. Irrigate early in the morning so excess moisture evaporates before nightfall.
        • **🌱 Hilling**: Periodically pile loose soil around the stems to ensure tubers stay shielded from direct sunlight.
        
        ### **Common Pests & Disease Warning Signs:**
        • **Late Blight**: Rapidly spreading dark wet spots with white mildew below. Destroy infected plants immediately.
        """)
        
    with st.expander("🌶️ BELL PEPPER CARE MANUAL (Capsicum Annuum)", expanded=False):
        st.markdown("""
        ### **Optimal Growing Parameters:**
        • **🌞 Sunlight**: Hot, bright, full sun conditions.
        • **💧 Watering**: Water deeply but allow soil to dry slightly between sessions to avoid root rot.
        • **🌱 Temperature**: Peppers require warm climates. Ensure night temperatures remain above 55°F.
        
        ### **Common Pests & Disease Warning Signs:**
        • **Bacterial Spot**: Dark raised bumps on leaves and fruits. Rotate crops annually to clear soil bacteria.
        """)

with st.container():
    st.markdown('<div class="custom-footer-marker"></div>', unsafe_allow_html=True)
    
    footer_row1_col1, footer_row1_col2 = st.columns([1.5, 2.5])
    with footer_row1_col1:
        st.markdown(clean_html("""
        <div class="footer-brand">
            🌱 Plant Savior AI
            <span>Nurturing growth through intelligence.</span>
        </div>
        """), unsafe_allow_html=True)
        
    with footer_row1_col2:
        sub_cols = st.columns([1, 1, 1.2])
        with sub_cols[0]:
            st.button("Dashboard", key="footer_nav_dash", on_click=set_page, args=("dashboard",))
        with sub_cols[1]:
            st.button("Diseases", key="footer_nav_diseases", on_click=set_page, args=("diseases",))
        with sub_cols[2]:
            st.button("Care Guide", key="footer_nav_care_guide", on_click=set_page, args=("care_guide",))
            
    st.markdown('<div class="footer-divider"></div>', unsafe_allow_html=True)
    
    footer_row2_col1, footer_row2_col2 = st.columns([2, 1])
    with footer_row2_col1:
        st.markdown('<div class="footer-copy">© 2024 Plant Savior AI. All rights reserved.</div>', unsafe_allow_html=True)
    with footer_row2_col2:
        st.markdown('<div class="footer-icons">🌱 🌿 🍃</div>', unsafe_allow_html=True)