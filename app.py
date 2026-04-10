import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="VORTEX: Master Domination Engine", layout="wide")

st.title("🌪️ VORTEX: Marketing & Content Domination Engine")
st.caption("Intelligence-Driven Content Factory for Heavy Equipment")

# --- Konfigurasi API ---
with st.sidebar:
    st.header("⚙️ Konfigurasi Sistem")
    api_key = st.text_input("Masukkan Gemini API Key", type="password")
    
    st.divider()
    st.markdown("**Monetization Link**")
    whatsapp_number = st.text_input("Nomor WhatsApp Sales", "+6281230857759")
    affiliate_link = st.text_input("Link Shopee Affiliate (Tools/Safety)", "https://shope.ee/...")

# --- State Management untuk menyimpan data antar Modul ---
if "intelligence_data" not in st.session_state:
    st.session_state.intelligence_data = ""

# ==========================================
# MODUL 1: THE INTELLIGENCE WEAPON
# ==========================================
st.header("🎯 Modul 1: Intelijen Data (The Weapon)")
with st.expander("Buka Radar Intelijen Pasar", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        brand = st.selectbox("Merek", ["AIMIX", "Tatsuo"])
        unit_type = st.text_input("Tipe Unit", "Self Loading Mixer + ABT60C")
    with col2:
        project_scenario = st.text_area("Skenario Proyek / Kondisi Lapangan", 
                                        "Proyek infrastruktur pelosok di Kalimantan, akses jalan sempit, sering hujan, dan tanah berlumpur.")

    if st.button("Analisis Sudut Serang (Marketing Angle)"):
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            intelligence_prompt = f"""
            Kamu adalah Ahli Intelijen Pasar Alat Berat. Analisis skenario berikut untuk produk {brand} {unit_type}.
            Kondisi Lapangan: {project_scenario}
            
            Hasilkan analisis tajam dalam format ini:
            1. Pain Points Utama Kontraktor (3 poin)
            2. Solusi Ekstrem yang ditawarkan alat ini (3 poin)
            3. Killer Marketing Angle (1 kalimat penawaran yang tidak bisa ditolak)
            """
            
            with st.spinner("Memindai data pasar dan psikologi kontraktor..."):
                response = model.generate_content(intelligence_prompt)
                st.session_state.intelligence_data = response.text
                st.success("Analisis Intelijen Selesai!")
                st.markdown(st.session_state.intelligence_data)
        else:
            st.error("API Key belum dimasukkan!")

st.divider()

# ==========================================
# MODUL 2: THE CONTENT FACTORY
# ==========================================
st.header("🏭 Modul 2: Pabrik Konten (The Executor)")
with st.expander("Buka Mesin Eksekusi Visual & Copy", expanded=True):
    visual_style = st.selectbox("Pilih Gaya Visual untuk Veo 3", 
                                ["Hyper-Realistic Documentary", "CGI Cinematic", "Industrial Blueprint"])
    
    if st.button("Generate Eksekusi Kampanye Maksimal"):
        if st.session_state.intelligence_data == "":
            st.warning("Jalankan Modul Intelijen terlebih dahulu!")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            factory_prompt = f"""
            Kamu adalah AI Content Factory tingkat lanjut. Gunakan Data Intelijen ini:
            {st.session_state.intelligence_data}
            
            Buatlah paket kampanye lengkap untuk produk {brand} dengan gaya visual {visual_style}.
            
            Keluarkan output dalam format JSON strict seperti ini:
            {{
              "copywriting": "Teks caption sosmed yang agresif, menyorot pain point, dan berujung pada Call to Action menghubungi WhatsApp {whatsapp_number} atau membeli alat safety via link {affiliate_link}",
              "veo_video_prompts": [
                {{
                  "scene_no": 1,
                  "visual_prompt": "Deskripsi visual sangat detail max 8 detik untuk Veo 3. Pertahankan konsistensi warna alat.",
                  "narator_vo": "Teks voice over",
                  "sfx": "Efek suara"
                }},
                // lanjutkan hingga 4 scene yang membangun cerita dari masalah ke solusi
              ]
            }}
            """
            
            with st.spinner("Memproduksi JSON Video Prompts dan Copywriting..."):
                response = model.generate_content(factory_prompt)
                clean_json = response.text.replace('```json', '').replace('```', '')
                
                try:
                    result_data = json.loads(clean_json)
                    st.subheader("📝 Copywriting Siap Posting")
                    st.info(result_data["copywriting"])
                    
                    st.subheader("🎬 Sequence Video Veo 3 (JSON)")
                    st.json(result_data["veo_video_prompts"])
                except Exception as e:
                    st.error("Terjadi kesalahan parsing JSON. Output mentah:")
                    st.write(response.text)
