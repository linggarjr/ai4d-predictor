import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ===================== SETUP FILE =====================
DATA_FILE = 'data.csv'
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['angka', 'tanggal', 'jam'])
    df.to_csv(DATA_FILE, index=False)

# ===================== UTILITAS =====================
def get_shio_info(tahun_lahir):
    shio_list = [
        ("Monyet", [0, 12, 24]),
        ("Ayam", [1, 13, 25]),
        ("Anjing", [2, 14, 26]),
        ("Babi", [3, 15, 27]),
        ("Tikus", [4, 16, 28]),
        ("Kerbau", [5, 17, 29]),
        ("Macan", [6, 18, 30]),
        ("Kelinci", [7, 19, 31]),
        ("Naga", [8, 20]),
        ("Ular", [9, 21]),
        ("Kuda", [10, 22]),
        ("Kambing", [11, 23]),
    ]
    tahun_shio = tahun_lahir % 12
    for nama, angka in shio_list:
        if tahun_shio == angka[0]:
            return nama, angka
    return "Tidak diketahui", []

def kombinasi_logika(angka):
    str_angka = str(angka).zfill(4)
    digits = list(map(int, str_angka))
    ganjil_genap = ["Ganjil" if d % 2 else "Genap" for d in digits]
    besar_kecil = ["Besar" if d >= 5 else "Kecil" for d in digits]
    posisi = ["As", "Kop", "Kepala", "Ekor"]
    silang = "Silang" if len(set(digits)) == 4 else "Homo"
    tengah_tepi = "Tengah" if 1000 <= angka <= 8999 else "Tepi"
    kembang = "Kembang" if digits[0] < digits[-1] else "Kempis"
    return {
        "Ganjil/Genap": dict(zip(posisi, ganjil_genap)),
        "Besar/Kecil": dict(zip(posisi, besar_kecil)),
        "Silang/Homo": silang,
        "Tengah/Tepi": tengah_tepi,
        "Kembang/Kempis": kembang
    }

def latih_model():
    df = pd.read_csv(DATA_FILE)
    if len(df) < 10:
        return None
    df = df.dropna()
    X = []
    y = []
    for angka in df['angka']:
        fitur = extract_features(angka)
        X.append(fitur)
        y.append(int(str(angka).zfill(4)))
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    model = LinearRegression().fit(X, y)
    return model, scaler

def extract_features(angka):
    digits = list(map(int, str(angka).zfill(4)))
    total = sum(digits)
    unique_digits = len(set(digits))
    return digits + [total, unique_digits]

def prediksi_angka(model, scaler):
    if model is None:
        return random.randint(1000, 9999)
    sample = random.randint(1000, 9999)
    fitur = extract_features(sample)
    X = scaler.transform([fitur])
    pred = int(model.predict(X)[0])
    return int(str(pred).zfill(4)[-4:])

# ===================== ANTARMUKA =====================
st.title("🔮 AI + Shio + Kombinasi Prediksi 4D")

# Input tanggal dan tahun lahir
st.subheader("Tanggal Hari Ini")
tanggal_hari_ini = st.date_input("Tanggal Hari Ini", datetime.date.today())

st.subheader("Tahun Lahir Anda")
tahun_lahir = st.number_input("Masukkan Tahun Lahir", min_value=1900, max_value=2100, value=2000)

# Prediksi angka
st.subheader("Masukkan Angka untuk Prediksi (opsional)")
input_manual = st.text_input("Masukkan angka (4 digit) atau kosongkan untuk random:")

if st.button("🔢 Prediksi Angka 4D"):
    model_scaler = latih_model()
    model, scaler = model_scaler if model_scaler else (None, None)

    if input_manual and input_manual.isdigit() and len(input_manual) == 4:
        angka_prediksi = int(input_manual)
    else:
        angka_prediksi = prediksi_angka(model, scaler)

    st.success(f"🎯 Hasil Prediksi AI: **{angka_prediksi:04d}**")

    # Kombinasi logika
    logika = kombinasi_logika(angka_prediksi)
    st.subheader("🔍 Analisis Kombinasi Logika")
    st.json(logika)

    # Info shio
    nama_shio, angka_shio = get_shio_info(tahun_lahir)
    st.subheader("🐲 Shio Anda")
    st.write(f"Shio: **{nama_shio}** | Angka Shio: {', '.join(map(str, angka_shio))}")

# ===================== INPUT ANGKA REAL =====================
st.subheader("📥 Input Angka Real untuk Latihan Ulang")
angka_real = st.text_input("Masukkan Angka Real 4D (jika ada)")
if st.button("Latih Ulang AI"):
    if angka_real.isdigit() and len(angka_real) == 4:
        now = datetime.datetime.now()
        new_data = pd.DataFrame({
            'angka': [int(angka_real)],
            'tanggal': [now.date()],
            'jam': [now.strftime('%H:%M')]
        })
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Data berhasil disimpan dan AI dilatih ulang.")
    else:
        st.error("❌ Masukkan 4 digit angka yang valid.")

# ===================== TAMPILKAN 30 ANGKA REAL TERAKHIR =====================
if os.path.exists(DATA_FILE):
    st.subheader("📊 30 Angka Real Terakhir")
    df = pd.read_csv(DATA_FILE).tail(30)
    st.dataframe(df)
else:
    st.warning("Belum ada data yang tersedia.")

