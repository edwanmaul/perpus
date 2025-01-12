# Import Library
import time
import datetime
import streamlit as st
import qrcode
from PIL import Image
from Array_Buku import buku
from Array_Peminjam import peminjam, key_peminjam

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Menu Peminjaman Buku",
    page_icon="📖",
    layout="centered"
)

# Inisialisasi Variabel
arynama, aryjudul, arytglpinjam, arytglkembali, aryaktif = [], [], [], [], []

# Elemen Halaman Streamlit
st.title("📖 Menu Peminjaman Buku")
st.write("Silahkan Masukkan Data Diri Anda")

# Form Input
form = st.form(key="form_peminjaman", clear_on_submit=False)
with form:
    # Input Data
    nama = st.text_input("Nama Lengkap:")
    judul = st.selectbox(
        'Pilih Judul Buku',
        ('', 
         '0 - As A Man Thinketh by James Allen',
         '1 - The Metamorphosis by Franz Kafka',
         '2 - 1984 by George Orwell',
         '3 - Manusia Setengah Salmon by Raditya Dika',
         '4 - Ubur-Ubur Lembur by Raditya Dika',
         '5 - Sang Pemimpi by Andrea Hirata',
         '6 - The Little Prince by Antonie De Saint-Exupery',
         '7 - The Laws Of Human Nature by Robert Greene',
         '8 - The Art Of Being Alone by Renuka Gavrani'
        )
    )
    tglpinjam = datetime.date.today()
    tglkembali = st.date_input("Tanggal Kembali:")
    
    # Batas maksimal pengembalian
    max_tglkembali = tglpinjam + datetime.timedelta(days=7)
    
    # Tombol Submit
    submitted = st.form_submit_button(label="Submit")
    
    if submitted:
        # Validasi Data
        if not nama:
            st.error("Nama lengkap harus diisi.")
        elif not judul:
            st.error("Pilih judul buku yang ingin dipinjam.")
        elif tglkembali > max_tglkembali:
            st.error("Tanggal kembali tidak boleh lebih dari 7 hari dari tanggal pinjam.")
        else:
            index = int(judul.split(" - ")[0]) 
            judul_buku = judul.split(" - ")[1] 

            if buku[index][1] == 0:  # Cek ketersediaan buku
                st.error("Maaf, buku yang Anda pilih sedang tidak tersedia.")
            else:
                # Kurangi jumlah buku
                buku[index][1] -= 1
                
                # Generate ID Peminjaman
                id_peminjaman = time.strftime("%d%m%y%H%M%S")
                
                # Tambahkan data ke array peminjam
                peminjam.append([
                    id_peminjaman,
                    nama,
                    judul_buku,
                    tglpinjam.strftime("%Y-%m-%d"),
                    tglkembali.strftime("%Y-%m-%d"),
                    '0',
                    index
                ])
                
                key_peminjam.append(f"{id_peminjaman} - {nama} - {judul_buku}")

                # Generate QR Code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4
                )
                qr.add_data(f"{id_peminjaman} - {nama} - {judul_buku}")
                qr.make(fit=True)
                img = qr.make_image(fill="black", back_color="white")
                img_path = f"qrcode-{id_peminjaman}.png"
                img.save(img_path)
                
                # Tampilkan QR Code
                qr_col1, qr_col2, qr_col3 = st.columns([1, 2, 1])
                with qr_col2:
                    st.image(img_path, caption="QR Code Peminjaman Buku")
                    st.write(f"ID Peminjaman: {id_peminjaman} - {nama} - {judul_buku}")
                
                st.success("Terima kasih telah meminjam buku di Perpustakaan Nasional!")
