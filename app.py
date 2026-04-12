import streamlit as st
import google.generativeai as genai
import json
import PyPDF2
from PIL import Image
import datetime
import io
import docx
import os

# ==========================================
# KONFIGURASI HALAMAN & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="VORTEX 4.0 | By Adjie Agung", page_icon="🌪️", layout="centered")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .footer { text-align: center; color: #888; font-size: 0.85rem; margin-top: 50px; padding-top: 10px; border-top: 1px solid #ddd; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ GEMINI_API_KEY tidak ditemukan di Secrets!")
    st.stop()

if "intelligence_data" not in st.session_state: st.session_state.intelligence_data = ""
if "campaign_data" not in st.session_state: st.session_state.campaign_data = None
if "project_scenario" not in st.session_state: st.session_state.project_scenario = ""
if "current_weather" not in st.session_state: st.session_state.current_weather = ""

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/engineering.png", width=70)
    st.title("⚙️ Command Center")
    st.success("Model: gemini-flash-latest")
    st.info("Library: AIMIX, Tatsuo, New Timehope")
    st.divider()
    wa_num = st.text_input("WhatsApp Sales", "+6281230857759")
    aff_link = st.text_input("Shopee Affiliate", "https://shope.ee/...")
    st.divider()
    st.caption("Engine: VORTEX 4.0 | By Adjie Agung")

st.title("🌪️ VORTEX 4.0")
st.subheader("Heavy-Asset Domination System")

# ==========================================
# MODUL 1: RADAR CUACA & TENDER
# ==========================================
with st.expander("📡 Modul 1: Radar Intelijen (Cuaca & Tender)", expanded=False):
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("**⛈️ Sensor Cuaca**")
        lokasi = st.selectbox("Lokasi Radar", ["Samarinda, ID", "Penajam (IKN), ID", "Balikpapan, ID"])
        if st.button("Tarik Cuaca", use_container_width=True):
            st.session_state.current_weather = "Hujan Ringan, Suhu 24-30°C, Kelembapan 98% (Tanah sangat basah/lumpur)"
            st.toast(f"Cuaca {lokasi} Terdeteksi!")

    with col_w2:
        st.markdown("**🏗️ Radar Tender**")
        cakupan_radar = st.selectbox("Wilayah", ["Kalimantan Timur & IKN", "Seluruh Kalimantan", "Maluku & Indonesia Timur"])
        if st.button("🛰️ Scan Tender", use_container_width=True):
            with st.spinner(f"Memindai LPSE di {cakupan_radar}..."):
                model_radar = genai.GenerativeModel('gemini-flash-latest')
                res = model_radar.generate_content(f"Cari info tren proyek infrastruktur, tambang di {cakupan_radar} bulan ini.")
                st.session_state.project_scenario = res.text
            st.toast("Radar Tender Berhasil!")

    final_scenario = st.text_area("Skenario Target", value=f"Cuaca: {st.session_state.current_weather}\n\nProyek: {st.session_state.project_scenario}", height=120)

# ==========================================
# MODUL 2: EKSTRAKSI & INTELIJEN PRODUK
# ==========================================
with st.expander("🎯 Modul 2: Ekstraksi Spek & Analisis", expanded=False):
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        brand = st.selectbox("Merek Produk", ["AIMIX", "Tatsuo", "New Timehope"])
        unit_type = st.text_input("Tipe Unit", "HSPD 360" if brand == "New Timehope" else "Self Loading Mixer + ABT60C")
    with col_u2:
        uploaded_file = st.file_uploader("Upload Brosur", type=["pdf", "png", "jpg", "jpeg"])
        
    pdf_text = ""
    image_data = None
    if uploaded_file:
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext == 'pdf':
            for page in PyPDF2.PdfReader(uploaded_file).pages:
                ex = page.extract_text()
                if ex: pdf_text += ex
            st.toast("📄 PDF Dibaca!")
        elif ext in ['png', 'jpg', 'jpeg']:
            image_data = Image.open(uploaded_file)
            st.toast("🖼️ Gambar Dibaca!")
        
    if st.button("🔍 Analisis Sudut Serang", use_container_width=True, type="primary"):
        model_intel = genai.GenerativeModel('gemini-flash-latest')
        intel_prompt = f"Analisis marketing untuk {brand} {unit_type}. Kondisi: {final_scenario}. Spek: {pdf_text}. Buat: 1. Pain Points, 2. Solusi Teknis, 3. Killer Angle."
        contents = [intel_prompt]
        if image_data: contents.append(image_data)
        with st.spinner("Menganalisis data..."):
            st.session_state.intelligence_data = model_intel.generate_content(contents).text
            st.toast("Intelijen Selesai!")

    if st.session_state.intelligence_data:
        st.info(st.session_state.intelligence_data)

