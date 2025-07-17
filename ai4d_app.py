import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os
import math
from datetime import datetime

# Inisialisasi file data dan model
DATA_FILE = "data.csv"
MODEL_FILE = "model.pkl"

# Buat file data jika belum ada
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["angka", "tanggal", "jam"])
    df.to_csv(DATA_FILE, index=False)

# Konversi angka 4D ke fitur numerik
def fitur_numerik(angka):
    return [
        int(angka[0]),              # As
        int(angka[1]),              # Kop
        int(angka[2]),              # Kepala
        int(angka[3]),              # Ekor
        int(angka) % 2,             # Genap/Ganjil
        int(angka) >= 5000,         # Besar/Kecil
        math.log10(int(angka) + 1)  # logaritma
    ]

# Fungsi melatih model AI
def latih_model():
    df = pd.read_csv(DATA_FILE)
    if len(df) < 10:
        return None
    X = np.array([fitur_numerik(str(a).zfill(4)) for a in df["angka"]])
    y = np.roll(df["angka"].values, -1)
    model = LinearRegression()
    model.fit(X[:-1], y[:-1])
    joblib.dump(model, MODEL_FILE)
    return model

# Fungsi load model
def load_model():
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    else:
        return latih_model()

# Fungsi prediksi
def prediksi_angka(angka):
    model = load_model()
    if model is None:
        return "Model belum cukup data"
    fitur = np.array(fitur_numerik(str(angka).zfill(4))).reshape(1, -1)
    hasil = model.predict(fitur)[0]
    return str(int(hasil)).zfill(4)

# Fungsi Shio
def hitung_shio_tahunan(tahun):
    daftar_shio = [
        "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular",
        "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"
    ]
    return daftar_shio[(tahun - 4) % 12]

def hitung_shio_harian(tanggal):
    try:
        tanggal_obj = datetime.strptime(tanggal, "%Y/%m/%d").date()
    except:
        return "Format tanggal salah. Gunakan format: YYYY/MM/DD"
    daftar_shio = [
        "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular",
        "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"
    ]
    return daftar_shio[tanggal_obj.toordinal() % 12]

# ============ UI STREAMLIT ============ #
st.title("🔢 Prediksi Angka 4D AI")
st.write("Gunakan pembelajaran logaritma dan AI untuk prediksi angka 4 digit.")

# Input pengguna
angka_input = st.text_input("Masukkan Angka 4D Terakhir", max_chars=4)
tanggal_input_4d = st.date_input("Tanggal", datetime.today())
jam_input = st.time_input("Jam", datetime.now().time())

# Tombol Prediksi
if st.button("📈 Prediksi Angka 4D Berikutnya", key="btn_prediksi"):
    if angka_input and len(angka_input) == 4 and angka_input.isdigit():
        prediksi = prediksi_angka(angka_input)
        st.success(f"Prediksi Angka 4D Berikutnya: {prediksi}")

        # Simpan data ke CSV
        df = pd.read_csv(DATA_FILE)
        df.loc[len(df.index)] = [angka_input, tanggal_input_4d, jam_input.strftime("%H:%M")]
        df.to_csv(DATA_FILE, index=False)
    else:
        st.error("Masukkan angka 4 digit yang valid.")

# Tombol Latih ulang model
if st.button("🔁 Latih Ulang Model (Jika Salah)", key="btn_latih_ulang"):
    model = latih_model()
    if model:
        st.success("Model berhasil dilatih ulang!")
    else:
        st.warning("Belum cukup data untuk melatih model.")

# ============ SHIO ============ #
st.subheader("🔮 Perhitungan Shio")

# Shio Tahunan
tahun_input = st.number_input("Masukkan Tahun untuk hitung Shio Tahunan", min_value=1900, max_value=2100, value=2025, key="tahun_shio_input")
if st.button("🔮 Hitung Shio Tahunan", key="btn_shio_tahunan"):
    shio = hitung_shio_tahunan(int(tahun_input))
    st.info(f"Shio Tahun {tahun_input}: {shio}")

# Shio Harian
tanggal_shio_input = st.text_input("Masukkan Tanggal untuk Hitung Shio Harian (format: YYYY/MM/DD)", value="2025/07/17", key="tanggal_shio_input")
if st.button("🔮 Hitung Shio Harian", key="btn_shio_harian"):
    shio_hari = hitung_shio_harian(tanggal_shio_input)
    st.success(f"Shio Harian untuk {tanggal_shio_input}: {shio_hari}")
