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
    page_title="Ultimate Professional CV Builder 2025",
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
# DİL DESTEĞİ (daha fazla dil eklenebilir)
# ────────────────────────────────────────────────
LANGUAGES = {
    "Türkçe": {
        "app_title": "🚀 Ultimate Profesyonel CV Oluşturucu 2025",
        "sidebar": {
            "language": "Dil Seçimi",
            "theme": "Tema Rengi",
            "photo": "Profil Fotoğrafı Ekle",
            "template": "Şablon Seçimi"
        },
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
            "level": "Seviye (A1–C2 / Başlangıç–Anadil)"
        },
        "buttons": {
            "add": "Ekle",
            "remove": "Sil",
            "generate": "📄 PDF Oluştur & İndir",
            "preview": "Önizleme Gör"
        },
        "tooltips": {
            "bullet": "Her maddeyi yeni satıra yazın. Otomatik • işareti eklenecek.",
            "required": "Bu alan zorunludur."
        }
    },
    # İngilizce çeviri (kısmen – tam çevirmek isterseniz deepL veya benzeri kullanabilirsiniz)
    "English": {
        "app_title": "🚀 Ultimate Professional CV Builder 2025",
        # ... aynı mantıkla İngilizce karşılıklarını ekleyin
        # Aşağıda sadece Türkçe kullandım, İngilizce'yi siz tamamlayabilirsiniz
    }
}

# Varsayılan olarak Türkçe başlıyoruz
if "lang" not in st.session_state:
    st.session_state.lang = "Türkçe"

texts = LANGUAGES["Türkçe"] # İngilizce desteği tamamlanırsa burayı dinamik yapabilirsiniz

# ────────────────────────────────────────────────
# SESSION STATE YÖNETİMİ
# ────────────────────────────────────────────────
keys = [
    "name", "title", "photo", "summary",
    "experiences", "educations", "certificates", "projects",
    "publications", "volunteering", "awards", "references",
    "skills", "languages", "additional"
]

for k in keys:
    if k not in st.session_state:
        if "experiences" in k or "educations" in k or "projects" in k or "certificates" in k:
            st.session_state[k] = []
        elif "skills" in k or "languages" in k:
            st.session_state[k] = {}
        else:
            st.session_state[k] = ""

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
with st.sidebar:
    st.title("Ayarlar")
    selected_lang = st.radio("Dil", ["Türkçe", "English"], index=0)
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

    st.session_state.theme_color = st.color_picker("Ana Tema Rengi", "#2b6cb0")

    uploaded_photo = st.file_uploader("Profil Fotoğrafı (isteğe bağlı)", type=["jpg","jpeg","png"])
    if uploaded_photo:
        st.session_state.photo = uploaded_photo.read()
        st.image(st.session_state.photo, width=180, caption="Önizleme")

    st.info("En iyi sonuç için fotoğrafı 1:1 oranında (kare) yükleyin.")

# ────────────────────────────────────────────────
# ANA EKRAN – FORMLAR
# ────────────────────────────────────────────────
st.title(texts["app_title"])
st.caption("2025 standartlarına uygun, ATS dostu, modern CV oluşturucu")

# ── Kişisel Bilgiler ───────────────────────────────
with st.expander(texts["sections"]["personal"], expanded=True):
    col1, col2 = st.columns([3,2])
    st.session_state.name = col1.text_input("Ad Soyad **", value=st.session_state.name, placeholder=texts["placeholders"]["name"])
    st.session_state.title = col2.text_input("Unvan / Hedef Pozisyon", value=st.session_state.title, placeholder=texts["placeholders"]["title"])

# ── İletişim ───────────────────────────────────────
with st.expander(texts["sections"]["contact"], expanded=True):
    cols = st.columns([2,2,2,1])
    email = cols[0].text_input("E-posta **", key="email")
    phone = cols[1].text_input("Telefon", key="phone")
    linkedin = cols[2].text_input("LinkedIn URL", key="linkedin")
    github = cols[3].text_input("GitHub", key="github")

