import re

with open("c:/Users/hp/Documents/GitHub/plant--savior--ai/streamlit_app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the giant style block
new_style = """<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&display=swap');

    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp {
        background-color: #f6f8f7;
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
    
    .text-primary { color: #10b981; }
    
    .main-header {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
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
        background-color: rgba(16, 185, 129, 0.1);
        color: #10b981;
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
        box-shadow: 0 20px 25px -5px rgba(16, 185, 129, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
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
        align-items: center;
        gap: 0.5rem;
    }
    
    .stats-section {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
        color: #10b981;
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
        background-color: rgba(16, 185, 129, 0.1);
        color: #10b981;
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
        color: #10b981;
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
        background: linear-gradient(90deg, #10b981, #34d399);
        border-radius: 9999px;
    }
    
    .confidence-text {
        font-weight: 700;
        color: #0f172a;
    }
    
    .treatment-box {
        background-color: rgba(16, 185, 129, 0.05);
        border-left: 4px solid #10b981;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
    }
    
    .treatment-text {
        color: #1e293b;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    div[data-baseweb="input"] {
        border-radius: 0.75rem !important;
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 1px #10b981 !important;
    }
    
    .stButton > button {
        background-color: #13ec92 !important;
        color: #0f172a !important;
        border: none !important;
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2) !important;
    }
    
    .stButton > button:hover {
        background-color: #10d482 !important;
        transform: translateY(-1px) !important;
    }
    
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
    
    .success-box, div[data-testid="stAlert"][data-baseweb="notification"] {
        background-color: #f0fdf4 !important;
        color: #166534 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 0.75rem !important;
    }
    
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(16, 185, 129, 0.2);
        border-top: 4px solid #10b981;
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
        color: #10b981;
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
    
    .error-box {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        color: #991b1b;
        margin: 1rem 0;
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
</style>"""

content = re.sub(r'<style>.*?</style>', new_style, content, flags=re.DOTALL)

# Now we also need to update HTML wrappers in st.markdown:
# Example: 🔐 ACCESS CONTROL -> System Authentication
# SECURE GATEWAY TO PLANT SAVIOR AI SYSTEM -> Authorized Personnel Access Only

# Let's replace the login page header
content = content.replace(
'''    <div class="main-header" style="padding: 2rem; margin-bottom: 2rem; animation: none;">
        <h1 class="logo-text" style="font-size: 3.5rem;">🔐 ACCESS CONTROL</h1>
        <p class="tagline">SECURE GATEWAY TO PLANT SAVIOR AI SYSTEM</p>
    </div>''',
'''    <div class="login-container shadow-sm border">
        <div style="display:flex; justify-content:center; align-items:center; flex-direction:column; gap:10px;">
           <span class="material-symbols-outlined text-primary" style="font-size: 3rem;">potted_plant</span>
           <h1 class="logo-text" style="font-size: 2.5rem;">System Authentication</h1>
           <p class="tagline">Authorized Personnel Access Only</p>
        </div>
    </div>'''
)

content = content.replace(
'''        st.markdown('<div class="glass-container fade-in-up" style="padding: 3rem; border: 1px solid rgba(0, 245, 255, 0.3);">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title" style="font-size: 2rem; margin-bottom: 2rem;">IDENTITY VERIFICATION</h2>', unsafe_allow_html=True)''',
'''        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title" style="font-size: 1.5rem; text-align:center;">Operator Login</h2>', unsafe_allow_html=True)'''
)

content = content.replace('👤 OPERATOR ID', 'Operator ID')
content = content.replace('🔑 ACCESS CODE', 'Access Code')
content = content.replace('🚀 INITIATE SYSTEM', 'Initiate System')

content = content.replace(
'''<div class="main-header">
    <h1 class="logo-text">🌱 PLANT SAVIOR AI</h1>
    <p class="tagline">NEXT-GENERATION PLANT DISEASE DETECTION POWERED BY ADVANCED ARTIFICIAL INTELLIGENCE</p>
</div>''',
'''<div class="hero-section">
    <h1 class="hero-title">Empowering Global Agriculture with AI</h1>
    <p class="hero-subtitle">Revolutionizing crop health with instant disease detection and precision farming insights using state-of-the-art neural networks.</p>
</div>'''
)

content = content.replace(
'''<div class="step-card">
        <div class="step-number">1</div>
        <div class="step-icon">📱</div>
        <h3 class="step-title">IMAGE CAPTURE</h3>''',
'''<div class="step-card">
        <div class="step-number">1</div>
        <h3 class="step-title"><span class="material-symbols-outlined">add_a_photo</span> IMAGE CAPTURE</h3>'''
)

content = content.replace(
'''<div class="step-card">
        <div class="step-number">2</div>
        <div class="step-icon">🧠</div>
        <h3 class="step-title">AI PROCESSING</h3>''',
'''<div class="step-card">
        <div class="step-number">2</div>
        <h3 class="step-title"><span class="material-symbols-outlined">memory</span> AI PROCESSING</h3>'''
)

content = content.replace(
'''<div class="step-card">
        <div class="step-number">3</div>
        <div class="step-icon">📊</div>
        <h3 class="step-title">INSTANT DIAGNOSIS</h3>''',
'''<div class="step-card">
        <div class="step-number">3</div>
        <h3 class="step-title"><span class="material-symbols-outlined">assessment</span> DIAGNOSIS</h3>'''
)

# Replace Loading Spinners
content = content.replace('🧠 AI PROCESSING IMAGE...', 'AI PROCESSING IMAGE...')
content = content.replace('🔍 DETECTING PATTERNS...', 'DETECTING PATTERNS...')
content = content.replace('📊 GENERATING DIAGNOSIS...', 'GENERATING DIAGNOSIS...')

# Results
content = content.replace('🎯 PRIMARY DIAGNOSIS', 'Primary Diagnosis')
content = content.replace('🎯 CONFIDENCE ANALYSIS', 'Confidence Analysis')
content = content.replace('🌿 CARE RECOMMENDATION', 'Care Recommendation')
content = content.replace('💊 TREATMENT PROTOCOL', 'Treatment Protocol')
content = content.replace('📈 ANALYSIS SUMMARY', 'Analysis Summary')

# Team
content = content.replace('👥 MEET THE TEAM', 'Meet The Team')

# Fix inline styles for Health Status
content = content.replace(
'''<span style="background: linear-gradient(90deg, #00ff88, #00cc66); color: white; padding: 0.5rem 2rem; border-radius: 25px; font-weight: bold; font-size: 1.1rem;">🌿 HEALTHY PLANT</span>''',
'''<span style="background-color: #dcfce7; color: #166534; padding: 0.5rem 1.5rem; border-radius: 9999px; font-weight: 600; font-size: 0.875rem;">Healthy Plant</span>'''
)

content = content.replace(
'''<span style="background: linear-gradient(90deg, #ff6b35, #ff2d95); color: white; padding: 0.5rem 2rem; border-radius: 25px; font-weight: bold; font-size: 1.1rem;">⚠️ DISEASE DETECTED</span>''',
'''<span style="background-color: #fee2e2; color: #991b1b; padding: 0.5rem 1.5rem; border-radius: 9999px; font-weight: 600; font-size: 0.875rem;">Disease Detected</span>'''
)

with open("c:/Users/hp/Documents/GitHub/plant--savior--ai/streamlit_app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced CSS and HTML formatting.")
