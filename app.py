import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io
import base64

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
# DİL DESTEĞİ (TAM TÜRKÇE VE İNGİLİZCE)
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
        "caption": "ATS dostu, modern CV oluşturucu",
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
            "publications": "Yayınlar & Makaleler",
            "volunteer": "Gönüllü Deneyim & Sosyal Sorumluluk",
            "awards": "Ödüller & Başarılar",
            "references": "Referanslar",
            "additional": "Ek Bilgiler / İlgi Alanları"
        },
        "placeholders": {
            "name": "Ad Soyad",
            "title": "Mevcut / Hedef Unvan (örn: Senior Veri Bilimci)",
            "summary": "Kendinizi 4–8 cümlede profesyonel olarak tanıtın...",
            "company": "Şirket / Organizasyon",
            "position": "Pozisyon / Unvan",
            "period": "Tarih aralığı (örn: Oca 2022 – Günümüz)",
            "location": "Şehir, Ülke",
            "description": "Başarılarınızı ve sorumluluklarınızı madde madde yazın...",
            "project_name": "Proje Adı",
            "tech_stack": "Kullanılan teknolojiler (örn: React, Node.js, AWS)",
            "degree": "Derece / Bölüm (örn: Bilgisayar Mühendisliği Lisans)",
            "school": "Okul / Üniversite",
            "gpa": "Not Ortalaması (isteğe bağlı)",
            "skill": "Yetenek (örn: Python – İleri Seviye)",
            "lang": "Dil (örn: İngilizce)",
            "level": "Seviye (A1–C2 / Başlangıç–Anadil)",
            "cert_name": "Sertifika Adı / Veren Kurum",
            "skill_inp": "Yetenek ekle (örn: Python – Uzman)",
            "lang_inp": "Dil ekle (örn: İngilizce – C1)",
            "awards_publications_volunteer": "Bu bölümleri aynı multi_entry_section mantığıyla genişletebilirsiniz."
        },
        "buttons": {
            "add": "Ekle",
            "remove": "Sil",
            "generate": "📄 PDF Oluştur & İndir",
            "preview": "Önizleme Gör",
            "add_cert": "+ Sertifika Ekle",
            "add_skill": "+ Yetenek",
            "add_lang": "+ Dil"
        },
        "tooltips": {
            "bullet": "Her maddeyi yeni satıra yazın. Otomatik • işareti eklenecek.",
            "required": "Bu alan zorunludur."
        },
        "help": {
            "summary": "Başarılarınızı sayısal verilerle destekleyin (örn: satışları %38 artırdım)"
        },
        "errors": {
            "required": "Ad Soyad ve E-posta alanları zorunludur."
        },
        "success": "CV başarıyla oluşturuldu! 🎉",
        "download_label": "📥 CV'yi PDF olarak İndir"
    },
    "English": {
        "app_title": "🚀 Ultimate Professional CV Builder",
        "sidebar_title": "Settings",
        "language_label": "Language",
        "theme_label": "Main Theme Color",
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
            "publications": "Publications & Articles",
            "volunteer": "Volunteer Experience & Social Responsibility",
            "awards": "Awards & Achievements",
            "references": "References",
            "additional": "Additional Information / Interests"
        },
        "placeholders": {
            "name": "Full Name",
            "title": "Current / Target Title (e.g. Senior Data Scientist)",
            "summary": "Introduce yourself professionally in 4–8 sentences...",
            "company": "Company / Organization",
            "position": "Position / Title",
            "period": "Date range (e.g. Jan 2022 – Present)",
            "location": "City, Country",
            "description": "List your achievements and responsibilities in bullets...",
            "project_name": "Project Name",
            "tech_stack": "Technologies used (e.g. React, Node.js, AWS)",
            "degree": "Degree / Major (e.g. Computer Engineering Bachelor's)",
            "school": "School / University",
            "gpa": "GPA (optional)",
            "skill": "Skill (e.g. Python – Advanced Level)",
            "lang": "Language (e.g. English)",
            "level": "Level (A1–C2 / Beginner–Native)",
            "cert_name": "Certificate Name / Issuing Organization",
            "skill_inp": "Add skill (e.g. Python – Expert)",
            "lang_inp": "Add language (e.g. English – C1)",
            "awards_publications_volunteer": "Expand these sections with the same multi_entry_section logic."
        },
        "buttons": {
            "add": "Add",
            "remove": "Remove",
            "generate": "📄 Generate & Download PDF",
            "preview": "View Preview",
            "add_cert": "+ Add Certificate",
            "add_skill": "+ Add Skill",
            "add_lang": "+ Add Language"
        },
        "tooltips": {
            "bullet": "Write each item on a new line. Bullet • will be added automatically.",
            "required": "This field is required."
        },
        "help": {
            "summary": "Support your achievements with quantitative data (e.g. increased sales by 38%)"
        },
        "errors": {
            "required": "Full Name and Email fields are required."
        },
        "success": "CV generated successfully! 🎉",
        "download_label": "📥 Download PDF"
    }
}

