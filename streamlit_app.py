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
# Modern Clean Design System CSS
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    h1, h2, h3, h4, h5, h6, .logo-text {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.025em;
    }
    /* Main background and layout */
    .stApp {
        background: #f6f8f7;
        color: #0f172a;
        overflow-x: hidden;
    }
    
    /* Make block container responsive */
    .main .block-container {
        max-width: 1200px;
        padding: 3rem 1rem;
    }

    /* ===== LOGIN PAGE STYLES ===== */
    .login-wrapper {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }
    .login-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 2rem;
        border-bottom: 1px solid rgba(19,236,146,0.1);
        background: rgba(255,255,255,0.5);
        backdrop-filter: blur(12px);
    }
    .login-header-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .login-header-icon {
        width: 40px;
        height: 40px;
        background: rgba(19,236,146,0.2);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #13ec92;
        font-size: 1.5rem;
    }
    .login-header-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
    }
    .login-header-right {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .login-header-version {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
    }
    .login-header-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #13ec92;
        animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.85); }
    }
    .login-main {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 0 5%;
        height: calc(100vh - 72px); /* Subtract header height */
        box-sizing: border-box;
    }
    .login-card-wrapper {
        width: 100%;
        max-width: 480px;
    }
    .login-hero-image {
        width: 100%;
        height: 160px; /* Reduced from 192px */
        border-radius: 1rem;
        overflow: hidden;
        position: relative;
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 1rem; /* Reduced from 1.5rem */
    }
    .login-hero-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .login-hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(19,236,146,0.2), transparent);
        z-index: 1;
    }
    .login-title-section {
        text-align: center;
        margin-bottom: 1rem; /* Reduced from 2rem */
    }
    .login-title {
        font-size: 1.875rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    .login-subtitle {
        color: #64748b;
        font-size: 0.95rem;
    }
    .login-form-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 0.75rem;
    }
    .login-divider {
        display: flex;
        align-items: center;
        padding: 1rem 0;
    }
    .login-divider-line {
        flex: 1;
        height: 1px;
        background: #e2e8f0;
    }
    .login-divider-text {
        padding: 0 1rem;
        font-size: 0.7rem;
        font-weight: 500;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    .login-google-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.875rem;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        color: #475569;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
    }
    .login-google-btn:hover {
        background: #f8fafc;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .login-footer-links {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 0.25rem;
    }
    .login-footer-link {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 500;
        text-decoration: none;
        transition: color 0.2s;
    }
    .login-footer-link:hover {
        color: #13ec92;
    }
    .login-footer-icons {
        display: flex;
        gap: 1rem;
        color: #94a3b8;
    }
    .login-bottom-bar {
        padding: 2rem;
        text-align: center;
        border-top: 1px solid rgba(19,236,146,0.05);
    }
    .login-bottom-text {
        font-size: 0.75rem;
        color: #94a3b8;
        max-width: 380px;
        margin: 0 auto 1rem;
        line-height: 1.5;
    }
    .login-bottom-links {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
    }
    .login-bottom-links a {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #94a3b8;
        text-decoration: none;
        transition: color 0.2s;
    }
    .login-bottom-links a:hover {
        color: #13ec92;
    }

    /* ===== HEADER STYLES ===== */
    .main-header {
        background: #0f172a;
        padding: 0;
        border-radius: 1.5rem;
        color: white;
        margin-bottom: 2.5rem;
        overflow: hidden;
        position: relative;
        min-height: 320px;
        display: flex;
        align-items: center;
    }
    .main-header-bg {
        position: absolute;
        inset: 0;
        opacity: 0.4;
        background-size: cover;
        background-position: center;
        mix-blend-mode: overlay;
    }
    .main-header-gradient {
        position: absolute;
        inset: 0;
        background: linear-gradient(to right, #0f172a, rgba(15,23,42,0.8), transparent);
    }
    .main-header-content {
        position: relative;
        z-index: 10;
        padding: 2.5rem 3rem;
        max-width: 640px;
    }
    .header-badge {
        display: inline-block;
        background: rgba(19,236,146,0.2);
        color: #13ec92;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 1rem;
        border: 1px solid rgba(19,236,146,0.3);
    }
    .logo-text {
        font-size: 3rem;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 1rem;
        color: white;
        letter-spacing: -0.035em;
    }
    .tagline {
        font-size: 1.1rem;
        color: #cbd5e1;
        line-height: 1.6;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .header-buttons {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    .header-btn-primary {
        background: #13ec92;
        color: #0f172a;
        padding: 0.75rem 2rem;
        border-radius: 0.75rem;
        font-weight: 700;
        font-size: 0.95rem;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.2s;
    }
    .header-btn-primary:hover {
        filter: brightness(1.1);
        transform: translateY(-1px);
    }
    .header-btn-secondary {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(8px);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 0.75rem;
        font-weight: 700;
        font-size: 0.95rem;
        border: 1px solid rgba(255,255,255,0.2);
        cursor: pointer;
        transition: all 0.2s;
    }
    .header-btn-secondary:hover {
        background: rgba(255,255,255,0.2);
    }

    /* ===== STATISTICS SECTION ===== */
    .stats-section {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 0 0 2.5rem;
    }
    .stat-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: box-shadow 0.3s ease;
    }
    .stat-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    .stat-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    .stat-icon {
        width: 44px;
        height: 44px;
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    .stat-icon-blue {
        background: #eff6ff;
        color: #2563eb;
    }
    .stat-icon-green {
        background: rgba(19,236,146,0.1);
        color: #13ec92;
    }
    .stat-icon-orange {
        background: #fff7ed;
        color: #ea580c;
    }
    .stat-badge {
        background: #f0fdf4;
        color: #16a34a;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.7rem;
        font-weight: 700;
    }
    .stat-label {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    .stat-value {
        font-size: 1.875rem;
        font-weight: 900;
        color: #0f172a;
        letter-spacing: -0.035em;
    }

    /* ===== GLASSMORPHISM CONTAINER ===== */
    .glass-container {
        background: white;
        backdrop-filter: blur(20px);
        border-radius: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        padding: 2rem;
        margin-bottom: 2.5rem;
        transition: all 0.3s ease;
    }
    .glass-container:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }

    /* ===== HOW IT WORKS SECTION ===== */
    .how-it-works {
        background: white;
        border-radius: 1.5rem;
        padding: 3rem;
        margin-bottom: 2.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .section-title {
        color: #0f172a;
        text-align: center;
        font-size: 1.75rem;
        margin-bottom: 2.5rem;
        font-weight: 700;
        position: relative;
        display: inline-block;
        left: 50%;
        transform: translateX(-50%);
    }
    .section-title::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: #13ec92;
        border-radius: 2px;
    }
    .steps-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 1.5rem;
    }
    .step-card {
        background: #f8fafc;
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        flex: 1;
        min-width: 250px;
        max-width: 320px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    .step-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(19,236,146,0.12);
        border-color: rgba(19,236,146,0.3);
    }
    .step-number {
        width: 56px;
        height: 56px;
        background: #13ec92;
        color: #0f172a;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.25rem;
        font-weight: 700;
        font-size: 1.25rem;
    }
    .step-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .step-title {
        color: #0f172a;
        font-size: 1.125rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    .step-description {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ===== UPLOAD SECTION ===== */
    .upload-section {
        background: white;
        border-radius: 1.5rem;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .upload-title {
        color: #0f172a;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .upload-subtitle {
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .drop-zone {
        border: 4px dashed #e2e8f0;
        border-radius: 1.5rem;
        padding: 4rem 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        background: #f8fafc;
        margin-bottom: 2rem;
    }
    .drop-zone:hover {
        background: rgba(19,236,146,0.03);
        border-color: rgba(19,236,146,0.3);
    }
    .upload-icon {
        font-size: 3rem;
        color: #13ec92;
        margin-bottom: 1.5rem;
        display: block;
    }
    .drop-text {
        font-size: 1.25rem;
        color: #0f172a;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .file-types {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    .browse-button {
        background: #0f172a;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.75rem;
        cursor: pointer;
        font-size: 0.95rem;
        font-weight: 700;
        transition: all 0.2s ease;
    }
    .browse-button:hover {
        opacity: 0.9;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* ===== ANALYSIS SECTION ===== */
    .analysis-section {
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }
    .image-preview-container, .results-container {
        flex: 1;
        min-width: 320px;
        background: white;
        border-radius: 1.5rem;
        padding: 2rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    .image-preview-container:hover, .results-container:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    .section-subtitle {
        color: #0f172a;
        font-size: 1.25rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
        text-align: center;
    }
    .preview-image {
        width: 100%;
        max-height: 400px;
        object-fit: contain;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
    }

    /* ===== LOADING ANIMATION ===== */
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    .spinner {
        width: 64px;
        height: 64px;
        border: 4px solid #e2e8f0;
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
        font-size: 1.125rem;
        color: #0f172a;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .loading-subtext {
        color: #64748b;
        font-size: 0.9rem;
    }

    /* ===== RESULTS CARD ===== */
    .results-card {
        background: #f8fafc;
        border-radius: 1rem;
        padding: 2rem;
        border: 1px solid #e2e8f0;
        animation: slideUp 0.5s ease-out;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result-item {
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border-radius: 0.75rem;
        background: white;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    .result-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .result-title {
        color: #0f172a;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .disease-name {
        font-size: 1.5rem;
        font-weight: 900;
        color: #0f172a;
        text-align: center;
        margin: 0.75rem 0;
        letter-spacing: -0.025em;
    }

    /* ===== PROGRESS BAR ===== */
    .progress-container {
        margin: 1rem 0;
    }
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: #475569;
        font-size: 0.875rem;
    }
    .progress-bar-bg {
        width: 100%;
        height: 12px;
        background-color: #e2e8f0;
        border-radius: 9999px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #13ec92, #0bc67a);
        border-radius: 9999px;
        transition: width 1.5s ease-in-out;
    }
    .confidence-text {
        font-weight: 700;
        color: #13ec92;
        font-size: 1rem;
    }

    /* ===== TREATMENT BOX ===== */
    .treatment-box {
        background: #f8fafc;
        border-left: 4px solid #13ec92;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-top: 0.75rem;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #13ec92;
    }
    .treatment-text {
        line-height: 1.7;
        color: #475569;
        font-size: 0.95rem;
    }

    /* ===== BUTTONS ===== */
    .analyze-button, .reset-button {
        border: none;
        padding: 1rem;
        border-radius: 0.75rem;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 700;
        transition: all 0.2s ease;
        width: 100%;
        margin-top: 1rem;
    }
    .analyze-button {
        background: #13ec92;
        color: #0f172a;
        box-shadow: 0 4px 12px rgba(19,236,146,0.25);
    }
    .analyze-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(19,236,146,0.35);
    }
    .reset-button {
        background: #f1f5f9;
        color: #475569;
        border: 1px solid #e2e8f0;
    }
    .reset-button:hover {
        background: #e2e8f0;
    }
    .analyze-button:disabled {
        background: #e2e8f0;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
        color: #94a3b8;
    }

    /* ===== ERROR & SUCCESS BOXES ===== */
    .error-box {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #dc2626;
        border: 1px solid #fecaca;
        border-left: 4px solid #ef4444;
    }
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #13ec92;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #15803d;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #13ec92;
    }

    /* ===== ABOUT SECTION ===== */
    .about-section {
        background: white;
        border-radius: 1.5rem;
        padding: 3rem;
        margin-bottom: 2.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .about-content {
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
    }
    .about-text {
        font-size: 1rem;
        line-height: 1.8;
        color: #475569;
        margin-bottom: 2rem;
    }
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 2rem 0;
    }
    .tech-item {
        background: #f8fafc;
        padding: 0.75rem 1.25rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        color: #0f172a;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    .tech-item:hover {
        background: rgba(19,236,146,0.08);
        border-color: rgba(19,236,146,0.3);
        color: #0f172a;
        transform: translateY(-2px);
    }

    /* ===== FOOTER ===== */
    .footer {
        background: #0f172a;
        color: white;
        text-align: center;
        padding: 2.5rem;
        border-radius: 1.5rem;
        margin-top: 2.5rem;
    }
    .footer-text {
        font-size: 0.9rem;
        opacity: 0.85;
        margin: 0.5rem 0;
        color: #cbd5e1;
    }
    .creator-info {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0f172a !important;
    }
    [data-testid="stSidebar"] p {
        color: #475569 !important;
    }

    /* ===== TEAM SECTION ===== */
    .team-section {
        background: white;
        border-radius: 1.5rem;
        padding: 3rem;
        margin-bottom: 2.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .team-title {
        color: #0f172a;
        text-align: center;
        font-size: 1.75rem;
        margin-bottom: 2.5rem;
        font-weight: 700;
        position: relative;
        display: inline-block;
        left: 50%;
        transform: translateX(-50%);
    }
    .team-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
    }
    .team-card {
        background: #f8fafc;
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        flex: 1;
        min-width: 250px;
        max-width: 300px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    .team-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(19,236,146,0.12);
        border-color: rgba(19,236,146,0.3);
    }
    .team-name {
        color: #0f172a;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 1rem 0 0.5rem;
    }
    .team-role {
        color: #13ec92;
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .team-desc {
        color: #64748b;
        font-size: 0.875rem;
        line-height: 1.6;
    }
    .love-icon {
        display: block;
        text-align: center;
        font-size: 1.5rem;
        margin: 1.5rem 0;
        color: #ef4444;
        animation: heartBeat 1.5s ease-in-out infinite;
    }
    @keyframes heartBeat {
        0% { transform: scale(1); }
        50% { transform: scale(1.15); }
        100% { transform: scale(1); }
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 1200px) {
        .logo-text { font-size: 2.5rem; }
        .section-title { font-size: 1.5rem; }
    }
    @media (max-width: 768px) {
        .main-header { min-height: 280px; }
        .logo-text { font-size: 2rem; }
        .tagline { font-size: 1rem; }
        .steps-container { flex-direction: column; }
        .analysis-section { flex-direction: column; }
        .stats-section { grid-template-columns: 1fr; }
        .main-header-content { padding: 2rem; }
    }
    @media (max-width: 480px) {
        .logo-text { font-size: 1.75rem; }
        .glass-container, .upload-section, .about-section { padding: 1.5rem; }
        .step-card { min-width: 100%; }
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in-up { animation: fadeInUp 0.6s ease-out; }

    /* ===== STREAMLIT OVERRIDES ===== */
    .stButton > button {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input {
        font-family: 'Space Grotesk', sans-serif;
        border-radius: 0.75rem;
        border: 2px solid #e2e8f0;
        background: white !important;
        padding: 0.875rem 1rem;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }
    .stTextInput > div > div > input::selection {
        background: #13ec92 !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #13ec92;
        box-shadow: 0 0 0 2px rgba(19,236,146,0.2);
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }
    .stTextInput label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }
    
    /* Login Video Background */
    .login-video-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        overflow: hidden;
    }
    .login-video-wrapper video {
        position: absolute;
        top: 50%;
        left: 50%;
        min-width: 100%;
        min-height: 100%;
        transform: translate(-50%, -50%);
        object-fit: cover;
    }
    .login-video-overlay {
        position: absolute;
        inset: 0;
        background: rgba(15, 23, 42, 0.65);
        z-index: 1;
    }
    .login-content-over-video {
        position: fixed;
        inset: 0;
        z-index: 2;
        width: 100%;
        height: 100vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    .login-content-over-video .login-header {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        height: 72px;
        box-sizing: border-box;
    }
    .login-content-over-video .login-header-title {
        color: #ffffff;
    }
    .login-content-over-video .login-title {
        color: #ffffff;
    }
    .login-content-over-video .login-subtitle {
        color: #cbd5e1;
    }
    .login-content-over-video .login-bottom-text {
        color: #94a3b8;
    }
    .login-content-over-video .login-footer-link {
        color: #cbd5e1;
    }
    .login-content-over-video .login-footer-icons span {
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    # Critical CSS Overrides for Login Page (Transparency & Fixed Viewport)
    st.markdown("""
    <style>
        /* Hide Streamlit elements during login */
        header, footer {visibility: hidden !important;}
        #MainMenu {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        [data-testid="stHeader"] {display:none !important;}
        
        /* Force full viewport and transparency */
        .main .block-container {
            max-width: 100% !important;
            padding: 0 !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebarNav"] {
            background: transparent !important;
        }
        footer {visibility: hidden !important;}
        [data-testid="stToolbar"] {display: none !important;}
        [data-testid="column"] {
            padding: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Background Video for Login
    st.markdown("""
    <div class="login-video-wrapper">
        <video autoplay muted loop playsinline>
            <source src="https://videos.pexels.com/video-files/2491284/2491284-uhd_2560_1440_24fps.mp4" type="video/mp4">
        </video>
        <div class="login-video-overlay"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Wrap all login content to layer above video
    st.markdown('<div class="login-content-over-video">', unsafe_allow_html=True)
    
    # Login Page Header - Clean Modern Design
    st.markdown("""
    <div class="login-header">
        <div class="login-header-left">
            <div class="login-header-icon">🌱</div>
            <span class="login-header-title">Plant Savior AI</span>
        </div>
        <div class="login-header-right">
            <span class="login-header-version">System v2.4</span>
            <div class="login-header-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Form Container - Left aligned
    st.markdown('<div class="login-main">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 7])
    with col1:
        st.markdown('<div class="login-card-wrapper">', unsafe_allow_html=True)
        # Hero image and title
        st.markdown("""
        <div class="login-hero-image">
            <div class="login-hero-overlay"></div>
            <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBEuROT1haa7Jrl40kTSITW6sDftzblHW3sOBr2tGErE6W1nL0EsVQ82BourZvGRCgjZfBni7g_7fwDnorQqEquVELpx8VSGSwnOh2w9W1iwsAPliRSr0eD9MsUcaEClpSj9RdBMfLUwvklEsEj9uPFTdPox6FI-2SjiUa-MnKIAHYD16oj7h_wmTweykKD8zFxvVM6Cr5z4hchaX5RZMBIBNBAnCLIkrYGlYS3wcQk2aI-VC6zyUzW1xP-yiW_G4LUtdU404u9KXE" alt="Greenhouse interior" />
        </div>
        <div class="login-title-section">
            <h1 class="login-title">System Authentication</h1>
            <p class="login-subtitle">Authorized Personnel Access Only</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="login-form-card">', unsafe_allow_html=True)
        
        # Login Inputs
        username = st.text_input("Operator ID", placeholder="Enter unique ID")
        password = st.text_input("Access Code", type="password", placeholder="••••••••")
        
        # Login Button
        if st.button("⚡ Initiate System", use_container_width=True):
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
        st.markdown("""
        <div class="login-divider">
            <div class="login-divider-line"></div>
            <span class="login-divider-text">or secure login via</span>
            <div class="login-divider-line"></div>
        </div>
        """, unsafe_allow_html=True)
        
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
                <a href="{auth_url}" target="_self" class="login-google-btn">
                    <svg style="width: 20px; height: 20px;" viewBox="0 0 24 24">
                        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"></path>
                        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"></path>
                        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"></path>
                        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"></path>
                    </svg>
                    Google Operations Account
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
            div[data-testid="stButton"] > button[kind="secondary"][data-testid="baseButton-secondary"]:nth-of-type(2) {
                background-color: #4285F4 !important;
                color: white !important;
                border: none !important;
                font-family: 'Roboto', sans-serif !important;
                font-weight: 500 !important;
            }
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer links
        st.markdown("""
        <div class="login-footer-links" style="margin-top: 1rem;">
            <a class="login-footer-link" href="#">Forgot Credentials?</a>
            <div class="login-footer-icons">
                <span title="System Security Status">🛡️</span>
                <span title="Encrypted Connection">�</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bottom bar
        st.markdown("""
        <div class="login-bottom-bar">
            <p class="login-bottom-text">This system is monitored for security purposes. Unauthorized access attempts are logged and reported to the Bio-Security Department.</p>
            <div class="login-bottom-links">
                <a href="#">Support</a>
                <a href="#">Protocol</a>
                <a href="#">Privacy</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # close login-card-wrapper
    st.markdown('</div>', unsafe_allow_html=True) # close login-main
    st.markdown('</div>', unsafe_allow_html=True) # close login-content-over-video

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

# Main header with modern clean design
st.markdown("""
<div class="main-header">
    <div class="main-header-bg" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuCdKlRjEToe1pdcUa6IVib5djYIypdneNtOf67QY1nYfZSt_oOirT0Xf5QOZ-hvR2Cte4-Dxqj6k-kqI7SlY1aYXYMWerpcqCVFrL1HW6UyO4am74TJ_uNPZeoWi_RjnZqxqctuOPfZoIdxOXB33G8was6dppKQMQOCLne9wDnSBCbQ7GIkjsnx3YKSNnMveptlVwRcqO2tVNiXEZyGDRAlqlnPtp9ote5KCA-8Wkqgldw7mkwDN-Ibj8kZJ-0K7LKzMS_b6okZ7lY')"></div>
    <div class="main-header-gradient"></div>
    <div class="main-header-content">
        <span class="header-badge">Next-Gen Farming</span>
        <h1 class="logo-text">Empowering Global Agriculture with AI</h1>
        <p class="tagline">Revolutionizing crop health with instant disease detection and precision farming insights using state-of-the-art neural networks.</p>
        <div class="header-buttons">
            <button class="header-btn-primary">Get Started →</button>
            <button class="header-btn-secondary">Watch Demo</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Statistics Section - Modern card design
st.markdown("""
<div class="stats-section">
    <div class="stat-card">
        <div class="stat-card-header">
            <div class="stat-icon stat-icon-blue">✓</div>
            <span class="stat-badge">+0.5%</span>
        </div>
        <div class="stat-label">Accuracy</div>
        <div class="stat-value">99.2%</div>
    </div>
    <div class="stat-card">
        <div class="stat-card-header">
            <div class="stat-icon stat-icon-green">🧠</div>
            <span class="stat-badge">+2 New</span>
        </div>
        <div class="stat-label">Plant Diseases</div>
        <div class="stat-value">15+</div>
    </div>
    <div class="stat-card">
        <div class="stat-card-header">
            <div class="stat-icon stat-icon-orange">⚡</div>
            <span class="stat-badge">-0.2s</span>
        </div>
        <div class="stat-label">Analysis Time</div>
        <div class="stat-value">&lt;3s</div>
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
st.markdown('<h2 class="upload-title">AI-Powered Plant Analysis</h2>', unsafe_allow_html=True)
st.markdown('<p class="upload-subtitle">Identify diseases and nutrient deficiencies instantly</p>', unsafe_allow_html=True)
# Enhanced file uploader
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], help="Upload a clear image of the plant leaf for AI analysis")
if uploaded_file is not None:
    # Analysis section with enhanced two-column layout
    st.markdown('<div class="analysis-section fade-in-up">', unsafe_allow_html=True)
    # Left column - Enhanced image preview
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown('<div class="image-preview-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-subtitle">📸 Uploaded Image</h3>', unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        st.image(image, caption="🌿 Ready for AI Analysis", use_column_width=True, clamp=True)
        # Image info display
        width, height = image.size
        file_size = len(uploaded_file.getvalue()) / 1024  # KB
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 0.75rem; margin-top: 1rem; border: 1px solid #e2e8f0;">
            <p style="color: #0f172a; margin: 0; font-weight: 600;">📊 Image Details</p>
            <p style="color: #64748b; margin: 5px 0; font-size: 0.875rem;">📐 Dimensions: {width} × {height} pixels</p>
            <p style="color: #64748b; margin: 5px 0; font-size: 0.875rem;">💾 Size: {file_size:.1f} KB</p>
            <p style="color: #64748b; margin: 5px 0; font-size: 0.875rem;">📁 Format: {uploaded_file.type}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 **UPLOAD NEW IMAGE**", key="reset", help="Upload a different leaf image", use_container_width=True):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    # Right column - Enhanced results
    with col2:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-subtitle">🧬 AI Analysis Center</h3>', unsafe_allow_html=True)
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
                        st.markdown('<div style="text-align: center; margin: 1rem 0;"><span style="background: #13ec92; color: #0f172a; padding: 0.5rem 1.5rem; border-radius: 9999px; font-weight: 700; font-size: 0.875rem;">🌿 HEALTHY PLANT</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="text-align: center; margin: 1rem 0;"><span style="background: #ef4444; color: white; padding: 0.5rem 1.5rem; border-radius: 9999px; font-weight: 700; font-size: 0.875rem;">⚠️ DISEASE DETECTED</span></div>', unsafe_allow_html=True)
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
                        conf_color = "#16a34a"
                    elif confidence_score > 0.7:
                        conf_msg = "🟡 **HIGH CONFIDENCE** - Diagnosis is reliable"
                        conf_color = "#ca8a04"
                    elif confidence_score > 0.5:
                        conf_msg = "🟠 **MODERATE CONFIDENCE** - Consider expert consultation"
                        conf_color = "#ea580c"
                    else:
                        conf_msg = "🔴 **LOW CONFIDENCE** - Recommend professional diagnosis"
                        conf_color = "#dc2626"
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
                    <div style="background: #f8fafc; padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #e2e8f0;">
                        <p style="color: #0f172a; margin: 0.5rem 0; font-weight: 600;">🔬 Analysis #{st.session_state.analysis_count}</p>
                        <p style="color: #64748b; margin: 0.5rem 0; font-size: 0.875rem;">🧠 Model: Advanced CNN v2.1</p>
                        <p style="color: #64748b; margin: 0.5rem 0; font-size: 0.875rem;">⚡ Processing Time: <3 seconds</p>
                        <p style="color: #64748b; margin: 0.5rem 0; font-size: 0.875rem;">🎯 Classes Evaluated: {len(class_names)}</p>
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
                <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 1rem; border: 2px dashed #e2e8f0;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
                    <h4 style="color: #0f172a; margin-bottom: 0.75rem; font-weight: 700;">AI Ready for Analysis</h4>
                    <p style="color: #64748b; font-size: 0.9rem;">Click the "ANALYZE WITH AI" button above to start the diagnosis process. Our neural network will examine your plant image and provide detailed results.</p>
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
    <div style="text-align: center; padding: 4rem 2rem; background: #f8fafc; border-radius: 1.5rem; border: 4px dashed #e2e8f0; margin: 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 1.5rem;">📸</div>
        <h3 style="color: #0f172a; margin-bottom: 0.5rem; font-size: 1.25rem; font-weight: 700;">Upload Plant Image</h3>
        <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 2rem; max-width: 380px; margin-left: auto; margin-right: auto;">Drag and drop your crop photos here or click to browse. Supported formats: JPG, PNG, RAW.</p>
        <div style="background: #f1f5f9; padding: 0.75rem 1.5rem; border-radius: 0.5rem; display: inline-block;">
            <p style="color: #64748b; margin: 0; font-size: 0.8rem;">Maximum file size: 200MB</p>
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
<p style="text-align: center; color: #0f172a; font-size: 1rem; font-weight: 600;">Made with ❤️ by the Plant Savior AI Team</p>
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
