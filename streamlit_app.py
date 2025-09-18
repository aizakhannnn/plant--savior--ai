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

    /* Global Styles */

    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Exo+2:wght@300;400;500;600;700;800&display=swap');

    * {

        font-family: 'Exo 2', sans-serif;

    }

    h1, h2, h3, h4, h5, h6, .logo-text, .cyberpunk-text {

        font-family: 'Orbitron', sans-serif;

        letter-spacing: 1px;

    }

    /* Main background and layout */

    .stApp {

        background: linear-gradient(135deg, #0a0a23, #1a1a3a, #2d2d5f, #0f0c29);

        background-size: 400% 400%;

        animation: gradientShift 15s ease infinite;

        color: #e0e0ff;

        overflow-x: hidden;

        min-height: 100vh;

    }

    @keyframes gradientShift {

        0% { background-position: 0% 50%; }

        50% { background-position: 100% 50%; }

        100% { background-position: 0% 50%; }

    }

    /* Floating Particles Background */

    .stApp::before {

        content: "";

        position: fixed;

        top: 0;

        left: 0;

        width: 100%;

        height: 100%;

        background-image: 

            radial-gradient(2px 2px at 20px 30px, rgba(0, 245, 255, 0.3), transparent),

            radial-gradient(2px 2px at 40px 70px, rgba(252, 0, 255, 0.2), transparent),

            radial-gradient(1px 1px at 90px 40px, rgba(0, 201, 255, 0.4), transparent),

            radial-gradient(1px 1px at 130px 80px, rgba(255, 45, 149, 0.3), transparent);

        background-repeat: repeat;

        background-size: 150px 150px;

        animation: particleFloat 20s linear infinite;

        pointer-events: none;

        z-index: -1;

    }

    @keyframes particleFloat {

        0% { transform: translateY(0px) translateX(0px); }

        33% { transform: translateY(-100px) translateX(50px); }

        66% { transform: translateY(-200px) translateX(-50px); }

        100% { transform: translateY(-300px) translateX(0px); }

    }

    /* Header Styles - Enhanced Cyberpunk */

    .main-header {

        background: linear-gradient(135deg, #00c9ff 0%, #1e60c4 50%, #fc00ff 100%);

        padding: 4rem 2rem;

        border-radius: 0;

        color: white;

        text-align: center;

        margin-bottom: 3rem;

        box-shadow: 

            0 0 50px rgba(30, 96, 196, 0.8),

            0 0 100px rgba(0, 201, 255, 0.4),

            inset 0 0 50px rgba(255, 255, 255, 0.1);

        position: relative;

        overflow: hidden;

        border-bottom: 4px solid #00f5ff;

        animation: headerPulse 4s infinite;

    }

    @keyframes headerPulse {

        0%, 100% { 

            box-shadow: 0 0 30px rgba(0, 245, 255, 0.5),

                       0 0 60px rgba(252, 0, 255, 0.3);

        }

        50% { 

            box-shadow: 0 0 50px rgba(0, 245, 255, 0.9),

                       0 0 100px rgba(252, 0, 255, 0.6);

        }

    }

    .main-header::before {

        content: "";

        position: absolute;

        top: -100%;

        left: -100%;

        width: 300%;

        height: 300%;

        background: conic-gradient(from 0deg, transparent, rgba(255,255,255,0.1), transparent);

        animation: headerRotate 8s linear infinite;

    }

    @keyframes headerRotate {

        0% { transform: rotate(0deg); }

        100% { transform: rotate(360deg); }

    }

    .logo-text {

        font-size: 5.5rem;

        font-weight: 900;

        margin-bottom: 1rem;

        text-shadow: 

            0 0 10px rgba(0, 245, 255, 0.8),

            0 0 20px rgba(252, 0, 255, 0.6),

            0 0 30px rgba(0, 201, 255, 0.4);

        color: white;

        animation: logoGlow 3s infinite alternate;

        position: relative;

        z-index: 2;

    }

    @keyframes logoGlow {

        from { 

            text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #00dbde, 0 0 20px #00dbde;

            transform: scale(1);

        }

        to { 

            text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fc00ff, 0 0 40px #fc00ff;

            transform: scale(1.05);

        }

    }

    .tagline {

        font-size: 1.8rem;

        opacity: 0.95;

        font-weight: 400;

        max-width: 1000px;

        margin: 0 auto;

        text-shadow: 0 0 10px rgba(255, 255, 255, 0.7);

        color: #e0f7ff;

        position: relative;

        z-index: 2;

        animation: taglinePulse 4s infinite;

    }

    @keyframes taglinePulse {

        0%, 100% { opacity: 0.9; }

        50% { opacity: 1; }

    }

    /* Statistics Section */

    .stats-section {

        display: flex;

        justify-content: center;

        gap: 3rem;

        margin: 3rem 0;

        flex-wrap: wrap;

    }

    .stat-card {

        background: rgba(255, 255, 255, 0.08);

        backdrop-filter: blur(15px);

        border-radius: 20px;

        padding: 2.5rem;

        text-align: center;

        min-width: 200px;

        border: 1px solid rgba(0, 245, 255, 0.3);

        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);

        transition: all 0.4s ease;

        position: relative;

        overflow: hidden;

    }

    .stat-card::before {

        content: "";

        position: absolute;

        top: 0;

        left: -100%;

        width: 100%;

        height: 100%;

        background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.1), transparent);

        transition: left 0.8s ease;

    }

    .stat-card:hover::before {

        left: 100%;

    }

    .stat-card:hover {

        transform: translateY(-10px) scale(1.05);

        box-shadow: 0 15px 40px rgba(0, 197, 255, 0.4);

        border: 1px solid rgba(0, 245, 255, 0.6);

    }

    .stat-value {

        font-size: 3.5rem;

        font-weight: 900;

        color: #00f5ff;

        text-shadow: 0 0 15px rgba(0, 245, 255, 0.8);

        margin-bottom: 0.5rem;

        font-family: 'Orbitron', sans-serif;

    }

    .stat-label {

        color: #c0d8ff;

        font-size: 1.2rem;

        font-weight: 600;

        text-transform: uppercase;

        letter-spacing: 1px;

    }

    /* Glassmorphism Container Enhanced */

    .glass-container {

        background: rgba(255, 255, 255, 0.1);

        backdrop-filter: blur(20px);

        -webkit-backdrop-filter: blur(20px);

        border-radius: 25px;

        border: 1px solid rgba(255, 255, 255, 0.2);

        box-shadow: 

            0 8px 32px rgba(0, 0, 0, 0.4),

            inset 0 1px 0 rgba(255, 255, 255, 0.1);

        padding: 3rem;

        margin-bottom: 3rem;

        transition: all 0.4s ease;

        position: relative;

        overflow: hidden;

    }

    .glass-container::before {

        content: "";

        position: absolute;

        top: 0;

        left: 0;

        right: 0;

        height: 1px;

        background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.6), transparent);

    }

    .glass-container:hover {

        transform: translateY(-8px);

        box-shadow: 

            0 15px 50px rgba(0, 197, 255, 0.3),

            0 5px 20px rgba(252, 0, 255, 0.2);

        border: 1px solid rgba(0, 197, 255, 0.4);

    }

    /* How It Works Section - Enhanced */

    .how-it-works {

        background: rgba(255, 255, 255, 0.08);

        backdrop-filter: blur(15px);

        border-radius: 25px;

        padding: 4rem;

        margin-bottom: 3rem;

        border: 1px solid rgba(0, 197, 255, 0.25);

        box-shadow: 

            0 10px 40px rgba(0, 0, 0, 0.4),

            inset 0 1px 0 rgba(255, 255, 255, 0.1);

        position: relative;

    }

    .section-title {

        color: #00f5ff;

        text-align: center;

        font-size: 3.2rem;

        margin-bottom: 3rem;

        font-weight: 900;

        text-shadow: 

            0 0 15px rgba(0, 245, 255, 0.8),

            0 0 30px rgba(0, 245, 255, 0.4);

        position: relative;

        display: inline-block;

        left: 50%;

        transform: translateX(-50%);

        animation: titleGlow 3s infinite alternate;

    }

    @keyframes titleGlow {

        from { 

            text-shadow: 0 0 10px rgba(0, 245, 255, 0.6),

                        0 0 20px rgba(0, 245, 255, 0.4);

        }

        to { 

            text-shadow: 0 0 20px rgba(0, 245, 255, 1),

                        0 0 40px rgba(0, 245, 255, 0.6);

        }

    }

    .section-title::after {

        content: "";

        position: absolute;

        bottom: -15px;

        left: 50%;

        transform: translateX(-50%);

        width: 150px;

        height: 4px;

        background: linear-gradient(90deg, transparent, #00f5ff, #fc00ff, #00f5ff, transparent);

        border-radius: 2px;

        animation: underlineFlow 3s infinite;

    }

    @keyframes underlineFlow {

        0%, 100% { background-position: 0% 50%; }

        50% { background-position: 100% 50%; }

    }

    .steps-container {

        display: flex;

        justify-content: space-around;

        flex-wrap: wrap;

        gap: 2.5rem;

    }

    .step-card {

        background: rgba(0, 30, 60, 0.8);

        border-radius: 20px;

        padding: 3rem 2.5rem;

        text-align: center;

        flex: 1;

        min-width: 280px;

        max-width: 350px;

        box-shadow: 

            0 10px 40px rgba(0, 0, 0, 0.4),

            inset 0 1px 0 rgba(255, 255, 255, 0.1);

        transition: all 0.5s ease;

        border: 1px solid rgba(0, 197, 255, 0.3);

        backdrop-filter: blur(10px);

        position: relative;

        overflow: hidden;

    }

    .step-card::before {

        content: "";

        position: absolute;

        top: 0;

        left: 0;

        width: 100%;

        height: 5px;

        background: linear-gradient(90deg, #00c9ff, #fc00ff, #00c9ff);

        background-size: 200% 100%;

        animation: borderFlow 3s linear infinite;

    }

    @keyframes borderFlow {

        0% { background-position: -200% 0; }

        100% { background-position: 200% 0; }

    }

    .step-card:hover {

        transform: translateY(-15px) scale(1.05);

        box-shadow: 

            0 20px 60px rgba(0, 197, 255, 0.5),

            0 10px 30px rgba(252, 0, 255, 0.3);

        border: 1px solid rgba(0, 245, 255, 0.7);

    }

    .step-number {

        width: 80px;

        height: 80px;

        background: linear-gradient(135deg, #00c9ff 0%, #1e60c4 50%, #fc00ff 100%);

        color: white;

        border-radius: 50%;

        display: flex;

        align-items: center;

        justify-content: center;

        margin: 0 auto 2rem;

        font-weight: 900;

        font-size: 2rem;

        box-shadow: 

            0 0 20px rgba(0, 197, 255, 0.6),

            0 0 40px rgba(252, 0, 255, 0.3);

        border: 3px solid rgba(255, 255, 255, 0.2);

        animation: numberPulse 2s infinite;

    }

    @keyframes numberPulse {

        0%, 100% { transform: scale(1); }

        50% { transform: scale(1.1); }

    }

    .step-icon {

        font-size: 4rem;

        margin-bottom: 2rem;

        color: #00f5ff;

        text-shadow: 0 0 15px rgba(0, 245, 255, 0.8);

        animation: iconFloat 4s ease-in-out infinite;

    }

    @keyframes iconFloat {

        0%, 100% { transform: translateY(0px); }

        50% { transform: translateY(-10px); }

    }

    .step-title {

        color: #00f5ff;

        font-size: 1.8rem;

        font-weight: 700;

        margin-bottom: 1.5rem;

        text-shadow: 0 0 10px rgba(0, 245, 255, 0.6);

        text-transform: uppercase;

        letter-spacing: 1px;

    }

    .step-description {

        color: #c0d8ff;

        font-size: 1.1rem;

        line-height: 1.6;

        font-weight: 400;

    }

    /* Upload Section - Enhanced */

    .upload-section {

        background: rgba(255, 255, 255, 0.08);

        backdrop-filter: blur(15px);

        border-radius: 25px;

        padding: 4rem;

        margin-bottom: 3rem;

        border: 1px solid rgba(0, 197, 255, 0.25);

        box-shadow: 

            0 10px 40px rgba(0, 0, 0, 0.4),

            inset 0 1px 0 rgba(255, 255, 255, 0.1);

    }

    .upload-title {

        color: #00f5ff;

        text-align: center;

        font-size: 2.8rem;

        margin-bottom: 3rem;

        font-weight: 800;

        text-shadow: 0 0 15px rgba(0, 245, 255, 0.8);

        text-transform: uppercase;

        letter-spacing: 2px;

    }

    /* Drop Zone - Ultra Futuristic */

    .drop-zone {

        border: 4px dashed transparent;

        border-radius: 25px;

        padding: 4rem;

        text-align: center;

        cursor: pointer;

        transition: all 0.5s ease;

        background: rgba(0, 30, 60, 0.4);

        margin-bottom: 3rem;

        position: relative;

        overflow: hidden;

        box-shadow: 

            0 0 30px rgba(0, 197, 255, 0.3),

            inset 0 0 30px rgba(0, 0, 0, 0.2);

    }

    .drop-zone::before {

        content: "";

        position: absolute;

        top: -5px;

        left: -5px;

        right: -5px;

        bottom: -5px;

        background: linear-gradient(45deg, #00c9ff, #1e60c4, #fc00ff, #00c9ff, #1e60c4);

        background-size: 600% 600%;

        animation: borderAnimation 4s ease infinite;

        z-index: -1;

        border-radius: 30px;

    }

    @keyframes borderAnimation {

        0%, 100% { background-position: 0% 50%; }

        50% { background-position: 100% 50%; }

    }

    .drop-zone::after {

        content: "";

        position: absolute;

        top: 0;

        left: 0;

        right: 0;

        bottom: 0;

        background: rgba(0, 30, 60, 0.9);

        border-radius: 25px;

        z-index: -1;

    }

    .drop-zone:hover {

        transform: scale(1.02);

        box-shadow: 

            0 0 50px rgba(0, 197, 255, 0.5),

            inset 0 0 50px rgba(0, 197, 255, 0.1);

    }

    .upload-icon {

        font-size: 6rem;

        color: #00f5ff;

        margin-bottom: 2rem;

        text-shadow: 

            0 0 20px rgba(0, 245, 255, 0.8),

            0 0 40px rgba(0, 245, 255, 0.4);

        animation: iconPulse 3s ease-in-out infinite;

    }

    @keyframes iconPulse {

        0%, 100% { 

            transform: scale(1) translateY(0px);

            text-shadow: 0 0 20px rgba(0, 245, 255, 0.6);

        }

        50% { 

            transform: scale(1.1) translateY(-5px);

            text-shadow: 0 0 30px rgba(0, 245, 255, 1);

        }

    }

    .drop-text {

        font-size: 1.8rem;

        color: #e0f7ff;

        margin-bottom: 1.5rem;

        font-weight: 600;

        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);

        text-transform: uppercase;

        letter-spacing: 1px;

    }

    .file-types {

        color: #a0d0ff;

        font-size: 1.2rem;

        margin-bottom: 2.5rem;

        font-weight: 500;

    }

    .browse-button {

        background: linear-gradient(135deg, #00c9ff 0%, #1e60c4 50%, #fc00ff 100%);

        color: white;

        border: none;

        padding: 1.5rem 3rem;

        border-radius: 50px;

        cursor: pointer;

        font-size: 1.4rem;

        font-weight: 700;

        transition: all 0.4s ease;

        box-shadow: 

            0 0 25px rgba(0, 197, 255, 0.6),

            0 0 50px rgba(252, 0, 255, 0.3);

        text-transform: uppercase;

        letter-spacing: 2px;

        border: 2px solid rgba(255, 255, 255, 0.2);

        position: relative;

        overflow: hidden;

    }

    .browse-button::before {

        content: "";

        position: absolute;

        top: 0;

        left: -100%;

        width: 100%;

        height: 100%;

        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);

        transition: left 0.6s ease;

    }

    .browse-button:hover::before {

        left: 100%;

    }

    .browse-button:hover {

        transform: translateY(-3px) scale(1.05);

        box-shadow: 

            0 15px 35px rgba(0, 197, 255, 0.8),

            0 5px 15px rgba(252, 0, 255, 0.6);

    }

    /* Analysis Section - Enhanced */

    .analysis-section {

        display: flex;

        gap: 3rem;

        flex-wrap: wrap;

        margin-bottom: 3rem;

    }

    .image-preview-container, .results-container {

        flex: 1;

        min-width: 350px;

        background: rgba(255, 255, 255, 0.08);

        backdrop-filter: blur(15px);

        border-radius: 25px;

        padding: 3rem;

        box-shadow: 

            0 10px 40px rgba(0, 0, 0, 0.4),

            inset 0 1px 0 rgba(255, 255, 255, 0.1);

        border: 1px solid rgba(0, 197, 255, 0.25);

        transition: all 0.4s ease;

    }

    .image-preview-container:hover, .results-container:hover {

        transform: translateY(-5px);

        box-shadow: 

            0 15px 50px rgba(0, 197, 255, 0.3),

            inset 0 1px 0 rgba(255, 255, 255, 0.15);

    }

    .section-subtitle {

        color: #00f5ff;

        font-size: 2.2rem;

        margin-bottom: 2.5rem;

        font-weight: 700;

        text-align: center;

        text-shadow: 0 0 15px rgba(0, 245, 255, 0.8);

        text-transform: uppercase;

        letter-spacing: 1px;

    }

    .preview-image {

        width: 100%;

        max-height: 450px;

        object-fit: contain;

        border-radius: 20px;

        box-shadow: 

            0 0 30px rgba(0, 197, 255, 0.4),

            0 0 60px rgba(252, 0, 255, 0.2);

        border: 3px solid rgba(0, 245, 255, 0.4);

        transition: all 0.4s ease;

    }

    .preview-image:hover {

        transform: scale(1.02);

        box-shadow: 

            0 0 40px rgba(0, 197, 255, 0.6),

            0 0 80px rgba(252, 0, 255, 0.3);

    }

    /* Loading Animation - Enhanced */

    .loading-container {

        text-align: center;

        padding: 4rem;

    }

    .spinner {

        width: 100px;

        height: 100px;

        border: 6px solid rgba(0, 197, 255, 0.3);

        border-top: 6px solid #00f5ff;

        border-right: 6px solid #fc00ff;

        border-radius: 50%;

        animation: multiSpin 1.5s linear infinite;

        margin: 0 auto 2.5rem;

        box-shadow: 

            0 0 30px rgba(0, 245, 255, 0.6),

            inset 0 0 30px rgba(0, 245, 255, 0.2);

        position: relative;

    }

    .spinner::before {

        content: "";

        position: absolute;

        top: 10px;

        left: 10px;

        right: 10px;

        bottom: 10px;

        border: 3px solid transparent;

        border-top: 3px solid rgba(252, 0, 255, 0.6);

        border-radius: 50%;

        animation: multiSpin 1s linear infinite reverse;

    }

    @keyframes multiSpin {

        0% { transform: rotate(0deg); }

        100% { transform: rotate(360deg); }

    }

    .loading-text {

        font-size: 1.8rem;

        color: #00f5ff;

        font-weight: 700;

        text-shadow: 0 0 15px rgba(0, 245, 255, 0.8);

        margin-bottom: 1rem;

        animation: textPulse 2s infinite;

    }

    @keyframes textPulse {

        0%, 100% { opacity: 0.8; }

        50% { opacity: 1; }

    }

    .loading-subtext {

        color: #a0d0ff;

        margin-top: 1rem;

        font-size: 1.2rem;

        font-weight: 500;

    }

    /* Results Card - Ultra Enhanced */

    .results-card {

        background: rgba(0, 30, 60, 0.8);

        border-radius: 20px;

        padding: 3rem;

        box-shadow: 

            0 10px 40px rgba(0, 0, 0, 0.4),

            inset 0 1px 0 rgba(255, 255, 255, 0.1);

        border: 1px solid rgba(0, 197, 255, 0.4);

        backdrop-filter: blur(10px);

        animation: cardSlideIn 0.8s ease-out;

    }

    @keyframes cardSlideIn {

        0% { 

            opacity: 0; 

            transform: translateY(30px);

        }

        100% { 

            opacity: 1; 

            transform: translateY(0);

        }

    }

    .result-item {

        margin-bottom: 2.5rem;

        padding: 2rem;

        border-radius: 15px;

        background: rgba(0, 20, 40, 0.6);

        border: 1px solid rgba(0, 197, 255, 0.3);

        transition: all 0.3s ease;

        position: relative;

        overflow: hidden;

    }

    .result-item::before {

        content: "";

        position: absolute;

        top: 0;

        left: 0;

        width: 100%;

        height: 2px;

        background: linear-gradient(90deg, #00c9ff, #fc00ff);

        animation: resultGlow 3s infinite;

    }

    @keyframes resultGlow {

        0%, 100% { opacity: 0.5; }

        50% { opacity: 1; }

    }

    .result-item:hover {

        transform: translateX(10px);

        box-shadow: 0 5px 20px rgba(0, 197, 255, 0.3);

    }

    .result-title {

        color: #00f5ff;

        font-size: 1.6rem;

        font-weight: 700;

        margin-bottom: 1.5rem;

        display: flex;

        align-items: center;

        gap: 1rem;

        text-shadow: 0 0 10px rgba(0, 245, 255, 0.6);

        text-transform: uppercase;

        letter-spacing: 1px;

    }

    .disease-name {

        font-size: 2.2rem;

        font-weight: 900;

        color: #ffffff;

        background: linear-gradient(45deg, #00dbde, #fc00ff, #00c9ff);

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        background-clip: text;

        text-shadow: 0 0 15px rgba(0, 245, 255, 0.8);

        text-align: center;

        margin: 1.5rem 0;

        animation: diseaseGlow 2s infinite alternate;

        text-transform: uppercase;

        letter-spacing: 2px;

    }

    @keyframes diseaseGlow {

        0% { 

            filter: brightness(1);

            transform: scale(1);

        }

        100% { 

            filter: brightness(1.2);

            transform: scale(1.05);

        }

    }

    /* Progress Bar - Ultra Futuristic */

    .progress-container {

        margin: 2rem 0;

    }

    .progress-label {

        display: flex;

        justify-content: space-between;

        margin-bottom: 1rem;

        font-weight: 600;

        color: #e0f7ff;

        font-size: 1.1rem;

    }

    .progress-bar-bg {

        width: 100%;

        height: 20px;

        background-color: rgba(0, 30, 60, 0.8);

        border-radius: 15px;

        overflow: hidden;

        box-shadow: 

            inset 0 0 15px rgba(0, 0, 0, 0.6),

            0 0 10px rgba(0, 197, 255, 0.3);

        border: 2px solid rgba(0, 197, 255, 0.4);

        position: relative;

    }

    .progress-bar-bg::before {

        content: "";

        position: absolute;

        top: 0;

        left: 0;

        right: 0;

        bottom: 0;

        background: linear-gradient(45deg, 

            rgba(0, 197, 255, 0.1) 25%, 

            transparent, 

            transparent 50%, 

            rgba(0, 197, 255, 0.1) 50%, 

            rgba(0, 197, 255, 0.1) 75%, 

            transparent);

        background-size: 20px 20px;

        animation: progressPattern 2s linear infinite;

    }

    @keyframes progressPattern {

        0% { background-position: 0 0; }

        100% { background-position: 20px 0; }

    }

    .progress-bar-fill {

        height: 100%;

        background: linear-gradient(90deg, #00c9ff, #1e60c4, #fc00ff, #00f5ff);

        background-size: 200% 100%;

        border-radius: 15px;

        transition: width 2s ease-in-out;

        box-shadow: 

            0 0 20px rgba(0, 245, 255, 0.8),

            inset 0 2px 10px rgba(255, 255, 255, 0.3);

        position: relative;

        animation: progressFlow 3s linear infinite;

    }

    @keyframes progressFlow {

        0% { background-position: 0% 50%; }

        100% { background-position: 200% 50%; }

    }

    .progress-bar-fill::after {

        content: "";

        position: absolute;

        top: 0;

        left: 0;

        right: 0;

        bottom: 0;

        background: linear-gradient(90deg, 

            transparent, 

            rgba(255, 255, 255, 0.4), 

            transparent);

        animation: progressShine 2s infinite;

    }

    @keyframes progressShine {

        0% { transform: translateX(-100%); }

        100% { transform: translateX(100%); }

    }

    .confidence-text {

        font-weight: 900;

        color: #00f5ff;

        text-shadow: 0 0 10px rgba(0, 245, 255, 0.8);

        font-size: 1.4rem;

        font-family: 'Orbitron', sans-serif;

    }

    /* Treatment Box - Enhanced */

    .treatment-box {

        background: rgba(0, 40, 80, 0.7);

        border-left: 6px solid #00f5ff;

        border-radius: 15px;

        padding: 2.5rem;

        margin-top: 1.5rem;

        box-shadow: 

            0 0 20px rgba(0, 197, 255, 0.4),

            inset 0 1px 0 rgba(255, 255, 255, 0.1);

        border: 1px solid rgba(0, 197, 255, 0.3);

        position: relative;

        overflow: hidden;

    }

    .treatment-box::before {

        content: "";

        position: absolute;

        top: 0;

        left: 0;

        width: 6px;

        height: 100%;

        background: linear-gradient(180deg, #00c9ff, #fc00ff, #00f5ff);

        animation: treatmentGlow 3s infinite;

    }

    @keyframes treatmentGlow {

        0%, 100% { opacity: 0.7; }

        50% { opacity: 1; }

    }

    .treatment-text {

        line-height: 1.8;

        color: #e0f7ff;

        font-size: 1.2rem;

        font-weight: 500;

        text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);

    }

    /* Buttons - Ultra Enhanced */

    .analyze-button, .reset-button {

        border: none;

        padding: 2rem;

        border-radius: 20px;

        cursor: pointer;

        font-size: 1.4rem;

        font-weight: 800;

        transition: all 0.4s ease;

        width: 100%;

        margin-top: 2rem;

        text-transform: uppercase;

        letter-spacing: 2px;

        position: relative;

        overflow: hidden;

        backdrop-filter: blur(10px);

    }

    .analyze-button {

        background: linear-gradient(135deg, #00c9ff 0%, #1e60c4 50%, #fc00ff 100%);

        color: white;

        box-shadow: 

            0 0 30px rgba(0, 197, 255, 0.6),

            0 0 60px rgba(252, 0, 255, 0.3);

        border: 2px solid rgba(255, 255, 255, 0.2);

    }

    .analyze-button::before {

        content: "";

        position: absolute;

        top: 0;

        left: -100%;

        width: 100%;

        height: 100%;

        background: linear-gradient(90deg, 

            transparent, 

            rgba(255, 255, 255, 0.3), 

            transparent);

        transition: left 0.8s ease;

    }

    .analyze-button:hover::before {

        left: 100%;

    }

    .analyze-button:hover {

        transform: translateY(-8px) scale(1.02);

        box-shadow: 

            0 15px 40px rgba(0, 197, 255, 0.8),

            0 5px 20px rgba(252, 0, 255, 0.6);

    }

    .reset-button {

        background: linear-gradient(135deg, #ff2d95 0%, #b30062 50%, #ff6b35 100%);

        color: white;

        box-shadow: 

            0 0 25px rgba(255, 45, 149, 0.5),

            0 0 50px rgba(179, 0, 98, 0.3);

        border: 2px solid rgba(255, 45, 149, 0.3);

    }

    .reset-button:hover {

        transform: translateY(-5px) scale(1.02);

        box-shadow: 

            0 12px 30px rgba(255, 45, 149, 0.7),

            0 5px 15px rgba(179, 0, 98, 0.5);

    }

    .analyze-button:disabled {

        background: linear-gradient(135deg, #2a2a4a, #1a1a3a);

        cursor: not-allowed;

        transform: none;

        box-shadow: none;

        border: 1px solid #444466;

        opacity: 0.5;

    }

    /* Error Message - Enhanced */

    .error-box {

        background: rgba(100, 0, 40, 0.5);

        border-left: 6px solid #ff2d95;

        border-radius: 15px;

        padding: 2rem;

        margin: 2rem 0;

        color: #ff7eb9;

        box-shadow:
