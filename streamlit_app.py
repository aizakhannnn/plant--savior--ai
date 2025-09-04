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
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Plant Savior AI - Plant Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the futuristic design with 3D elements and mobile responsiveness
st.markdown("""
<style>
    /* Cyberpunk-inspired futuristic theme */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #00f5ff;
        --secondary: #ff00c8;
        --accent: #00ff9d;
        --dark-bg: #0a0e17;
        --darker-bg: #050811;
        --card-bg: #121a2a;
        --text: #e0f7fa;
        --text-secondary: #b0bec5;
        --glow-primary: 0 0 10px #00f5ff, 0 0 20px #00f5ff;
        --glow-secondary: 0 0 10px #ff00c8, 0 0 20px #ff00c8;
    }
    
    /* Global Styles */
    * {
        font-family: 'Exo 2', sans-serif;
        transition: all 0.3s ease;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
    }
    
    /* Main background and layout */
    .stApp {
        background: var(--dark-bg);
        color: var(--text);
        overflow-x: hidden;
    }
    
    /* Animated background */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 10% 20%, rgba(0, 245, 255, 0.05) 0%, transparent 20%),
            radial-gradient(circle at 90% 80%, rgba(255, 0, 200, 0.05) 0%, transparent 20%);
        z-index: -1;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0); }
        50% { transform: translate(20px, 20px); }
        100% { transform: translate(0, 0); }
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, var(--darker-bg) 0%, var(--dark-bg) 100%);
        padding: 2.5rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--glow-primary);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(0, 245, 255, 0.3);
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 245, 255, 0.1) 0%, rgba(0, 245, 255, 0) 70%);
        transform: rotate(30deg);
    }
    
    .logo-text {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: var(--glow-primary);
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        transform: translateZ(30px);
    }
    
    .tagline {
        font-size: 1.4rem;
        opacity: 0.95;
        font-weight: 300;
        max-width: 800px;
        margin: 0 auto;
        color: var(--text-secondary);
        transform: translateZ(20px);
    }
    
    /* How It Works Section */
    .how-it-works {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    .section-title {
        color: var(--primary);
        text-align: center;
        font-size: 2rem;
        margin-bottom: 2rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
    }
    
    .steps-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 1.5rem;
    }
    
    .step-card {
        background: rgba(18, 26, 42, 0.7);
        border-radius: 12px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        flex: 1;
        min-width: 220px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 245, 255, 0.1);
        backdrop-filter: blur(10px);
        transform-style: preserve-3d;
        perspective: 1000px;
        transform: translateZ(10px);
    }
    
    .step-card:hover {
        transform: translateY(-10px) translateZ(20px);
        box-shadow: var(--glow-primary);
        border-color: var(--primary);
    }
    
    .step-number {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.2rem;
        font-weight: bold;
        font-size: 1.2rem;
        box-shadow: var(--glow-primary);
        transform: translateZ(20px);
    }
    
    .step-icon {
        font-size: 2.5rem;
        margin-bottom: 1.2rem;
        color: var(--primary);
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
        animation: pulse-icon 3s infinite;
    }
    
    @keyframes pulse-icon {
        0% { text-shadow: 0 0 10px rgba(0, 245, 255, 0.5); }
        50% { text-shadow: 0 0 20px rgba(0, 245, 255, 0.8), 0 0 30px rgba(0, 245, 255, 0.6); }
        100% { text-shadow: 0 0 10px rgba(0, 245, 255, 0.5); }
    }
    
    .step-title {
        color: var(--primary);
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        transform: translateZ(15px);
    }
    
    /* Upload Section */
    .upload-section {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    .upload-title {
        color: var(--primary);
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
    }
    
    /* Drop Zone */
    .drop-zone {
        border: 3px dashed var(--primary);
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        background-color: rgba(0, 245, 255, 0.05);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        perspective: 1000px;
        transform: translateZ(10px);
    }
    
    .drop-zone:hover {
        background-color: rgba(0, 245, 255, 0.1);
        border-color: var(--secondary);
        transform: scale(1.02) translateZ(20px);
        box-shadow: var(--glow-primary);
    }
    
    .drop-zone.active {
        background-color: rgba(255, 0, 200, 0.1);
        border-color: var(--secondary);
        box-shadow: var(--glow-secondary);
    }
    
    .upload-icon {
        font-size: 4rem;
        color: var(--primary);
        margin-bottom: 1.5rem;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
        animation: float-icon 4s ease-in-out infinite;
    }
    
    @keyframes float-icon {
        0% { transform: translateY(0) translateZ(20px); }
        50% { transform: translateY(-15px) translateZ(20px); }
        100% { transform: translateY(0) translateZ(20px); }
    }
    
    .drop-text {
        font-size: 1.3rem;
        color: var(--text);
        margin-bottom: 0.8rem;
        font-weight: 500;
        transform: translateZ(15px);
    }
    
    .file-types {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: 1.5rem;
        transform: translateZ(10px);
    }
    
    .browse-button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        border: none;
        padding: 0.9rem 2rem;
        border-radius: 50px;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: var(--glow-primary);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        transform: translateZ(20px);
        position: relative;
        overflow: hidden;
    }
    
    .browse-button:hover {
        transform: translateY(-3px) translateZ(30px);
        box-shadow: 0 0 20px var(--primary), 0 0 30px var(--secondary);
    }
    
    .browse-button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
    
    .browse-button:hover::before {
        left: 100%;
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
        background: var(--card-bg);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform-style: preserve-3d;
        perspective: 1000px;
        transform: translateZ(10px);
    }
    
    .results-container {
        flex: 1;
        min-width: 300px;
        background: var(--card-bg);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform-style: preserve-3d;
        perspective: 1000px;
        transform: translateZ(10px);
    }
    
    .section-subtitle {
        color: var(--primary);
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
    }
    
    .preview-image {
        width: 100%;
        max-height: 400px;
        object-fit: contain;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform: translateZ(10px);
    }
    
    .reset-button {
        background: linear-gradient(135deg, var(--secondary) 0%, #ff5252 100%);
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
        box-shadow: var(--glow-secondary);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        transform: translateZ(20px);
        position: relative;
        overflow: hidden;
    }
    
    .reset-button:hover {
        transform: translateY(-2px) translateZ(30px);
        box-shadow: 0 0 20px var(--secondary);
    }
    
    .reset-button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
    
    .reset-button:hover::before {
        left: 100%;
    }
    
    /* Loading State */
    .loading-container {
        text-align: center;
        padding: 2rem;
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    .spinner {
        width: 60px;
        height: 60px;
        border: 5px solid rgba(0, 245, 255, 0.3);
        border-top: 5px solid var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.5rem;
        box-shadow: 0 0 15px var(--primary);
        transform: translateZ(20px);
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg) translateZ(20px); }
        100% { transform: rotate(360deg) translateZ(20px); }
    }
    
    .loading-text {
        font-size: 1.3rem;
        color: var(--primary);
        font-weight: 500;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(15px);
    }
    
    .loading-subtext {
        color: var(--text-secondary);
        margin-top: 0.5rem;
        transform: translateZ(10px);
    }
    
    /* Results Card */
    .results-card {
        background: rgba(18, 26, 42, 0.7);
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.1);
        backdrop-filter: blur(10px);
        transform-style: preserve-3d;
        perspective: 1000px;
        transform: translateZ(10px);
    }
    
    .result-item {
        margin-bottom: 1.5rem;
    }
    
    .result-title {
        color: var(--primary);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        text-shadow: 0 0 5px rgba(0, 245, 255, 0.5);
        transform: translateZ(15px);
    }
    
    .disease-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text);
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
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
        transform: translateZ(10px);
    }
    
    .progress-bar-bg {
        width: 100%;
        height: 12px;
        background-color: rgba(0, 245, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);
        transform: translateZ(10px);
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border-radius: 10px;
        transition: width 1s ease-in-out;
        box-shadow: 0 0 10px var(--primary);
        transform: translateZ(15px);
    }
    
    .confidence-text {
        font-weight: 600;
        color: var(--text);
        text-shadow: 0 0 5px rgba(0, 245, 255, 0.5);
        transform: translateZ(10px);
    }
    
    /* Treatment Box */
    .treatment-box {
        background: rgba(0, 255, 157, 0.1);
        border-left: 4px solid var(--accent);
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 0.5rem;
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
        transform: translateZ(10px);
    }
    
    .treatment-text {
        line-height: 1.6;
        color: var(--text);
    }
    
    /* Analyze Button */
    .analyze-button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        border: none;
        padding: 1.2rem;
        border-radius: 12px;
        cursor: pointer;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: var(--glow-primary);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        margin-top: 1rem;
        transform: translateZ(20px);
        position: relative;
        overflow: hidden;
    }
    
    .analyze-button:hover {
        transform: translateY(-3px) translateZ(30px);
        box-shadow: 0 0 20px var(--primary), 0 0 30px var(--secondary);
    }
    
    .analyze-button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
    
    .analyze-button:hover::before {
        left: 100%;
    }
    
    .analyze-button:disabled {
        background: #cccccc;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    /* Error Message */
    .error-box {
        background-color: rgba(255, 82, 82, 0.1);
        border-left: 4px solid #ff5252;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #ff8a80;
        box-shadow: 0 0 10px rgba(255, 82, 82, 0.2);
        transform: translateZ(10px);
    }
    
    /* About Section */
    .about-section {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    .about-content {
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
    }
    
    .about-text {
        font-size: 1.1rem;
        line-height: 1.7;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        transform: translateZ(10px);
    }
    
    .stats-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 2rem;
        margin-top: 1.5rem;
    }
    
    .stat-card {
        background: rgba(18, 26, 42, 0.7);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        min-width: 180px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.1);
        backdrop-filter: blur(10px);
        transform-style: preserve-3d;
        perspective: 1000px;
        transform: translateZ(10px);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-10px) translateZ(20px);
        box-shadow: var(--glow-primary);
        border-color: var(--primary);
    }
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 1rem;
        transform: translateZ(10px);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, var(--darker-bg) 0%, var(--dark-bg) 100%);
        color: var(--text);
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: var(--glow-primary);
        border: 1px solid rgba(0, 245, 255, 0.3);
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    .footer-text {
        font-size: 1.1rem;
        opacity: 0.9;
        transform: translateZ(10px);
    }
    
    /* Responsive Design */
    @media (max-width: 1200px) {
        .logo-text {
            font-size: 3rem;
        }
        
        .tagline {
            font-size: 1.3rem;
        }
        
        .steps-container {
            gap: 1rem;
        }
        
        .step-card {
            padding: 1.5rem 1.2rem;
        }
        
        .step-title {
            font-size: 1.2rem;
        }
    }
    
    @media (max-width: 992px) {
        .logo-text {
            font-size: 2.8rem;
        }
        
        .tagline {
            font-size: 1.2rem;
        }
        
        .section-title {
            font-size: 1.8rem;
        }
        
        .steps-container {
            flex-direction: column;
            align-items: center;
        }
        
        .step-card {
            width: 100%;
            max-width: 500px;
        }
        
        .analysis-section {
            flex-direction: column;
        }
        
        .image-preview-container, .results-container {
            width: 100%;
        }
        
        .stats-container {
            gap: 1.5rem;
        }
        
        .stat-card {
            min-width: 160px;
            padding: 1.3rem;
        }
        
        .stat-value {
            font-size: 2rem;
        }
    }
    
    @media (max-width: 768px) {
        .logo-text {
            font-size: 2.5rem;
        }
        
        .tagline {
            font-size: 1.1rem;
        }
        
        .main-header {
            padding: 2rem 1.5rem;
        }
        
        .how-it-works, .upload-section, .about-section, .dashboard, .comparison-section, .ar-preview-container {
            padding: 1.5rem;
        }
        
        .section-title {
            font-size: 1.6rem;
        }
        
        .drop-zone {
            padding: 2rem 1rem;
        }
        
        .drop-text {
            font-size: 1.1rem;
        }
        
        .file-types {
            font-size: 0.9rem;
        }
        
        .browse-button {
            padding: 0.8rem 1.5rem;
            font-size: 1rem;
        }
        
        .section-subtitle {
            font-size: 1.3rem;
        }
        
        .stats-container {
            gap: 1rem;
        }
        
        .stat-card {
            min-width: 140px;
            padding: 1.2rem;
        }
        
        .stat-value {
            font-size: 1.8rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
        }
        
        .footer {
            padding: 1.5rem;
        }
        
        .footer-text {
            font-size: 1rem;
        }
    }
    
    @media (max-width: 576px) {
        .logo-text {
            font-size: 2rem;
        }
        
        .tagline {
            font-size: 1rem;
        }
        
        .main-header {
            padding: 1.5rem 1rem;
        }
        
        .how-it-works, .upload-section, .about-section, .dashboard, .comparison-section, .ar-preview-container {
            padding: 1.2rem;
        }
        
        .section-title {
            font-size: 1.4rem;
        }
        
        .step-card {
            padding: 1.2rem 1rem;
        }
        
        .step-number {
            width: 40px;
            height: 40px;
            font-size: 1rem;
        }
        
        .step-icon {
            font-size: 2rem;
        }
        
        .step-title {
            font-size: 1.1rem;
        }
        
        .drop-zone {
            padding: 1.5rem 0.8rem;
        }
        
        .upload-icon {
            font-size: 3rem;
        }
        
        .drop-text {
            font-size: 1rem;
        }
        
        .file-types {
            font-size: 0.8rem;
        }
        
        .browse-button {
            padding: 0.7rem 1.2rem;
            font-size: 0.9rem;
        }
        
        .section-subtitle {
            font-size: 1.2rem;
        }
        
        .disease-name {
            font-size: 1.5rem;
        }
        
        .result-title {
            font-size: 1.1rem;
        }
        
        .stats-container {
            flex-direction: column;
            align-items: center;
        }
        
        .stat-card {
            width: 100%;
            max-width: 250px;
        }
        
        .stat-value {
            font-size: 1.6rem;
        }
        
        .stat-label {
            font-size: 0.8rem;
        }
        
        .footer {
            padding: 1.2rem;
        }
        
        .footer-text {
            font-size: 0.9rem;
        }
        
        /* Mobile-specific navigation */
        .nav-container {
            flex-wrap: wrap;
        }
        
        .nav-button {
            padding: 0.6rem 1rem;
            font-size: 0.9rem;
        }
        
        /* Mobile chatbot */
        .chatbot-window {
            width: 300px;
            height: 400px;
        }
        
        /* Mobile voice command */
        .voice-command-button {
            width: 60px;
            height: 60px;
            font-size: 1.5rem;
        }
    }
    
    @media (max-width: 400px) {
        .logo-text {
            font-size: 1.8rem;
        }
        
        .tagline {
            font-size: 0.9rem;
        }
        
        .main-header {
            padding: 1.2rem 0.8rem;
        }
        
        .how-it-works, .upload-section, .about-section, .dashboard, .comparison-section, .ar-preview-container {
            padding: 1rem;
        }
        
        .section-title {
            font-size: 1.3rem;
        }
        
        .step-card {
            padding: 1rem 0.8rem;
        }
        
        .step-title {
            font-size: 1rem;
        }
        
        .drop-zone {
            padding: 1.2rem 0.6rem;
        }
        
        .upload-icon {
            font-size: 2.5rem;
        }
        
        .drop-text {
            font-size: 0.9rem;
        }
        
        .browse-button {
            padding: 0.6rem 1rem;
            font-size: 0.8rem;
        }
        
        .section-subtitle {
            font-size: 1.1rem;
        }
        
        .disease-name {
            font-size: 1.3rem;
        }
        
        .nav-button {
            padding: 0.5rem 0.8rem;
            font-size: 0.8rem;
        }
        
        .chatbot-window {
            width: 280px;
            height: 350px;
        }
    }
    
    /* Futuristic elements */
    .glow-border {
        border: 1px solid rgba(0, 245, 255, 0.3);
        box-shadow: 0 0 10px rgba(0, 245, 255, 0.3);
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(0, 245, 255, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(0, 245, 255, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(0, 245, 255, 0);
        }
    }
    
    /* Floating animation for cards */
    @keyframes float-card {
        0% { transform: translateY(0px) translateZ(10px); }
        50% { transform: translateY(-10px) translateZ(10px); }
        100% { transform: translateY(0px) translateZ(10px); }
    }
    
    .floating-card {
        animation: float-card 4s ease-in-out infinite;
    }
    
    /* File preview */
    .file-preview {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem;
        background: rgba(0, 245, 255, 0.1);
        border-radius: 8px;
        margin-top: 1rem;
        transform: translateZ(10px);
    }
    
    .file-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .file-icon {
        font-size: 2rem;
        color: var(--primary);
    }
    
    .file-name {
        font-weight: 500;
    }
    
    .file-size {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .remove-file {
        color: var(--secondary);
        cursor: pointer;
        font-size: 1.5rem;
    }
    
    /* Chart container */
    .chart-container {
        background: rgba(18, 26, 42, 0.7);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.1);
        backdrop-filter: blur(10px);
        transform: translateZ(10px);
    }
    
    /* Tabs */
    .tab-container {
        display: flex;
        margin-bottom: 1rem;
        transform: translateZ(10px);
    }
    
    .tab {
        padding: 0.8rem 1.5rem;
        background: rgba(0, 245, 255, 0.1);
        border: 1px solid rgba(0, 245, 255, 0.2);
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        transform: translateZ(10px);
    }
    
    .tab:first-child {
        border-radius: 8px 0 0 8px;
    }
    
    .tab:last-child {
        border-radius: 0 8px 8px 0;
    }
    
    .tab.active {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        font-weight: 600;
    }
    
    .tab-content {
        display: none;
        padding: 1rem;
        transform: translateZ(10px);
    }
    
    .tab-content.active {
        display: block;
    }
    
    /* Confidence meter */
    .confidence-meter {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 1rem 0;
        transform: translateZ(10px);
    }
    
    .confidence-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
    }
    
    .confidence-label {
        font-size: 1rem;
        color: var(--text-secondary);
    }
    
    /* Disease info card */
    .disease-info-card {
        background: rgba(18, 26, 42, 0.7);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.1);
        backdrop-filter: blur(10px);
        transform: translateZ(10px);
    }
    
    .disease-info-title {
        color: var(--primary);
        font-size: 1.3rem;
        margin-bottom: 1rem;
        font-weight: 600;
        text-shadow: 0 0 5px rgba(0, 245, 255, 0.5);
    }
    
    .disease-info-content {
        line-height: 1.6;
        color: var(--text);
    }
    
    /* Dashboard */
    .dashboard {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    .dashboard-title {
        color: var(--primary);
        text-align: center;
        font-size: 2rem;
        margin-bottom: 2rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
    }
    
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }
    
    .dashboard-card {
        background: rgba(18, 26, 42, 0.7);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.1);
        backdrop-filter: blur(10px);
        transform: translateZ(10px);
    }
    
    .dashboard-card-title {
        color: var(--primary);
        font-size: 1.3rem;
        margin-bottom: 1rem;
        font-weight: 600;
        text-shadow: 0 0 5px rgba(0, 245, 255, 0.5);
        transform: translateZ(15px);
    }
    
    /* Navigation */
    .nav-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
        transform: translateZ(10px);
        flex-wrap: wrap;
    }
    
    .nav-button {
        padding: 0.8rem 2rem;
        background: rgba(0, 245, 255, 0.1);
        border: 1px solid rgba(0, 245, 255, 0.2);
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        transform: translateZ(10px);
    }
    
    .nav-button:first-child {
        border-radius: 8px 0 0 8px;
    }
    
    .nav-button:last-child {
        border-radius: 0 8px 8px 0;
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        font-weight: 600;
    }
    
    .nav-button:hover:not(.active) {
        background: rgba(0, 245, 255, 0.2);
    }
    
    /* Chatbot */
    .chatbot-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        transform: translateZ(50px);
    }
    
    .chatbot-toggle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: var(--glow-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .chatbot-toggle:hover {
        transform: scale(1.1);
        box-shadow: 0 0 20px var(--primary), 0 0 30px var(--secondary);
    }
    
    .chatbot-window {
        width: 350px;
        height: 500px;
        background: var(--card-bg);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transform: translateZ(50px);
        margin-bottom: 10px;
    }
    
    .chatbot-header {
        background: linear-gradient(135deg, var(--darker-bg) 0%, var(--dark-bg) 100%);
        padding: 1rem;
        color: var(--text);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(0, 245, 255, 0.2);
    }
    
    .chatbot-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--primary);
        text-shadow: 0 0 5px rgba(0, 245, 255, 0.5);
    }
    
    .chatbot-close {
        background: none;
        border: none;
        color: var(--text-secondary);
        font-size: 1.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .chatbot-close:hover {
        color: var(--primary);
    }
    
    .chatbot-messages {
        flex: 1;
        padding: 1rem;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }
    
    .message {
        max-width: 80%;
        padding: 0.8rem;
        border-radius: 12px;
        font-size: 0.9rem;
        line-height: 1.4;
        transform: translateZ(10px);
    }
    
    .user-message {
        background: rgba(0, 245, 255, 0.1);
        border: 1px solid rgba(0, 245, 255, 0.2);
        align-self: flex-end;
        color: var(--text);
    }
    
    .bot-message {
        background: rgba(255, 0, 200, 0.1);
        border: 1px solid rgba(255, 0, 200, 0.2);
        align-self: flex-start;
        color: var(--text);
    }
    
    .chatbot-input {
        display: flex;
        padding: 1rem;
        background: var(--darker-bg);
        border-top: 1px solid rgba(0, 245, 255, 0.2);
    }
    
    .chatbot-input input {
        flex: 1;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid rgba(0, 245, 255, 0.2);
        background: rgba(18, 26, 42, 0.7);
        color: var(--text);
        font-size: 0.9rem;
    }
    
    .chatbot-input button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-left: 0.5rem;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--glow-primary);
    }
    
    .chatbot-input button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px var(--primary), 0 0 20px var(--secondary);
    }
    
    /* Hidden by default */
    .chatbot-window {
        display: none;
    }
    
    .chatbot-window.active {
        display: flex;
    }
    
    /* Comparison Section */
    .comparison-section {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform-style: preserve-3d;
        perspective: 1000px;
        display: none;
    }
    
    .comparison-title {
        color: var(--primary);
        text-align: center;
        font-size: 2rem;
        margin-bottom: 2rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
    }
    
    .comparison-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }
    
    .comparison-card {
        background: rgba(18, 26, 42, 0.7);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.1);
        backdrop-filter: blur(10px);
        transform: translateZ(10px);
    }
    
    .comparison-card-title {
        color: var(--primary);
        font-size: 1.3rem;
        margin-bottom: 1rem;
        font-weight: 600;
        text-shadow: 0 0 5px rgba(0, 245, 255, 0.5);
        transform: translateZ(15px);
    }
    
    .comparison-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 1rem;
        transform: translateZ(10px);
    }
    
    .comparison-result {
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        transform: translateZ(10px);
    }
    
    .comparison-confidence {
        font-size: 0.9rem;
        color: var(--text-secondary);
        transform: translateZ(10px);
    }
    
    .comparison-date {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        transform: translateZ(10px);
    }
    
    /* Toggle button for comparison section */
    .comparison-toggle {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: var(--glow-primary);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        transform: translateZ(20px);
        margin: 1rem auto;
        display: block;
    }
    
    .comparison-toggle:hover {
        transform: translateY(-2px) translateZ(30px);
        box-shadow: 0 0 15px var(--primary), 0 0 20px var(--secondary);
    }
    
    /* Voice Command Button */
    .voice-command-container {
        text-align: center;
        margin: 2rem 0;
        transform: translateZ(10px);
    }
    
    .voice-command-button {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        border: none;
        font-size: 2rem;
        cursor: pointer;
        box-shadow: var(--glow-primary);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        transform: translateZ(20px);
    }
    
    .voice-command-button:hover {
        transform: scale(1.1) translateZ(30px);
        box-shadow: 0 0 20px var(--primary), 0 0 30px var(--secondary);
    }
    
    .voice-command-button.listening {
        animation: pulse 1s infinite;
        background: linear-gradient(135deg, var(--secondary) 0%, #ff5252 100%);
    }
    
    .voice-command-text {
        margin-top: 1rem;
        color: var(--text-secondary);
        font-size: 1rem;
        transform: translateZ(10px);
    }
    
    .voice-command-result {
        margin-top: 1rem;
        padding: 1rem;
        background: rgba(0, 245, 255, 0.1);
        border-radius: 8px;
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform: translateZ(10px);
    }
    
    /* AR Preview */
    .ar-preview-container {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 245, 255, 0.2);
        transform-style: preserve-3d;
        perspective: 1000px;
        display: none;
    }
    
    .ar-preview-title {
        color: var(--primary);
        text-align: center;
        font-size: 2rem;
        margin-bottom: 2rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        transform: translateZ(20px);
    }
    
    .ar-preview-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2rem;
        transform: translateZ(10px);
    }
    
    .ar-preview-placeholder {
        width: 100%;
        height: 400px;
        background: rgba(0, 245, 255, 0.05);
        border: 2px dashed var(--primary);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary);
        font-size: 1.5rem;
        text-align: center;
        transform: translateZ(10px);
    }
    
    .ar-instructions {
        max-width: 600px;
        text-align: center;
        color: var(--text-secondary);
        line-height: 1.6;
        transform: translateZ(10px);
    }
    
    .ar-button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: var(--darker-bg);
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: var(--glow-primary);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        transform: translateZ(20px);
        font-size: 1.1rem;
    }
    
    .ar-button:hover {
        transform: translateY(-2px) translateZ(30px);
        box-shadow: 0 0 15px var(--primary), 0 0 20px var(--secondary);
    }
    
    .ar-button:disabled {
        background: #cccccc;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        .chatbot-container {
            bottom: 10px;
            right: 10px;
        }
        
        .chatbot-toggle {
            width: 50px;
            height: 50px;
            font-size: 1.2rem;
        }
        
        .chatbot-window {
            width: 300px;
            height: 400px;
        }
        
        .voice-command-button {
            width: 70px;
            height: 70px;
            font-size: 1.8rem;
        }
        
        .ar-preview-placeholder {
            height: 300px;
            font-size: 1.2rem;
        }
        
        .ar-button {
            padding: 0.8rem 1.5rem;
            font-size: 1rem;
        }
    }
    
    @media (max-width: 576px) {
        .chatbot-window {
            width: 280px;
            height: 350px;
        }
        
        .voice-command-button {
            width: 60px;
            height: 60px;
            font-size: 1.5rem;
        }
        
        .ar-preview-placeholder {
            height: 250px;
            font-size: 1rem;
        }
        
        .ar-instructions {
            font-size: 0.9rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add custom JavaScript for interactive elements, drag & drop functionality, voice commands, AR preview, and mobile responsiveness
st.markdown("""
<script>
// Add 3D effect to cards on mouse move
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.step-card, .stat-card, .dashboard-card, .comparison-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const cardRect = card.getBoundingClientRect();
            const cardCenterX = cardRect.left + cardRect.width / 2;
            const cardCenterY = cardRect.top + cardRect.height / 2;
            
            const mouseX = e.clientX;
            const mouseY = e.clientY;
            
            const rotateY = (mouseX - cardCenterX) / 20;
            const rotateX = (cardCenterY - mouseY) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(20px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(10px)';
        });
    });
    
    // Drag and drop functionality
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.querySelector('.file-input');
    
    if (dropZone && fileInput) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            dropZone.classList.add('active');
        }
        
        function unhighlight() {
            dropZone.classList.remove('active');
        }
        
        dropZone.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }
        
        function handleFiles(files) {
            if (files.length > 0) {
                const file = files[0];
                if (file.type.match('image.*')) {
                    // Create a new FileList with the dropped file
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    fileInput.files = dataTransfer.files;
                    
                    // Trigger change event
                    const event = new Event('change', { bubbles: true });
                    fileInput.dispatchEvent(event);
                }
            }
        }
    }
    
    // Tab functionality
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and content
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding content
            const tabId = tab.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Navigation functionality
    const navButtons = document.querySelectorAll('.nav-button');
    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            // Hide all sections
            document.querySelectorAll('.upload-section, .dashboard, .comparison-section, .ar-preview-container').forEach(s => s.style.display = 'none');
            
            // Show corresponding section
            const sectionId = button.getAttribute('data-section');
            document.getElementById(sectionId).style.display = 'block';
        });
    });
    
    // Chatbot functionality
    const chatbotToggle = document.querySelector('.chatbot-toggle');
    const chatbotWindow = document.querySelector('.chatbot-window');
    const chatbotClose = document.querySelector('.chatbot-close');
    const chatbotInput = document.querySelector('.chatbot-input input');
    const chatbotSend = document.querySelector('.chatbot-input button');
    const chatbotMessages = document.querySelector('.chatbot-messages');
    
    if (chatbotToggle && chatbotWindow && chatbotClose) {
        chatbotToggle.addEventListener('click', () => {
            chatbotWindow.classList.toggle('active');
        });
        
        chatbotClose.addEventListener('click', () => {
            chatbotWindow.classList.remove('active');
        });
        
        // Function to add a message to the chat
        function addMessage(text, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
            messageDiv.textContent = text;
            chatbotMessages.appendChild(messageDiv);
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }
        
        // Function to get bot response
        function getBotResponse(userMessage) {
            const responses = {
                'hello': 'Hello! I\\'m the Plant Savior AI assistant. How can I help you today?',
                'hi': 'Hi there! I\\'m here to help with plant disease detection. What do you need?',
                'help': 'I can help you with plant disease detection. Upload an image of an affected leaf, and I\\'ll analyze it for you. You can also ask questions about plant care.',
                'how it works': 'Simply upload a clear photo of a plant leaf, and our AI will analyze it to detect any diseases. You\\'ll get a diagnosis with confidence score and treatment recommendations.',
                'accuracy': 'Our AI model has an accuracy rate of 91.02% across 38 different plant diseases.',
                'supported diseases': 'We support detection for tomato diseases (10 types), potato diseases (3 types), and pepper diseases (2 types).',
                'default': 'I\\'m here to help with plant disease detection. Upload an image of an affected leaf, or ask me about how the system works!'
            };
            
            const lowerMessage = userMessage.toLowerCase();
            for (const [key, response] of Object.entries(responses)) {
                if (lowerMessage.includes(key)) {
                    return response;
                }
            }
            return responses['default'];
        }
        
        // Send message function
        function sendMessage() {
            const message = chatbotInput.value.trim();
            if (message) {
                addMessage(message, true);
                chatbotInput.value = '';
                
                // Simulate bot thinking
                setTimeout(() => {
                    const botResponse = getBotResponse(message);
                    addMessage(botResponse, false);
                }, 1000);
            }
        }
        
        // Event listeners for chat
        if (chatbotSend) {
            chatbotSend.addEventListener('click', sendMessage);
        }
        
        if (chatbotInput) {
            chatbotInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        }
        
        // Add initial bot message
        setTimeout(() => {
            addMessage('Hello! I\\'m the Plant Savior AI assistant. How can I help you today?', false);
        }, 1000);
    }
    
    // Comparison section toggle
    const comparisonToggle = document.querySelector('.comparison-toggle');
    if (comparisonToggle) {
        comparisonToggle.addEventListener('click', () => {
            const comparisonSection = document.querySelector('.comparison-section');
            if (comparisonSection) {
                comparisonSection.style.display = comparisonSection.style.display === 'block' ? 'none' : 'block';
            }
        });
    }
    
    // Voice command functionality
    const voiceButton = document.querySelector('.voice-command-button');
    const voiceText = document.querySelector('.voice-command-text');
    const voiceResult = document.querySelector('.voice-command-result');
    
    if (voiceButton && 'webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            voiceButton.classList.add('listening');
            voiceText.textContent = 'Listening...';
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            voiceText.textContent = 'Processing command...';
            voiceResult.innerHTML = `<strong>You said:</strong> ${transcript}`;
            
            // Process voice commands
            processVoiceCommand(transcript);
        };
        
        recognition.onerror = function(event) {
            voiceText.textContent = 'Error occurred in recognition: ' + event.error;
            voiceButton.classList.remove('listening');
        };
        
        recognition.onend = function() {
            voiceButton.classList.remove('listening');
            voiceText.textContent = 'Click the microphone to speak';
        };
        
        voiceButton.addEventListener('click', () => {
            if (voiceButton.classList.contains('listening')) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });
        
        // Function to process voice commands
        function processVoiceCommand(command) {
            const lowerCommand = command.toLowerCase();
            
            if (lowerCommand.includes('upload') || lowerCommand.includes('analyze')) {
                // Simulate clicking the analyze button
                const analyzeButton = document.querySelector('.analyze-button');
                if (analyzeButton) {
                    analyzeButton.click();
                    voiceResult.innerHTML += '<br><strong>Action:</strong> Started analysis';
                }
            } else if (lowerCommand.includes('dashboard')) {
                // Navigate to dashboard
                document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
                document.querySelector('[data-section="dashboard"]').classList.add('active');
                document.querySelectorAll('.upload-section, .comparison-section, .ar-preview-container').forEach(s => s.style.display = 'none');
                document.getElementById('dashboard').style.display = 'block';
                voiceResult.innerHTML += '<br><strong>Action:</strong> Navigated to dashboard';
            } else if (lowerCommand.includes('history')) {
                // Navigate to history
                document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
                document.querySelector('[data-section="comparison-section"]').classList.add('active');
                document.querySelectorAll('.upload-section, .dashboard, .ar-preview-container').forEach(s => s.style.display = 'none');
                document.getElementById('comparison-section').style.display = 'block';
                voiceResult.innerHTML += '<br><strong>Action:</strong> Navigated to history';
            } else if (lowerCommand.includes('ar') || lowerCommand.includes('augmented reality')) {
                // Navigate to AR preview
                document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
                document.querySelector('[data-section="ar-preview-container"]').classList.add('active');
                document.querySelectorAll('.upload-section, .dashboard, .comparison-section').forEach(s => s.style.display = 'none');
                document.getElementById('ar-preview-container').style.display = 'block';
                voiceResult.innerHTML += '<br><strong>Action:</strong> Navigated to AR preview';
            } else {
                voiceResult.innerHTML += '<br><strong>Action:</strong> Command not recognized';
            }
        }
    } else if (voiceButton) {
        voiceButton.style.display = 'none';
        if (voiceText) {
            voiceText.textContent = 'Voice commands not supported in this browser';
        }
    }
    
    // AR Preview functionality
    const arButton = document.querySelector('.ar-button');
    if (arButton) {
        arButton.addEventListener('click', () => {
            // Simulate AR functionality
            arButton.disabled = true;
            arButton.textContent = 'Initializing AR...';
            
            // Simulate loading
            setTimeout(() => {
                arButton.disabled = false;
                arButton.textContent = 'Start AR Experience';
                
                // Show AR placeholder
                const placeholder = document.querySelector('.ar-preview-placeholder');
                if (placeholder) {
                    placeholder.innerHTML = `
                        <div>
                            <div style="font-size: 3rem; margin-bottom: 1rem;">🌱</div>
                            <div>AR Experience Active</div>
                            <div style="font-size: 0.9rem; margin-top: 0.5rem;">Point your camera at a plant leaf to begin analysis</div>
                        </div>
                    `;
                }
            }, 2000);
        });
    }
    
    // Mobile menu toggle for smaller screens
    function handleMobileMenu() {
        const navContainer = document.querySelector('.nav-container');
        const navButtons = document.querySelectorAll('.nav-button');
        
        if (window.innerWidth <= 768) {
            // Stack buttons vertically on mobile
            navContainer.style.flexDirection = 'column';
            navButtons.forEach(button => {
                button.style.width = '100%';
                button.style.marginBottom = '0.5rem';
                button.style.borderRadius = '8px';
            });
        } else {
            // Reset to default layout on larger screens
            navContainer.style.flexDirection = 'row';
            navButtons[0].style.borderRadius = '8px 0 0 8px';
            for (let i = 1; i < navButtons.length - 1; i++) {
                navButtons[i].style.borderRadius = '0';
            }
            navButtons[navButtons.length - 1].style.borderRadius = '0 8px 8px 0';
            navButtons.forEach(button => {
                button.style.width = 'auto';
                button.style.marginBottom = '0';
            });
        }
    }
    
    // Handle mobile menu on load and resize
    handleMobileMenu();
    window.addEventListener('resize', handleMobileMenu);
});
</script>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Initialize history in session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Navigation
st.markdown("""
<div class="nav-container">
    <div class="nav-button active" data-section="upload-section">Home</div>
    <div class="nav-button" data-section="dashboard">Dashboard</div>
    <div class="nav-button" data-section="comparison-section">History</div>
    <div class="nav-button" data-section="ar-preview-container">AR Preview</div>
</div>
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
    <div class="step-card floating-card">
        <div class="step-number">1</div>
        <div class="step-icon">📸</div>
        <h3 class="step-title">Upload Image</h3>
        <p>Take a clear photo of the affected plant leaf and upload it to our system</p>
    </div>
    <div class="step-card floating-card">
        <div class="step-number">2</div>
        <div class="step-icon">🤖</div>
        <h3 class="step-title">AI Analysis</h3>
        <p>Our advanced AI model analyzes the image to detect any plant diseases</p>
    </div>
    <div class="step-card floating-card">
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

# Main content area - Home Page
st.markdown('<div class="upload-section" id="upload-section">', unsafe_allow_html=True)
st.markdown('<h2 class="upload-title">Upload Plant Leaf Image</h2>', unsafe_allow_html=True)

# Voice command button
st.markdown("""
<div class="voice-command-container">
    <button class="voice-command-button">🎤</button>
    <div class="voice-command-text">Click the microphone to speak</div>
    <div class="voice-command-result"></div>
</div>
""", unsafe_allow_html=True)

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
                    
                    # Save to history
                    history_entry = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "image": uploaded_file.name,
                        "disease": predicted_disease,
                        "confidence": confidence_score,
                        "treatment": treatment
                    }
                    st.session_state.history.append(history_entry)
                    
                    # Display results in enhanced card with tabs
                    st.markdown('<div class="results-card">', unsafe_allow_html=True)
                    
                    # Tab navigation
                    st.markdown("""
                    <div class="tab-container">
                        <div class="tab active" data-tab="diagnosis">Diagnosis</div>
                        <div class="tab" data-tab="confidence">Confidence</div>
                        <div class="tab" data-tab="treatment">Treatment</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Diagnosis tab
                    st.markdown(f"""
                    <div class="tab-content active" id="diagnosis">
                        <div class="result-item">
                            <h4 class="result-title">🪴 Predicted Disease</h4>
                            <p class="disease-name">{predicted_disease}</p>
                        </div>
                        <div class="disease-info-card">
                            <h4 class="disease-info-title">About This Disease</h4>
                            <p class="disease-info-content">This is a common plant disease that affects various crops. Early detection and treatment are crucial for preventing the spread and minimizing crop damage.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Confidence tab
                    st.markdown(f"""
                    <div class="tab-content" id="confidence">
                        <div class="result-item">
                            <h4 class="result-title">📊 Confidence Score</h4>
                            <div class="confidence-meter">
                                <div class="confidence-value">{confidence_score*100:.1f}%</div>
                                <div class="confidence-label">Confidence Level</div>
                            </div>
                            <div class="progress-container">
                                <div class="progress-bar-bg">
                                    <div class="progress-bar-fill" style="width: {confidence_score*100}%"></div>
                                </div>
                            </div>
                        </div>
                        <div class="chart-container">
                            <h4 class="result-title">📈 Prediction Distribution</h4>
                            <p>Top 5 predictions with confidence scores:</p>
                            <ul>
                    """, unsafe_allow_html=True)
                    
                    # Show top 5 predictions
                    top_5_indices = np.argsort(predictions[0])[::-1][:5]
                    for i in top_5_indices:
                        disease_name = class_names[i]
                        score = predictions[0][i]
                        st.markdown(f"<li>{disease_name}: {score*100:.1f}%</li>", unsafe_allow_html=True)
                    
                    st.markdown("""
                            </ul>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Treatment tab
                    st.markdown(f"""
                    <div class="tab-content" id="treatment">
                        <div class="result-item">
                            <h4 class="result-title">🌿 Treatment Recommendation</h4>
                            <div class="treatment-box">
                                <p class="treatment-text">{treatment}</p>
                            </div>
                        </div>
                        <div class="disease-info-card">
                            <h4 class="disease-info-title">Prevention Tips</h4>
                            <p class="disease-info-content">To prevent this disease in the future, ensure proper plant spacing for air circulation, avoid overhead watering, and remove infected plant debris promptly.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
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

# Dashboard Page
st.markdown('<div class="dashboard" id="dashboard" style="display: none;">', unsafe_allow_html=True)
st.markdown('<h2 class="dashboard-title">Analytics Dashboard</h2>', unsafe_allow_html=True)

# Sample data for dashboard
data = {
    'Disease': ['Tomato Healthy', 'Tomato Septoria Leaf Spot', 'Tomato Blight', 'Potato Healthy', 'Potato Blight'],
    'Count': [45, 32, 28, 51, 19],
    'Confidence': [95.2, 87.6, 91.3, 96.1, 89.7]
}

df = pd.DataFrame(data)

st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)

# Disease Distribution Chart
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.markdown('<h3 class="dashboard-card-title">Disease Distribution</h3>', unsafe_allow_html=True)

fig = px.pie(df, values='Count', names='Disease', 
             color_discrete_sequence=[ '#00f5ff', '#ff00c8', '#00ff9d', '#ff5252', '#5252ff'])
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e0f7fa'),
    title_font=dict(color='#00f5ff')
)
st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Confidence Scores Chart
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.markdown('<h3 class="dashboard-card-title">Average Confidence Scores</h3>', unsafe_allow_html=True)

fig2 = px.bar(df, x='Disease', y='Confidence', 
              color='Disease',
              color_discrete_sequence=['#00f5ff', '#ff00c8', '#00ff9d', '#ff5252', '#5252ff'])
fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e0f7fa'),
    title_font=dict(color='#00f5ff')
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Summary Stats
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.markdown('<h3 class="dashboard-card-title">Summary Statistics</h3>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total Diagnoses", "175", "↗️ 12%")
col2.metric("Accuracy Rate", "91.2%", "↗️ 2.3%")
col3.metric("Avg. Confidence", "91.8%", "↘️ 0.5%")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Comparison/Historical Results Section
st.markdown('<div class="comparison-section" id="comparison-section">', unsafe_allow_html=True)
st.markdown('<h2 class="comparison-title">Historical Results</h2>', unsafe_allow_html=True)

if st.session_state.history:
    st.markdown('<div class="comparison-grid">', unsafe_allow_html=True)
    
    # Show last 6 results
    for entry in st.session_state.history[-6:]:
        st.markdown(f"""
        <div class="comparison-card">
            <h3 class="comparison-card-title">{entry['disease']}</h3>
            <div class="comparison-result">Confidence: {entry['confidence']*100:.1f}%</div>
            <div class="comparison-date">{entry['date']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No historical results yet. Analyze some plant images to see your history here!")

st.markdown('</div>', unsafe_allow_html=True)

# AR Preview Section
st.markdown('<div class="ar-preview-container" id="ar-preview-container">', unsafe_allow_html=True)
st.markdown('<h2 class="ar-preview-title">Augmented Reality Preview</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="ar-preview-content">
    <div class="ar-preview-placeholder">
        <div>
            <div style="font-size: 3rem; margin-bottom: 1rem;">📱</div>
            <div>AR Experience Ready</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem;">Click below to start the augmented reality experience</div>
        </div>
    </div>
    <div class="ar-instructions">
        <p>Our augmented reality feature allows you to point your device's camera at a plant leaf for instant disease detection. 
        The AI will analyze the leaf in real-time and provide immediate feedback on potential diseases.</p>
        <p><strong>Note:</strong> This feature requires a mobile device with camera access and AR capabilities.</p>
    </div>
    <button class="ar-button">Start AR Experience</button>
</div>
""", unsafe_allow_html=True)

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
        <div class="stat-card floating-card">
            <div class="stat-value">91.02%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        <div class="stat-card floating-card">
            <div class="stat-value">38</div>
            <div class="stat-label">Disease Types</div>
        </div>
        <div class="stat-card floating-card">
            <div class="stat-value">224×224</div>
            <div class="stat-label">Image Resolution</div>
        </div>
        <div class="stat-card floating-card">
            <div class="stat-value">24/7</div>
            <div class="stat-label">Availability</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chatbot
st.markdown("""
<div class="chatbot-container">
    <button class="chatbot-toggle">💬</button>
    <div class="chatbot-window">
        <div class="chatbot-header">
            <div class="chatbot-title">Plant Savior AI Assistant</div>
            <button class="chatbot-close">×</button>
        </div>
        <div class="chatbot-messages">
            <!-- Messages will be added here by JavaScript -->
        </div>
        <div class="chatbot-input">
            <input type="text" placeholder="Ask me anything...">
            <button>Send</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer with enhanced design
st.markdown("""
<div class="footer">
    <p class="footer-text">🌱 Plant Savior AI - Making agriculture smarter with AI technology</p>
    <p class="footer-text">© 2025 Plant Savior AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
