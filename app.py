import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# ────────────────────────────────────────────────
# SAYFA AYARLARI & TEMEL STİL
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="Professional CV Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f8f9fc; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.2rem; font-weight: bold; }
    .stButton>button[kind="primary"] { background-color: #4361ee; color: white; }
    .st-expander { border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# DİL DESTEĞİ
# ────────────────────────────────────────────────
LANGUAGES = {
    "Türkçe": {
        "title": "Profesyonel CV Oluşturucu",
        "caption": "ATS uyumlu, modern CV hazırlama aracı",
        "personal": "Kişisel Bilgiler",
        "contact": "İletişim",
        "summary": "Profesyonel Özet",
        "experience": "İş Deneyimi",
        "education": "Eğitim",
        "certificates": "Sertifikalar",
        "skills": "Yetenekler",
        "languages": "Diller",
        "projects": "Projeler",
        "labels": {
            "name": "Ad Soyad *",
            "title": "Unvan / Hedef Pozisyon",
            "email": "E-posta *",
            "phone": "Telefon",
            "linkedin": "LinkedIn",
            "github": "GitHub",
            "summary": "Kendinizi kısaca tanıtın...",
            "summary_help": "Başarılarınızı rakamlarla destekleyin",
            "position": "Pozisyon",
            "company": "Kurum / Şirket",
            "period": "Tarih Aralığı",
            "location": "Şehir, Ülke",
            "description": "Açıklama / Başarılar (her satıra bir madde)",
            "cert_name": "Sertifika Adı / Veren Kurum",
            "cert_date": "Tarih",
            "skill_inp": "Yetenek ekle (örn: Python – Uzman)",
            "lang_inp": "Dil ekle (örn: İngilizce – C1)",
        },
        "buttons": {
            "generate": "PDF Oluştur ve İndir",
            "add_cert": "+ Sertifika Ekle",
            "add_skill": "+ Yetenek",
            "add_lang": "+ Dil",
            "remove": "Sil"
        },
        "errors": {"required": "Ad Soyad ve E-posta zorunludur."},
        "success": "CV başarıyla oluşturuldu! 🎉"
    },
    "English": {
        "title": "Professional CV Builder",
        "caption": "ATS-friendly modern CV creator",
        "personal": "Personal Information",
        "contact": "Contact",
        "summary": "Professional Summary",
        "experience": "Experience",
        "education": "Education",
        "certificates": "Certificates",
        "skills": "Skills",
        "languages": "Languages",
        "projects": "Projects",
        "labels": {
            "name": "Full Name *",
            "title": "Title / Target Role",
            "email": "Email *",
            "phone": "Phone",
            "linkedin": "LinkedIn",
            "github": "GitHub",
            "summary": "Brief professional introduction...",
            "summary_help": "Support achievements with numbers",
            "position": "Position / Role",
            "company": "Company / Organization",
            "period": "Date Range",
            "location": "City, Country",
            "description": "Description / Achievements (one per line)",
            "cert_name": "Certificate Name / Issuer",
            "cert_date": "Date",
            "skill_inp": "Add skill (e.g. Python – Expert)",
            "lang_inp": "Add language (e.g. English – C1)",
        },
        "buttons": {
            "generate": "Generate & Download PDF",
            "add_cert": "+ Add Certificate",
            "add_skill": "+ Add Skill",
            "add_lang": "+ Add Language",
            "remove": "Remove"
        },
        "errors": {"required": "Full Name and Email are required."},
        "success": "CV generated successfully! 🎉"
    }
}

# Varsayılan dil
if "lang" not in st.session_state:
    st.session_state.lang = "Türkçe"

texts = LANGUAGES[st.session_state.lang]

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
with st.sidebar:
    st.title("Ayarlar" if st.session_state.lang == "Türkçe" else "Settings")
    
    lang_choice = st.radio(
        "Dil / Language",
        ["Türkçe", "English"],
        index=0 if st.session_state.lang == "Türkçe" else 1,
        key="lang_radio"
    )
    
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        texts = LANGUAGES[st.session_state.lang]
        st.rerun()

    theme_color = st.color_picker(
        "Tema Rengi / Theme Color",
        "#2b6cb0",
        key="theme_picker"
    )

    photo = st.file_uploader(
        "Fotoğraf (isteğe bağlı) / Photo (optional)",
        type=["jpg", "jpeg", "png"],
        key="photo_upload"
    )
    if photo:
        st.session_state.photo = photo.read()
        st.image(st.session_state.photo, width=160)

# ────────────────────────────────────────────────
# ANA İÇERİK
# ────────────────────────────────────────────────
st.title(texts["title"])
st.caption(texts["caption"])

# Kişisel Bilgiler
with st.expander(texts["personal"], expanded=True):
    c1, c2 = st.columns([3,2])
    name = c1.text_input(texts["labels"]["name"], key=f"name_{st.session_state.lang}")
    title = c2.text_input(texts["labels"]["title"], key=f"title_{st.session_state.lang}")

# İletişim
with st.expander(texts["contact"], expanded=True):
    cols = st.columns([2,2,2,1])
    email = cols[0].text_input(texts["labels"]["email"], key=f"email_{st.session_state.lang}")
    phone = cols[1].text_input(texts["labels"]["phone"], key=f"phone_{st.session_state.lang}")
    linkedin = cols[2].text_input(texts["labels"]["linkedin"], key=f"linkedin_{st.session_state.lang}")
    github = cols[3].text_input(texts["labels"]["github"], key=f"github_{st.session_state.lang}")

# Özet
with st.expander(texts["summary"], expanded=True):
    summary = st.text_area(
        texts["labels"]["summary"],
        height=140,
        help=texts["labels"]["summary_help"],
        key=f"summary_{st.session_state.lang}"
    )

# İş Deneyimi (basit versiyon – genişletilebilir)
with st.expander(texts["experience"]):
    exp_text = st.text_area(
        "Deneyimlerinizi madde madde yazın...",
        height=180,
        key=f"exp_{st.session_state.lang}"
    )

# Eğitim
with st.expander(texts["education"]):
    edu_text = st.text_area(
        "Eğitim bilgilerinizi madde madde yazın...",
        height=180,
        key=f"edu_{st.session_state.lang}"
    )

# Yetenekler & Diller
with st.expander(texts["skills"] + " & " + texts["languages"]):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**" + texts["skills"] + "**")
        skills_text = st.text_area("Python, SQL, Power BI, vs...", height=120, key=f"skills_{st.session_state.lang}")
    with col2:
        st.markdown("**" + texts["languages"] + "**")
        languages_text = st.text_area("Türkçe (Anadil), İngilizce (C1), vs...", height=120, key=f"langs_{st.session_state.lang}")

# Sertifikalar
with st.expander(texts["certificates"]):
    certs_text = st.text_area("Sertifika isimlerini ve tarihlerini yazın...", height=140, key=f"certs_{st.session_state.lang}")

# ────────────────────────────────────────────────
# PDF ÜRETİMİ
# ────────────────────────────────────────────────
if st.button(texts["buttons"]["generate"], type="primary"):
    if not name.strip() or not email.strip():
        st.error(texts["errors"]["required"])
    else:
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        r, g, b = int(theme_color.lstrip('#')[0:2], 16), int(theme_color.lstrip('#')[2:4], 16), int(theme_color.lstrip('#')[4:6], 16)
        pdf.set_fill_color(r, g, b)
        pdf.rect(0, 0, 210, 40, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 12, name.upper(), ln=1, align="C")
        pdf.set_font("Helvetica", "I", 14)
        pdf.cell(0, 10, title, ln=1, align="C")
        
        # İletişim
        pdf.set_y(35)
        pdf.set_text_color(240, 240, 240)
        pdf.set_font("Helvetica", "", 10)
        contacts = [email, phone, linkedin, github]
        contacts = [c for c in contacts if c.strip()]
        pdf.cell(0, 6, " • ".join(contacts), align="C")
        
        pdf.set_y(50)
        pdf.set_text_color(0, 0, 0)
        
        # Özet
        if summary.strip():
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 8, texts["summary"].upper(), ln=1)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, summary)
            pdf.ln(8)
        
        # Deneyim
        if exp_text.strip():
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 8, texts["experience"].upper(), ln=1)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, exp_text)
            pdf.ln(8)
        
        # Eğitim
        if edu_text.strip():
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 8, texts["education"].upper(), ln=1)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, edu_text)
            pdf.ln(8)
        
        # Yetenekler & Diller
        if skills_text.strip() or languages_text.strip():
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 8, "Skills & Languages / Yetenekler & Diller".upper(), ln=1)
            pdf.set_font("Helvetica", "", 11)
            if skills_text.strip():
                pdf.multi_cell(0, 7, "Skills: " + skills_text)
            if languages_text.strip():
                pdf.multi_cell(0, 7, "Languages: " + languages_text)
            pdf.ln(8)
        
        # Sertifikalar
        if certs_text.strip():
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 8, texts["certificates"].upper(), ln=1)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, certs_text)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', errors='replace')

        st.download_button(
            label="📥 " + ("Download PDF" if st.session_state.lang == "English" else "PDF İndir"),
            data=pdf_bytes,
            file_name=f"{name.replace(' ', '_') or 'cv'}_CV.pdf",
            mime="application/pdf"
        )

        st.success(texts["success"])
        st.balloons()
