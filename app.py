import streamlit as st
from fpdf import FPDF
import io
from datetime import datetime

# ────────────────────────────────────────────────
# SAYFA AYARLARI
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="Ultimate Professional CV Builder 2026",
    page_icon="📄✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ────────────────────────────────────────────────
# STİL (temel)
# ────────────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #f8f9fc; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.2rem;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 0.6rem 0;
    }
    .stButton>button[kind="primary"] {
        background-color: #4361ee;
        color: white;
    }
    .package-card {
        padding: 1.4rem;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        margin-bottom: 1rem;
        background: white;
    }
    .package-card.selected {
        border-color: #4361ee;
        box-shadow: 0 0 0 3px rgba(67,97,238,0.2);
    }
    .price-tag {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2d3748;
    }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# PAKET / ŞABLON SEÇİMİ
# ────────────────────────────────────────────────
if "selected_package" not in st.session_state:
    st.session_state.selected_package = "Minimalist (Ücretsiz)"

st.sidebar.title("CV Paket Seçimi – 2026")

packages = {
    "Minimalist (Ücretsiz)": {
        "name": "Minimalist",
        "price": 0,
        "desc": "Temiz, sade, ATS dostu tasarım",
        "color": (50, 50, 50), # koyu gri
        "accent": (100, 100, 100),
        "header_height": 32,
        "font_style": "Helvetica",
        "premium_features": False
    },
    "Professional (4.99$)": {
        "name": "Professional",
        "price": 4.99,
        "desc": "Modern renkler, zarif header, ikon desteği",
        "color": (33, 150, 243), # mavi
        "accent": (13, 71, 161),
        "header_height": 42,
        "font_style": "Helvetica-Bold",
        "premium_features": True
    },
    "Premium (4.99$)": {
        "name": "Premium",
        "price": 4.99,
        "desc": "Lüks görünüm, gradient header, gölgeler",
        "color": (79, 70, 229), # mor-mavi
        "accent": (49, 46, 129),
        "header_height": 48,
        "font_style": "Helvetica-BoldOblique",
        "premium_features": True
    }
}

# Paket kartları (ana sayfada veya sidebar'da gösterilebilir)
st.markdown("### 2026 CV Paketleri")
cols = st.columns(3)

for i, (pkg_name, pkg) in enumerate(packages.items()):
    with cols[i]:
        is_selected = st.session_state.selected_package == pkg_name
        class_name = "package-card selected" if is_selected else "package-card"
        
        st.markdown(f"""
        <div class="{class_name}">
            <h4>{pkg['name']}</h4>
            <p>{pkg['desc']}</p>
            <div class="price-tag">
                {'Ücretsiz' if pkg['price'] == 0 else f'${pkg["price"]:.2f}'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seç", key=f"select_{pkg_name}", disabled=is_selected):
            st.session_state.selected_package = pkg_name
            st.rerun()

# Seçili paketi al
current_pkg = packages[st.session_state.selected_package]

st.info(f"Seçili paket: **{current_pkg['name']}** "
        f"{'(Ücretsiz)' if current_pkg['price'] == 0 else f'– Tek seferlik ${current_pkg['price']:.2f}'}")

if current_pkg["price"] > 0:
    st.warning("Not: Gerçek ödeme entegrasyonu henüz eklenmedi. "
               "Şu an sadece önizleme / demo amaçlı seçebilirsiniz. "
               "Daha sonra Stripe veya yerel ödeme sistemleriyle tamamlayabilirsiniz.")

# ────────────────────────────────────────────────
# PDF SINIFI – Pakete göre özelleşecek
# ────────────────────────────────────────────────
class CVPDF2026(FPDF):
    def __init__(self, package):
        super().__init__()
        self.pkg = package
        self.theme_r, self.theme_g, self.theme_b = package["color"]
        self.accent_r, self.accent_g, self.accent_b = package["accent"]

    def header(self):
        # Header yüksekliği pakete göre değişiyor
        hh = self.pkg["header_height"]
        self.set_fill_color(self.theme_r, self.theme_g, self.theme_b)
        self.rect(0, 0, 210, hh, style="F")
        
        self.set_y(6)
        self.set_font("Helvetica", "B", 22 if self.pkg["premium_features"] else 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, st.session_state.get("name", "").upper(), align="C", ln=1)
        
        self.set_font("Helvetica", "I", 14 if self.pkg["premium_features"] else 12)
        self.cell(0, 8, st.session_state.get("title", ""), align="C", ln=1)

    def contact_line(self):
        y_pos = self.pkg["header_height"] - 6 if self.pkg["premium_features"] else self.pkg["header_height"] - 4
        self.set_y(y_pos)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(240, 240, 240)
        contacts = []
        if email := st.session_state.get("email"): contacts.append(email)
        if phone := st.session_state.get("phone"): contacts.append(phone)
        if linkedin := st.session_state.get("linkedin"): contacts.append(linkedin)
        self.cell(0, 6, " • ".join(contacts), align="C")

    def section_title(self, title):
        self.set_text_color(self.theme_r, self.theme_g, self.theme_b)
        self.set_font(self.pkg["font_style"], "B", 15 if self.pkg["premium_features"] else 14)
        self.cell(0, 9, title.upper(), ln=1)
        self.set_draw_color(*self.accent_r, self.accent_g, self.accent_b)
        self.set_line_width(0.8 if self.pkg["premium_features"] else 0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    # ... (geri kalan add_bullet_list, multi_cell vs. önceki kodla aynı kalabilir)

# ────────────────────────────────────────────────
# PDF ÜRETİM (önceki kodun devamı)
# ────────────────────────────────────────────────
# (buraya önceki mesajdaki formlar, multi_entry_section, session_state yönetimi vs. aynı şekilde gelecek)

if st.button("📄 2026 CV PDF Oluştur & İndir", type="primary", use_container_width=True):
    if not st.session_state.get("name", "").strip():
        st.error("Lütfen en azından Ad Soyad alanını doldurun.")
    else:
        pdf = CVPDF2026(current_pkg)
        pdf.add_page()
        pdf.contact_line()
        pdf.set_y(current_pkg["header_height"] + 10)

        # Özet, deneyim, eğitim vs. bölümleri önceki gibi ekle...
        # (burayı önceki kodunuzdaki gibi doldurabilirsiniz)

        pdf_bytes = pdf.output(dest='S').encode('latin-1', errors='replace')

        file_name = f"{st.session_state.get('name','cv').replace(' ','_')}_2026_{current_pkg['name'].lower().replace(' ','_')}.pdf"

        st.download_button(
            label=f"İndir – {current_pkg['name']} Şablonu",
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf",
            use_container_width=True
        )
        st.success(f"{current_pkg['name']} şablonu başarıyla oluşturuldu! 🎉")
        if current_pkg["price"] > 0:
            st.info("Teşekkürler! Satın alma işleminiz demo amaçlı tamamlandı.")
