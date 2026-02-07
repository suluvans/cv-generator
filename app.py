import streamlit as st
from fpdf import FPDF
from PIL import Image
import io
import base64

# ----------------------------
# Sayfa Yapılandırması ve Dil Verileri
# ----------------------------
st.set_page_config(
    page_title="Profesyonel CV Oluşturucu",
    page_icon="📄",
    layout="wide"
)

# Dil desteği için metin sözlükleri
TEXTS = {
    "tr": {
        "title": "Profesyonel CV Oluşturucu",
        "personal_info": "Kişisel Bilgiler",
        "photo_optional": "Fotoğraf (Opsiyonel)",
        "photo_click": "Fotoğraf yüklemek için tıklayın",
        "first_name": "Ad",
        "last_name": "Soyad",
        "profession": "Meslek/Unvan",
        "country": "Ülke",
        "city": "Şehir",
        "email": "E-posta",
        "phone": "Telefon",
        "summary": "Profesyonel Özet",
        "experience": "İş Deneyimi",
        "add_experience": "➕ İş Deneyimi Ekle",
        "education": "Eğitim",
        "add_education": "➕ Eğitim Ekle",
        "skills": "Yetenekler",
        "skills_placeholder": "Örn: JavaScript, Python, Proje Yönetimi",
        "certificates": "Sertifikalar",
        "add_certificate": "➕ Sertifika Ekle",
        "preview": "CV Önizleme",
        "generate_pdf": "📄 PDF Oluştur ve İndir",
        "reset": "🔄 Formu Sıfırla",
        "company": "Şirket",
        "position": "Pozisyon",
        "start_date": "Başlangıç Tarihi (YYYY-AA)",
        "end_date": "Bitiş Tarihi (YYYY-AA)",
        "description": "Açıklama",
        "school": "Okul/Üniversite",
        "degree": "Derece",
        "field": "Alan",
        "cert_name": "Sertifika Adı",
        "issuer": "Kurum",
        "date": "Tarih (YYYY-AA)",
        "present": "Günümüz"
    },
    "en": {
        "title": "Professional CV Builder",
        "personal_info": "Personal Information",
        "photo_optional": "Photo (Optional)",
        "photo_click": "Click to upload photo",
        "first_name": "First Name",
        "last_name": "Last Name",
        "profession": "Profession/Title",
        "country": "Country",
        "city": "City",
        "email": "Email",
        "phone": "Phone",
        "summary": "Professional Summary",
        "experience": "Work Experience",
        "add_experience": "➕ Add Work Experience",
        "education": "Education",
        "add_education": "➕ Add Education",
        "skills": "Skills",
        "skills_placeholder": "e.g., JavaScript, Python, Project Management",
        "certificates": "Certificates",
        "add_certificate": "➕ Add Certificate",
        "preview": "CV Preview",
        "generate_pdf": "📄 Generate & Download PDF",
        "reset": "🔄 Reset Form",
        "company": "Company",
        "position": "Position",
        "start_date": "Start Date (YYYY-MM)",
        "end_date": "End Date (YYYY-MM)",
        "description": "Description",
        "school": "School/University",
        "degree": "Degree",
        "field": "Field",
        "cert_name": "Certificate Name",
        "issuer": "Issuer",
        "date": "Date (YYYY-MM)",
        "present": "Present"
    }
}

# ----------------------------
# Session State (Oturum Durumu) Yönetimi
# ----------------------------
def init_session_state():
    """Session state (oturum durumu) değişkenlerini başlatır."""
    if 'language' not in st.session_state:
        st.session_state.language = 'tr'
    if 'photo' not in st.session_state:
        st.session_state.photo = None
    if 'experiences' not in st.session_state:
        st.session_state.experiences = [{'company': '', 'position': '', 'start': '', 'end': '', 'desc': ''}]
    if 'education' not in st.session_state:
        st.session_state.education = [{'school': '', 'degree': '', 'field': '', 'start': '', 'end': ''}]
    if 'certificates' not in st.session_state:
        st.session_state.certificates = [{'name': '', 'issuer': '', 'date': ''}]

