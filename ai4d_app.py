import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import math
from datetime import datetime
from sklearn.linear_model import LinearRegression

# ====== Konstanta dan File ======
DATA_FILE = "data.csv"
MODEL_FILE = "model.pkl"

# ====== Inisialisasi File Data ======
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["angka", "tanggal", "jam"])
    df.to_csv(DATA_FILE, index=False)

# ====== Fungsi Ekstraksi Fitur Angka ======
def fitur_numerik(angka):
    angka_str = str(angka).zfill(4)
    as_, kop, kepala, ekor = map(int, angka_str)
    total = int(angka_str)
    return [
        as_, kop, kepala, ekor,
        total % 2,                  # Genap/Ganjil
        int(total >= 5000),        # Besar/Kecil
        int(as_ == ekor),          # Silang/Homo
        int(1 <= kop <= 8),        # Tengah/Tepi
        int(as_ > kop),            # Kembang/Kempis
        round(math.log10(total + 1), 4)  # Logaritma
    ]

# ====== Fungsi Pelatihan Model ======
def latih_model():
    df = pd.read_csv(DATA_FILE)
    if len(df) < 10:
        return None
    X = np.array([fitur_numerik(a) for a in df["angka"]])
    y = np.roll(df["angka"].values, -1)
    model = LinearRegression()
    model.fit(X[:-1], y[:-1])
    joblib.dump(model, MODEL_FILE)
    return model

# ====== Fungsi Load Model ======
def load_model():
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    else:
        return latih_model()

# ====== Fungsi Prediksi ======
def prediksi_angka(angka):
    model = load_model()
    if model is None:
        return "Model belum cukup data"
    fitur = np.array(fitur_numerik(angka)).reshape(1, -1)
    hasil = model.predict(fitur)[0]
    hasil_bulat = max(0, min(9999, int(round(hasil))))
    return str(hasil_bulat).zfill(4)

# ====== Fungsi Shio ======
shio_list = [
    "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular",
    "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"
]
shio_angka = {
    "Tikus": [2, 15, 28, 41], "Kerbau": [3, 16, 29, 42],
    "Macan": [4, 17, 30, 43], "Kelinci": [5, 18, 31, 44],
    "Naga": [6, 19, 32, 45], "Ular": [7, 20, 33, 46],
    "Kuda": [8, 21, 34, 47], "Kambing": [9, 22, 35, 48],
    "Monyet": [10, 23, 36, 49], "Ayam": [11, 24, 37],
    "Anjing": [12, 25, 38], "Babi": [1, 14, 27, 40]
}

def hitung_shio_tahunan(tahun):
    nama = shio_list[(tahun - 4) % 12]
    return nama, shio_angka.get(nama, [])

def hitung_shio_harian(tanggal):
    try:
        tgl = datetime.strptime(tanggal, "%Y/%m/%d").date()
        nama = shio_list[tgl.toordinal() % 12]
        return nama, shio_angka.get(nama, [])
    except:
        return "Format salah", []

# ====== UI STREAMLIT ======
st.set_page_config(page_title="Prediksi AI 4D", layout="centered")
st.title("🔢 Prediksi Angka 4D AI Lengkap")
st.caption("Dengan AI, Logika Kombinasi, dan Perhitungan Shio")

# ====== Input Manual Data Real ======
st.subheader("📝 Input Angka Real")
angka_input = st.text_input("Masukkan Angka 4D Terakhir", max_chars=4)
tanggal_input = st.date_input("Tanggal", datetime.today())
jam_input = st.time_input("Jam", datetime.now().time())

if st.button("💾 Simpan Angka Real"):
    if angka_input and len(angka_input) == 4 and angka_input.isdigit():
        df = pd.read_csv(DATA_FILE)
        df.loc[len(df.index)] = [angka_input, tanggal_input, jam_input.strftime("%H:%M")]
        df.to_csv(DATA_FILE, index=False)
        st.success("Data angka real berhasil disimpan!")
    else:
        st.error("Masukkan angka 4 digit valid.")

# ====== Prediksi Angka Berikutnya ======
if st.button("📈 Prediksi Angka 4D Berikutnya"):
    if angka_input and len(angka_input) == 4 and angka_input.isdigit():
        hasil = prediksi_angka(angka_input)
        st.success(f"Prediksi AI: {hasil}")

        fitur = fitur_numerik(hasil)
        label = ["As", "Kop", "Kepala", "Ekor", "Ganjil/Genap", "Besar/Kecil",
                 "Silang/Homo", "Tengah/Tepi", "Kembang/Kempis", "Log(angka)"]
        st.subheader("🔍 Logika Kombinasi Prediksi")
        for i, val in enumerate(fitur):
            st.write(f"{label[i]}: {val}")
    else:
        st.error("Masukkan angka 4 digit valid terlebih dahulu.")

# ====== Latih Ulang Model ======
if st.button("🔁 Latih Ulang Model"):
    model = latih_model()
    if model:
        st.success("Model berhasil dilatih ulang!")
    else:
        st.warning("Belum cukup data untuk melatih model.")

# ====== Perhitungan Shio ======
st.subheader("🔮 Perhitungan Shio")
tahun_input = st.number_input("Masukkan Tahun", min_value=1900, max_value=2100, value=2025)
if st.button("🔮 Hitung Shio Tahunan"):
    nama, kode = hitung_shio_tahunan(int(tahun_input))
    st.info(f"Shio Tahun {tahun_input}: {nama} ({kode})")

tanggal_sh = st.text_input("Masukkan Tanggal (YYYY/MM/DD)", value="2025/07/17")
if st.button("🔮 Hitung Shio Harian"):
    nama, kode = hitung_shio_harian(tanggal_sh)
    st.success(f"Shio Harian: {nama} ({kode})")

# ====== Tampilkan 30 Angka Real Terakhir ======
st.subheader("📜 30 Angka Real Terakhir")
try:
    df = pd.read_csv(DATA_FILE)
    df_sorted = df.sort_values(by="tanggal", ascending=False).head(30)
    st.dataframe(df_sorted)
except:
    st.warning("Belum ada data yang tersimpan.")
