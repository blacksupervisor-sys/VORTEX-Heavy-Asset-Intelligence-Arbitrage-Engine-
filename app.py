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

# --- CSS KHUSUS UNTUK TAMPILAN HP (MOBILE OPTIMIZED) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .footer { text-align: center; color: #888; font-size: 0.85rem; margin-top: 50px; padding-top: 10px; border-top: 1px solid #ddd; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- AMBIL API KEY DARI SECRETS ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ GEMINI_API_KEY tidak ditemukan di Secrets! Pastikan file .streamlit/secrets.toml sudah benar.")
    st.stop()

# Inisialisasi Memori (Session State)
if "intelligence_data" not in st.session_state: st.session_state.intelligence_data = ""
if "campaign_data" not in st.session_state: st.session_state.campaign_data = None
if "project_scenario" not in st.session_state: st.session_state.project_scenario = ""
if "current_weather" not in st.session_state: st.session_state.current_weather = ""

# ==========================================
# SIDEBAR: SETTING COMMAND CENTER
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/engineering.png", width=70)
    st.title("⚙️ Command Center")
    
    st.divider()
    st.subheader("📡 Engine Status")
    st.success("Model: gemini-flash-latest")
    st.info("Library: AIMIX, Tatsuo, New Timehope")
    
    st.divider()
    st.subheader("🔗 Sales Funnel")
    wa_num = st.text_input("WhatsApp Sales", "+6281230857759")
    aff_link = st.text_input("Shopee Affiliate", "https://shope.ee/...")
    
    st.divider()
    st.caption("Engine: VORTEX 4.0 | By Adjie Agung")

# Header Utama Aplikasi
st.title("🌪️ VORTEX 4.0")
st.subheader("Heavy-Asset Domination System")

# ==========================================
# MODUL 1: RADAR CUACA & TENDER
# ==========================================
with st.expander("📡 Modul 1: Radar Intelijen (Cuaca & Tender)", expanded=True):
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("**⛈️ Sensor Cuaca**")
        lokasi = st.selectbox("Lokasi Radar", ["Samarinda, ID", "Penajam (IKN), ID", "Balikpapan, ID"])
        if st.button("Tarik Cuaca Real-Time", use_container_width=True):
            st.session_state.current_weather = "Hujan Ringan, Suhu 24-30°C, Kelembapan 98% (Tanah sangat basah/lumpur)"
            st.toast(f"Cuaca {lokasi} Terdeteksi!")

    with col_w2:
        st.markdown("**🏗️ Radar Tender**")
        cakupan_radar = st.selectbox("Cakupan Wilayah:", ["Kalimantan Timur & IKN", "Seluruh Kalimantan", "Maluku & Indonesia Timur", "Nasional (Seluruh Indonesia)"])
        
        if st.button("🛰️ Scan Tender Area Terpilih", use_container_width=True):
            with st.spinner(f"Memindai LPSE & Proyek di {cakupan_radar}..."):
                model_radar = genai.GenerativeModel('gemini-flash-latest')
                res = model_radar.generate_content(f"Cari info singkat tren proyek infrastruktur, gedung, atau pembukaan lahan tambang terbaru di wilayah {cakupan_radar} bulan ini. Buat 2 paragraf padat yang fokus pada kebutuhan alat berat.")
                st.session_state.project_scenario = res.text
            st.toast("Radar Tender Berhasil!")

    # Gabungan Output Radar
    gabungan_radar = f"Kondisi Cuaca: {st.session_state.current_weather}\n\nKondisi Proyek: {st.session_state.project_scenario}"
    final_scenario = st.text_area("Final Scenario (Suntikan AI)", value=gabungan_radar, height=120)

