#Import Libary
import streamlit as st
from PIL import Image
from Array_Buku import buku

#Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Home Page", page_icon="📚", layout="centered")

#Elemen Halaman Streamlit
st.title("📚Selamat Datang Di Perpustakaan Nasional.")
st.write("Berikut ini adalah daftar buku yang tersedia di perpustakaan kami")

# Membuat kolom untuk menampilkan cover buku
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(1)

i = 0
for col in row1 + row2 + row3 + row4:
    with col:
        st.image(Image.open(buku[i][0]), width=200)
        st.write("Tersedia " + str(buku[i][1]) + " Buku")
        if st.button("Detail Buku " + str(i + 1)):
            st.write(str(buku[i][2]))
    i += 1