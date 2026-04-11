import streamlit as st
import google.generativeai as genai
import json
import PyPDF2
from PIL import Image
import datetime

# ==========================================
# KONFIGURASI HALAMAN & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="VORTEX 3.1: Ultimate Flash Engine", page_icon="🌪️", layout="wide")

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
    st.success("Model: gemini-1.5-flash-latest")
    st.success("Speed: Ultra-Fast")
    
    st.divider()
    st.subheader("🔗 Sales Funnel")
    wa_num = st.text_input("WhatsApp Sales", "+6281230857759")
    aff_link = st.text_input("Shopee Affiliate", "https://shope.ee/...")
    
    st.divider()
    st.caption("VORTEX 3.1 | Powered by Gemini Flash")

st.title("🌪️ VORTEX 3.1: Lightning Speed Domination")
st.subheader("Automated Radar, Intelligence, and Content Factory")

# ==========================================
# MODUL 1: RADAR CUACA & TENDER (LIVE INTEL)
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
            with st.spinner("Memindai berita proyek & LPSE dengan kecepatan Flash..."):
                # Menggunakan gemini-1.5-flash-latest
                model_radar = genai.GenerativeModel('gemini-1.5-flash-latest')
                res = model_radar.generate_content("Cari info singkat tren proyek infrastruktur atau tambang terbaru di Kalimantan Timur bulan ini. Buat dalam 2 paragraf singkat.")
                st.session_state.project_scenario = res.text
                st.success("Radar Tender Berhasil!")

if st.session_state.project_scenario or st.session_state.current_weather:
    with st.expander("📝 Hasil Scan Radar (Klik untuk Edit)", expanded=True):
        gabungan_radar = f"Kondisi Cuaca: {st.session_state.current_weather}\n\nKondisi Proyek: {st.session_state.project_scenario}"
        final_scenario = st.text_area("Final Scenario (Akan disuntikkan ke AI)", value=gabungan_radar, height=150)

# ==========================================
# MODUL 2: THE INTELLIGENCE WEAPON
# ==========================================
st.header("🎯 Modul 2: Ekstraksi Spesifikasi & Intelijen")
with st.container(border=True):
    col_u1, col_u2 = st.columns([1, 1])
    with col_u1:
        brand = st.selectbox("Merek Produk", ["AIMIX", "Tatsuo"])
        unit_type = st.text_input("Tipe Unit", "Self Loading Mixer + ABT60C")
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
                if extracted:
                    pdf_text += extracted
            st.success("📄 Dokumen PDF berhasil diserap!")
        elif file_extension in ['png', 'jpg', 'jpeg']:
            image_data = Image.open(uploaded_file)
            st.image(image_data, caption="Visual Data Injected", use_container_width=True)
            st.success("🖼️ Gambar Brosur berhasil diserap!")
        
    if st.button("🔍 Jalankan Analisis Intelijen", use_container_width=True, type="primary"):
        # Menggunakan gemini-1.5-flash-latest
        model_intel = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        intelligence_prompt = f"""
        Kamu adalah Ahli Intelijen Pasar Alat Berat. Analisis skenario lapangan dan cocokkan dengan spesifikasi alat.
        Produk: {brand} {unit_type}
        Skenario & Cuaca: {final_scenario if 'final_scenario' in locals() else 'Jalanan berlumpur, proyek dikebut'}
        
        DATA SPESIFIKASI:
        "{pdf_text if pdf_text else 'Baca dari gambar jika ada, atau gunakan pengetahuan umummu.'}"
        
        Output:
        1. Pain Points Utama
        2. Solusi Teknis Alat
        3. Killer Marketing Angle
        """
        
        prompt_contents = [intelligence_prompt]
        if image_data is not None: prompt_contents.append(image_data)
        
        with st.spinner("Memproses Analisis Intelijen..."):
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
            # Menggunakan gemini-1.5-flash-latest dengan format JSON Strict
            model_factory = genai.GenerativeModel('gemini-1.5-flash-latest', generation_config={"response_mime_type": "application/json"})
            
            factory_prompt = f"""
            Gunakan data ini: {st.session_state.intelligence_data}
            Buat kampanye untuk {brand} {unit_type} gaya {visual_style}.
            
            Output HANYA JSON strict:
            {{
              "copywriting": "Caption sosmed agresif, call to action ke WA {wa_num} & link alat safety {aff_link}",
              "veo_prompts": [
                {{
                  "scene": 1,
                  "visual": "Prompt Veo 3 detail max 8s",
                  "vo": "Voice over",
                  "sfx": "Sound effect"
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
    
    # Dashboard Auto-Publish (Simulasi UI)
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        json_dl = json.dumps(data, indent=4)
        st.download_button("💾 Download JSON", data=json_dl, file_name="Campaign.json", use_container_width=True)
    with col_p2:
        st.button("📲 Post to TikTok Now", use_container_width=True)
    with col_p3:
        post_date = st.date_input("Jadwalkan", datetime.date.today(), label_visibility="collapsed")
        if st.button("⏰ Set Schedule", use_container_width=True):
            st.success(f"Konten siap diluncurkan pada {post_date}")
