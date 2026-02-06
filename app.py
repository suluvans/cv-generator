import streamlit as st
from fpdf import FPDF
import base64
import re
from datetime import datetime
import io

# ────────────────────────────────────────────────
# SAYFA AYARLARI & TEMEL STİL
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="Ultimate Professional CV Builder",
    page_icon="📄✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f8f9fc; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.2rem;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 1rem 0;
    }
    .stButton>button[kind="primary"] {
        background-color: #4361ee;
        color: white;
    }
    .st-expander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    h1, h2, h3 { color: #2d3748; }
    .section-title {
        color: #2b6cb0;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    hr { border-color: #cbd5e0; margin: 2rem 0; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# DİL DESTEĞİ — TAM İNGİLİZCE ÇEVİRİ
# ────────────────────────────────────────────────
LANGUAGES = {
    "Türkçe": {
        "app_title": "🚀 Ultimate Profesyonel CV Oluşturucu",
        "sidebar_title": "Ayarlar",
        "language_label": "Dil",
        "theme_label": "Ana Tema Rengi",
        "photo_label": "Profil Fotoğrafı (isteğe bağlı)",
        "photo_caption": "Önizleme",
        "photo_info": "En iyi sonuç için fotoğrafı 1:1 oranında (kare) yükleyin.",
        "caption": "2025 standartlarına uygun, ATS dostu, modern CV oluşturucu",
        "sections": {
            "personal": "Kişisel Bilgiler",
            "contact": "İletişim Bilgileri",
            "summary": "Profesyonel Özet / Kariyer Hedefi",
            "experience": "İş Deneyimi",
            "education": "Eğitim",
            "certificates": "Sertifikalar & Belgeler",
            "skills": "Yetenekler",
            "languages": "Diller",
            "projects": "Projeler",
            "awards_publications_volunteer": "Ödüller & Başarılar / Yayınlar / Gönüllü Deneyim",
        },
        "labels": {
            "name": "Ad Soyad **",
            "title": "Unvan / Hedef Pozisyon",
            "email": "E-posta **",
            "phone": "Telefon",
            "linkedin": "LinkedIn URL",
            "github": "GitHub",
            "summary_title": "Kariyer Özeti (4–8 cümle önerilir)",
            "summary_help": "Başarılarınızı sayısal verilerle destekleyin (örn: satışları %38 artırdım)",
            "position": "Pozisyon / Rol",
            "company": "Kurum / Şirket",
            "period": "Tarih Aralığı",
            "location": "Konum",
            "description": "Açıklama / Başarılar (her satıra bir madde)",
            "cert_name": "Sertifika Adı / Veren Kurum",
            "cert_date": "Tarih",
            "add_cert": "+ Sertifika Ekle",
            "skills_title": "**Yetenekler**",
            "skills_placeholder": "Yetenek ekle (örn: Python – Uzman)",
            "add_skill": "+ Yetenek",
            "languages_title": "**Diller**",
            "lang_placeholder": "Dil ekle (örn: İngilizce – C1)",
            "add_lang": "+ Dil",
        },
        "buttons": {
            "add": "Ekle",
            "remove": "Sil",
            "generate": "📄 PDF Oluştur & İndir"
        },
        "tooltips": {
            "bullet": "Her maddeyi yeni satıra yazın. Otomatik • işareti eklenecek."
        },
        "errors": {
            "required": "Ad Soyad ve E-posta alanları zorunludur."
        },
        "success": "CV başarıyla oluşturuldu! 🎉"
    },

    "English": {
        "app_title": "🚀 Ultimate Professional CV Builder",
        "sidebar_title": "Settings",
        "language_label": "Language",
        "theme_label": "Theme Color",
        "photo_label": "Profile Photo (optional)",
        "photo_caption": "Preview",
        "photo_info": "For best results, upload a square (1:1) photo.",
        "caption": "ATS-friendly, modern CV builder",
        "sections": {
            "personal": "Personal Information",
            "contact": "Contact Information",
            "summary": "Professional Summary / Career Objective",
            "experience": "Work Experience",
            "education": "Education",
            "certificates": "Certificates & Credentials",
            "skills": "Skills",
            "languages": "Languages",
            "projects": "Projects",
            "awards_publications_volunteer": "Awards & Achievements / Publications / Volunteer Experience",
        },
        "labels": {
            "name": "Full Name **",
            "title": "Title / Target Position",
            "email": "Email **",
            "phone": "Phone",
            "linkedin": "LinkedIn URL",
            "github": "GitHub",
            "summary_title": "Professional Summary (4–8 sentences recommended)",
            "summary_help": "Support achievements with numbers (e.g. increased sales by 38%)",
            "position": "Position / Role",
            "company": "Company / Organization",
            "period": "Date Range",
            "location": "Location",
            "description": "Description / Achievements (one bullet per line)",
            "cert_name": "Certificate Name / Issuing Organization",
            "cert_date": "Date",
            "add_cert": "+ Add Certificate",
            "skills_title": "**Skills**",
            "skills_placeholder": "Add skill (e.g. Python – Expert)",
            "add_skill": "+ Add Skill",
            "languages_title": "**Languages**",
            "lang_placeholder": "Add language (e.g. English – C1)",
            "add_lang": "+ Add Language",
        },
        "buttons": {
            "add": "Add",
            "remove": "Remove",
            "generate": "📄 Generate & Download PDF"
        },
        "tooltips": {
            "bullet": "Write each item on a new line. Bullet • will be added automatically."
        },
        "errors": {
            "required": "Full Name and Email fields are required."
        },
        "success": "CV generated successfully! 🎉"
    }
}

# Varsayılan dil
if "lang" not in st.session_state:
    st.session_state.lang = "Türkçe"

# ────────────────────────────────────────────────
# DİL SEÇİMİ
# ────────────────────────────────────────────────
with st.sidebar:
    st.title(LANGUAGES[st.session_state.lang]["sidebar_title"])
    selected_lang = st.radio(
        LANGUAGES[st.session_state.lang]["language_label"],
        ["Türkçe", "English"],
        index=0 if st.session_state.lang == "Türkçe" else 1
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

texts = LANGUAGES[st.session_state.lang]

# ────────────────────────────────────────────────
# SIDEBAR DEVAMI
# ────────────────────────────────────────────────
with st.sidebar:
    st.session_state.theme_color = st.color_picker(
        texts["labels"]["theme_label"],
        "#2b6cb0"
    )

    uploaded_photo = st.file_uploader(
        texts["labels"]["photo_label"],
        type=["jpg","jpeg","png"]
    )
    if uploaded_photo:
        st.session_state.photo = uploaded_photo.read()
        st.image(st.session_state.photo, width=180, caption=texts["labels"]["photo_caption"])

    st.info(texts["labels"]["photo_info"])

# ────────────────────────────────────────────────
# ANA EKRAN
# ────────────────────────────────────────────────
st.title(texts["app_title"])
st.caption(texts["caption"])

# Kişisel Bilgiler
with st.expander(texts["sections"]["personal"], expanded=True):
    col1, col2 = st.columns([3,2])
    st.session_state.name = col1.text_input(
        texts["labels"]["name"],
        value=st.session_state.get("name", ""),
        placeholder=texts["placeholders"].get("name", "Ad Soyad")
    )
    st.session_state.title = col2.text_input(
        texts["labels"]["title"],
        value=st.session_state.get("title", ""),
        placeholder=texts["placeholders"].get("title", "Unvan")
    )

# İletişim
with st.expander(texts["sections"]["contact"], expanded=True):
    cols = st.columns([2,2,2,1])
    email = cols[0].text_input(texts["labels"]["email"], key="email")
    phone = cols[1].text_input(texts["labels"]["phone"], key="phone")
    linkedin = cols[2].text_input(texts["labels"]["linkedin"], key="linkedin")
    github = cols[3].text_input(texts["labels"]["github"], key="github")

# Özet
with st.expander(texts["sections"]["summary"], expanded=True):
    st.session_state.summary = st.text_area(
        texts["labels"]["summary_title"],
        value=st.session_state.get("summary", ""),
        height=140,
        placeholder=texts["placeholders"].get("summary", "..."),
        help=texts["labels"]["summary_help"]
    )

# ────────────────────────────────────────────────
# multi_entry_section ve diğer expander'lar aynı kalıyor
# Sadece title parametreleri texts üzerinden geliyor
# ────────────────────────────────────────────────

# İş Deneyimi
with st.expander(texts["sections"]["experience"], expanded=False):
    multi_entry_section("experiences", texts["sections"]["experience"], texts["placeholders"])

# Eğitim
with st.expander(texts["sections"]["education"]):
    multi_entry_section("educations", texts["sections"]["education"], texts["placeholders"])

# Projeler
with st.expander(texts["sections"]["projects"]):
    multi_entry_section("projects", texts["sections"]["projects"], texts["placeholders"])

# Sertifikalar
with st.expander(texts["sections"]["certificates"]):
    # ... aynı kod (sadece metinler texts üzerinden çekilebilir)
    # örneğin:
    new_cert = col1.text_input(texts["labels"]["cert_name"], key="new_cert_name")
    # st.button(texts["labels"]["add_cert"], key="add_cert")

# Yetenekler & Diller
with st.expander(texts["sections"]["skills"] + " & " + texts["sections"]["languages"]):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(texts["labels"]["skills_title"])
        skill_input = st.text_input(texts["labels"]["skills_placeholder"], key="skill_inp")
        if st.button(texts["labels"]["add_skill"], key="add_skill"):
            # aynı mantık
    with col2:
        st.markdown(texts["labels"]["languages_title"])
        lang_input = st.text_input(texts["labels"]["lang_placeholder"], key="lang_inp")
        if st.button(texts["labels"]["add_lang"], key="add_lang"):
            # aynı mantık

# PDF üretim kısmı da aynı kalıyor
# Sadece section_title içindeki metinleri dile göre değiştirmek istersen:
# pdf.section_title("PROFESSIONAL SUMMARY" if st.session_state.lang == "English" else "PROFESYONEL ÖZET")

# Buton ve mesajlar
if st.button(texts["buttons"]["generate"], type="primary", use_container_width=True):
    if not st.session_state.name.strip() or not email.strip():
        st.error(texts["errors"]["required"])
    else:
        # pdf üretimi aynı...
        st.success(texts["success"])
        st.balloons()