# ==========================================
# MODUL 3: PABRIK KONTEN & PUBLISHING
# ==========================================
with st.expander("🏭 Modul 3: Pabrik Konten & Publishing", expanded=False):
    visual_style = st.selectbox("Style Video Veo", ["Industrial Action", "CGI Cinematic", "Blueprint Tech"])
    if st.button("🚀 GENERATE CAMPAIGN (JSON)", use_container_width=True, type="primary"):
        if not st.session_state.intelligence_data:
            st.warning("Jalankan Modul 2 dulu!")
        else:
            model_factory = genai.GenerativeModel('gemini-flash-latest', generation_config={"response_mime_type": "application/json"})
            factory_prompt = f"Data: {st.session_state.intelligence_data}. Buat kampanye {brand} {unit_type}. JSON strict: {{'copywriting': 'teks', 'veo_prompts': [{{'scene': 1, 'visual': 'prompt', 'vo': 'suara', 'sfx': 'efek'}}]}}"
            with st.spinner("Memproduksi JSON..."):
                res_json = model_factory.generate_content(factory_prompt)
                st.session_state.campaign_data = json.loads(res_json.text)

    if st.session_state.campaign_data:
        data = st.session_state.campaign_data
        st.info(data.get("copywriting", ""))
        for s in data.get("veo_prompts", []):
            st.markdown(f"**S{s.get('scene')}:** `{s.get('visual')}`", unsafe_allow_html=True)
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.download_button("💾 Download JSON", data=json.dumps(data), file_name="Kampanye.json", use_container_width=True)
        with col_p2:
            st.button("⏰ Set Schedule", use_container_width=True)

# ==========================================
# MODUL 4: AI COMMENT SNIPER
# ==========================================
with st.expander("💬 Modul 4: AI Comment Sniper", expanded=False):
    komen = st.text_area("Paste Komentar Prospek/Haters:")
    if st.button("🎯 Tembak Balasan", use_container_width=True):
        model_sniper = genai.GenerativeModel('gemini-flash-latest')
        with st.spinner("Meracik balasan..."):
            st.success(model_sniper.generate_content(f"Balas komentar: '{komen}' untuk {brand} {unit_type}. Deteksi Hot Lead/Skeptis/Troll, patahkan argumennya.").text)

# ==========================================
# MODUL 5: B2B FINANCIAL SNIPER
# ==========================================
with st.expander("💰 Modul 5: Financial Sniper (ROI)", expanded=False):
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        inv = st.number_input("Harga Unit (Rp)", value=1500000000, step=10000000)
        prod = st.number_input("Target/Hari", value=100)
        harga = st.number_input("Profit/m3 (Rp)", value=150000)
    with c_f2:
        ops = st.number_input("Biaya Ops/Bln (Rp)", value=30000000)
        lama = st.number_input("Biaya Lama (Rp)", value=80000000)
        hari = st.number_input("Hari Kerja", value=25)

    if st.button("🧮 Generate ROI Proposal", use_container_width=True):
        profit_bln = (prod * harga * hari) - ops
        bep = inv / profit_bln if profit_bln > 0 else 0
        st.markdown(f"**BEP:** {bep:.1f} Bulan | **Hemat:** Rp {lama-ops:,.0f}/bln")
        
        model_fin = genai.GenerativeModel('gemini-flash-latest')
        res_fin = model_fin.generate_content(f"Buat Executive Summary meyakinkan. Alat {brand}. Investasi Rp {inv:,.0f}, BEP {bep:.1f} bulan.")
        st.info(res_fin.text)

        doc = docx.Document()
        doc.add_heading('Executive Summary', 0)
        for p in res_fin.text.split('\n'): doc.add_paragraph(p.strip())
        bio = io.BytesIO()
        doc.save(bio)
        st.download_button("📄 Download Proposal", data=bio.getvalue(), file_name=f"Proposal_{brand}.docx", use_container_width=True)

