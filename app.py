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
    aff_link = st.text_input("Shopee Affiliate", "https://collshp.com/vortex_catalog?share_channel_code=1")
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
# MODUL 8: EXECUTIVE PRODUCTION & ROI DASHBOARD
# ==========================================
with st.expander("💎 MODUL 8: EXECUTIVE PRODUCTION & ROI DASHBOARD", expanded=True):
    st.markdown("### 📊 Analisis Finansial & Teknis Terpadu")
    
    # TAB UTAMA
    tab1, tab2, tab3 = st.tabs(["🧮 Kalkulator ROI", "🧪 Formula & Material", "⚡ Efisiensi Produksi"])

    # ---------------------------------------------------------
    # TAB 1: KALKULATOR ROI (KREDIT & CASHFLOW)
    # ---------------------------------------------------------
    with tab1:
        c_roi1, c_roi2 = st.columns(2)
        with c_roi1:
            st.markdown("**💰 Investasi Unit**")
            h_alat = st.number_input("Harga Alat (Rp):", value=850000000)
            dp = st.slider("DP (%)", 0, 50, 20)
            bunga = st.number_input("Bunga Efektif (%/Thn):", value=10.0)
            tenor = st.number_input("Tenor (Bulan):", value=36)
        
        plafon = h_alat * (1 - (dp/100))
        i = (bunga / 100) / 12
        cicilan = (plafon * i) / (1 - (1 + i)**-tenor)
        
        with c_roi2:
            st.markdown("**🏗️ Target Operasional**")
            vol_bulan = st.number_input("Estimasi Produksi / Bulan (m3):", value=300)
            margin_m3 = st.number_input("Profit Bersih / m3 (Rp):", value=350000)
            
        profit_kotor = vol_bulan * margin_m3
        sisa_cash = profit_kotor - cicilan
        pb_period = h_alat / profit_kotor if profit_kotor > 0 else 0
        
        st.divider()
        r1, r2, r3 = st.columns(3)
        r1.metric("Cicilan / Bulan", f"Rp {cicilan:,.0f}")
        r2.metric("Nett Cashflow", f"Rp {sisa_cash:,.0f}")
        r3.metric("Payback Period", f"{pb_period:.1f} Bulan")

    # ---------------------------------------------------------
    # TAB 2: FORMULA SNI & TOTAL MATERIAL PROYEK
    # ---------------------------------------------------------
    with tab2:
        # Database SNI per m3 (kg)
        db_sni = {
            "K-100": {"s": 230, "p": 893, "k": 1027},
            "K-175": {"s": 326, "p": 760, "k": 1029},
            "K-225": {"s": 371, "p": 698, "k": 1047},
            "K-250": {"s": 384, "p": 692, "k": 1039},
            "K-300": {"s": 413, "p": 681, "k": 1021},
            "K-350": {"s": 448, "p": 667, "k": 1000},
            "K-400": {"s": 470, "p": 625, "k": 1025}
        }
        
        c_f1, c_f2 = st.columns([1, 2])
        with c_f1:
            mutu = st.selectbox("Mutu Beton (SNI):", list(db_sni.keys()), index=4)
            total_vol_proyek = st.number_input("Total Volume Proyek (m3):", value=1000)
        
        # Hitung Kebutuhan Total
        f = db_sni[mutu]
        tot_semen = (f['s'] / 50) * total_vol_proyek
        tot_pasir = (f['p'] / 1400) * total_vol_proyek
        tot_koral = (f['k'] / 1350) * total_vol_proyek
        
        with c_f2:
            st.markdown(f"**📦 Kebutuhan Material Proyek ({total_vol_proyek} m3):**")
            st.write(f"- Semen: **{tot_semen:,.0f} Sak** (50kg)")
            st.write(f"- Pasir: **{tot_pasir:,.1f} m3**")
            st.write(f"- Koral: **{tot_koral:,.1f} m3**")

    # ---------------------------------------------------------
    # TAB 3: PERBANDINGAN KECEPATAN & TENAGA KERJA
    # ---------------------------------------------------------
    with tab3:
        st.markdown("**🚀 Self-Loading Mixer vs Manual (8 Jam Kerja)**")
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            st.info("👴 **Metode Manual**")
            st.write("Output: ± 15 m3 / Hari")
            st.write("Tenaga: 15-20 Orang")
            st.write("Biaya Upah: Tinggi")
            
        with col_v2:
            st.success("🤖 **VORTEX / AIMIX Engine**")
            output_aimix = 60 # Rata-rata 3.5m3 per 12-15 menit
            st.write(f"Output: ± {output_aimix} m3 / Hari")
            st.write("Tenaga: 1 Operator + 1 Helper")
            st.write("Biaya Upah: Sangat Rendah")
            
        st.divider()
        st.subheader(f"Efisiensi: {output_aimix/15:.1f}x Lebih Cepat & Hemat 90% SDM!")

    # TOMBOL COPY FINAL
    if st.button("📝 Generate Full Analysis Report"):
        report = f"""
        *EXECUTIVE SUMMARY - {mutu}*
        Volume Proyek: {total_vol_proyek} m3
        Payback Period: {pb_period:.1f} Bulan
        ---------------------------
        KEBUTUHAN MATERIAL TOTAL:
        - Semen: {tot_semen:,.0f} Sak
        - Pasir: {tot_pasir:,.1f} m3
        - Koral: {tot_koral:,.1f} m3
        ---------------------------
        EFISIENSI PRODUKSI:
        Metode Aimix {output_aimix/15:.1f}x lebih cepat dibanding manual.
        """
        st.code(report, language="markdown")
        
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
# MODUL 11: ELITE DIGITAL CARD (PERFECT BALANCE EDITION)
# ==========================================
import base64 