# ────────────────────────────────────────────────
# SESSION STATE YÖNETİMİ
# ────────────────────────────────────────────────
keys = [
    "lang", "name", "title", "photo", "summary",
    "experiences", "educations", "certificates", "projects",
    "publications", "volunteering", "awards", "references",
    "skills", "languages", "additional", "theme_color", "email", "phone", "linkedin", "github"
]

for k in keys:
    if k not in st.session_state:
        if k == "lang":
            st.session_state[k] = "Türkçe"
        elif k == "theme_color":
            st.session_state[k] = "#2b6cb0"
        elif "experiences" in k or "educations" in k or "projects" in k or "certificates" in k or "publications" in k or "volunteering" in k or "awards" in k or "references" in k:
            st.session_state[k] = []
        elif "skills" in k or "languages" in k:
            st.session_state[k] = {}
        else:
            st.session_state[k] = ""

# ────────────────────────────────────────────────
# SIDEBAR
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

st.session_state.theme_color = st.color_picker(
    texts["theme_label"],
    st.session_state.theme_color
)

uploaded_photo = st.file_uploader(
    texts["photo_label"],
    type=["jpg", "jpeg", "png"]
)
if uploaded_photo:
    st.session_state.photo = uploaded_photo.read()
    st.image(st.session_state.photo, width=180, caption=texts["photo_caption"])

st.info(texts["photo_info"])

# ────────────────────────────────────────────────
# ANA EKRAN – FORMLAR
# ────────────────────────────────────────────────
st.title(texts["app_title"])
st.caption(texts["caption"])

# ── Kişisel Bilgiler ───────────────────────────────
with st.expander(texts["sections"]["personal"], expanded=True):
    col1, col2 = st.columns([3,2])
    st.session_state.name = col1.text_input(
        "Full Name / Ad Soyad **" if st.session_state.lang == "English" else "Ad Soyad **",
        value=st.session_state.name,
        placeholder=texts["placeholders"]["name"]
    )
    st.session_state.title = col2.text_input(
        "Title / Unvan" if st.session_state.lang == "English" else "Unvan / Hedef Pozisyon",
        value=st.session_state.title,
        placeholder=texts["placeholders"]["title"]
    )

# ── İletişim ───────────────────────────────────────
with st.expander(texts["sections"]["contact"], expanded=True):
    cols = st.columns([2,2,2,1])
    st.session_state.email = cols[0].text_input(
        "Email / E-posta **",
        key="email",
        value=st.session_state.get("email", "")
    )
    st.session_state.phone = cols[1].text_input(
        "Phone / Telefon",
        key="phone",
        value=st.session_state.get("phone", "")
    )
    st.session_state.linkedin = cols[2].text_input(
        "LinkedIn URL",
        key="linkedin",
        value=st.session_state.get("linkedin", "")
    )
    st.session_state.github = cols[3].text_input(
        "GitHub",
        key="github",
        value=st.session_state.get("github", "")
    )