# ── Profesyonel Özet ──────────────────────────────
with st.expander(texts["sections"]["summary"], expanded=True):
    st.session_state.summary = st.text_area(
        "Kariyer Özeti (4–8 cümle önerilir)",
        value=st.session_state.summary,
        height=140,
        placeholder=texts["placeholders"]["summary"],
        help="Başarılarınızı sayısal verilerle destekleyin (örn: satışları %38 artırdım)"
    )

# ── Çoklu Giriş Yardımcı Fonksiyonu ───────────────
def multi_entry_section(section_key, title, placeholders, max_entries=6):
    st.subheader(title)
    container = st.container()

    if len(st.session_state[section_key]) < max_entries:
        if container.button(f"+ {texts['buttons']['add']} {title.lower()}", key=f"add_{section_key}"):
            st.session_state[section_key].append({
                "company": "", "position": "", "period": "", "location": "", "desc": ""
            })
            st.rerun()

    for i, entry in enumerate(st.session_state[section_key]):
        with st.expander(f"{entry.get('position','???')} — {entry.get('company','???')}", expanded=(i==0)):
            c1, c2 = st.columns(2)
            entry["position"] = c1.text_input("Pozisyon / Rol", value=entry["position"], key=f"{section_key}_{i}_pos")
            entry["company"] = c2.text_input("Kurum / Şirket", value=entry["company"], key=f"{section_key}_{i}_comp")

            c1, c2, c3 = st.columns([2,2,1.5])
            entry["period"] = c1.text_input("Tarih Aralığı", value=entry["period"], key=f"{section_key}_{i}_per", placeholder="Oca 2021 – Haz 2024 ya da 2022 – Günümüz")
            entry["location"] = c2.text_input("Konum", value=entry["location"], key=f"{section_key}_{i}_loc")
            
            if container.button(texts["buttons"]["remove"], key=f"del_{section_key}_{i}"):
                st.session_state[section_key].pop(i)
                st.rerun()

            entry["desc"] = st.text_area(
                "Açıklama / Başarılar (her satıra bir madde)",
                value=entry["desc"],
                height=140,
                key=f"{section_key}_{i}_desc",
                help=texts["tooltips"]["bullet"]
            )

# İş Deneyimi
with st.expander(texts["sections"]["experience"], expanded=False):
    multi_entry_section("experiences", texts["sections"]["experience"], texts["placeholders"])

# Eğitim
with st.expander(texts["sections"]["education"]):
    multi_entry_section("educations", texts["sections"]["education"], texts["placeholders"])

# Projeler
with st.expander(texts["sections"]["projects"]):
    multi_entry_section("projects", texts["sections"]["projects"], texts["placeholders"])

# Sertifikalar (daha basit yapı)
with st.expander(texts["sections"]["certificates"]):
    if "certificates" not in st.session_state:
        st.session_state.certificates = []
    
    col1, col2 = st.columns([3,1])
    new_cert = col1.text_input("Sertifika Adı / Veren Kurum", key="new_cert_name")
    new_date = col2.date_input("Tarih", value=datetime.now().date(), key="new_cert_date")
    
    if st.button("+ Sertifika Ekle", key="add_cert"):
        if new_cert.strip():
            st.session_state.certificates.append(f"{new_cert} — {new_date.strftime('%b %Y')}")
            st.rerun()

    for i, cert in enumerate(st.session_state.certificates):
        col1, col2 = st.columns([5,1])
        col1.write(f"• {cert}")
        if col2.button("×", key=f"del_cert_{i}", help="Sil"):
            st.session_state.certificates.pop(i)
            st.rerun()

