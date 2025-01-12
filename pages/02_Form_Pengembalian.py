# Import Library
import datetime
import streamlit as st
from PIL import Image
import Array_Peminjam
import Array_Buku

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Menu Pengembalian Buku", page_icon="📄", layout="centered")

# Elemen Halaman Streamlit
st.title("📄 Menu Pengembalian Buku")
st.write("Silakan scan QR Code Anda untuk memproses pengembalian buku.")

# Input Form untuk Scan QR Code
form_qr = st.form(key="form_scan_qr", clear_on_submit=True)
with form_qr:
    qr_code_input = st.text_input("Scan QR Code di sini:")
    scan_submitted = st.form_submit_button(label="Scan QR Code")

if scan_submitted:
    if not qr_code_input:
        st.error("QR Code tidak boleh kosong. Silakan coba lagi.")
    else:
        # Memeriksa apakah QR Code valid
        if qr_code_input in Array_Peminjam.key_peminjam:
            index_peminjam = Array_Peminjam.key_peminjam.index(qr_code_input)
            data_peminjam = Array_Peminjam.peminjam[index_peminjam]

            # Menampilkan informasi peminjam
            st.write("### Data Peminjaman:")
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

# Input Form untuk Pengembalian Buku
form_return = st.form(key="form_return_book", clear_on_submit=False)
with form_return:
    tgl_deadline = st.date_input("Tanggal Deadline Pengembalian:")
    return_submitted = st.form_submit_button(label="Kembalikan Buku")

if return_submitted:
    if not qr_code_input:
        st.error("Silakan scan QR Code terlebih dahulu.")
    elif qr_code_input in Array_Peminjam.key_peminjam:
        index_peminjam = Array_Peminjam.key_peminjam.index(qr_code_input)
        data_peminjam = Array_Peminjam.peminjam[index_peminjam]

        # Menghitung denda
        tgl_kembali_asli = datetime.datetime.strptime(data_peminjam[4], "%Y-%m-%d").date()
        selisih_hari = (tgl_deadline - tgl_kembali_asli).days
        denda = max(0, selisih_hari * 5000)

        # Update data buku
        index_buku = data_peminjam[6]
        Array_Buku.buku[index_buku][1] += 1

        # Menghapus data peminjam
        Array_Peminjam.peminjam.pop(index_peminjam)
        Array_Peminjam.key_peminjam.pop(index_peminjam)

        # Menampilkan hasil
        if denda == 0:
            st.success("Terima kasih sudah mengembalikan buku tepat waktu! 🎉")
            st.balloons()
        else:
            st.warning(f"Anda terlambat {selisih_hari} hari. Harap membayar denda sebesar Rp {denda}.")
    else:
        st.error("Data peminjaman tidak valid. Silakan scan ulang QR Code Anda.")
