import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import math
from sklearn.linear_model import LinearRegression
from datetime import datetime

# ===== Konstanta File =====
DATA_FILE = "data.csv"
MODEL_FILE = "model.pkl"

# ===== Inisialisasi File CSV =====
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["angka", "tanggal", "jam"])
    df_init.to_csv(DATA_FILE, index=False)

# ===== Fungsi Fitur Numerik (Algoritma Logaritma) =====
def fitur_numerik(angka):
    angka_str = str(angka).zfill(4)
    as_, kop, kepala, ekor = map(int, angka_str)
    total = int(angka)
    return [
        as_, kop, kepala, ekor,
        total % 2,                  # Genap/Ganjil
        total >= 5000,             # Besar/Kecil
        int(as_ == ekor),          # Silang/Homo
        int(1 <= kop <= 8),        # Tengah/Tepi
        int(as_ > kop),            # Kembang/Kempis
        math.log10(total + 1)      # Logaritma
    ]

# ===== Model Training =====
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

def load_model():
    return joblib.load(MODEL_FILE) if os.path.exists(MODEL_FILE) else latih_model()

# ===== Prediksi Angka =====
def prediksi_angka(angka):
    model = load_model()
    if model is None:
        return []
    fitur = np.array(fitur_numerik(angka)).reshape(1, -1)
    hasil = model.predict(fitur)[0]
    top5 = [str(int(hasil + i)).zfill(4) for i in range(5)]
    return top5

# ===== Perhitungan Shio =====
shio_list = ["Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular", "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"]
shio_angka = {
    "Tikus": [2, 15, 28, 41], "Kerbau": [3, 16, 29, 42], "Macan": [4, 17, 30, 43],
    "Kelinci": [5, 18, 31, 44], "Naga": [6, 19, 32, 45], "Ular": [7, 20, 33, 46],
    "Kuda": [8, 21, 34, 47], "Kambing": [9, 22, 35, 48], "Monyet": [10, 23, 36, 49],
    "Ayam": [11, 24, 37], "Anjing": [12, 25, 38], "Babi": [1, 14, 27, 40]
}

def hitung_shio_tahunan(tahun):
    return shio_list[(tahun - 4) % 12]

def hitung_shio_harian(tanggal):
    try:
        tgl = datetime.strptime(tanggal, "%Y/%m/%d").date()
        return shio_list[tgl.toordinal() % 12]
    except:
        return "Format tanggal salah"

# ===== UI STREAMLIT =====
st.set_page_config(page_title="Prediksi AI 4D", layout="centered")
st.title("🔢 Prediksi Angka 4D AI Lengkap")
st.caption("Dengan AI, Logika Kombinasi, dan Perhitungan Shio")

# ===== Input Manual =====
angka_input = st.text_input("Masukkan Angka 4D Terakhir", max_chars=4)
tanggal_input = st.date_input("Tanggal", datetime.today())
jam_input = st.time_input("Jam", datetime.now().time())

# ===== Tombol Prediksi =====
if st.button("📥 Simpan dan Prediksi"):
    if angka_input and len(angka_input) == 4 and angka_input.isdigit():
        df = pd.read_csv(DATA_FILE)
        df.loc[len(df)] = [angka_input, tanggal_input, jam_input.strftime("%H:%M")]
        df.to_csv(DATA_FILE, index=False)

        top5 = prediksi_angka(angka_input)
        if top5:
            st.success(f"Top 5 Prediksi Angka 4D: {', '.join(top5)}")
        else:
            st.warning("Model belum cukup data untuk prediksi.")

        # ===== Tampilkan Fitur Kombinasi =====
        fitur = fitur_numerik(angka_input)
        label = ["As", "Kop", "Kepala", "Ekor", "Ganjil/Genap", "Besar/Kecil", "Silang/Homo", "Tengah/Tepi", "Kembang/Kempis", "Log(angka)"]
        st.subheader("🔍 Kombinasi Logika Angka")
        for i, val in enumerate(fitur):
            st.write(f"{label[i]}: {val}")
    else:
        st.error("Masukkan angka 4 digit yang valid.")

# ===== Latih Ulang Model =====
if st.button("🔁 Latih Ulang Model"):
    model = latih_model()
    if model:
        st.success("Model berhasil dilatih ulang!")
    else:
        st.warning("Belum cukup data untuk melatih model.")

# ===== Perhitungan Shio =====
st.subheader("🔮 Perhitungan Shio")

# Shio Tahunan
tahun_input = st.number_input("Masukkan Tahun (Shio Tahunan)", min_value=1900, max_value=2100, value=2025)
if st.button("🔮 Hitung Shio Tahunan"):
    nama_shio = hitung_shio_tahunan(int(tahun_input))
    angka_shio = shio_angka.get(nama_shio, [])
    st.info(f"Shio Tahun {tahun_input}: {nama_shio} → Angka: {angka_shio}")

# Shio Harian
tanggal_sh = st.text_input("Masukkan Tanggal (YYYY/MM/DD) untuk Shio Harian", value="2025/07/17")
if st.button("🔮 Hitung Shio Harian"):
    shio_hari = hitung_shio_harian(tanggal_sh)
    st.success(f"Shio Harian {tanggal_sh}: {shio_hari} → Angka: {shio_angka.get(shio_hari, [])}")