# ── Profesyonel Özet ──────────────────────────────
with st.expander(texts["sections"]["summary"], expanded=True):
    st.session_state.summary = st.text_area(
        "Career Summary / Kariyer Özeti (4–8 sentences / cümle önerilir)" if st.session_state.lang == "English" else "Kariyer Özeti (4–8 cümle önerilir)",
        value=st.session_state.summary,
        height=140,
        placeholder=texts["placeholders"]["summary"],
        help=texts["help"]["summary"]
    )

# ── Çoklu Giriş Yardımcı Fonksiyonu ───────────────
def multi_entry_section(section_key, title, max_entries=6):
    st.subheader(title)
    container = st.container()

    if len(st.session_state[section_key]) < max_entries:
        add_label = f"+ {texts['buttons']['add']} {title.lower()}"
        if container.button(add_label, key=f"add_{section_key}"):
            st.session_state[section_key].append({
                "position": "", "company": "", "period": "", "location": "", "desc": ""
            })
            st.rerun()

    for i, entry in enumerate(st.session_state[section_key]):
        with st.expander(f"{entry.get('position','???')} — {entry.get('company','???')}", expanded=(i==0)):
            c1, c2 = st.columns(2)
            entry["position"] = c1.text_input(
                "Position / Pozisyon" if st.session_state.lang == "English" else "Pozisyon / Rol",
                value=entry["position"],
                key=f"{section_key}_{i}_pos",
                placeholder=texts["placeholders"]["position"]
            )
            entry["company"] = c2.text_input(
                "Company / Kurum" if st.session_state.lang == "English" else "Kurum / Şirket",
                value=entry["company"],
                key=f"{section_key}_{i}_comp",
                placeholder=texts["placeholders"]["company"]
            )

            c1, c2 = st.columns(2)
            entry["period"] = c1.text_input(
                "Period / Tarih Aralığı" if st.session_state.lang == "English" else "Tarih Aralığı",
                value=entry["period"],
                key=f"{section_key}_{i}_per",
                placeholder=texts["placeholders"]["period"]
            )
            entry["location"] = c2.text_input(
                "Location / Konum" if st.session_state.lang == "English" else "Konum",
                value=entry["location"],
                key=f"{section_key}_{i}_loc",
                placeholder=texts["placeholders"]["location"]
            )

            entry["desc"] = st.text_area(
                "Description / Açıklama (bullets / madde madde)" if st.session_state.lang == "English" else "Açıklama / Başarılar (her satıra bir madde)",
                value=entry["desc"],
                height=140,
                key=f"{section_key}_{i}_desc",
                help=texts["tooltips"]["bullet"]
            )

            if st.button(texts["buttons"]["remove"], key=f"del_{section_key}_{i}"):
                st.session_state[section_key].pop(i)
                st.rerun()

# İş Deneyimi
with st.expander(texts["sections"]["experience"], expanded=False):
    multi_entry_section("experiences", texts["sections"]["experience"])

# Eğitim
with st.expander(texts["sections"]["education"]):
    multi_entry_section("educations", texts["sections"]["education"])

# Projeler
with st.expander(texts["sections"]["projects"]):
    multi_entry_section("projects", texts["sections"]["projects"])

# Sertifikalar
with st.expander(texts["sections"]["certificates"]):
    col1, col2 = st.columns([3,1])
    new_cert = col1.text_input(
        "Certificate Name / Sertifika Adı" if st.session_state.lang == "English" else "Sertifika Adı / Veren Kurum",
        key="new_cert_name",
        placeholder=texts["placeholders"]["cert_name"]
    )
    new_date = col2.date_input(
        "Date / Tarih" if st.session_state.lang == "English" else "Tarih",
        value=datetime.now()
    )

    if st.button(texts["buttons"]["add_cert"], key="add_cert"):
        if new_cert.strip():
            st.session_state.certificates.append(f"{new_cert} — {new_date.strftime('%b %Y')}")
            st.rerun()

    for i, cert in enumerate(st.session_state.certificates):
        col1, col2 = st.columns([5,1])
        col1.write(f"• {cert}")
        if col2.button("×", key=f"del_cert_{i}", help="Remove / Sil"):
            st.session_state.certificates.pop(i)
            st.rerun()

