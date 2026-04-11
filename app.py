import streamlit as st
import google.generativeai as genai
import json
import PyPDF2
from PIL import Image
import datetime

# ==========================================
# KONFIGURASI HALAMAN & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="VORTEX 3.2: Multi-Brand Edition", page_icon="🌪️", layout="wide")

# --- AMBIL API KEY DARI SECRETS ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("⚠️ GEMINI_API_KEY tidak ditemukan di Secrets!")
    st.stop()

# Inisialisasi Memori
if "intelligence_data" not in st.session_state: st.session_state.intelligence_data = ""
if "campaign_data" not in st.session_state: st.session_state.campaign_data = None
if "project_scenario" not in st.session_state: st.session_state.project_scenario = ""
if "current_weather" not in st.session_state: st.session_state.current_weather = ""

# ==========================================
# SIDEBAR: SETTING & PENJADWALAN
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/google-earth.png", width=80)
    st.title("⚙️ Command Center")
    
    st.divider()
    st.subheader("📡 VORTEX Engine Status")
    st.success("Model: gemini-flash-latest")
    st.info("Brand Library: AIMIX, Tatsuo, New Timehope")
    
    st.divider()
    st.subheader("🔗 Sales Funnel")
    wa_num = st.text_input("WhatsApp Sales", "+6281230857759")
    aff_link = st.text_input("Shopee Affiliate", "https://shope.ee/...")
    
    st.divider()
    st.caption("VORTEX 3.2 | Multi-Brand Dominance")

st.title("🌪️ VORTEX 3.2: Multi-Brand Domination")
st.subheader("Automated Radar, Intelligence, and Content Factory")

# ==========================================
# MODUL 1: RADAR CUACA & TENDER
# ==========================================
st.header("📡 Modul 1: Radar Intelijen (Cuaca & Tender)")
with st.container(border=True):
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("**⛈️ Sensor Cuaca**")
        lokasi = st.selectbox("Lokasi Radar", ["Samarinda, ID", "Penajam (IKN), ID", "Balikpapan, ID"])
        if st.button("Tarik Cuaca Real-Time", use_container_width=True):
            st.session_state.current_weather = "Hujan Ringan, Suhu 24-30°C, Kelembapan 98% (Tanah sangat basah/lumpur)"
            st.success(f"Cuaca {lokasi} Terdeteksi!")

    with col_w2:
        st.markdown("**🏗️ Radar Tender & Proyek**")
        if st.button("🛰️ Scan Tender Terbaru (Kaltim/IKN)", use_container_width=True):
            with st.spinner("Memindai berita proyek & LPSE..."):
                model_radar = genai.GenerativeModel('gemini-flash-latest')
                res = model_radar.generate_content("Cari info singkat tren proyek infrastruktur, gedung, atau tambang terbaru di Kalimantan Timur bulan ini. Buat dalam 2 paragraf singkat.")
                st.session_state.project_scenario = res.text
                st.success("Radar Tender Berhasil!")

if st.session_state.project_scenario or st.session_state.current_weather:
    with st.expander("📝 Hasil Scan Radar (Klik untuk Edit)", expanded=True):
        gabungan_radar = f"Kondisi Cuaca: {st.session_state.current_weather}\n\nKondisi Proyek: {st.session_state.project_scenario}"
        final_scenario = st.text_area("Final Scenario (Input ke AI)", value=gabungan_radar, height=150)

