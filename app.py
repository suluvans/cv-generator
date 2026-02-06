import streamlit as st
from fpdf import FPDF
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
    hr { border-color: #cbd5e0; margin: 2rem 0; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# DİL DESTEĞİ
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
            "awards_publications_volunteer": "Ödüller / Yayınlar / Gönüllü Deneyim",
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
            "awards_publications_volunteer": "Awards / Publications / Volunteer Experience",
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

texts = LANGUAGES[st.session_state.lang]

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
with st.sidebar:
    st.title(texts["sidebar_title"])
    
    selected_lang = st.radio(
        texts["language_label"],
        ["Türkçe", "English"],
        index=0 if st.session_state.lang == "Türkçe" else 1,
        key="language_selector"
    )
    
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

    st.session_state.theme_color = st.color_picker(
        texts["theme_label"],
        "#2b6cb0"
    )

    uploaded_photo = st.file_uploader(
        texts["photo_label"],
        type=["jpg", "jpeg", "png"],
        key="photo_uploader"
    )
    if uploaded_photo:
        st.session_state.photo = uploaded_photo.read()
        st.image(st.session_state.photo, width=180, caption=texts["photo_caption"])

    st.info(texts["photo_info"])

# ────────────────────────────────────────────────
# ANA EKRAN
# ────────────────────────────────────────────────
st.title(texts["app_title"])
st.caption(texts["caption"])

# ── Kişisel Bilgiler ───────────────────────────────
with st.expander(texts["sections"]["personal"], expanded=True):
    col1, col2 = st.columns([3,2])
    st.session_state.name = col1.text_input(
        texts["labels"]["name"],
        value=st.session_state.get("name", ""),
        key=f"name_input_{st.session_state.lang}"
    )
    st.session_state.title = col2.text_input(
        texts["labels"]["title"],
        value=st.session_state.get("title", ""),
        key=f"title_input_{st.session_state.lang}"
    )

# ── İletişim ───────────────────────────────────────
with st.expander(texts["sections"]["contact"], expanded=True):
    cols = st.columns([2,2,2,1])
    st.session_state.email = cols[0].text_input(
        texts["labels"]["email"],
        value=st.session_state.get("email", ""),
        key=f"email_input_{st.session_state.lang}"
    )
    st.session_state.phone = cols[1].text_input(
        texts["labels"]["phone"],
        value=st.session_state.get("phone", ""),
        key=f"phone_input_{st.session_state.lang}"
    )
    st.session_state.linkedin = cols[2].text_input(
        texts["labels"]["linkedin"],
        value=st.session_state.get("linkedin", ""),
        key=f"linkedin_input_{st.session_state.lang}"
    )
    st.session_state.github = cols[3].text_input(
        texts["labels"]["github"],
        value=st.session_state.get("github", ""),
        key=f"github_input_{st.session_state.lang}"
    )

# ── Profesyonel Özet ──────────────────────────────
with st.expander(texts["sections"]["summary"], expanded=True):
    st.session_state.summary = st.text_area(
        texts["labels"]["summary_title"],
        value=st.session_state.get("summary", ""),
        height=140,
        placeholder=texts["placeholders"].get("summary", "..."),
        help=texts["labels"]["summary_help"],
        key=f"summary_area_{st.session_state.lang}"
    )

# ── Çoklu Giriş Yardımcı Fonksiyonu ───────────────
def multi_entry_section(section_key, title, max_entries=6):
    st.subheader(title)
    container = st.container()

    if len(st.session_state.get(section_key, [])) < max_entries:
        if container.button(f"+ {texts['buttons']['add']} {title.lower()}", key=f"add_{section_key}_{st.session_state.lang}"):
            if section_key not in st.session_state:
                st.session_state[section_key] = []
            st.session_state[section_key].append({
                "position": "", "company": "", "period": "", "location": "", "desc": ""
            })
            st.rerun()

    current_list = st.session_state.get(section_key, [])
    for i, entry in enumerate(current_list):
        with st.expander(f"{entry.get('position','???')} — {entry.get('company','???')}", expanded=(i==0)):
            c1, c2 = st.columns(2)
            entry["position"] = c1.text_input(
                texts["labels"]["position"],
                value=entry["position"],
                key=f"{section_key}_{i}_pos_{st.session_state.lang}"
            )
            entry["company"] = c2.text_input(
                texts["labels"]["company"],
                value=entry["company"],
                key=f"{section_key}_{i}_comp_{st.session_state.lang}"
            )

            c1, c2 = st.columns(2)
            entry["period"] = c1.text_input(
                texts["labels"]["period"],
                value=entry["period"],
                key=f"{section_key}_{i}_per_{st.session_state.lang}"
            )
            entry["location"] = c2.text_input(
                texts["labels"]["location"],
                value=entry["location"],
                key=f"{section_key}_{i}_loc_{st.session_state.lang}"
            )

            entry["desc"] = st.text_area(
                texts["labels"]["description"],
                value=entry["desc"],
                height=140,
                key=f"{section_key}_{i}_desc_{st.session_state.lang}",
                help=texts["tooltips"]["bullet"]
            )

            if st.button(texts["buttons"]["remove"], key=f"del_{section_key}_{i}_{st.session_state.lang}"):
                current_list.pop(i)
                st.session_state[section_key] = current_list
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
        texts["labels"]["cert_name"],
        key=f"new_cert_name_{st.session_state.lang}"
    )
    new_date = col2.date_input(
        texts["labels"]["cert_date"],
        value=datetime.now(),
        key=f"new_cert_date_{st.session_state.lang}"
    )

    if st.button(texts["buttons"]["add_cert"], key=f"add_cert_btn_{st.session_state.lang}"):
        if new_cert.strip():
            if "certificates" not in st.session_state:
                st.session_state.certificates = []
            st.session_state.certificates.append(f"{new_cert} — {new_date.strftime('%b %Y')}")
            st.rerun()

    for i, cert in enumerate(st.session_state.get("certificates", [])):
        col1, col2 = st.columns([5,1])
        col1.write(f"• {cert}")
        if col2.button("×", key=f"del_cert_{i}_{st.session_state.lang}", help="Sil"):
            st.session_state.certificates.pop(i)
            st.rerun()

