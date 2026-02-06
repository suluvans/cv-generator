import streamlit as st
from fpdf import FPDF
import io
from datetime import datetime

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
    hr { border-color: #cbd5e0; margin: 2rem 0; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# TAM DİL DESTEĞİ
# ────────────────────────────────────────────────
LANGUAGES = {
    "Türkçe": {
        "app_title": "🚀 Ultimate Profesyonel CV Oluşturucu",
        "caption": "ATS dostu, modern CV oluşturucu",
        "personal": "Kişisel Bilgiler",
        "contact": "İletişim Bilgileri",
        "summary": "Profesyonel Özet / Kariyer Hedefi",
        "experience": "İş Deneyimi",
        "education": "Eğitim",
        "certificates": "Sertifikalar & Belgeler",
        "skills": "Yetenekler",
        "languages": "Diller",
        "projects": "Projeler",
        "awards_publications_volunteer": "Ödüller / Yayınlar / Gönüllü Deneyim",
        "placeholders": {
            "name": "Ad Soyad",
            "title": "Mevcut / Hedef Unvan (örn: Senior Veri Bilimci)",
            "summary": "Kendinizi 4–8 cümlede profesyonel olarak tanıtın...",
            "company": "Şirket / Organizasyon",
            "position": "Pozisyon / Unvan",
            "period": "Tarih aralığı (örn: Oca 2022 – Günümüz)",
            "location": "Şehir, Ülke",
            "description": "Başarılarınızı ve sorumluluklarınızı madde madde yazın...",
            "cert_name": "Sertifika Adı / Veren Kurum",
            "skill_example": "Yetenek ekle (örn: Python – Uzman)",
            "lang_example": "Dil ekle (örn: İngilizce – C1)"
        },
        "buttons": {
            "add": "Ekle",
            "remove": "Sil",
            "generate": "📄 PDF Oluştur & İndir",
            "add_cert": "+ Sertifika Ekle",
            "add_skill": "+ Yetenek",
            "add_lang": "+ Dil"
        },
        "help": {
            "summary": "Başarılarınızı sayısal verilerle destekleyin (örn: satışları %38 artırdım)",
            "bullet": "Her maddeyi yeni satıra yazın. Otomatik • işareti eklenecek.",
            "photo": "En iyi sonuç için fotoğrafı 1:1 oranında (kare) yükleyin."
        },
        "required": "Ad Soyad ve E-posta zorunludur.",
        "success": "CV başarıyla oluşturuldu! 🎉",
        "download_label": "📥 CV'yi PDF olarak İndir"
    },
    "English": {
        "app_title": "🚀 Ultimate Professional CV Builder",
        "caption": "ATS-friendly, modern CV creator",
        "personal": "Personal Information",
        "contact": "Contact Information",
        "summary": "Professional Summary / Career Objective",
        "experience": "Work Experience",
        "education": "Education",
        "certificates": "Certificates & Credentials",
        "skills": "Skills",
        "languages": "Languages",
        "projects": "Projects",
        "awards_publications_volunteer": "Awards / Publications / Volunteer Experience",
        "placeholders": {
            "name": "Full Name",
            "title": "Current / Target Title (e.g. Senior Data Scientist)",
            "summary": "Introduce yourself professionally in 4–8 sentences...",
            "company": "Company / Organization",
            "position": "Position / Role",
            "period": "Date range (e.g. Jan 2022 – Present)",
            "location": "City, Country",
            "description": "List your achievements and responsibilities as bullets...",
            "cert_name": "Certificate Name / Issuing Organization",
            "skill_example": "Add skill (e.g. Python – Expert)",
            "lang_example": "Add language (e.g. English – C1)"
        },
        "buttons": {
            "add": "Add",
            "remove": "Remove",
            "generate": "📄 Generate & Download PDF",
            "add_cert": "+ Add Certificate",
            "add_skill": "+ Add Skill",
            "add_lang": "+ Add Language"
        },
        "help": {
            "summary": "Support your achievements with numbers (e.g. increased sales by 38%)",
            "bullet": "Write each item on a new line. Bullet • will be added automatically.",
            "photo": "For best results, upload a square (1:1) photo."
        },
        "required": "Full Name and Email are required.",
        "success": "CV generated successfully! 🎉",
        "download_label": "📥 Download PDF"
    }
}

# ────────────────────────────────────────────────
# DİL SEÇİMİ & AKTİF DİL ATAMA
# ────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "Türkçe"

with st.sidebar:
    st.title("Settings" if st.session_state.lang == "English" else "Ayarlar")
    selected_lang = st.radio(
        "Language / Dil",
        ["Türkçe", "English"],
        index=0 if st.session_state.lang == "Türkçe" else 1
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

texts = LANGUAGES[st.session_state.lang]

# Tema rengi (her dilde aynı kalabilir)
st.session_state.theme_color = st.sidebar.color_picker(
    "Theme Color / Tema Rengi",
    "#2b6cb0"
)

# Fotoğraf yükleme
uploaded_photo = st.sidebar.file_uploader(
    texts["placeholders"].get("photo", "Upload Profile Photo (optional)"),
    type=["jpg", "jpeg", "png"]
)
if uploaded_photo:
    st.session_state.photo = uploaded_photo.read()
    st.sidebar.image(st.session_state.photo, width=180, caption="Preview / Önizleme")

st.sidebar.info(texts["help"]["photo"])

# ────────────────────────────────────────────────
# ANA İÇERİK
# ────────────────────────────────────────────────
st.title(texts["app_title"])
st.caption(texts["caption"])

# Kişisel Bilgiler
with st.expander(texts["personal"], expanded=True):
    col1, col2 = st.columns([3,2])
    name = col1.text_input(
        "Full Name / Ad Soyad **",
        value=st.session_state.get("name", ""),
        placeholder=texts["placeholders"]["name"],
        key="name_input"
    )
    title = col2.text_input(
        "Title / Unvan",
        value=st.session_state.get("title", ""),
        placeholder=texts["placeholders"]["title"],
        key="title_input"
    )
    st.session_state.name = name
    st.session_state.title = title

# İletişim
with st.expander(texts["contact"], expanded=True):
    cols = st.columns([2,2,2,1])
    email = cols[0].text_input("Email / E-posta **", key="email")
    phone = cols[1].text_input("Phone / Telefon", key="phone")
    linkedin = cols[2].text_input("LinkedIn URL", key="linkedin")
    github = cols[3].text_input("GitHub", key="github")

# Özet
with st.expander(texts["summary"], expanded=True):
    st.session_state.summary = st.text_area(
        texts["summary"],
        value=st.session_state.get("summary", ""),
        height=140,
        placeholder=texts["placeholders"]["summary"],
        help=texts["help"]["summary"]
    )

# ── multi_entry_section fonksiyonu aynı kalabilir (önceki kodunuzdaki gibi) ──
# ... (iş deneyimi, eğitim, projeler, sertifikalar, yetenekler & diller bölümleri aynı mantıkla devam eder)

# PDF oluşturma butonu
if st.button(texts["buttons"]["generate"], type="primary", use_container_width=True):
    if not st.session_state.name.strip() or not email.strip():
        st.error(texts["required"])
    else:
        # PDF sınıfı ve üretim kısmı önceki kodunuzdaki gibi kalabilir
        # Sadece başlık, section title'lar vs. texts sözlüğünden çekilecek şekilde güncellenmeli
        # Örnek:
        # pdf.section_title("PROFESSIONAL SUMMARY" if lang == "English" else "PROFESYONEL ÖZET")

        st.success(texts["success"])
        st.balloons()
        # download_button label → texts["download_label"]

st.caption