# Yetenekler & Diller
with st.expander(texts["sections"]["skills"] + " & " + texts["sections"]["languages"]):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Skills / Yetenekler**")
        skill_input = st.text_input(
            texts["placeholders"]["skill_inp"],
            key="skill_inp"
        )
        if st.button(texts["buttons"]["add_skill"], key="add_skill"):
            if skill_input.strip():
                parts = [p.strip() for p in skill_input.split("–")]
                name = parts[0]
                level = parts[1] if len(parts) > 1 else ""
                st.session_state.skills[name] = level
                st.rerun()

        for sk, lvl in list(st.session_state.skills.items()):
            col_a, col_b = st.columns([4,1])
            col_a.write(f"• {sk}" + (f" — {lvl}" if lvl else ""))
            if col_b.button("×", key=f"del_sk_{sk}"):
                del st.session_state.skills[sk]
                st.rerun()

    with col2:
        st.markdown("**Languages / Diller**")
        lang_input = st.text_input(
            texts["placeholders"]["lang_inp"],
            key="lang_inp"
        )
        if st.button(texts["buttons"]["add_lang"], key="add_lang"):
            if lang_input.strip():
                parts = [p.strip() for p in lang_input.split("–")]
                name = parts[0]
                level = parts[1] if len(parts) > 1 else ""
                st.session_state.languages[name] = level
                st.rerun()

        for lg, lvl in list(st.session_state.languages.items()):
            col_a, col_b = st.columns([4,1])
            col_a.write(f"• {lg}" + (f" — {lvl}" if lvl else ""))
            if col_b.button("×", key=f"del_lg_{lg}"):
                del st.session_state.languages[lg]
                st.rerun()

# Diğer Bölümler
with st.expander(texts["sections"]["awards"] + " / " + texts["sections"]["publications"] + " / " + texts["sections"]["volunteer"]):
    st.info(texts["placeholders"]["awards_publications_volunteer"])

# ────────────────────────────────────────────────
# PDF ÜRETİM SINIFI
# ────────────────────────────────────────────────
class ModernPDF(FPDF):
    def __init__(self, theme_color=(43,108,176)):
        super().__init__()
        self.theme_r, self.theme_g, self.theme_b = theme_color

    def header(self):
        self.set_fill_color(self.theme_r, self.theme_g, self.theme_b)
        self.rect(0, 0, 210, 38, style="F")
        self.set_y(8)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(255,255,255)
        self.cell(0, 10, st.session_state.name.upper(), align="C", ln=1)
        
        self.set_font("Helvetica", "I", 13)
        self.cell(0, 8, st.session_state.title, align="C", ln=1)

    def contact_line(self):
        self.set_y(32)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(220,220,220)
        parts = []
        if st.session_state.email: parts.append(st.session_state.email)
        if st.session_state.phone: parts.append(st.session_state.phone)
        if st.session_state.linkedin: parts.append(st.session_state.linkedin.replace("https://",""))
        if st.session_state.github: parts.append(st.session_state.github.replace("https://github.com/","GitHub: @"))
        self.cell(0, 6, " • ".join(parts), align="C")

    def section_title(self, title):
        self.set_text_color(self.theme_r, self.theme_g, self.theme_b)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, title.upper(), ln=1)
        self.set_draw_color(self.theme_r, self.theme_g, self.theme_b)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def add_bullet_list(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40,40,40)
        for line in text.strip().split("\n"):
            if line.strip():
                self.cell(5, 6, "•", align="L")
                self.multi_cell(0, 6, line.strip(), align="L")
        self.ln(2)

# ────────────────────────────────────────────────
# PDF OLUŞTURMA & İNDİRME
# ────────────────────────────────────────────────
if st.button(texts["buttons"]["generate"], type="primary", use_container_width=True):
    if not st.session_state.name.strip() or not st.session_state.email.strip():
        st.error(texts["errors"]["required"])
    else:
        theme_color = tuple(int(st.session_state.theme_color.lstrip('#')[i:i+2], 16) for 
