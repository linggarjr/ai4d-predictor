import streamlit as st 

import pandas as pd 

import numpy as np 

import joblib 

import os 

import math

from datetime import datetime

from sklearn.linear_model import LinearRegression

Fungsi untuk load atau inisialisasi data.csv ---

def load_data(): if not os.path.exists("data.csv"): df = pd.DataFrame(columns=["angka", "tanggal", "jam"]) df.to_csv("data.csv", index=False) return pd.read_csv("data.csv")

--- Fungsi menyimpan hasil baru ke data.csv ---

def save_data(angka, tanggal, jam): df = load_data() new_row = {"angka": angka, "tanggal": tanggal, "jam": jam} df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True) df.to_csv("data.csv", index=False)

--- Fungsi melatih model AI ---

def train_model(): df = load_data() if len(df) < 2: return None df['angka'] = df['angka'].astype(str).str.zfill(4) df[['d1', 'd2', 'd3', 'd4']] = df['angka'].apply(lambda x: pd.Series([int(x[0]), int(x[1]), int(x[2]), int(x[3])])) df['timestamp'] = pd.to_datetime(df['tanggal'] + ' ' + df['jam']) df['timestamp'] = df['timestamp'].astype(np.int64) // 10**9

X = df[['d1', 'd2', 'd3', 'timestamp']]
y = df['d4']

model = LinearRegression()
model.fit(X, y)
return model

--- Fungsi prediksi AI ---

def predict_next(model): df = load_data() if model is None or df.empty: return "Model belum dilatih." last = df.iloc[-1] angka = str(last['angka']).zfill(4) timestamp = int(pd.Timestamp.now().timestamp()) X_pred = np.array([[int(angka[0]), int(angka[1]), int(angka[2]), timestamp]]) pred = model.predict(X_pred) pred_digit = max(0, min(9, int(round(pred[0])))) hasil = angka[:3] + str(pred_digit) return hasil.zfill(4)

--- Fungsi logika kombinasi angka ---

def kombinasi_logika(angka): angka = str(angka).zfill(4) d = list(map(int, angka)) return { "As": d[0], "Kop": d[1], "Kepala": d[2], "Ekor": d[3], "Ganjil/Genap": sum([i%2 for i in d]), "Besar/Kecil": sum(d)/4 >= 5, "Silang/Homo": len(set(d)) > 2, "Tengah/Tepi": sum([1 if 3<=x<=6 else 0 for x in d]), "Kembang/Kempis": int(d[0] < d[-1]), "Log(angka)": math.log(int(angka)) if int(angka) > 0 else 0 }

--- Fungsi shio tahunan ---

def hitung_shio_tahunan(tahun): daftar_shio = ["Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular", "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"] return daftar_shio[(tahun - 4) % 12]

--- Fungsi shio harian dari tanggal ---

def hitung_shio_harian(tanggal): try: tgl = pd.to_datetime(tanggal) kode = (tgl.day + tgl.month + tgl.year) % 12 daftar_shio = ["Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular", "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"] return daftar_shio[kode] except: return "Format tanggal salah"

--- UI Streamlit ---

st.set_page_config(layout="wide") st.title("🎯 Prediksi AI Angka 4D + Shio + Kombinasi")

st.subheader("🧮 Input Data") angka_input = st.text_input("Masukkan Angka 4D Terakhir", max_chars=4) tanggal_input = st.text_input("Tanggal", value=str(datetime.date.today())) jam_input = st.text_input("Jam", value=datetime.datetime.now().strftime("%H:%M"))

model = train_model() predicted_number = "" logika_prediksi = {}

if st.button("📊 Prediksi Angka 4D Berikutnya"): if angka_input and len(angka_input) == 4 and angka_input.isdigit(): save_data(angka_input, tanggal_input, jam_input) model = train_model() predicted_number = predict_next(model) logika_prediksi = kombinasi_logika(predicted_number) st.success(f"Prediksi AI 4D Berikutnya: {predicted_number}") else: st.warning("Masukkan angka 4 digit valid terlebih dahulu.")

if st.button("🔁 Latih Ulang Model"): model = train_model() st.success("Model berhasil dilatih ulang dengan data terbaru.")

if predicted_number: st.subheader("🔢 Logika Kombinasi Angka Prediksi") st.write(logika_prediksi)

st.subheader("🔮 Perhitungan Shio") tahun_shio = st.number_input("Masukkan Tahun", min_value=1900, max_value=2100, value=datetime.date.today().year) if st.button("🔮 Hitung Shio Tahunan"): shio_tahun = hitung_shio_tahunan(tahun_shio) st.success(f"Shio Tahun {tahun_shio}: {shio_tahun}")

tanggal_shio = st.text_input("Masukkan Tanggal (YYYY/MM/DD)", value=str(datetime.date.today())) if st.button("🔮 Hitung Shio Harian"): shio_harian = hitung_shio_harian(tanggal_shio) st.success(f"Shio Harian untuk {tanggal_shio}: {shio_harian}")

st.caption("Versi Final - Terintegrasi Penuh oleh AI4D")

