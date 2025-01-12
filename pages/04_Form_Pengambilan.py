# Import Library
import datetime
import streamlit as st
from PIL import Image
import Array_Peminjam
import Array_Buku

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Menu Peminjaman Buku", page_icon="📖", layout="centered")

# Elemen Halaman Streamlit
st.title("📖 Menu Peminjaman Buku")

# Form untuk Scan QR Code
st.write("### Silakan Scan QR Code Anda:")
form_scan = st.form(key="form_scan_qr", clear_on_submit=True)
with form_scan:
    qr_code_input = st.text_input("Scan di sini:")
    scan_submitted = st.form_submit_button(label="Scan QR Code")

if scan_submitted:
    if not qr_code_input:
        st.error("QR Code tidak boleh kosong. Silakan coba lagi.")
    else:
        # Memeriksa validitas QR Code
        if qr_code_input in Array_Peminjam.key_peminjam:
            index_peminjam = Array_Peminjam.key_peminjam.index(qr_code_input)
            data_peminjam = Array_Peminjam.peminjam[index_peminjam]

            # Menampilkan informasi peminjam
            st.write("### Data Peminjam:")
            st.write(f"**ID Peminjaman:** {data_peminjam[0]}")
            st.write(f"**Nama Peminjam:** {data_peminjam[1]}")
            st.write(f"**Judul Buku:** {data_peminjam[2]}")
            st.write(f"**Tanggal Pinjam:** {data_peminjam[3]}")
            st.write(f"**Tanggal Kembali:** {data_peminjam[4]}")

            # Menampilkan gambar buku
            image_path = Array_Buku.buku[data_peminjam[6]][0]
            image = Image.open(image_path)
            st.image(image, caption=f"Tersedia: {Array_Buku.buku[data_peminjam[6]][1]} Buku")
        else:
            st.error("Data tidak ditemukan. QR Code tidak valid.")

# Form untuk Peminjaman Buku
st.write("### Proses Peminjaman Buku:")
form_borrow = st.form(key="form_borrow_book", clear_on_submit=False)
with form_borrow:
    borrow_submitted = st.form_submit_button(label="Serahkan Buku")

if borrow_submitted:
    if not qr_code_input:
        st.error("Silakan scan QR Code terlebih dahulu.")
    else:
        # Memproses data peminjaman
        id_peminjam = str(qr_code_input.split(" - ")[0])
        judul_buku = str(qr_code_input.split(" - ")[2])

        # Mencari indeks data peminjam dan buku
        index_peminjam = next((i for i, sublist in enumerate(Array_Peminjam.peminjam) if id_peminjam in sublist), None)
        index_buku = next((i for i, sublist in enumerate(Array_Buku.buku) if judul_buku in sublist), None)

        if index_buku is not None and Array_Buku.buku[index_buku][1] == 0:
            st.error("Maaf, buku yang Anda pilih sedang tidak tersedia.")
        elif index_peminjam is not None and Array_Peminjam.peminjam[index_peminjam][5] == 1:
            st.error("QR Code sudah digunakan.")
        else:
            # Update data peminjaman
            Array_Peminjam.peminjam[index_peminjam][5] = 1
            Array_Buku.buku[index_buku][1] -= 1
            st.success("Buku berhasil dipinjam.")
