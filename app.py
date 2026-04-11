import streamlit as st
import google.generativeai as genai
import json
import PyPDF2
from PIL import Image
import datetime
import io
import docx

# ==========================================
# KONFIGURASI HALAMAN & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="VORTEX 4.0 | By Adjie Agung", page_icon="🌪️", layout="centered")

# --- CSS KHUSUS UNTUK TAMPILAN HP (MOBILE OPTIMIZED) ---
st.markdown("""
    <style>
    /* Mengurangi padding default agar muat di layar kecil */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    /* Menata font footer */
    .footer { text-align: center; color: #888; font-size: 0.85rem; margin-top: 50px; }
    /* Mempercantik tombol utama */
    .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- AMBIL API KEY DARI SECRETS ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ GEMINI_API_KEY tidak ditemukan di Secrets!")
    st.stop()

# Inisialisasi Memori
if "intelligence_data" not in st.session_state: st.session_state.intelligence_data = ""
if "project_scenario" not in st.session_state: st.session_state.project_scenario = ""
if "current_weather" not in st.session_state: st.session_state.current_weather = ""

# ==========================================
# SIDEBAR: SETTING & PENJADWALAN
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/google-earth.png", width=60)
    st.title("⚙️ Pengaturan")
    st.success("⚡ Mesin: Flash-Latest")
    
    st.divider()
    st.markdown("**🔗 Kontak Bisnis**")
    wa_num = st.text_input("No. WA Sales", "+6281230857759")
    aff_link = st.text_input("Link Shopee Affiliate", "https://shope.ee/...")
    
    st.divider()
    st.caption("Engine: VORTEX 4.0")

# Header Utama
st.title("🌪️ VORTEX 4.0")
st.caption("Heavy-Asset Domination System")

# ==========================================
# MODUL 1: RADAR (CUACA & TENDER)
# ==========================================
with st.expander("📡 1. Radar Pasar & Cuaca", expanded=True):
    lokasi = st.selectbox("Titik Pantau:", ["Samarinda, ID", "Penajam (IKN), ID", "Balikpapan, ID"])
    
    col1a, col1b = st.columns(2)
    with col1a:
        if st.button("🌦️ Tarik Cuaca", use_container_width=True):
            st.session_state.current_weather = "Hujan Ringan, Suhu 26°C, Kelembapan 95% (Medan Berlumpur)"
            st.toast("Data cuaca disuntikkan!")
    with col1b:
        if st.button("🏗️ Scan Tender", use_container_width=True):
            with st.spinner("Memindai LPSE..."):
                model_radar = genai.GenerativeModel('gemini-flash-latest')
                res = model_radar.generate_content("Info singkat tren proyek infrastruktur IKN & Kaltim bulan ini.")
                st.session_state.project_scenario = res.text
            st.toast("Radar Tender sukses!")

    if st.session_state.project_scenario or st.session_state.current_weather:
        final_scenario = st.text_area("Data Intelijen (Otomatis):", 
                                      value=f"{st.session_state.current_weather}\n\n{st.session_state.project_scenario}", 
                                      height=100)

# ==========================================
# MODUL 2: PRODUK & ANALISIS
# ==========================================
with st.expander("🎯 2. Ekstraksi Spesifikasi", expanded=False):
    col2a, col2b = st.columns(2)
    with col2a: brand = st.selectbox("Merek", ["AIMIX", "Tatsuo", "New Timehope"])
    with col2b: unit_type = st.text_input("Tipe Unit", "Self Loading Mixer + ABT60C" if brand != "New Timehope" else "HSPD 360")
    
    uploaded_file = st.file_uploader("Upload Brosur (PDF/IMG)", type=["pdf", "png", "jpg"])
    
    pdf_text = ""
    image_data = None
    if uploaded_file:
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext == 'pdf':
            for page in PyPDF2.PdfReader(uploaded_file).pages:
                ex = page.extract_text()
                if ex: pdf_text += ex
            st.toast("PDF Terbaca")
        elif ext in ['png', 'jpg']:
            image_data = Image.open(uploaded_file)
            st.toast("Gambar Terbaca")

    if st.button("🔍 Mulai Analisis Sudut Serang", use_container_width=True, type="primary"):
        model_intel = genai.GenerativeModel('gemini-flash-latest')
        prompt_intel = f"""Buat analisis marketing untuk {brand} {unit_type}. 
        Kondisi: {final_scenario if 'final_scenario' in locals() else 'Proyek sulit'}.
        Berdasarkan gambar/teks ini: {pdf_text}. 
        Format: 1. Pain Points, 2. Solusi Alat, 3. Killer Angle."""
        
        contents = [prompt_intel]
        if image_data: contents.append(image_data)
        
        with st.spinner("Menganalisis..."):
            try:
                res_intel = model_intel.generate_content(contents)
                st.session_state.intelligence_data = res_intel.text
            except Exception as e:
                st.error(e)

if st.session_state.intelligence_data:
    st.info(st.session_state.intelligence_data)

# ==========================================
# MODUL 3: FINANCIAL ROI & PROPOSAL
# ==========================================
with st.expander("💰 3. Kalkulator ROI & Proposal B2B", expanded=False):
    c_roi1, c_roi2 = st.columns(2)
    with c_roi1:
        inv = st.number_input("Harga Beli (Rp)", value=1500000000, step=10000000)
        prod = st.number_input("Target Produksi/Hari", value=100)
        harga = st.number_input("Profit/Unit (Rp)", value=150000)
    with c_roi2:
        ops = st.number_input("Biaya Ops Alat (Rp/Bln)", value=30000000)
        lama = st.number_input("Biaya Cara Lama (Rp/Bln)", value=80000000)
        hari = st.number_input("Hari Kerja/Bln", value=25)

    if st.button("🧮 Generate Eksekutif Proposal", use_container_width=True):
        profit = (prod * harga * hari) - ops
        hemat = lama - ops
        bep = inv / profit if profit > 0 else 0
        
        st.markdown(f"**BEP:** {bep:.1f} Bulan | **Hemat:** Rp{hemat:,.0f}/bln")
        
        model_fin = genai.GenerativeModel('gemini-flash-latest')
        prompt_fin = f"Buat Executive Summary elegan untuk Direktur. Alat: {brand} {unit_type}. Investasi Rp{inv:,.0f}, BEP {bep:.1f} bulan, Penghematan Rp{hemat:,.0f}/bulan. Jelaskan ini alat pencetak uang. Jangan sebutkan biaya cara lama jika tidak logis."
        
        with st.spinner("Merumuskan proposal..."):
            res_fin = model_fin.generate_content(prompt_fin)
            
            # Konversi ke DOCX
            doc = docx.Document()
            doc.add_heading('Executive Summary', 0)
            for p in res_fin.text.split('\n'):
                if p.strip(): doc.add_paragraph(p.strip())
            bio = io.BytesIO()
            doc.save(bio)
            
            st.download_button("📄 Download File Word", data=bio.getvalue(), file_name=f"Proposal_{brand}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)

# ==========================================
# MODUL 4: AI COMMENT SNIPER
# ==========================================
with st.expander("💬 4. AI Comment Sniper (Sosmed)", expanded=False):
    komen = st.text_area("Paste Komentar Prospek/Haters:")
    if st.button("🎯 Tembak Balasan", use_container_width=True):
        model_sniper = genai.GenerativeModel('gemini-flash-latest')
        prompt_sniper = f"Balas komentar ini: '{komen}' untuk produk {brand} {unit_type}. Jika haters, balas dengan fakta spek teknis. Jika hot lead, arahkan ke WA {wa_num}."
        with st.spinner("Meracik balasan..."):
            st.success(model_sniper.generate_content(prompt_sniper).text)

# ==========================================
# MODUL 5: TENDER HACKER & KILL-SWITCH
# ==========================================
with st.expander("⚔️ 5. Alat Tempur Ekstra (Tender & Kompetitor)", expanded=False):
    st.markdown("**Battlecard Kompetitor**")
    kom_brand = st.text_input("Merek Kompetitor")
    if st.button("☠️ Generate Battlecard"):
        model_kill = genai.GenerativeModel('gemini-flash-latest')
        with st.spinner("Menganalisis..."):
            st.info(model_kill.generate_content(f"Buat battlecard membandingkan {brand} {unit_type} vs {kom_brand}. Beri 2 kelemahan mereka dan cara kita menang.").text)

# ==========================================
# FOOTER (DEVELOPER SIGNATURE)
# ==========================================
st.markdown("<div class='footer'>Architected & Developed by <b>Adjie Agung</b> <br> VORTEX 4.0 - Heavy-Asset Intelligence System</div>", unsafe_allow_html=True)