with st.expander("📇 Modul 11: Elite Digital Card (Dual-Core Design)", expanded=True):
    st.markdown("*screenshot*")
    st.divider()

    # --- BAGIAN 1: PENGATURAN KUSTOMISASI ---
    st.markdown("**🛠️ Pengaturan Tampilan Kartu**")
    card_choice = st.radio(
        "Pilih Fokus Desain Kartu Anda:",
        [
            "Dual-Focus (Tatsuo & Aimix)",
            "Single-Focus (Satu Produk Khusus)"
        ],
        horizontal=True
    )

    # PERBAIKAN 1: Pilihan Merek Khusus Modul 11 (Anti-Stuck)
    single_brand = None
    if card_choice == "Single-Focus (Satu Produk Khusus)":
        single_brand = st.selectbox("🎯 Pilih Merek yang ingin ditonjolkan di kartu:", ["Tatsuo", "AIMIX", "New Timehope"])

    st.divider()

    # Drag & Drop Background
    st.markdown("**🖼️ Drag & Drop Background**")
    st.caption("Fokus Dual: input Tatsuo & Aimix . Fokus Single: input 1 visual.")
    bg_uploads = st.file_uploader("Upload gambar (PNG/JPG):", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    # --- BAGIAN 2: DATA & LOGIKA DINAMIS ---
    url_azarindo = "https://raw.githubusercontent.com/blacksupervisor-sys/VORTEX-Heavy-Asset-Intelligence-Arbitrage-Engine-/main/AZARINDO.png"
    url_tatsuo = "https://raw.githubusercontent.com/blacksupervisor-sys/VORTEX-Heavy-Asset-Intelligence-Arbitrage-Engine-/main/TATSUO.png" 
    url_aimix = "https://raw.githubusercontent.com/blacksupervisor-sys/VORTEX-Heavy-Asset-Intelligence-Arbitrage-Engine-/main/AIMIX.png"
    url_timehope = "https://raw.githubusercontent.com/blacksupervisor-sys/VORTEX-Heavy-Asset-Intelligence-Arbitrage-Engine-/main/TIMEHOPE.png"

    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={aff_link}"

    # Logika Penentuan Logo & Warna 
    header_logo_html = ""
    accent_color = ""

    if card_choice == "Dual-Focus (Tatsuo & Aimix)":
        accent_color = "#E74C3C" 
        # PERBAIKAN 2: Proporsi Ukuran (Tatsuo dibuat 18px, Aimix dibesarkan jadi 28px agar sejajar)
        header_logo_html = (
            "<div style='display: flex; justify-content: center; align-items: center; gap: 15px; flex-wrap: wrap; margin-top: 5px;'>"
            f"<img src='{url_tatsuo}' height='18px' alt='Tatsuo Logo'>"
            "<div style='border-left: 2px solid #ddd; height: 22px;'></div>"
            f"<img src='{url_aimix}' height='28px' alt='Aimix Logo'>"
            "</div>"
        )
    else:
        # Menggunakan pilihan langsung dari Modul 11 (Bukan Modul 2)
        if single_brand == "Tatsuo":
            header_logo_html = f"<img src='{url_tatsuo}' height='28px' style='margin-top: 5px;'>"
            accent_color = "#FFD700" 
        elif single_brand == "AIMIX":
            # AIMIX single focus dibesarkan signifikan
            header_logo_html = f"<img src='{url_aimix}' height='42px' style='margin-top: 5px;'>"
            accent_color = "#1E90FF" 
        elif single_brand == "New Timehope": 
            # Timehope single focus
            header_logo_html = f"<img src='{url_timehope}' height='45px' style='margin-top: 5px;'>"
            accent_color = "#C0392B" 

    # Logika Latar Belakang Multiple
    bg_html = ""
    if bg_uploads:
        images_to_use = bg_uploads[:2]
        bg_html += "<div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; display: flex; opacity: 0.15; filter: grayscale(70%);'>"
        for img in images_to_use:
            base64_img = base64.b64encode(img.read()).decode("utf-8")
            bg_html += f"<div style='flex: 1; background-image: url(data:{img.type};base64,{base64_img}); background-size: cover; background-position: center; border-right: 1px solid rgba(255,255,255,0.3);'></div>"
        bg_html += "</div>" 
    else:
        bg_html = f"<div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); opacity: 0.04; z-index: 0;'><img src='{url_azarindo}' style='width: 350px;'></div>"

    # --- BAGIAN 3: RENDER KARTU NAMA ---
    st.divider()
    st.markdown("**📱 Preview Kartu Nama Digital Anda**")

    html_card = (
        f"<div style='position: relative; border: 2px solid {accent_color}; border-radius: 12px; background-color: #ffffff; padding: 25px; box-shadow: 0px 10px 20px rgba(0,0,0,0.05); overflow: hidden; margin-top: 15px;'>"
        
        f"{bg_html}"
        
        "<div style='position: relative; z-index: 1;'>"
        
        # Header Logo
        "<div style='text-align: center; margin-bottom: 30px;'>"
        f"<img src='{url_azarindo}' height='50px' style='margin-bottom: 5px;' alt='Azarindo Logo'>"
        "<div style='color: #7f8c8d; font-size: 0.7em; margin-top: 5px; margin-bottom: 12px; font-weight: bold; letter-spacing: 1.5px;'>OFFICIAL PARTNER:</div>"
        f"{header_logo_html}"
        "</div>"
        
        f"<hr style='border: 0; border-top: 2px solid {accent_color}; opacity: 0.2; margin: 20px 0;'>"
        
        # Nama & Jabatan (Tengah + Garis)
        "<div style='display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 35px;'>"
        "<h1 style='color: #2c3e50; margin: 0; font-size: 24px; font-weight: 900; letter-spacing: 1px;'>ADJIE AGUNG</h1>"
        "<div style='width: 60px; height: 2px; background-color: #e0e0e0; margin: 10px 0;'></div>" 
        f"<p style='color: {accent_color}; margin: 0; font-size: 11px; font-weight: 700; letter-spacing: 2px;'>HEAVY EQUIPMENT SALES</p>"
        "</div>"
        
        # Footer Kontak
        "<div style='display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 20px;'>"
        "<div style='flex: 1 1 180px; font-size: 12px; color: #34495e; line-height: 2.0;'>"
        "<div>🌐 <b>Website:</b> <span style='color: #2980b9;'>azarindo.id</span></div>"
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
    # ELITE ACTION BAR (WA SHARE & vCARD)
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        # Teks otomatis untuk WhatsApp
        pesan_wa = "Selamat pagi/siang Bapak/Ibu. Perkenalkan saya Adjie Agung, Heavy Equipment Specialist dari Azarindo. Berikut saya lampirkan kartu nama digital saya. Jika proyek Anda membutuhkan alat Konstruksi yang efisiensi (Excavator wheel track, Self Loading mixer, Concrete Pump, HSPD), saya siap membantu. Terima kasih."
        link_wa = f"https://api.whatsapp.com/send?text={pesan_wa.replace(' ', '%20')}"
        st.markdown(f'<a href="{link_wa}" target="_blank" style="display: block; text-align: center; background-color: #25D366; color: white; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold;">💬 Kirim Pengantar WA</a>', unsafe_allow_html=True)

    with col_btn2:
        # Membuat file vCard (Kontak HP Otomatis)
        vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N:Agung;Adjie;;;
FN:Adjie Agung
TITLE:Heavy Equipment Sales
ORG:Azarindo (Tatsuo, AIMIX, Timehope)
TEL;TYPE=CELL:{wa_num}
URL:azarindo.id
END:VCARD"""
        st.download_button(
            label="📇 Download File Kontak (vCard)",
            data=vcard_data,
            file_name="Adjie_Agung_Azarindo.vcf",
            mime="text/vcard",
            use_container_width=True
        )
    
# ==========================================
# FOOTER
# ==========================================
st.markdown("<div class='footer'>Architected & Developed by <b>Adjie Agung</b> <br> VORTEX 4.0 - Heavy-Asset Domination System</div>", unsafe_allow_html=True)
