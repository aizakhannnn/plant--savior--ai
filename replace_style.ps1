$ErrorActionPreference = "Stop"

$path = "c:\Users\hp\Documents\GitHub\plant--savior--ai\streamlit_app.py"
$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

$newStyle = @"
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
"@

$content = [System.Text.RegularExpressions.Regex]::Replace($content, "(?s)<style>.*?</style>", $newStyle)
[System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
Write-Output "Style Replaced Successfully."
