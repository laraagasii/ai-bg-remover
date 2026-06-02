import streamlit as st
from PIL import Image
import io

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="✂️",
    layout="centered" # Membuat tampilan fokus di tengah (bagus untuk single-function app)
)

# ==========================================
# 2. HEADER APLIKASI
# ==========================================
st.title("✂️ AI Background Remover")
st.write("Aplikasi segmentasi citra otomatis berbasis Deep Learning (U2-Net) untuk menghapus latar belakang gambar secara instan.")
st.write("---")

# ==========================================
# 3. WIDGET UPLOAD GAMBAR
# ==========================================
file_diupload = st.file_uploader(
    "Unggah foto kamu di sini (Format: JPG, JPEG, PNG)", 
    type=["jpg", "jpeg", "png"]
)

# ==========================================
# 4. PROSES INTI (JALAN JIKA ADA GAMBAR)
# ==========================================
if file_diupload is not None:
    st.write("") # Kasih space sedikit
    
    # Buat 2 kolom berdampingan untuk komparasi Before vs After
    kolom1, kolom2 = st.columns(2)
    
    # Buka gambar yang diunggah
    gambar_asli = Image.open(file_diupload)
    
    # Kolom Kiri: Tampilkan Gambar Asli
    with kolom1:
        st.subheader("📷 Gambar Asli")
        st.image(gambar_asli, use_container_width=True)
        
    # Kolom Kanan: Proses AI & Tampilkan Hasil
    with kolom2:
        st.subheader("✨ Hasil Segmentasi")
        
        # Animasi loading saat model AI bekerja
        with st.spinner("AI sedang memotong background..."):
            try:
                # Import fungsi rembg di sini agar load aplikasi awal super cepat
                from rembg import remove
                
                # Eksekusi pemotongan background
                gambar_hasil = remove(gambar_asli)
                
                # Tampilkan hasil potongan transparan (.png)
                st.image(gambar_hasil, use_container_width=True)
                
                # Konversi hasil ke format bytes agar bisa di-download user
                buf = io.BytesIO()
                gambar_hasil.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # Tombol Download Hasil
                st.download_button(
                    label="📥 Unduh Gambar (.png)",
                    data=byte_im,
                    file_name="hasil_rembg_lara.png",
                    mime="image/png",
                    use_container_width=True # Membuat tombol full-width biar rapi
                )
                
            except Exception as e:
                st.error(f"Gagal memproses gambar: {str(e)}")