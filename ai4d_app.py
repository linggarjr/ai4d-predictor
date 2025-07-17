import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import math
from datetime import datetime
from sklearn.linear_model import LinearRegression

# ==== Konstanta ====
DATA_FILE = "data.csv"
MODEL_FILE = "model.pkl"

# ==== Inisialisasi File ====
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["angka", "tanggal", "shio_tahun", "shio_hari",
                               "ganjil_genap", "besar_kecil", "posisi", "silang_homo", 
                               "tengah_tepi", "kembang_kempis", "label"])
    df.to_csv(DATA_FILE, index=False)

# ==== Load data dan model ====
data = pd.read_csv(DATA_FILE)

if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)
else:
    model = LinearRegression()

# ==== Fungsi bantu kombinasi angka ====
def kombinasi_logika(angka):
    str_angka = str(angka).zfill(4)
    digits = [int(d) for d in str_angka]

    ganjil_genap = "ganjil" if sum(d % 2 for d in digits) > 2 else "genap"
    besar_kecil = "besar" if sum(digits) >= 20 else "kecil"
    posisi = f"{str_angka[0]}-{str_angka[1]}-{str_angka[2]}-{str_angka[3]}"
    silang_homo = "silang" if len(set(digits)) > 2 else "homo"
    tengah_tepi = "tengah" if 1000 < angka < 9000 else "tepi"
    kembang_kempis = "kembang" if digits == sorted(digits) else "kempis"

    return ganjil_genap, besar_kecil, posisi, silang_homo, tengah_tepi, kembang_kempis

# ==== Fungsi Shio ====
def hitung_shio_tahun(tahun):
    shio_list = ["Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular",
                 "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"]
    return shio_list[(tahun - 4) % 12]

def hitung_shio_harian(tanggal):
    day = datetime.strptime(tanggal, "%Y-%m-%d").day
    return hitung_shio_tahun(day + 2000)  # cara sederhana

# ==== Fungsi prediksi ====
def prediksi_ai():
    X = data[["shio_tahun", "shio_hari", "ganjil_genap", "besar_kecil"]].fillna(0).apply(lambda col: pd.factorize(col)[0])
    y = data["angka"]
    if len(X) > 5:
        model.fit(X, y)
        joblib.dump(model, MODEL_FILE)
        pred_input = pd.DataFrame([[
            pd.factorize(data["shio_tahun"])[0][-1],
            pd.factorize(data["shio_hari"])[0][-1],
            pd.factorize(data["ganjil_genap"])[0][-1],
            pd.factorize(data["besar_kecil"])[0][-1]
        ]])
        pred = int(model.predict(pred_input)[0]) % 10000
        return str(pred).zfill(4)
    return "0000"

# ==== Streamlit UI ====
st.title("🔮 Prediksi Angka 4D AI + Shio + Kombinasi")

# Input tanggal dan tahun
tanggal = st.date_input("Tanggal Hari Ini", datetime.today())
tahun = st.number_input("Tahun Lahir Anda", min_value=1900, max_value=2100, value=2000)

if st.button("🔢 Prediksi Angka 4D"):
    shio_tahun = hitung_shio_tahun(tahun)
    shio_hari = hitung_shio_harian(str(tanggal))

    dummy_angka = np.random.randint(0, 10000)
    ganjil_genap, besar_kecil, posisi, silang_homo, tengah_tepi, kembang_kempis = kombinasi_logika(dummy_angka)

    new_row = {
        "angka": dummy_angka,
        "tanggal": str(tanggal),
        "shio_tahun": shio_tahun,
        "shio_hari": shio_hari,
        "ganjil_genap": ganjil_genap,
        "besar_kecil": besar_kecil,
        "posisi": posisi,
        "silang_homo": silang_homo,
        "tengah_tepi": tengah_tepi,
        "kembang_kempis": kembang_kempis,
        "label": "prediksi"
    }
    data = data.append(new_row, ignore_index=True)
    data.to_csv(DATA_FILE, index=False)

    hasil = prediksi_ai()

    st.success(f"🎯 Hasil Prediksi: {hasil}")
    st.info(f"Shio Tahun: {shio_tahun}, Shio Harian: {shio_hari}")
    st.write("Kombinasi Angka:")
    st.write(f"Ganjil/Genap: {ganjil_genap}, Besar/Kecil: {besar_kecil}")
    st.write(f"Posisi: {posisi}, Silang/Homo: {silang_homo}")
    st.write(f"Tengah/Tepi: {tengah_tepi}, Kembang/Kempis: {kembang_kempis}")

# ==== Tambahan Input Data Real ====
st.subheader("📥 Input Angka Real untuk Latihan Ulang")
angka_real = st.text_input("Masukkan Angka Real 4D (jika ada)")
if st.button("Latih Ulang AI"):
    if angka_real.isdigit() and len(angka_real) == 4:
        real_angka = int(angka_real)
        ganjil_genap, besar_kecil, posisi, silang_homo, tengah_tepi, kembang_kempis = kombinasi_logika(real_angka)
        new_row = {
            "angka": real_angka,
            "tanggal": str(datetime.today().date()),
            "shio_tahun": hitung_shio_tahun(datetime.today().year),
            "shio_hari": hitung_shio_harian(str(datetime.today().date())),
            "ganjil_genap": ganjil_genap,
            "besar_kecil": besar_kecil,
            "posisi": posisi,
            "silang_homo": silang_homo,
            "tengah_tepi": tengah_tepi,
            "kembang_kempis": kembang_kempis,
            "label": "real"
        }
        data = data.append(new_row, ignore_index=True)
        data.to_csv(DATA_FILE, index=False)
        st.success("✅ Data Real berhasil disimpan dan model siap dilatih ulang.")
    else:
        st.error("❌ Angka harus terdiri dari 4 digit!")
