#!/usr/bin/env python3
"""
Professional CV Builder Web Application
Built with Streamlit - Modern, Clean, User-Friendly Interface
Supports PDF and Word export with Turkish character support and multilingual interface
"""

import streamlit as st
import io
import os
from datetime import datetime, date
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Page configuration
st.set_page_config(
    page_title="Professional CV Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling with improved language selector
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .language-container {
        position: fixed;
        top: 10px;
        right: 20px;
        z-index: 999;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 10px 20px;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        min-width: 200px;
    }
    
    .language-container .stSelectbox label {
        color: white !important;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    
    .language-container .stSelectbox > div > div {
        background: rgba(255,255,255,0.2) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 15px !important;
    }
    
    .language-container .stSelectbox > div > div > div {
        color: white !important;
        font-weight: 600;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3498db;
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .preview-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .language-container {
            position: relative;
            top: 0;
            right: 0;
            margin-bottom: 1rem;
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

def setup_unicode_font():
    """Setup Unicode font for Turkish character support in PDF"""
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "C:/Windows/Fonts/arial.ttf",  # Windows
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('UnicodeFont', font_path))
                return 'UnicodeFont'
        
        return 'Helvetica'
        
    except Exception as e:
        print(f"Font setup error: {e}")
        return 'Helvetica'

def initialize_session_state():
    """Initialize session state variables"""
    if 'cv_data' not in st.session_state:
        st.session_state.cv_data = {
            'personal_info': {},
            'work_experience': [],
            'education': [],
            'skills': [],
            'languages': [],
            'certifications': [],
            'projects': []
        }
    
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