# Yetenekler & Diller
with st.expander(texts["sections"]["skills"] + " & " + texts["sections"]["languages"]):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(texts["labels"]["skills_title"])
        skill_input = st.text_input(
            texts["labels"]["skills_placeholder"],
            key=f"skill_inp_{st.session_state.lang}"
        )
        if st.button(texts["buttons"]["add_skill"], key=f"add_skill_btn_{st.session_state.lang}"):
            if skill_input.strip():
                parts = [p.strip() for p in skill_input.split("–")]
                name = parts[0]
                level = parts[1] if len(parts) > 1 else ""
                if "skills" not in st.session_state:
                    st.session_state.skills = {}
                st.session_state.skills[name] = level
                st.rerun()

        for sk, lvl in list(st.session_state.get("skills", {}).items()):
            col_a, col_b = st.columns([4,1])
            col_a.write(f"• {sk}" + (f" — {lvl}" if lvl else ""))
            if col_b.button("×", key=f"del_sk_{sk}_{st.session_state.lang}"):
                del st.session_state.skills[sk]
                st.rerun()

    with col2:
        st.markdown(texts["labels"]["languages_title"])
        lang_input = st.text_input(
            texts["labels"]["lang_placeholder"],
            key=f"lang_inp_{st.session_state.lang}"
        )
        if st.button(texts["buttons"]["add_lang"], key=f"add_lang_btn_{st.session_state.lang}"):
            if lang_input.strip():
                parts = [p.strip() for p in lang_input.split("–")]
                name = parts[0]
                level = parts[1] if len(parts) > 1 else ""
                if "languages" not in st.session_state:
                    st.session_state.languages = {}
                st.session_state.languages[name] = level
                st.rerun()

        for lg, lvl in list(st.session_state.get("languages", {}).items()):
            col_a, col_b = st.columns([4,1])
            col_a.write(f"• {lg}" + (f" — {lvl}" if lvl else ""))
            if col_b.button("×", key=f"del_lg_{lg}_{st.session_state.lang}"):
                del st.session_state.languages[lg]
                st.rerun()

