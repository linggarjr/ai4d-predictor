import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Prediksi Angka 4D AI")
st.write("Gunakan pembelajaran logaritma dan AI untuk prediksi angka 4 digit.")

# Masukkan angka terbaru manual
angka_terakhir = st.text_input("Masukkan Angka 4D Terakhir", "1234")
tanggal = st.date_input("Tanggal", datetime.today())
jam = st.time_input("Jam", datetime.now().time())

if st.button("Prediksi Angka 4D Berikutnya"):
    # Simulasi model AI, nanti diganti dengan model beneran
    prediksi = str((int(angka_terakhir) * 73) % 10000).zfill(4)
    st.success(f"Prediksi Angka 4D Berikutnya: {prediksi}")