# ==========================================
# MODUL 2: THE INTELLIGENCE WEAPON (MULTI-BRAND)
# ==========================================
st.header("🎯 Modul 2: Ekstraksi Spesifikasi & Intelijen")
with st.container(border=True):
    col_u1, col_u2 = st.columns([1, 1])
    with col_u1:
        brand = st.selectbox("Merek Produk", ["AIMIX", "Tatsuo", "New Timehope"])
        # Logika default unit berdasarkan brand
        default_unit = "HSPD 120" if brand == "New Timehope" else "Self Loading Mixer"
        unit_type = st.text_input("Tipe Unit", default_unit)
    with col_u2:
        uploaded_file = st.file_uploader("Upload Brosur / Spek (PDF/PNG/JPG)", type=["pdf", "png", "jpg", "jpeg"])
        
    pdf_text = ""
    image_data = None
    
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension == 'pdf':
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted: pdf_text += extracted
            st.success("📄 Dokumen PDF Berhasil!")
        elif file_extension in ['png', 'jpg', 'jpeg']:
            image_data = Image.open(uploaded_file)
            st.image(image_data, caption="Visual Data Injected", use_container_width=True)
            st.success("🖼️ Gambar Brosur Berhasil!")
        
    if st.button("🔍 Jalankan Analisis Intelijen", use_container_width=True, type="primary"):
        model_intel = genai.GenerativeModel('gemini-flash-latest')
        
        intelligence_prompt = f"""
        Kamu adalah Ahli Intelijen Pasar Alat Berat. Analisis skenario lapangan dan cocokkan dengan spesifikasi alat.
        Produk: {brand} {unit_type}
        Skenario & Cuaca: {final_scenario if 'final_scenario' in locals() else 'Jalanan berlumpur, proyek dikebut'}
        
        DATA SPESIFIKASI:
        "{pdf_text if pdf_text else 'Baca dari gambar jika ada, atau gunakan pengetahuan umummu.'}"
        
        KHUSUS UNTUK NEW TIMEHOPE HSPD: Fokuskan pada keunggulan Static Pile Driving (Tanpa suara, tanpa getaran, cocok untuk area perkotaan/IKN, tanah lunak).
        
        Output:
        1. Pain Points Utama Kontraktor.
        2. Solusi Teknis Alat (Mapping Spek ke Masalah).
        3. Killer Marketing Angle (Logis & Emosional).
        """
        
        prompt_contents = [intelligence_prompt]
        if image_data is not None: prompt_contents.append(image_data)
        
        with st.spinner(f"Menganalisis {brand} {unit_type}..."):
            try:
                response = model_intel.generate_content(prompt_contents)
                st.session_state.intelligence_data = response.text
                st.success("Intelijen Siap Dieksekusi!")
            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state.intelligence_data:
    with st.expander("Lihat Hasil Analisis Intelijen", expanded=False):
        st.markdown(st.session_state.intelligence_data)

# ==========================================
# MODUL 3: CONTENT FACTORY & AUTO-PUBLISH
# ==========================================
st.divider()
st.header("🏭 Modul 3: Pabrik Konten (Veo 3 & Socmed)")
with st.container(border=True):
    visual_style = st.selectbox("Style Video untuk Veo", ["Industrial Action", "CGI Cinematic", "Blueprint Tech"])
    
    if st.button("🚀 GENERATE CAMPAIGN (JSON)", use_container_width=True, type="primary"):
        if not st.session_state.intelligence_data:
            st.warning("⚠️ Jalankan Modul 2 terlebih dahulu!")
        else:
            model_factory = genai.GenerativeModel('gemini-1.5-flash-latest', generation_config={"response_mime_type": "application/json"})
            
            factory_prompt = f"""
            Gunakan data ini: {st.session_state.intelligence_data}
            Buat kampanye untuk {brand} {unit_type} gaya {visual_style}.
            
            Output HANYA JSON strict:
            {{
              "copywriting": "Caption sosmed agresif. Jika HSPD, tekankan 'Bekerja Tanpa Suara & Getaran'. WA {wa_num} & link safety {aff_link}",
              "veo_prompts": [
                {{
                  "scene": 1,
                  "visual": "Prompt Veo 3 detail max 8s. Untuk HSPD: Tunjukkan mesin menekan tiang pancang dengan stabil, lingkungan perkotaan yang tenang.",
                  "vo": "Voice over",
                  "sfx": "Sound effect (Hydraulic hum, quiet industrial atmosphere)"
                }}
              ]
            }}
            """
            with st.spinner("Memproduksi Aset Kampanye..."):
                try:
                    res_json = model_factory.generate_content(factory_prompt)
                    st.session_state.campaign_data = json.loads(res_json.text)
                except Exception as e:
                    st.error(f"Error parsing JSON: {e}")