# PDF Üretimi
if st.button(texts["buttons"]["generate"], type="primary", use_container_width=True):
    if not st.session_state.get("name", "").strip() or not st.session_state.get("email", "").strip():
        st.error(texts["errors"]["required"])
    else:
        # Tema rengini güvenli şekilde dönüştür
        hex_color = st.session_state.theme_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            theme_color = (r, g, b)
        else:
            theme_color = (43, 108, 176) # varsayılan

        pdf = ModernPDF(theme_color=theme_color)
        pdf.add_page()
        pdf.contact_line()
        pdf.set_y(48)

        # Özet
        if st.session_state.get("summary", "").strip():
            pdf.section_title(texts["sections"]["summary"].upper())
            pdf.multi_cell(0, 7, st.session_state.summary.strip())
            pdf.ln(8)

        # İş Deneyimi
        if st.session_state.get("experiences", []):
            pdf.section_title(texts["sections"]["experience"].upper())
            for exp in st.session_state.experiences:
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 7, f"{exp['position']} — {exp['company']}", ln=1)
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(0, 6, f"{exp['period']} • {exp['location']}", ln=1)
                pdf.add_bullet_list(exp["desc"])
                pdf.ln(4)

        # Eğitim
        if st.session_state.get("educations", []):
            pdf.section_title(texts["sections"]["education"].upper())
            for edu in st.session_state.educations:
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 7, f"{edu['position']} — {edu['company']}", ln=1)
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(0, 6, f"{edu['period']} • {edu['location']}", ln=1)
                pdf.add_bullet_list(edu["desc"])
                pdf.ln(2)

        # Yetenekler
        if st.session_state.get("skills", {}):
            pdf.section_title(texts["sections"]["skills"].upper())
            skills_text = ", ".join([f"{k} ({v})" if v else k for k, v in st.session_state.skills.items()])
            pdf.multi_cell(0, 7, skills_text)
            pdf.ln(4)

        # Diller
        if st.session_state.get("languages", {}):
            pdf.section_title(texts["sections"]["languages"].upper())
            langs_text = ", ".join([f"{k} – {v}" if v else k for k, v in st.session_state.languages.items()])
            pdf.multi_cell(0, 7, langs_text)
            pdf.ln(4)

        # Sertifikalar
        if st.session_state.get("certificates", []):
            pdf.section_title(texts["sections"]["certificates"].upper())
            pdf.add_bullet_list("\n".join(st.session_state.certificates))

        pdf_bytes = pdf.output(dest='S').encode('latin-1', errors='replace')

        st.download_button(
            label=texts["buttons"]["generate"].replace("📄 ", "📥 "),
            data=pdf_bytes,
            file_name=f"{st.session_state.get('name', 'cv').replace(' ', '_')}_CV.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.success(texts["success"])
        st.balloons()

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
        self.cell(0, 10, st.session_state.get("name", "").upper(), align="C", ln=1)
        
        self.set_font("Helvetica", "I", 13)
        self.cell(0, 8, st.session_state.get("title", ""), align="C", ln=1)

    def contact_line(self):
        self.set_y(32)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(220,220,220)
        parts = []
        if st.session_state.get("email"): parts.append(st.session_state.email)
        if st.session_state.get("phone"): parts.append(st.session_state.phone)
        if st.session_state.get("linkedin"): parts.append(st.session_state.linkedin.replace("https://",""))
        if st.session_state.get("github"): parts.append(st.session_state.github.replace("https://github.com/","GitHub: @"))
        self.cell(0, 6, " • ".join(parts), align="C")

    def section_title(self, title):
        self.set_text_color(self.theme_r, self.theme_g, self.theme_b)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, title.upper(), ln=1)
        self.set_draw_color(self.theme_r, self.theme_g, self.theme_b)
        self.set_lin