# Yetenekler & Diller (tag-style)
with st.expander(texts["sections"]["skills"] + " & " + texts["sections"]["languages"]):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Yetenekler**")
        skill_input = st.text_input("Yetenek ekle (örn: Python – Uzman)", key="skill_inp")
        if st.button("+ Yetenek", key="add_skill"):
            if skill_input.strip():
                parts = [p.strip() for p in skill_input.split("–")]
                name = parts[0]
                level = parts[1] if len(parts)>1 else ""
                st.session_state.skills[name] = level
                st.rerun()

        for sk, lvl in list(st.session_state.skills.items()):
            col_a, col_b = st.columns([4,1])
            col_a.write(f"• {sk}" + (f" — {lvl}" if lvl else ""))
            if col_b.button("×", key=f"del_sk_{sk}"):
                del st.session_state.skills[sk]
                st.rerun()

    with col2:
        st.markdown("**Diller**")
        lang_input = st.text_input("Dil ekle (örn: İngilizce – C1)", key="lang_inp")
        if st.button("+ Dil", key="add_lang"):
            if lang_input.strip():
                parts = [p.strip() for p in lang_input.split("–")]
                name = parts[0]
                level = parts[1] if len(parts)>1 else ""
                st.session_state.languages[name] = level
                st.rerun()

        for lg, lvl in list(st.session_state.languages.items()):
            col_a, col_b = st.columns([4,1])
            col_a.write(f"• {lg}" + (f" — {lvl}" if lvl else ""))
            if col_b.button("×", key=f"del_lg_{lg}"):
                del st.session_state.languages[lg]
                st.rerun()

# Diğer bölümler (kısaca – aynı mantıkla genişletebilirsiniz)
with st.expander(texts["sections"]["awards"] + " / " + texts["sections"]["publications"] + " / " + texts["sections"]["volunteer"]):
    st.info("Bu bölümleri aynı multi_entry_section mantığıyla genişletebilirsiniz.")

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
        if email: parts.append(email)
        if phone: parts.append(phone)
        if linkedin: parts.append(linkedin.replace("https://",""))
        if github: parts.append(github.replace("https://github.com/","GitHub: @"))
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
    if not st.session_state.name.strip() or not email.strip():
        st.error("Ad Soyad ve E-posta alanları zorunludur.")
    else:
        pdf = ModernPDF(theme_color=tuple(int(st.session_state.theme_color.lstrip('#')[i:i+2], 16) for i in (0,2,4)))

        pdf.add_page()
        pdf.contact_line()

        pdf.set_y(48)

        # Özet
        if st.session_state.summary.strip():
            pdf.section_title("PROFESYONEL ÖZET")
            pdf.multi_cell(0, 7, st.session_state.summary.strip())
            pdf.ln(8)

        # İş Deneyimi
        if st.session_state.experiences:
            pdf.section_title("İŞ DENEYİMİ")
            for exp in st.session_state.experiences:
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 7, f"{exp['position']} — {exp['company']}", ln=1)
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(0, 6, f"{exp['period']} • {exp['location']}", ln=1)
                pdf.add_bullet_list(exp["desc"])
                pdf.ln(4)

        # Eğitim
        if st.session_state.educations:
            pdf.section_title("EĞİTİM")
            for edu in st.session_state.educations:
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 7, f"{edu['position']} — {edu['company']}", ln=1)
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(0, 6, f"{edu['period']} • {edu['location']}", ln=1)
                pdf.add_bullet_list(edu["desc"])
                pdf.ln(2)

        # Yetenekler
        if st.session_state.skills:
            pdf.section_title("YETENEKLER")
            skills_text = ", ".join([f"{k} ({v})" if v else k for k,v in st.session_state.skills.items()])
            pdf.multi_cell(0, 7, skills_text)
            pdf.ln(4)

        # Diller
        if st.session_state.languages:
            pdf.section_title("DİLLER")
            langs_text = ", ".join([f"{k} – {v}" if v else k for k,v in st.session_state.languages.items()])
            pdf.multi_cell(0, 7, langs_text)
            pdf.ln(4)

        # Sertifikalar
        if st.session_state.certificates:
            pdf.section_title("SERTİFİKALAR")
            pdf.add_bullet_list("\n".join(st.session_state.certificates))

        pdf_bytes = pdf.output(dest='S').encode('latin-1', errors='replace')

        st.download_button(
            label="📥 CV'yi PDF olarak İndir",
            data=pdf_bytes,
            file_name=f"{st.session_state.name.replace(' ','_')}_CV_2025.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.success("CV başarıyla oluşturuldu! 🎉")
        st.balloons()

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption
