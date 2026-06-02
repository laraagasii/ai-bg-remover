import streamlit as st
from PIL import Image
import io

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="✂️",
    layout="centered"
)

# ==========================================
# 2. HEADER APLIKASI
# ==========================================
st.title("✂️ AI Background Remover")
st.write("Aplikasi segmentasi citra otomatis berbasis Deep Learning untuk menghapus latar belakang gambar secara instan.")
st.write("---")

# ==========================================
# 3. WIDGET UPLOAD GAMBAR
# ==========================================
file_diupload = st.file_uploader(
    "Unggah foto kamu di sini (Format: JPG, JPEG, PNG)", 
    type=["jpg", "jpeg", "png"]
)

# ==========================================
# 4. PROSES INTI
# ==========================================
if file_diupload is not None:
    st.write("") 
    
    kolom1, kolom2 = st.columns(2)
    gambar_asli = Image.open(file_diupload)
    
    with kolom1:
        st.subheader("📷 Gambar Asli")
        st.image(gambar_asli, use_container_width=True)
        
    with kolom2:
        st.subheader("✨ Hasil Segmentasi")
        
        with st.spinner("AI sedang memotong background... (Proses pertama mungkin memakan waktu 1-2 menit)"):
            try:
                from rembg import remove
                
                # OPTIMASI RAM: Jika gambar terlalu besar, kecilkan sementara untuk proses AI
                # Ini rahasia agar server Streamlit Cloud tidak crash (OOM)
                max_size = 1200
                if max(gambar_asli.size) > max_size:
                    gambar_proses = gambar_asli.copy()
                    gambar_proses.thumbnail((max_size, max_size))
                else:
                    gambar_proses = gambar_asli
                
                # Eksekusi pemotongan menggunakan gambar yang sudah dioptimasi ukurannya
                gambar_hasil = remove(gambar_proses)
                
                st.image(gambar_hasil, use_container_width=True)
                
                buf = io.BytesIO()
                gambar_hasil.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 Unduh Gambar (.png)",
                    data=byte_im,
                    file_name="hasil_rembg_lara.png",
                    mime="image/png",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Gagal memproses gambar. Silakan coba gambar dengan ukuran lebih kecil. Error: {str(e)}")