import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Inisialisasi atau buat data.csv jika belum ada
if not os.path.exists("data.csv"):
    df_init = pd.DataFrame(columns=["tanggal", "angka"])
    df_init.to_csv("data.csv", index=False)

def generate_features(angka):
    angka_str = str(angka).zfill(4)
    digits = [int(d) for d in angka_str]
    ganjil_genap = [d % 2 for d in digits]
    besar_kecil = [1 if d >= 5 else 0 for d in digits]
    silang_homo = [1 if digits[0] % 2 != digits[1] % 2 else 0]
    tengah_tepi = [1 if digits[1] in [4,5,6] or digits[2] in [4,5,6] else 0]
    kembang_kempis = [1 if digits[2] > digits[1] else 0]
    return digits + ganjil_genap + besar_kecil + silang_homo + tengah_tepi + kembang_kempis

def predict_next_number(data):
    if len(data) < 10:
        return np.random.randint(1000, 9999)
    data["angka"] = data["angka"].astype(str).str.zfill(4).astype(int)
    data["fitur"] = data["angka"].apply(generate_features)
    X = np.vstack(data["fitur"].values[:-1])
    y = np.array([int(str(x).zfill(4)) for x in data["angka"].values[1:]])
    model = LinearRegression()
    model.fit(X, y)
    pred = model.predict([generate_features(data.iloc[-1]["angka"])])
    return int(str(int(pred[0]))[-4:])

def get_shio(tahun):
    shio_list = ["Kambing", "Monyet", "Ayam", "Anjing", "Babi", "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular", "Kuda"]
    angka_shio = [52, 30, 28, 46, 16, 19, 37, 24, 18, 12, 14, 25]
    index = tahun % 12
    return shio_list[index], angka_shio[index]

def display_kombinasi(angka):
    angka_str = str(angka).zfill(4)
    digits = [int(d) for d in angka_str]
    as_digit, kop_digit, kepala_digit, ekor_digit = digits
    kombinasi = {
        "As": as_digit,
        "Kop": kop_digit,
        "Kepala": kepala_digit,
        "Ekor": ekor_digit,
        "Ganjil/Genap": ["Ganjil" if d%2 else "Genap" for d in digits],
        "Besar/Kecil": ["Besar" if d >= 5 else "Kecil" for d in digits],
        "Silang/Homo": "Silang" if as_digit%2 != kop_digit%2 else "Homo",
        "Tengah/Tepi": "Tengah" if kop_digit in [4,5,6] or kepala_digit in [4,5,6] else "Tepi",
        "Kembang/Kempis": "Kembang" if kepala_digit > kop_digit else "Kempis"
    }
    return kombinasi

st.set_page_config(page_title="Prediksi 4D AI + Shio + Kombinasi", layout="centered")
st.title("🔮 Prediksi Angka 4D\nAI + Shio + Kombinasi")

today = st.date_input("Tanggal Hari Ini", datetime.date.today())
tahun_lahir = st.number_input("Tahun Lahir Anda", min_value=1900, max_value=2100, step=1, value=2000)

if st.button("🔢 Prediksi Angka 4D"):
    data = pd.read_csv("data.csv")
    prediksi = predict_next_number(data)
    st.success(f"🎯 Prediksi Angka 4D: {str(prediksi).zfill(4)}")

    shio_nama, shio_angka = get_shio(tahun_lahir)
    st.info(f"🐲 Shio Anda: {shio_nama} (Angka: {shio_angka})")

    kombinasi = display_kombinasi(prediksi)
    with st.expander("🔍 Logika Kombinasi Angka"):
        for k,v in kombinasi.items():
            st.write(f"{k}: {v}")

st.markdown("---")
st.subheader("📥 Input Angka Real untuk Latihan Ulang")
angka_real = st.text_input("Masukkan Angka Real 4D (jika ada)")
if st.button("Latih Ulang AI") and angka_real:
    df = pd.read_csv("data.csv")
    df = pd.concat([df, pd.DataFrame({"tanggal":[str(today)], "angka":[angka_real]})], ignore_index=True)
    df.to_csv("data.csv", index=False)
    st.success("Model telah diperbarui dengan data baru.")

st.markdown("---")
st.subheader("📊 30 Angka Real Terakhir")
data = pd.read_csv("data.csv")
if len(data) > 0:
    st.dataframe(data.tail(30))
else:
    st.write("Belum ada data angka real.")

