import streamlit as st
from fpdf import FPDF

# Sayfa Ayarları
st.set_page_config(page_title="Multi-Language CV Maker", page_icon="🌍")

# --- DİL SÖZLÜĞÜ ---
languages = {
    "Türkçe": {
        "title": "🏆 Profesyonel CV Sihirbazı",
        "personal": "👤 Kişisel Bilgiler",
        "name": "Ad Soyad",
        "job": "Meslek",
        "edu": "📖 Eğitim",
        "exp": "💼 Deneyim",
        "skills": "🛠️ Yetenekler",
        "summary": "📝 Özet",
        "button": "🚀 CV'yi Oluştur",
        "success": "Tebrikler! CV'niz hazır.",
        "download": "📥 PDF İndir"
    },
    "English": {
        "title": "🏆 Professional CV Builder",
        "personal": "👤 Personal Information",
        "name": "Full Name",
        "job": "Job Title",
        "edu": "📖 Education",
        "exp": "💼 Experience",
        "skills": "🛠️ Skills",
        "summary": "📝 Summary",
        "button": "🚀 Generate CV",
        "success": "Congrats! Your CV is ready.",
        "download": "📥 Download PDF"
    }
}

# --- DİL SEÇİMİ ---
lang_choice = st.sidebar.selectbox("Dil / Language", ["Türkçe", "English"])
texts = languages[lang_choice]

st.title(texts["title"])
st.markdown("---")

# --- GİRİŞ ALANLARI ---
st.sidebar.header(texts["personal"])
name = st.sidebar.text_input(texts["name"])
job = st.sidebar.text_input(texts["job"])
email = st.sidebar.text_input("E-posta / Email")
phone = st.sidebar.text_input("Tel")

col1, col2 = st.columns(2)
with col1:
    edu = st.text_area(texts["edu"])
with col2:
    exp = st.text_area(texts["exp"])

skills = st.text_input(texts["skills"])
summary = st.text_area(texts["summary"])

# --- PDF OLUŞTURMA ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, name.upper(), ln=True, align="C")
    pdf.set_font("Arial", "I", 14)
    pdf.cell(0, 10, job, ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    sections = {
        texts["summary"]: summary,
        texts["edu"]: edu,
        texts["exp"]: exp,
        texts["skills"]: skills
    }
    
    for title, content in sections.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, title.upper(), ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, content)
        pdf.ln(5)
    
    return pdf.output(dest="S").encode("latin-1", errors="replace")

# --- ÇALIŞTIR ---
if st.button(texts["button"]):
    if name and email:
        pdf_bytes = create_pdf()
        st.balloons()
        st.success(texts["success"])
        st.download_button(texts["download"], data=pdf_bytes, file_name="CV.pdf")

