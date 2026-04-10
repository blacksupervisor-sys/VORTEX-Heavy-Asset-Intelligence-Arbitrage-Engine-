import streamlit as st
import google.generativeai as genai
import json
import PyPDF2
from PIL import Image  # Tambahan library untuk membaca file gambar

# ==========================================
# KONFIGURASI HALAMAN & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="VORTEX: Master Domination Engine", page_icon="🌪️", layout="wide")

if "intelligence_data" not in st.session_state:
    st.session_state.intelligence_data = ""
if "campaign_data" not in st.session_state:
    st.session_state.campaign_data = None

# ==========================================
# SIDEBAR: SETTING MESIN & MONETISASI
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/engineering.png", width=80)
    st.title("⚙️ VORTEX Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    
    st.divider()
    st.markdown("**Corong Konversi (Funnel)**")
    whatsapp_number = st.text_input("Nomor WhatsApp Sales", "+6281230857759")
    affiliate_link = st.text_input("Link Shopee Affiliate", "https://shope.ee/...")
    
    st.divider()
    st.caption("Developed for Heavy-Asset Domination | by Adjie")

st.title("🌪️ VORTEX Engine")
st.subheader("Intelligence-Driven Content Factory for Heavy Equipment")

# ==========================================
# MODUL 1: THE INTELLIGENCE WEAPON
# ==========================================
st.header("🎯 Modul 1: Radar Intelijen & Visual Ekstraksi")
with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.selectbox("Merek Produk", ["AIMIX", "Tatsuo"])
        unit_type = st.text_input("Tipe Unit", "Self Loading Mixer + ABT60C")
        
        # FITUR BARU: Menerima PDF, PNG, JPG, JPEG
        st.markdown("**Bahan Bakar Spesifikasi (PDF/Image)**")
        uploaded_file = st.file_uploader("Unggah Brosur / Technical Spec", type=["pdf", "png", "jpg", "jpeg"])
        
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
                # Membaca gambar menggunakan PIL
                image_data = Image.open(uploaded_file)
                st.image(image_data, caption="Visual Data Injected", use_container_width=True)
                st.success("🖼️ Gambar Brosur berhasil diserap oleh Mata AI!")

    with col2:
        project_scenario = st.text_area("Skenario Proyek / Kondisi Lapangan", 
                                        "Proyek infrastruktur dan tambang di area Kaltim, akses jalan tanah liat yang licin saat hujan, jarak cor jauh, butuh efisiensi waktu tinggi.")

    if st.button("🔍 Analisis Sudut Serang (Marketing Angle)", use_container_width=True, type="primary"):
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            intelligence_prompt = f"""
            Kamu adalah Ahli Intelijen Pasar Alat Berat dan Copywriter Kelas Kakap. 
            Tugasmu menganalisis skenario lapangan dan mencocokkannya dengan spesifikasi teknis alat.
            
            Produk: {brand} {unit_type}
            Kondisi Lapangan: {project_scenario}
            
            DATA SPESIFIKASI TEKNIS:
            "{pdf_text if pdf_text else 'Jika ada gambar yang dilampirkan, baca seluruh spesifikasi dari gambar tersebut. Jika tidak, gunakan pengetahuan umummu.'}"
            
            Hasilkan analisis dalam format teks yang rapi dan terstruktur:
            1. 🛑 Pain Points Utama Kontraktor di lapangan tersebut.
            2. ⚡ Solusi Ekstrem dari {brand} (berdasarkan spesifikasi di gambar/teks).
            3. 🎯 Killer Marketing Angle (Penawaran emosional dan logis).
            """
            
            # FITUR BARU: Menggabungkan teks dan gambar (Multimodal)
            prompt_contents = [intelligence_prompt]
            if image_data is not None:
                prompt_contents.append(image_data)
            
            with st.spinner("Memindai visual/dokumen teknis dan psikologi pasar..."):
                try:
                    response = model.generate_content(prompt_contents)
                    st.session_state.intelligence_data = response.text
                    st.success("Analisis Intelijen Selesai!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("⚠️ Masukkan Gemini API Key di sidebar terlebih dahulu!")

if st.session_state.intelligence_data:
    with st.expander("Lihat Hasil Analisis Intelijen", expanded=False):
        st.markdown(st.session_state.intelligence_data)

st.divider()

# ==========================================
# MODUL 2: THE CONTENT FACTORY
# ==========================================
st.header("🏭 Modul 2: Pabrik Konten & Veo 3 Injector")
with st.container(border=True):
    visual_style = st.selectbox("Pilih Gaya Visual untuk Video", 
                                ["CGI Cinematic (Hyper-realistic, Studio Lighting)", 
                                 "Industrial Action (Berdebu, Lumpur, Real-world)", 
                                 "Blueprint & Tech (Garis skematik, modern, profesional)"])
    
    if st.button("🚀 Generate Eksekusi Kampanye Maksimal", use_container_width=True, type="primary"):
        if st.session_state.intelligence_data == "":
            st.warning("⚠️ Jalankan Modul 1 terlebih dahulu untuk mendapatkan data intelijen!")
        elif not api_key:
            st.error("⚠️ Masukkan Gemini API Key di sidebar terlebih dahulu!")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro', generation_config={"response_mime_type": "application/json"})
            
            factory_prompt = f"""
            Kamu adalah AI Content Factory tingkat lanjut. Gunakan Data Intelijen ini:
            {st.session_state.intelligence_data}
            
            Buatlah paket kampanye lengkap untuk {brand} {unit_type} dengan gaya visual: {visual_style}.
            
            Keluarkan output HANYA dalam format JSON dengan struktur ini:
            {{
              "copywriting_caption": "Caption IG/TikTok/LinkedIn yang mematikan, hard-selling, gunakan hashtag. Akhiri dengan ajakan chat ke WhatsApp {whatsapp_number} atau cek perlengkapan proyek di {affiliate_link}",
              "veo_video_prompts": [
                {{
                  "scene_no": 1,
                  "visual_prompt": "Instruksi VEO 3: Deskripsi visual SANGAT DETAIL (Max 8s). Sebutkan pergerakan kamera (drone pan, close up tilt), pencahayaan, tekstur alat, dan lingkungan.",
                  "narator_vo": "Teks voice over singkat (bahasa Indonesia)",
                  "sfx": "Instruksi sound effect (misal: Heavy diesel engine rumble)"
                }}
                // Buat tepat 4 scene yang menyambung (Problem -> Agitate -> Solution -> Call to Action)
              ]
            }}
            """
            
            with st.spinner("Memproduksi JSON Video Prompts dan Copywriting (Membutuhkan 10-20 detik)..."):
                try:
                    response = model.generate_content(factory_prompt)
                    st.session_state.campaign_data = json.loads(response.text)
                except Exception as e:
                    st.error(f"Gagal memproses JSON: {e}")

# ==========================================
# HASIL EKSEKUSI (DISPLAY & DOWNLOAD)
# ==========================================
if st.session_state.campaign_data:
    data = st.session_state.campaign_data
    
    st.subheader("📝 1. Copywriting Sosial Media (Auto-Convert)")
    st.info(data.get("copywriting_caption", "Teks tidak ditemukan."))
    
    st.subheader("🎬 2. Script & Visual Prompt (Veo 3)")
    scenes = data.get("veo_video_prompts", [])
    
    for scene in scenes:
        with st.expander(f"Scene {scene['scene_no']}: {scene['narator_vo'][:30]}...", expanded=True):
            st.markdown(f"**🎥 Visual (Veo Prompt):** `{scene['visual_prompt']}`")
            st.markdown(f"**🎙️ Narasi (VO):** {scene['narator_vo']}")
            st.markdown(f"**🔊 SFX:** {scene['sfx']}")
            
    st.divider()
    json_string = json.dumps(data, indent=4)
    st.download_button(
        label="💾 Download Full Campaign (JSON)",
        file_name=f"VORTEX_{brand}_Campaign.json",
        mime="application/json",
        data=json_string,
        type="primary"
    )