# ----------------------------
# PDF Oluşturma Fonksiyonu
# ----------------------------
def create_pdf(data, lang):
    """CV verilerini kullanarak PDF oluşturur ve byte olarak döndürür."""
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    
    # Ana sayfa
    pdf.add_page()
    pdf.set_font("helvetica", style='B', size=20)
    
    # Üst Bilgi - İsim ve Unvan
    pdf.set_text_color(37, 99, 235) # Mavi renk
    pdf.cell(0, 15, f"{data['first_name']} {data['last_name']}", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font("helvetica", size=14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, data['profession'], new_x="LMARGIN", new_y="NEXT", align='C')
    
    # İletişim Bilgileri
    pdf.set_font("helvetica", size=10)
    contact_line = f"{data['city']}, {data['country']} | {data['email']} | {data['phone']}"
    pdf.cell(0, 6, contact_line, new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    
    # Profesyonel Özet
    pdf.set_font("helvetica", style='B', size=12)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 8, TEXTS[lang]['summary'], new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, data['summary'])
    pdf.ln(8)
    
    # İş Deneyimi
    if any(exp['company'] or exp['position'] for exp in data['experiences']):
        pdf.set_font("helvetica", style='B', size=12)
        pdf.set_text_color(37, 99, 235)
        pdf.cell(0, 8, TEXTS[lang]['experience'], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", size=11)
        pdf.set_text_color(0, 0, 0)
        
        for exp in data['experiences']:
            if exp['company'] or exp['position']:
                pdf.set_font("helvetica", style='B', size=11)
                pdf.cell(0, 6, exp['position'], new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", style='I', size=10)
                pdf.cell(0, 5, exp['company'], new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", size=10)
                date_str = f"{exp['start']} - {exp['end'] if exp['end'] else TEXTS[lang]['present']}"
                pdf.cell(0, 5, date_str, new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", size=10)
                pdf.multi_cell(0, 5, exp['desc'])
                pdf.ln(3)
    
    # Eğitim
    if any(edu['school'] or edu['degree'] for edu in data['education']):
        pdf.set_font("helvetica", style='B', size=12)
        pdf.set_text_color(37, 99, 235)
        pdf.cell(0, 8, TEXTS[lang]['education'], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", size=11)
        pdf.set_text_color(0, 0, 0)
        
        for edu in data['education']:
            if edu['school'] or edu['degree']:
                pdf.set_font("helvetica", style='B', size=11)
                pdf.cell(0, 6, f"{edu['degree']} - {edu['field']}", new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", style='I', size=10)
                pdf.cell(0, 5, edu['school'], new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", size=10)
                date_str = f"{edu['start']} - {edu['end'] if edu['end'] else TEXTS[lang]['present']}"
                pdf.cell(0, 5, date_str, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(3)
    
    # Yetenekler
    if data['skills']:
        pdf.set_font("helvetica", style='B', size=12)
        pdf.set_text_color(37, 99, 235)
        pdf.cell(0, 8, TEXTS[lang]['skills'], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", size=10)
        pdf.set_text_color(0, 0, 0)
        skills_text = ", ".join(data['skills'])
        pdf.multi_cell(0, 6, skills_text)
        pdf.ln(5)
    
    # Sertifikalar
    if any(cert['name'] or cert['issuer'] for cert in data['certificates']):
        pdf.set_font("helvetica", style='B', size=12)
        pdf.set_text_color(37, 99, 235)
        pdf.cell(0, 8, TEXTS[lang]['certificates'], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", size=11)
        pdf.set_text_color(0, 0, 0)
        
        for cert in data['certificates']:
            if cert['name'] or cert['issuer']:
                pdf.set_font("helvetica", style='B', size=11)
                pdf.cell(0, 6, cert['name'], new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", size=10)
                pdf.cell(0, 5, f"{cert['issuer']} | {cert['date']}", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(3)
    
    return pdf.output(dest='S').encode('latin-1')

# ----------------------------
# Dinamik Alan Yönetimi
# ----------------------------
def add_experience_field():
    """Yeni bir iş deneyimi alanı ekler."""
    st.session_state.experiences.append({'company': '', 'position': '', 'start': '', 'end': '', 'desc': ''})

def remove_experience_field(index):
    """Belirtilen indeksteki iş deneyimi alanını kaldırır."""
    if len(st.session_state.experiences) > 1:
        st.session_state.experiences.pop(index)

def add_education_field():
    """Yeni bir eğitim alanı ekler."""
    st.session_state.education.append({'school': '', 'degree': '', 'field': '', 'start': '', 'end': ''})

def remove_education_field(index):
    """Belirtilen indeksteki eğitim alanını kaldırır."""
    if len(st.session_state.education) > 1:
        st.session_state.education.pop(index)

def add_certificate_field():
    """Yeni bir sertifika alanı ekler."""
    st.session_state.certificates.append({'name': '', 'issuer': '', 'date': ''})

def remove_certificate_field(index):
    """Belirtilen indeksteki sertifika alanını kaldırır."""
    if len(st.session_state.certificates) > 1:
        st.session_state.certificates.pop(index)

# ----------------------------
# Ana Uygulama Arayüzü
# ----------------------------
def main():
    # Session state'i başlat
    init_session_state()
    
    # Dil seçimi
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(TEXTS[st.session_state.language]['title'])
    with col2:
        lang = st.radio("Dil / Language", ["TR", "EN"], horizontal=True, label_visibility="collapsed")
        st.session_state.language = lang.lower()
    
    current_lang = st.session_state.language
    
    # Ana içerik - iki sütun
    col_left, col_right = st.columns([1, 1], gap="large")
    
    # ----------------------------
    # SOL SÜTUN: Form Girişleri
    # ----------------------------
    with col_left:
        with st.expander(TEXTS[current_lang]['personal_info'], expanded=True):
            # Fotoğraf yükleme
            st.write(TEXTS[current_lang]['photo_optional'])
            uploaded_photo = st.file_uploader(
                TEXTS[current_lang]['photo_click'],
                type=['jpg', 'jpeg', 'png'],
                label_visibility="collapsed",
                key="photo_uploader"
            )
            if uploaded_photo:
                st.session_state.photo = Image.open(uploaded_photo)
                st.image(st.session_state.photo, width=150)
            
            # Kişisel bilgiler
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input(TEXTS[current_lang]['first_name'], key="first_name")
                country = st.text_input(TEXTS[current_lang]['country'], key="country")
                email = st.text_input(TEXTS[current_lang]['email'], key="email")
            with col2:
                last_name = st.text_input(TEXTS[current_lang]['last_name'], key="last_name")
                city = st.text_input(TEXTS[current_lang]['city'], key="city")
                phone = st.text_input(TEXTS[current_lang]['phone'], key="phone")
            
            profession = st.text_input(TEXTS[current_lang]['profession'], key="profession")
            summary = st.text_area(TEXTS[current_lang]['summary'], height=100, key="summary")
        
        # İş Deneyimi
        with st.expander(TEXTS[current_lang]['experience'], expanded=True):
            for i, exp in enumerate(st.session_state.experiences):
                cols = st.columns([4, 1])
                with cols[0]:
                    st.write(f"**{TEXTS[current_lang]['experience']} {i+1}**")
                with cols[1]:
                    if st.button("🗑️", key=f"del_exp_{i}"):
                        remove_experience_field(i)
                        st.rerun()
                
                st.session_state.experiences[i]['company'] = st.text_input(
                    TEXTS[current_lang]['company'],
                    value=exp['company'],
                    key=f"exp_company_{i}"
                )
                st.session_state.experiences[i]['position'] = st.text_input(
                    TEXTS[current_lang]['position'],
                    value=exp['position'],
                    key=f"exp_position_{i}"
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.experiences[i]['start'] = st.text_input(
                        TEXTS[current_lang]['start_date'],
                        value=exp['start'],
                        key=f"exp_start_{i}"
                    )
                with col2:
                    st.session_state.experiences[i]['end'] = st.text_input(
                        TEXTS[current_lang]['end_date'],
                        value=exp['end'],
                        key=f"exp_end_{i}"
                    )
                st.session_state.experiences[i]['desc'] = st.text_area(
                    TEXTS[current_lang]['description'],
                    value=exp['desc'],
                    height=80,
                    key=f"exp_desc_{i}"
                )
                st.divider()
            
            if st.button(TEXTS[current_lang]['add_experience']):
                add_experience_field()
                st.rerun()
        
        # Eğitim
        with st.expander(TEXTS[current_lang]['education'], expanded=True):
            for i, edu in enumerate(st.session_state.education):
                cols = st.columns([4, 1])
                with cols[0]:
                    st.write(f"**{TEXTS[current_lang]['education']} {i+1}**")
                with cols[1]:
                    if st.button("🗑️", key=f"del_edu_{i}"):
                        remove_education_field(i)
                        st.rerun()
                
                st.session_state.education[i]['school'] = st.text_input(
                    TEXTS[current_lang]['school'],
                    value=edu['school'],
                    key=f"edu_school_{i}"
                )
                st.session_state.education[i]['degree'] = st.text_input(
                    TEXTS[current_lang]['degree'],
                    value=edu['degree'],
                    key=f"edu_degree_{i}"
                )
                st.session_state.education[i]['field'] = st.text_input(
                    TEXTS[current_lang]['field'],
                    value=edu['field'],
                    key=f"edu_field_{i}"
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.education[i]['start'] = st.text_input(
                        TEXTS[current_lang]['start_date'],
                        value=edu['start'],
                        key=f"edu_start_{i}"
                    )
                with col2:
                    st.session_state.education[i]['end'] = st.text_input(
                        TEXTS[current_lang]['end_date'],
                        value=edu['end'],
                        key=f"edu_end_{i}"
                    )
                st.divider()
            
            if st.button(TEXTS[current_lang]['add_education']):
                add_education_field()
                st.rerun()
        
        # Yetenekler
        with st.expander(TEXTS[current_lang]['skills'], expanded=True):
            skills_input = st.text_input(
                TEXTS[current_lang]['skills'],
                placeholder=TEXTS[current_lang]['skills_placeholder'],
                key="skills_input",
                label_visibility="collapsed"
            )
            skills_list = [s.strip() for s in skills_input.split(',') if s.strip()] if skills_input else []
        
        # Sertifikalar
        with st.expander(TEXTS[current_lang]['certificates'], expanded=True):
            for i, cert in enumerate(st.session_state.certificates):
                cols = st.columns([4, 1])
                with cols[0]:
                    st.write(f"**{TEXTS[current_lang]['certificates']} {i+1}**")
                with cols[1]:
                    if st.button("🗑️", key=f"del_cert_{i}"):
                        remove_certificate_field(i)
                        st.rerun()
                
                st.session_state.certificates[i]['name'] = st.text_input(
                    TEXTS[current_lang]['cert_name'],
                    value=cert['name'],
                    key=f"cert_name_{i}"
                )
                st.session_state.certificates[i]['issuer'] = st.text_input(
                    TEXTS[current_lang]['issuer'],
                    value=cert['issuer'],
                    key=f"cert_issuer_{i}"
                )
                st.session_state.certificates[i]['date'] = st.text_input(
                    TEXTS[current_lang]['date'],
                    value=cert['date'],
                    key=f"cert_date_{i}"
                )
                st.divider()
            
            if st.button(TEXTS[current_lang]['add_certificate']):
                add_certificate_field()
                st.rerun()
    
    # ----------------------------
    # SAĞ SÜTUN: CV Önizleme ve PDF İndirme
    # ----------------------------
    with col_right:
        st.subheader(TEXTS[current_lang]['preview'])
        
        # Önizleme kartı
        with st.container():
            st.markdown(f"""
            <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h1 style='color: #2563eb; margin-bottom: 5px;'>{first_name or "Ad"} {last_name or "Soyad"}</h1>
                <h3 style='color: #666; margin-top: 0; margin-bottom: 20px;'>{profession or "Meslek/Unvan"}</h3>
                
                <p style='color: #555;'><strong>{city or "Şehir"}, {country or "Ülke"} | {email or "E-posta"} | {phone or "Telefon"}</strong></p>
                
                <hr style='border-color: #2563eb;'>
                
                <h4 style='color: #2563eb;'>Profesyonel Özet</h4>
                <p>{summary or "Özet bilgisi burada görünecek..."}</p>
                
                <h4 style='color: #2563eb;'>İş Deneyimi</h4>
                {"".join([f"<p><strong>{exp['position'] or 'Pozisyon'}</strong><br><em>{exp['company'] or 'Şirket'}</em><br>{exp['start'] or 'Başlangıç'} - {exp['end'] or 'Bitiş'}<br>{exp['desc'] or 'Açıklama'}</p>" for exp in st.session_state.experiences if exp['company'] or exp['position']]) or "<p>İş deneyimi bilgisi eklenmemiş</p>"}
                
                <h4 style='color: #2563eb;'>Eğitim</h4>
                {"".join([f"<p><strong>{edu['degree'] or 'Derece'} - {edu['field'] or 'Alan'}</strong><br><em>{edu['school'] or 'Okul'}</em><br>{edu['start'] or 'Başlangıç'} - {edu['end'] or 'Bitiş'}</p>" for edu in st.session_state.education if edu['school'] or edu['degree']]) or "<p>Eğitim bilgisi eklenmemiş</p>"}
                
                <h4 style='color: #2563eb;'>Yetenekler</h4>
                <p>{', '.join(skills_list) or "Yetenek bilgisi eklenmemiş"}</p>
                
                <h4 style='color: #2563eb;'>Sertifikalar</h4>
                {"".join([f"<p><strong>{cert['name'] or 'Sertifika Adı'}</strong><br>{cert['issuer'] or 'Kurum'} | {cert['date'] or 'Tarih'}</p>" for cert in st.session_state.certificates if cert['name'] or cert['issuer']]) or "<p>Sertifika bilgisi eklenmemiş</p>"}
            </div>
            """, unsafe_allow_html=True)
        
        # PDF İndirme butonu
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
       