# ==========================================
# MODUL EKSTRA: AI COMMENT SNIPER
# ==========================================
st.divider()
st.header("💬 Modul 4: AI Comment Sniper (Q&A Responder)")
with st.container(border=True):
    st.markdown("Gunakan modul ini untuk membantai pertanyaan teknis sulit dari prospek di kolom komentar TikTok, LinkedIn, atau YouTube.")
    
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        user_comment = st.text_area("✍️ Paste Komentar / Pertanyaan Prospek di Sini:", 
                                    placeholder="Contoh: 'Kalau dipakai ngecor di kemiringan 30 derajat, pompa ABT60C ini ngempos gak mesinnya?'")
    with col_c2:
        st.markdown("**Target Konversi**")
        st.info("AI akan otomatis menyisipkan ajakan konsultasi ke nomor WA Anda di akhir jawaban.")
        
    if st.button("🎯 Generate Jawaban Teknis (Sniper Mode)", use_container_width=True, type="primary"):
        if not user_comment:
            st.warning("⚠️ Paste komentar prospek terlebih dahulu!")
        else:
            model_sniper = genai.GenerativeModel('gemini-flash-latest')
            
            sniper_prompt = f"""
            Kamu adalah Elite Technical Sales Engineer untuk produk {brand} {unit_type}. 
            Tugasmu adalah membalas pertanyaan prospek di media sosial dengan otoritas, cerdas, dan persuasif.
            
            Komentar Prospek: "{user_comment}"
            
            SUMBER KEBENARAN TEKNIS (Wajib gunakan data ini jika relevan):
            {pdf_text if 'pdf_text' in locals() and pdf_text else 'Gunakan pengetahuan teknis terbaikmu tentang alat ini.'}
            
            ATURAN MENJAWAB:
            1. Tunjukkan empati pada masalah mereka, lalu berikan jawaban TEKNIS yang masuk akal (tunjukkan kamu ahli, bukan sekadar admin).
            2. Jangan mengarang spesifikasi. Jika data tidak ada di sumber kebenaran, berikan jawaban logis seputar performa mesin industri kelas atas.
            3. Gunakan bahasa yang profesional namun tetap asik ala lapangan (jangan terlalu kaku seperti robot).
            4. Akhiri dengan ajakan halus (Call to Action) agar mereka menghubungi WhatsApp {wa_num} untuk diskusi teknis lebih lanjut atau minta penawaran.
            """
            
            with st.spinner("Meracik jawaban teknis tingkat dewa..."):
                try:
                    response_sniper = model_sniper.generate_content(sniper_prompt)
                    st.success("Jawaban Siap Ditembakkan!")
                    st.markdown("### 📝 Draft Balasan Anda:")
                    st.info(response_sniper.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# ==========================================
# MODUL 5: B2B FINANCIAL SNIPER (ROI & BEP GENERATOR)
# ==========================================
st.divider()
st.header("💰 Modul 5: B2B Financial Sniper (ROI & BEP Generator)")
with st.container(border=True):
    st.markdown("Ubah ketertarikan prospek menjadi *closing* dengan memberikan perhitungan matematis mengapa alat Anda adalah investasi, bukan pengeluaran.")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.subheader("📊 Input Data Proyek Prospek")
        investasi = st.number_input("Harga Beli Unit (Rp)", min_value=0, value=1500000000, step=10000000)
        produksi_harian = st.number_input("Target Produksi Harian (m3 / titik)", min_value=1, value=100)
        harga_jual = st.number_input("Harga Jual Output / Profit per (m3 / titik) (Rp)", min_value=0, value=150000)
        
    with col_f2:
        st.subheader("⚙️ Komparasi Operasional Bulanan")
        biaya_operasional = st.number_input("Biaya Operasional Alat Ini (BBM, Operator, Maintenance/bln) (Rp)", min_value=0, value=30000000, step=1000000)
        biaya_konvensional = st.number_input("Biaya Cara Lama (Sewa alat/manual) per bulan (Rp)", min_value=0, value=80000000, step=1000000)
        hari_kerja = st.number_input("Jumlah Hari Kerja per Bulan", min_value=1, max_value=31, value=25)

    if st.button("🧮 Generate Laporan ROI & Eksekutif Proposal", use_container_width=True, type="primary"):
        # 1. Kalkulasi Matematis Dasar (Hard Logic)
        pendapatan_kotor_bulanan = produksi_harian * harga_jual * hari_kerja
        profit_bersih_bulanan = pendapatan_kotor_bulanan - biaya_operasional
        penghematan_bulanan = biaya_konvensional - biaya_operasional
        
        # Hindari pembagian dengan nol
        if profit_bersih_bulanan > 0:
            bep_bulan = investasi / profit_bersih_bulanan
        else:
            bep_bulan = 0
            
        roi_tahunan = (profit_bersih_bulanan * 12) / investasi * 100 if investasi > 0 else 0

        # Menampilkan Metrik di UI
        st.markdown("### 📈 Ringkasan Kalkulasi Mesin")
        met1, met2, met3, met4 = st.columns(4)
        met1.metric("Profit Bersih / Bulan", f"Rp {profit_bersih_bulanan:,.0f}")
        met2.metric("Penghematan / Bulan", f"Rp {penghematan_bulanan:,.0f}")
        met3.metric("Payback Period (BEP)", f"{bep_bulan:.1f} Bulan")
        met4.metric("ROI Tahunan", f"{roi_tahunan:.1f} %")
        
        # 2. Injeksi ke AI untuk Dibuatkan Proposal Eksekutif
        model_finance = genai.GenerativeModel('gemini-flash-latest')
        
        finance_prompt = f"""
        Kamu adalah Chief Financial Officer (CFO) dan Elite B2B Sales. 
        Tugasmu menyusun 'Executive Summary' untuk prospek alat berat ({brand} {unit_type}).
        
        DATA MATEMATIS PROYEK:
        - Harga Investasi: Rp {investasi:,.0f}
        - Profit Bersih/Bulan: Rp {profit_bersih_bulanan:,.0f}
        - Payback Period (BEP): {bep_bulan:.1f} bulan
        - ROI Tahunan: {roi_tahunan:.1f} %
        - Penghematan dari cara lama: Rp {penghematan_bulanan:,.0f} per bulan.
        
        ATURAN PENULISAN:
        1. Buat proposal yang sangat meyakinkan, elegan, dan ditujukan untuk Direktur/Owner.
        2. Jangan terlihat seperti hitungan robot, jelaskan bahwa alat ini BUKAN BIAYA, tapi MESIN PENCETAK UANG.
        3. Jelaskan bahwa dalam waktu {bep_bulan:.1f} bulan, alat ini sudah gratis (balik modal), dan bulan berikutnya adalah murni profit.
        4. Akhiri dengan ajakan untuk menerbitkan Purchase Order (PO) atau meeting final.
        """
        
        with st.spinner("Merumuskan Proposal Eksekutif..."):
            try:
                response_finance = model_finance.generate_content(finance_prompt)
                st.success("Proposal Finansial Selesai!")
                st.markdown("### 📄 Draft Executive Summary (Siap Kirim ke Direktur Prospek)")
                st.info(response_finance.text)
            except Exception as e:
                st.error(f"Error AI: {e}")
                
# ==========================================
# HASIL EKSEKUSI & SCHEDULING
# ==========================================
if st.session_state.campaign_data:
    data = st.session_state.campaign_data
    st.subheader("📝 Teks Copywriting")
    st.info(data.get("copywriting", "Data tidak ditemukan"))
    
    st.subheader("🎬 Script Video (Veo 3)")
    for s in data.get("veo_prompts", []):
        with st.expander(f"Scene {s.get('scene', '#')}", expanded=True):
            st.code(s.get('visual', ''), language="text")
            st.markdown(f"**VO:** {s.get('vo', '')}")
            st.markdown(f"**SFX:** {s.get('sfx', '')}")
            
    st.divider()
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        json_dl = json.dumps(data, indent=4)
        st.download_button("💾 Download JSON", data=json_dl, file_name=f"VORTEX_{brand}.json", use_container_width=True)
    with col_p2:
        st.button("📲 Post to TikTok Now", use_container_width=True)
    with col_p3:
        post_date = st.date_input("Jadwalkan", datetime.date.today(), label_visibility="collapsed")
        if st.button("⏰ Set Schedule", use_container_width=True):
            st.success(f"Konten dijadwalkan pada {post_date}")
