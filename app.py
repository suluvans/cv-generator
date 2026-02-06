import streamlit as st
from fpdf import FPDF
import base64

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Pro CV Builder", page_icon="📄", layout="wide")

# --- CUSTOM CSS (Görsel İyileştirme) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- DİL SÖZLÜĞÜ ---
languages = {
    "Türkçe": {
        "title": "🚀 Profesyonel CV Oluşturucu",
        "personal": "👤 Kişisel Bilgiler",
        "contact": "📞 İletişim",
        "edu": "🎓 Eğitim Bilgileri",
        "exp": "💼 İş Deneyimi",
        "skills": "🛠️ Yetenekler & Diller",
        "summary": "📝 Profil Özeti",
        "btn": "CV'yi PDF Olarak Hazırla",
        "placeholders": ["Ad Soyad", "Unvan (Örn: Veri Analisti)", "Özet bilginizi buraya yazın..."]
    },
    "English": {
        "title": "🚀 Professional CV Builder",
        "personal": "👤 Personal Info",
        "contact": "📞 Contact",
        "edu": "🎓 Education",
        "exp": "💼 Experience",
        "skills": "🛠️ Skills & Languages",
        "summary": "📝 Profile Summary",
        "btn": "Generate CV PDF",
        "placeholders": ["Full Name", "Title (e.g. Software Engineer)", "Write your summary here..."]
    }
}

# --- SİDEBAR & DİL SEÇİMİ ---
lang_choice = st.sidebar.radio("Dil / Language", ["Türkçe", "English"])
texts = languages[lang_choice]

# --- VERİ TOPLAMA ---
st.title(texts["title"])

with st.expander(texts["personal"], expanded=True):
    col1, col2 = st.columns(2)
    name = col1.text_input(texts["placeholders"][0])
    title = col2.text_input(texts["placeholders"][1])
    
    c1, c2, c3 = st.columns(3)
    email = c1.text_input("E-posta")
    phone = c2.text_input("Telefon")
    linkedin = c3.text_input("LinkedIn (Link)")

with st.container():
    summary = st.text_area(texts["summary"], placeholder=texts["placeholders"][2])
    
    col_edu, col_exp = st.columns(2)
    with col_edu:
        edu = st.text_area(texts["edu"], height=200, help="Her birini yeni satıra yazın")
    with col_exp:
        exp = st.text_area(texts["exp"], height=200, help="Her birini yeni satıra yazın")
    
    skills = st.text_area(texts["skills"], placeholder="Python, SQL, İngilizce (C1)...")

# --- PDF GENERATOR SINIFI ---
class PDF(FPDF):
    def header(self):
        # Header kısmı boş bırakılabilir veya logo eklenebilir
        pass

    def add_cv_header(self, name, title, email, phone, linkedin):
        self.set_fill_color(40, 54, 85) # Lacivert Tema
        self.rect(0, 0, 210, 50, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 24)
        self.cell(0, 10, name.upper(), ln=True, align="C")
        self.set_font("Arial", "I", 14)
        self.cell(0, 10, title, ln=True, align="C")
        
        self.set_font("Arial", "", 10)
        contact_info = f"{email} | {phone} | {linkedin}"
        self.cell(0, 10, contact_info, ln=True, align="C")
        self.ln(15)

    def add_section(self, title, content):
        self.set_text_color(40, 54, 85)
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title.upper(), ln=True)
        self.set_draw_color(40, 54, 85)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 7, content)
        self.ln(5)

def create_pdf():
    # 'Arial' standart PDF fontudur. 
    # Not: Daha kompleks fontlar (Roboto vb.) için .ttf dosyası yüklemek gerekir.
    pdf = PDF()
    pdf.add_page()
    
    # Header
    pdf.add_cv_header(name, title, email, phone, linkedin)
    
    # Body
    if summary: pdf.add_section(texts["summary"], summary)
    if edu: pdf.add_section(texts["edu"], edu)
    if exp: pdf.add_section(texts["exp"], exp)
    if skills: pdf.add_section(texts["skills"], skills)
    
    # Latin-1 replace hatayı önler ama Unicode font yüklemek en iyisidir
    return pdf.output(dest="S").encode("latin-1", errors="replace")

# --- ÇIKTI VE İNDİRME ---
st.markdown("---")
if st.button(texts["btn"]):
    if not name or not email:
        st.error("Lütfen en azından Ad ve E-posta alanlarını doldurun!")
    else:
        try:
            pdf_data = create_pdf()
            st.balloons()
            
            # PDF Önizleme ve İndirme
            st.success("✅ CV Başarıyla Oluşturuldu!")
            st.download_button(
                label="📥 " + ("Download PDF" if lang_choice == "English" else "PDF Olarak İndir"),
                data=pdf_data,
                file_name=f"{name.replace(' ', '_')}_CV.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")



