import streamlit as st
from fpdf import FPDF
docx dosyasından Document dosyasını içe aktar
from io import BytesIO

# Sayfa Genişliği ve Tema
st.set_page_config(page_title="Profesyonel CV Ustası", page_icon="💼", layout="wide")

# --- TASARIM (CSS) ---
st.markdown("""
<style>
.main { background-color: #f5f7f9; }
.stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
.stTextInput>div>div>input { border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- DİL SÖZLÜĞÜ ---
lang = st.sidebar.selectbox("🌍 Dil / Language", ["Türkçe", "English"])
t = {
Türkçe: {
"header": "🏆 Profesyonel CV Oluşturucu",
"kişisel": "👤 Kişisel Bilgiler",
"edu": "🎓 Eğitim Bilgileri",
"work": "💼 İşni",
"beceriler": "🛠️Yetenekler & Sertifikalar",
"özet": "📝 Kariyer Özeti",
"isim": "Ad Soyad", "iş": "Meslek", "telefon": "Telefon", "sosyal": "LinkedIn/Github",
"oluştur": "🚀 CV'yi Hazırla",
"success": "✅ CV Başarıyla Hazırlandı!",
"download_pdf": "📥 PDF Olarak İndir",
"download_word": "📥 Word (DOCX) Olarak İndir"
},
"İngilizce": {
"başlık": "🏆 Profesyonel CV Oluşturucu",
"kişisel": "👤 Kişisel Bilgiler",
"edu": "🎓 Eğitim",
"iş": "💼 İş Deneyimi",
"Beceriler": "🛠️ Beceriler ve Sertifikalar",
"Özet": "📝 Kariyer Özeti",
"İsim": "Tam Adı", "İş": "İş Unvanı", "Telefon": "Telefon", "Sosyal Medya": "LinkedIn/Github",
"oluştur": "🚀 CV Oluştur",
"Başarı": "✅ Özgeçmiş Başarıyla Oluşturuldu!",
"download_pdf": "📥 PDF olarak indir",
"download_word": "📥 Word olarak indir"
}
}[lang]

st.title(t["header"])

# --- GİRİŞ PANELİ ---
st.container() ile:
sütun1, sütun2 = st.sütunlar([1, 2])
col1 ile:
st.altbaşlık(t["kişisel"])
isim = st.text_input(t["isim"])
iş = st.text_input(t["iş"])
e-posta = st.text_input("E-posta / Email")
telefon = st.text_input(t["telefon"])
sosyal = st.text_input(t["sosyal"])
col2 ile:
st.altbaşlık(t["özet"])
özet = st.text_area(t["özet"], yükseklik=100)
st.altbaşlık(t["edu"])
edu = st.text_area(t["edu"], placeholder="Okul Adı - Bölüm - Yıl", height=100)

st.markdown("---")
sütun3, sütun4 = st.sütunlar(2)
col3 ile:
st.alt başlık(t["iş"])
iş = st.text_area(t["iş"], placeholder="Şirket - Pozisyon - Süre - Görevler", yükseklik=150)
col4 ile:
st.altbaşlık(t["beceriler"])
beceriler = st.text_area(t["beceriler"], placeholder="Python, SQL, Proje Yönetimi vb.", height=150)

# --- DOSYA OLUŞTURMA FONKSİYONLARI ---

def make_pdf():
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 24)
pdf.cell(0, 15, name, ln=True, align="C")
pdf.set_font("Arial", "I", 14)
pdf.cell(0, 10, job, ln=True, align="C")
pdf.set_font("Arial", "", 10)
pdf.cell(0, 5, f"{email} | {phone} | {social}", ln=True, align="C")
pdf.ln(10)
başlık için, [(t["summary"], özet), (t["edu"], eğitim), (t["work"], iş), (t["skills"], beceriler)] içindeki içerik:
pdf.set_font("Arial", "B", 12)
pdf.hücre(0, 10, başlık, ln=True)
pdf.set_font("Arial", "", 11)
pdf.multi_cell(0, 7, content)
pdf.ln(5)
pdf.output(dest="S").encode("latin-1", errors="replace") döndür

def make_word():
belge = Belge()
doc.add_heading(name, 0)
doc.add_paragraph(f"{iş}\n{e-posta} | {telefon} | {sosyal medya}")
başlık için, [(t["summary"], özet), (t["edu"], eğitim), (t["work"], iş), (t["skills"], beceriler)] içindeki içerik:
doc.add_heading(title, level=1)
doc.add_paragraph(content)
bio = BytesIO()
belge.kaydet(biyografi)
bio.getvalue() değerini döndür

# --- AKSİYON BUTONU ---
eğer st.button(t["generate"]):
İsim ve e-posta adresi varsa:
st.balonlar()
st.başarı(t["başarı"])
sütun_pdf, sütun_kelime = st.sütunlar(2)
col_pdf ile:
st.download_button(t["download_pdf"], data=make_pdf(), file_name="cv.pdf", mime="application/pdf")
col_word ile:
st.download_button(t["download_word"], data=make_word(), file_name="cv.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
başka:
st.warning("Lütfen zorunlu alanları doldurun!")