# ==========================================
# MODUL 2: EKSTRAKSI & INTELIJEN PRODUK
# ==========================================
with st.expander("🎯 Modul 2: Ekstraksi Spek & Analisis", expanded=False):
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        brand = st.selectbox("Merek Produk", ["AIMIX", "Tatsuo", "New Timehope"])
        default_unit = "HSPD 360" if brand == "New Timehope" else "Self Loading Mixer + ABT60C"
        unit_type = st.text_input("Tipe Unit", default_unit)
    with col_u2:
        uploaded_file = st.file_uploader("Upload Brosur (PDF/IMG)", type=["pdf", "png", "jpg", "jpeg"])
        
    pdf_text = ""
    image_data = None
    
    if uploaded_file:
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext == 'pdf':
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted: pdf_text += extracted
            st.toast("📄 PDF Berhasil Dibaca!")
        elif ext in ['png', 'jpg', 'jpeg']:
            image_data = Image.open(uploaded_file)
            st.toast("🖼️ Gambar Berhasil Dibaca!")
        
    if st.button("🔍 Analisis Sudut Serang (Marketing Angle)", use_container_width=True, type="primary"):
        model_intel = genai.GenerativeModel('gemini-flash-latest')
        intel_prompt = f"""
        Kamu Ahli Intelijen Pasar Alat Berat.
        Produk: {brand} {unit_type}. Skenario: {final_scenario}
        Data Spek: {pdf_text if pdf_text else 'Gunakan gambar terlampir atau pengetahuanmu.'}
        Khusus New Timehope HSPD: Tekankan Static Pile Driving (Tanpa suara/getaran).
        Output: 1. Pain Points, 2. Solusi Teknis, 3. Killer Angle.
        """
        contents = [intel_prompt]
        if image_data: contents.append(image_data)
        
        with st.spinner("Menganalisis data lapangan dan spesifikasi..."):
            try:
                st.session_state.intelligence_data = model_intel.generate_content(contents).text
                st.toast("Intelijen Selesai!")
            except Exception as e:
                st.error(e)

    if st.session_state.intelligence_data:
        st.info(st.session_state.intelligence_data)

# ==========================================
# MODUL 3: PABRIK KONTEN & PUBLISHING
# ==========================================
with st.expander("🏭 Modul 3: Pabrik Konten & Publishing", expanded=False):
    visual_style = st.selectbox("Style Video Veo 3", ["Industrial Action", "CGI Cinematic", "Blueprint Tech"])
    
    if st.button("🚀 GENERATE CAMPAIGN (JSON)", use_container_width=True, type="primary"):
        if not st.session_state.intelligence_data:
            st.warning("Jalankan Modul 2 terlebih dahulu!")
        else:
            model_factory = genai.GenerativeModel('gemini-flash-latest', generation_config={"response_mime_type": "application/json"})
            factory_prompt = f"""
            Gunakan data ini: {st.session_state.intelligence_data}. Buat kampanye untuk {brand} {unit_type} gaya {visual_style}.
            HANYA JSON:
            {{
              "copywriting": "Caption agresif. WA: {wa_num}, Safety gear: {aff_link}",
              "veo_prompts": [
                {{ "scene": 1, "visual": "Prompt Veo detail max 8s", "vo": "Voice over narator", "sfx": "Instruksi SFX" }}
              ]
            }}
            """
            with st.spinner("Memproduksi Aset..."):
                try:
                    res_json = model_factory.generate_content(factory_prompt)
                    st.session_state.campaign_data = json.loads(res_json.text)
                except Exception as e:
                    st.error(f"Error JSON: {e}")

    # Penjadwalan & Download
    if st.session_state.campaign_data:
        data = st.session_state.campaign_data
        st.markdown("**📝 Copywriting:**")
        st.info(data.get("copywriting", ""))
        
        st.markdown("**🎬 Script Veo 3:**")
        for s in data.get("veo_prompts", []):
            st.markdown(f"**Scene {s.get('scene')}:** `{s.get('visual')}` <br> *VO: {s.get('vo')}*", unsafe_allow_html=True)
            
        st.divider()
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            json_dl = json.dumps(data, indent=4)
            st.download_button("💾 Download JSON", data=json_dl, file_name=f"Kampanye_{brand}.json", use_container_width=True)
            st.button("📲 Post to TikTok", use_container_width=True)
        with col_p2:
            post_date = st.date_input("Jadwal Post", datetime.date.today())
            if st.button("⏰ Set Schedule", use_container_width=True):
                st.success(f"Dijadwalkan: {post_date}")