# ==========================================
# MODUL 6 & 7: KOMPETITOR & UPSELL
# ==========================================
with st.expander("⚔️ Modul 6 & 7: Kill-Switch & Upsell", expanded=False):
    st.markdown("**Kompetitor Kill-Switch**")
    kom_brand = st.text_input("Merek Lawan")
    if st.button("☠️ Generate Battlecard", use_container_width=True):
        st.success(genai.GenerativeModel('gemini-flash-latest').generate_content(f"Bandingkan {brand} vs {kom_brand}. Beri kelemahan lawan dan cara kita menang.").text)
    
    st.divider()
    st.markdown("**Upsell Predictor**")
    nama_klien = st.text_input("Klien", "PT. Tambang Maju")
    tgl_beli = st.date_input("Tgl Beli", datetime.date(2026, 1, 1))
    if st.button("🔮 Prediksi Maintenance", use_container_width=True):
        hari_op = (datetime.date.today() - tgl_beli).days
        st.info(genai.GenerativeModel('gemini-flash-latest').generate_content(f"Alat {brand} jalan {hari_op*10} jam. Apa yang harus diganti? Buat WA Upsell.").text)

# ==========================================
# MODUL 8: TENDER HACKER
# ==========================================
with st.expander("🏛️ Modul 8: LPSE Tender Hacker", expanded=False):
    tender_file = st.file_uploader("Upload RKS (PDF)", type=["pdf"])
    if st.button("🕵️‍♂️ Retas Dokumen", use_container_width=True):
        if tender_file:
            tdr_txt = "".join([PyPDF2.PdfReader(tender_file).pages[i].extract_text() for i in range(min(len(PyPDF2.PdfReader(tender_file).pages), 40))])
            with st.spinner("Membedah tender..."):
                st.success(genai.GenerativeModel('gemini-flash-latest').generate_content(f"Ekstrak syarat alat dari teks ini: {tdr_txt[:15000]}. Buktikan {brand} memenuhi syarat.").text)

# ==========================================
# MODUL 9: CRM MEMORY
# ==========================================
with st.expander("📊 Modul 9: CRM Memory & Report", expanded=False):
    DB_FILE = "sales_memory.json"
    def load_memory():
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f: return json.load(f)
        return []
    def save_memory(tgl, catatan):
        data = load_memory()
        data.append({"tanggal": tgl, "catatan": catatan})
        with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

    t1, t2 = st.tabs(["📝 Input Harian", "📈 Tarik Laporan"])
    with t1:
        tgl_harian = st.date_input("Tanggal", datetime.date.today())
        raw_notes = st.text_area("Catatan:", height=100)
        if st.button("Simpan & Buat Laporan"):
            if raw_notes:
                save_memory(str(tgl_harian), raw_notes)
                res_daily = genai.GenerativeModel('gemini-flash-latest').generate_content(f"Rapikan jadi laporan sales: {raw_notes}")
                st.info(res_daily.text)
                
                doc_d = docx.Document()
                doc_d.add_heading(f'Laporan {tgl_harian}', 0)
                for p in res_daily.text.split('\n'): doc_d.add_paragraph(p.strip())
                bio_d = io.BytesIO()
                doc_d.save(bio_d)
                st.download_button("📄 Download Word", data=bio_d.getvalue(), file_name=f"Harian_{tgl_harian}.docx", use_container_width=True)

    with t2:
        memori = load_memory()
        st.caption(f"📦 Memory: {len(memori)} catatan")
        if st.button("Generate Laporan Panjang"):
            if memori:
                big_data = "\n".join([f"{i['tanggal']}: {i['catatan']}" for i in memori])
                res_annual = genai.GenerativeModel('gemini-flash-latest').generate_content(f"Buat Laporan Eksekutif dari riwayat ini:\n{big_data}")
                st.success(res_annual.text)

# ==========================================
# MODUL 10: EXPAT NEGOTIATOR
# ==========================================
with st.expander("🌐 Modul 10: Expat Negotiator", expanded=False):
    teks_indo = st.text_area("Teks (Indonesia):", placeholder="Contoh: Pak, ROI mesin ini hanya 2 bulan...")
    bahasa_target = st.selectbox("Terjemahkan ke:", ["Mandarin (Simplified - Tiongkok)", "Inggris (Business)", "Korea (Corporate)"])
    if st.button("🔠 Terjemahkan", use_container_width=True):
        if teks_indo:
            st.info(genai.GenerativeModel('gemini-flash-latest').generate_content(f"Terjemahkan ke {bahasa_target} dengan nada eksekutif B2B: {teks_indo}").text)

# ==========================================
# MODUL 11: ELITE DIGITAL CARD (DUAL-CORE EDITION)
# ==========================================
import base64 # Library untuk menerjemahkan gambar ke HTML (Pastikan ada di app.py)

