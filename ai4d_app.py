import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

st.set_page_config(page_title="Prediksi Angka 4D AI + Shio + Kombinasi", layout="centered")
st.title("🔮 Prediksi Angka 4D\nAI + Shio + Kombinasi")

# --- Fungsi Shio ---
def hitung_shio_tahun(tahun):
    daftar_shio = ['Kambing', 'Monyet', 'Ayam', 'Anjing', 'Babi', 'Tikus', 'Kerbau', 'Macan', 'Kelinci', 'Naga', 'Ular', 'Kuda']
    return daftar_shio[tahun % 12]

def hitung_shio_harian(tanggal):
    hari = tanggal.day
    daftar_shio_harian = ['Tikus', 'Kerbau', 'Macan', 'Kelinci', 'Naga', 'Ular', 'Kuda', 'Kambing', 'Monyet', 'Ayam', 'Anjing', 'Babi']
    return daftar_shio_harian[hari % 12]

# --- Fungsi Kombinasi Logika Angka ---
def kombinasi_logika(angka):
    angka_str = str(angka).zfill(4)
    digits = [int(d) for d in angka_str]
    ganjil_genap = ['Ganjil' if d % 2 else 'Genap' for d in digits]
    besar_kecil = ['Besar' if d >= 5 else 'Kecil' for d in digits]
    posisi = ['As', 'Kop', 'Kepala', 'Ekor']
    silang_homo = 'Silang' if len(set(digits)) > 2 else 'Homo'
    tengah_tepi = 'Tengah' if 1 < digits[2] < 8 else 'Tepi'
    kembang_kempis = 'Kembang' if digits[0] < digits[-1] else 'Kempis'

    return {
        'Angka': angka_str,
        'Ganjil/Genap': ganjil_genap,
        'Besar/Kecil': besar_kecil,
        'Posisi': posisi,
        'Silang/Homo': silang_homo,
        'Tengah/Tepi': tengah_tepi,
        'Kembang/Kempis': kembang_kempis
    }

# --- Fungsi Prediksi ---
def load_data():
    if os.path.exists("data.csv"):
        return pd.read_csv("data.csv")
    else:
        df = pd.DataFrame(columns=['input1', 'input2', 'hasil'])
        df.to_csv("data.csv", index=False)
        return df

def simpan_data(input1, input2, hasil):
    df = load_data()
    df.loc[len(df)] = [input1, input2, hasil]
    df.to_csv("data.csv", index=False)

def latih_model():
    df = load_data()
    if len(df) < 10:
        return None
    X = df[['input1', 'input2']]
    y = df['hasil']
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, "model.pkl")
    return model

def prediksi_angka(model, input1, input2):
    prediksi = model.predict([[input1, input2]])[0]
    return int(str(int(abs(prediksi))).zfill(4)[-4:])

# --- Input User ---
tanggal_input = st.date_input("Tanggal Hari Ini", datetime.date.today())
tahun_lahir = st.number_input("Tahun Lahir Anda", min_value=1900, max_value=2100, value=2000, step=1)

# --- Tombol Prediksi ---
if st.button("\ud83c\udf21\ufe0f Prediksi Angka 4D"):
    input1 = tanggal_input.day
    input2 = tahun_lahir % 100
    
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
    else:
        model = latih_model()

    if model is not None:
        hasil_prediksi = prediksi_angka(model, input1, input2)
        simpan_data(input1, input2, hasil_prediksi)

        st.success(f"\ud83c\udf1f Angka Prediksi AI 4D: {hasil_prediksi}")

        # Shio
        shio_tahun = hitung_shio_tahun(tahun_lahir)
        shio_hari = hitung_shio_harian(tanggal_input)
        st.info(f"\ud83d\udccc Shio Tahun Anda: {shio_tahun}")
        st.info(f"\ud83d\udcc6 Shio Hari Ini: {shio_hari}")

        # Kombinasi Logika
        st.subheader("\ud83d\udd04 Logika Kombinasi Angka")
        kombinasi = kombinasi_logika(hasil_prediksi)
        for k, v in kombinasi.items():
            st.write(f"**{k}**: {v}")
    else:
        st.warning("Model belum cukup data untuk dilatih. Silakan input angka real dulu.")

# --- Input Latihan Ulang ---
st.subheader("\ud83d\udce5 Input Angka Real untuk Latihan Ulang")
angka_real = st.text_input("Masukkan Angka Real 4D (jika ada)")
if st.button("Latih Ulang AI"):
    if angka_real.isdigit() and len(angka_real) == 4:
        input1 = tanggal_input.day
        input2 = tahun_lahir % 100
        simpan_data(input1, input2, int(angka_real))
        model = latih_model()
        st.success("Model berhasil dilatih ulang.")
    else:
        st.error("Masukkan angka 4 digit yang valid.")