# ==========================================
# MODUL 4: AI COMMENT SNIPER
# ==========================================
with st.expander("💬 Modul 4: AI Comment Sniper (Intent Radar)", expanded=False):
    user_comment = st.text_area("✍️ Paste Komentar Prospek:", placeholder="Contoh: Mesin beginian pasti gampang overheat.")
    st.caption("🟢 Hot Lead 🟡 Skeptis 🔴 Troll/Kompetitor")
    
    if st.button("🎯 Deteksi & Tembak Balasan", use_container_width=True, type="primary"):
        if user_comment:
            model_sniper = genai.GenerativeModel('gemini-flash-latest')
            sniper_prompt = f"""
            Tugasmu membalas komentar: "{user_comment}" untuk produk {brand} {unit_type}.
            1. Analisis Niat (Hot Lead / Skeptis / Troll).
            2. Buat balasan. Gunakan spek teknis untuk membungkam troll. Arahkan Hot lead ke WA {wa_num}.
            Format Output: [STATUS] \n [DRAFT BALASAN]
            """
            with st.spinner("Membidik target..."):
                st.success(model_sniper.generate_content(sniper_prompt).text)
        else:
            st.warning("Isi komentar dulu!")

# ==========================================
# MODUL 5: B2B FINANCIAL SNIPER
# ==========================================
with st.expander("💰 Modul 5: Financial Sniper (ROI Generator)", expanded=False):
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        inv = st.number_input("Harga Unit (Rp)", value=1500000000, step=10000000)
        prod = st.number_input("Target/Hari", value=100)
        harga = st.number_input("Profit/m3 (Rp)", value=150000)
    with c_f2:
        ops = st.number_input("Biaya Ops/Bln (Rp)", value=30000000)
        lama = st.number_input("Biaya Cara Lama (Rp)", value=80000000)
        hari = st.number_input("Hari Kerja/Bln", value=25)

    if st.button("🧮 Generate ROI & Proposal", use_container_width=True, type="primary"):
        profit_bln = (prod * harga * hari) - ops
        hemat_bln = lama - ops
        bep = inv / profit_bln if profit_bln > 0 else 0
        
        st.markdown(f"**BEP:** {bep:.1f} Bulan | **Penghematan:** Rp {hemat_bln:,.0f}/bln")
        
        model_fin = genai.GenerativeModel('gemini-flash-latest')
        fin_prompt = f"Buat Executive Summary meyakinkan untuk Direktur. Alat {brand} {unit_type}. Investasi Rp {inv:,.0f}, BEP {bep:.1f} bulan. Hemat Rp {hemat_bln:,.0f}/bulan. Ini bukan biaya, tapi aset."
        
        with st.spinner("Merumuskan dokumen eksekutif..."):
            res_fin = model_fin.generate_content(fin_prompt)
            st.info(res_fin.text)
            
            # Export Word
            doc = docx.Document()
            doc.add_heading(f'Executive Summary - {brand}', 0)
            for p in res_fin.text.split('\n'):
                if p.strip(): doc.add_paragraph(p.strip())
            bio = io.BytesIO()
            doc.save(bio)
            st.download_button("📄 Download Proposal (Word)", data=bio.getvalue(), file_name=f"Proposal_{brand}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)

# ==========================================
# MODUL 6: COMPETITOR KILL-SWITCH
# ==========================================
with st.expander("⚔️ Modul 6: Competitor Kill-Switch", expanded=False):
    col_k1, col_k2 = st.columns(2)
    with col_k1: kom_brand = st.text_input("Merek Kompetitor", placeholder="Misal: Sany")
    with col_k2: kom_tipe = st.text_input("Tipe Kompetitor", placeholder="Misal: SY215")
    
    if st.button("☠️ Generate Battlecard", use_container_width=True):
        if kom_brand:
            model_kill = genai.GenerativeModel('gemini-flash-latest')
            kill_prompt = f"Prospek membandingkan {brand} {unit_type} vs {kom_brand} {kom_tipe}. Buat Battlecard: 1. Titik Buta Kompetitor, 2. Keunggulan Kita, 3. Skrip Elegan menjatuhkan argumen lawan."
            with st.spinner("Mencari kelemahan musuh..."):
                st.success(model_kill.generate_content(kill_prompt).text)
        else: st.warning("Masukkan merek kompetitor!")

# ==========================================
# MODUL 7: INFINITE UPSELL PREDICTOR
# ==========================================
with st.expander("🔄 Modul 7: Upsell Predictor (Purna Jual)", expanded=False):
    c_up1, c_up2 = st.columns(2)
    with c_up1: nama_klien = st.text_input("Nama Klien", "PT. Maju Konstruksi")
    with c_up2: tgl_beli = st.date_input("Tgl Beli", datetime.date(2026, 1, 1))
    
    if st.button("🔮 Prediksi Maintenance & Draft WA", use_container_width=True):
        hari_op = (datetime.date.today() - tgl_beli).days
        st.markdown(f"**Umur Alat:** {hari_op} hari (~{hari_op*10} Jam Kerja)")
        
        model_up = genai.GenerativeModel('gemini-flash-latest')
        up_prompt = f"Klien {nama_klien} pakai {brand} {unit_type} selama {hari_op*10} jam kerja. Apa komponen yang harus diganti? Buat Draft WA ramah untuk ingatkan jadwal ganti & selipkan tawaran beli sparepart/safety via link: {aff_link}"
        with st.spinner("Menganalisis jadwal..."):
            st.info(model_up.generate_content(up_prompt).text)

# ==========================================
# MODUL 8: LPSE TENDER HACKER
# ==========================================
with st.expander("🏛️ Modul 8: LPSE Tender Hacker", expanded=False):
    nama_proyek = st.text_input("Nama Proyek", placeholder="Pembangunan Gedung...")
    tender_file = st.file_uploader("Upload Dokumen RKS (PDF)", type=["pdf"])
    
    if st.button("🕵️‍♂️ Retas Dokumen & Buat Strategi", use_container_width=True, type="primary"):
        if tender_file:
            tender_txt = ""
            pdf_tender = PyPDF2.PdfReader(tender_file)
            for i in range(min(len(pdf_tender.pages), 40)): # Limit 40 halaman agar super cepat
                ex = pdf_tender.pages[i].extract_text()
                if ex: tender_txt += ex
            
            model_tdr = genai.GenerativeModel('gemini-flash-latest')
            tdr_prompt = f"Bedah tender {nama_proyek}. Ekstrak syarat alat berat dari teks ini: {tender_txt[:15000]}. Buat Matriks Kepatuhan membuktikan {brand} {unit_type} memenuhi syarat, dan buat strategi menangnya."
            with st.spinner("Membedah dokumen lelang..."):
                st.success(model_tdr.generate_content(tdr_prompt).text)
        else: st.warning("Upload RKS Tender dulu!")

# ==========================================
# MODUL 9: AUTO-REPORT GENERATOR (WITH CRM MEMORY)
# ==========================================
with st.expander("📊 Modul 9: Laporan Sales & Memori CRM", expanded=False):
    st.markdown("Mesin menyimpan riwayat kunjungan harian Anda. Laporan Tahunan dapat ditarik otomatis dari akumulasi data memori.")
    
    # Fungsi Database Lokal
    DB_FILE = "sales_memory.json"
    
    def load_memory():
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                return json.load(f)
        return []

    def save_memory(tanggal, catatan):
        data = load_memory()
        data.append({"tanggal": tanggal, "catatan": catatan})
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
            
    # Antarmuka Modul 9
    tab1, tab2 = st.tabs(["📝 Input Harian", "📈 Tarik Laporan Triwulan/Tahunan"])
    
    with tab1:
        st.subheader("Catatan Kunjungan Harian")
        tgl_harian = st.date_input("Tanggal Kunjungan", datetime.date.today())
        raw_notes = st.text_area("✍️ Catatan Mentah (Voice Note/Ketik Cepat):", 
                                 placeholder="Ke PT A nawarin Tatsuo, bos minta diskon. Lanjut PT B...", height=100)
        simpan_db = st.checkbox("💾 Simpan ke Brankas Memori Jangka Panjang", value=True)
        
        if st.button("📝 Buat Laporan Harian", use_container_width=True, type="primary"):
            if not raw_notes:
                st.warning("Masukkan catatan mentah!")
            else:
                if simpan_db:
                    save_memory(str(tgl_harian), raw_notes)
                    st.toast("✅ Data tersimpan di Brankas Memori!")
                
                model_daily = genai.GenerativeModel('gemini-flash-latest')
                prompt_daily = f"Rapikan catatan sales ini menjadi laporan harian profesional tanggal {tgl_harian}: '{raw_notes}'. Format: Ringkasan, Status Prospek, Rencana Lanjutan."
                
                with st.spinner("Menyusun Laporan Harian..."):
                    res_daily = model_daily.generate_content(prompt_daily)
                    st.info(res_daily.text)
                    
                    # Fitur Download Harian
                    doc_d = docx.Document()
                    doc_d.add_heading(f'Laporan Harian - {tgl_harian}', 0)
                    for p in res_daily.text.split('\n'):
                        if p.strip(): doc_d.add_paragraph(p.strip())
                    bio_d = io.BytesIO()
                    doc_d.save(bio_d)
                    st.download_button("📄 Download Laporan Harian (Word)", data=bio_d.getvalue(), file_name=f"Laporan_Harian_{tgl_harian}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    with tab2:
        st.subheader("Ekstraksi Memori Besar (Triwulan/Tahunan)")
        jenis_laporan = st.selectbox("Jenis Laporan", ["Triwulan (Quarterly)", "Tahunan (Annual)"])
        
        memori_tersimpan = load_memory()
        st.caption(f"📦 Total data tersimpan di Brankas: **{len(memori_tersimpan)} catatan kunjungan**")
        
        if st.button("🚀 Rangkum & Generate Laporan Eksekutif", use_container_width=True, type="primary"):
            if len(memori_tersimpan) == 0:
                st.warning("Brankas memori masih kosong! Input laporan harian terlebih dahulu.")
            else:
                # Menggabungkan seluruh data memori menjadi satu string besar
                big_data = "\n".join([f"Tgl {item['tanggal']}: {item['catatan']}" for item in memori_tersimpan])
                
                model_annual = genai.GenerativeModel('gemini-flash-latest')
                prompt_annual = f"""
                Kamu adalah Executive Assistant. Buatkan Laporan {jenis_laporan} berdasarkan SELURUH riwayat kunjungan harian ini:
                
                {big_data}
                
                Struktur Wajib:
                1. 📝 Executive Summary (Rangkuman performa selama periode ini)
                2. 🏆 Pencapaian & Hot Leads (Sebutkan klien mana yang paling potensial)
                3. 🚧 Kendala Utama di Lapangan (Analisis hambatan tersering)
                4. 🎯 Strategi Kedepan
                
                Gunakan bahasa korporat kelas atas yang elegan.
                """
                
                with st.spinner(f"Membaca seluruh memori dan menyusun Laporan {jenis_laporan}..."):
                    res_annual = model_annual.generate_content(prompt_annual)
                    st.success("Laporan Eksekutif Selesai!")
                    st.info(res_annual.text)
                    
                    # Fitur Download Tahunan
                    doc_a = docx.Document()
                    doc_a.add_heading(f'Laporan {jenis_laporan} Sales', 0)
                    for p in res_annual.text.split('\n'):
                        if p.strip(): doc_a.add_paragraph(p.strip())
                    bio_a = io.BytesIO()
                    doc_a.save(bio_a)
                    st.download_button(f"📄 Download Laporan {jenis_laporan} (Word)", data=bio_a.getvalue(), file_name=f"Laporan_{jenis_laporan}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                    
# ==========================================
# FOOTER (DEVELOPER SIGNATURE)
# ==========================================
st.markdown("<div class='footer'>Architected & Developed by <b>Adjie Agung</b> <br> VORTEX 4.0 - B2B Heavy-Asset Domination System</div>", unsafe_allow_html=True)