with st.expander("📇 Modul 11: Elite Digital Card (Dual-Core Design)", expanded=True):
    st.markdown("Tunjukkan layar ini ke klien, atau *screenshot* untuk dikirim via WA.")
    st.divider()

    # --- BAGIAN 1: PENGATURAN KUSTOMISASI (SIDEBAR DALAM MODUL) ---
    st.markdown("**🛠️ Pengaturan Tampilan Kartu**")
    
    # PERUBAHAN UTAMA: Tombol Pilihan Desain
    card_choice = st.radio(
        "Pilih Fokus Desain Kartu Anda:",
        [
            "Dual-Focus (Tatsuo & Aimix Only)", # Pilihan 1 (Utama)
            "Single-Focus Dynamic (Sesuai Produk di Modul 2)" # Pilihan 2 (Second Choice)
        ],
        horizontal=True
    )

    st.divider()

    # PERUBAHAN UTAMA: Multi-Drag & Drop Background (Bisa 1 atau 2 Gambar)
    st.markdown("**🖼️ Drag & Drop Gambar Latar Belakang**")
    st.caption("Fokus Dual: Masukkan 1 gambar Tatsuo & 1 gambar Aimix sekaligus. Fokus Single: Masukkan 1 gambar saja.")
    bg_uploads = st.file_uploader("Upload gambar (PNG/JPG):", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    # --- BAGIAN 2: DATA & LOGIKA DINAMIS ---
    
    # Link Logo Dealer
    url_azarindo = "https://raw.githubusercontent.com/blacksupervisor-sys/VORTEX-Heavy-Asset-Intelligence-Arbitrage-Engine-/main/AZARINDO.png"
    url_tatsuo = "https://raw.githubusercontent.com/blacksupervisor-sys/VORTEX-Heavy-Asset-Intelligence-Arbitrage-Engine-/main/TATSUO.png" 
    url_aimix = "https://raw.githubusercontent.com/blacksupervisor-sys/VORTEX-Heavy-Asset-Intelligence-Arbitrage-Engine-/main/AIMIX.png"
    # url_timehope = "https://raw.githubusercontent.com/blacksupervisor-sys/VORTEX-Heavy-Asset-Intelligence-Arbitrage-Engine-/main/TIMEHOPE.png" # Di-comment karena fokus Dual hanya Tatsuo-Aimix

    # Membuat QR Code dinamis dari link Affiliate
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={aff_link}"

    # Logika Penentuan Logo & Warna (Dinamis atau Statis)
    header_logo_html = ""
    accent_color = ""

    if card_choice == "Dual-Focus (Tatsuo & Aimix Only)":
        # Desain Utama: Menampilkan kedua logo berdampingan
        accent_color = "#E74C3C" # Merah Azarindo sebagai warna netral
        header_logo_html = (
            "<div style='display: flex; justify-content: center; align-items: center; gap: 10px; flex-wrap: wrap;'>"
            f"<img src='{url_tatsuo}' height='20px' alt='Tatsuo Logo'>"
            "<div style='border-left: 1px solid #ccc; height: 16px;'></div>"
            f"<img src='{url_aimix}' height='20px' alt='Aimix Logo'>"
            "</div>"
        )
    else:
        # Desain 'Second Choice': Berganti SKIN secara dinamis mengikuti produk di Modul 2
        # Kita ambil variabel 'brand' yang sudah Anda pilih di bagian atas app.py
        if brand == "Tatsuo":
            header_logo_html = f"<img src='{url_tatsuo}' height='25px' style='margin-top: 5px;'>"
            accent_color = "#FFD700" # Kuning Emas Tatsuo
        elif brand == "AIMIX":
            header_logo_html = f"<img src='{url_aimix}' height='25px' style='margin-top: 5px;'>"
            accent_color = "#1E90FF" # Biru AIMIX
        else: # Timehope (Jika dipilih di Modul 2)
            url_timehope = "https://raw.githubusercontent.com/blacksupervisor-sys/VORTEX-Heavy-Asset-Intelligence-Arbitrage-Engine-/main/TIMEHOPE.png"
            header_logo_html = f"<img src='{url_timehope}' height='35px' style='margin-top: 5px;'>"
            accent_color = "#000000" # Hitam/Netral

    # Logika Latar Belakang Multiple (Dukungan Drag & Drop)
    bg_html = ""
    if bg_uploads:
        # Ambil maksimal 2 gambar saja (Tatsuo & Aimix)
        images_to_use = bg_uploads[:2]
        
        # Buka container background (Mode Flexbox sejajar)
        bg_html += "<div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; display: flex; opacity: 0.15; filter: grayscale(70%);'>"
        
        # Looping: Terjemahkan setiap gambar yang diupload ke Base64
        for img in images_to_use:
            base64_img = base64.b64encode(img.read()).decode("utf-8")
            # Bagi rata ruang layar (flex: 1) untuk setiap gambar
            bg_html += f"<div style='flex: 1; background-image: url(data:{img.type};base64,{base64_img}); background-size: cover; background-position: center; border-right: 1px solid rgba(255,255,255,0.3);'></div>"
            
        bg_html += "</div>" # Tutup container
    else:
        # Jika belum ada gambar yang diupload, pakai Watermark Azarindo statis
        bg_html = f"<div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); opacity: 0.04; z-index: 0;'><img src='{url_azarindo}' style='width: 350px;'></div>"

    # --- BAGIAN 3: RENDER KARTU NAMA (HTML & CSS) ---
    st.divider()
    st.markdown("**📱 Preview Kartu Nama Digital Anda**")

    # Metode penggabungan string (Bulletproof HTML untuk Mobile)
    html_card = (
        f"<div style='position: relative; border: 2px solid {accent_color}; border-radius: 12px; background-color: #ffffff; padding: 25px; box-shadow: 0px 10px 20px rgba(0,0,0,0.05); overflow: hidden; margin-top: 15px;'>"
        
        # Injeksi Background Dinamis (Upload / Watermark)
        f"{bg_html}"
        
        "<div style='position: relative; z-index: 1;'>"
        
        # Header Logo (Dilebarkan agar aman di HP)
        "<div style='text-align: center; margin-bottom: 30px;'>"
        f"<img src='{url_azarindo}' height='50px' style='margin-bottom: 5px;' alt='Azarindo Logo'>"
        "<div style='color: #7f8c8d; font-size: 0.7em; margin-top: 5px; margin-bottom: 12px; font-weight: bold; letter-spacing: 1.5px;'>OFFICIAL PARTNER:</div>"
        
        # Injeksi Logo Dinamis/Statis berdasarkan Pilihan Desain
        f"{header_logo_html}"
        
        "</div>"
        
        # Garis Pemisah (Warna mengikuti Aksen)
        f"<hr style='border: 0; border-top: 2px solid {accent_color}; opacity: 0.2; margin: 20px 0;'>"
        
        # Nama & Jabatan
        "<div style='text-align: center; margin-bottom: 35px;'>"
        "<h1 style='color: #2c3e50; margin: 0; font-size: 24px; font-weight: 900; letter-spacing: 1px;'>ADJIE AGUNG</h1>"
        f"<p style='color: {accent_color}; margin: 5px 0 0 0; font-size: 11px; font-weight: 700; letter-spacing: 2px;'>HEAVY EQUIPMENT SALES SPECIALIST</p>"
        "</div>"
        
        # Footer Kontak & QR Code (Mobile Responsive)
        "<div style='display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 20px;'>"
        "<div style='flex: 1 1 180px; font-size: 12px; color: #34495e; line-height: 2.0;'>"
        "<div>🌐 <b>Website:</b> <span style='color: #2980b9;'>AZARINDO.ID</span></div>"
        f"<div>📱 <b>WhatsApp:</b> {wa_num}</div>"
        "<div>💼 <b>Area:</b> Kalimantan & Timur</div>"
        "<div>🏢 <b>Kantor:</b> Samarinda, Kaltim</div>"
        "</div>"
        "<div style='flex: 0 0 auto; text-align: center; margin: 0 auto;'>"
        f"<img src='{qr_url}' style='width: 75px; height: 75px; border: 1px solid #eee; padding: 5px; border-radius: 6px; background: #fff;' alt='QR Code'><br>"
        "<span style='color: #7f8c8d; font-size: 9px; font-weight: bold; letter-spacing: 0.5px;'>E-STORE SUKU CADANG</span>"
        "</div>"
        "</div>"
        
        "</div>"
        "</div>"
    )
    
    st.markdown(html_card, unsafe_allow_html=True)
    
# ==========================================
# FOOTER
# ==========================================
st.markdown("<div class='footer'>Architected & Developed by <b>Adjie Agung</b> <br> VORTEX 4.0 - Heavy-Asset Domination System</div>", unsafe_allow_html=True)
