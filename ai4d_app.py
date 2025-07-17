import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os
import math
from datetime import datetime

# Inisialisasi atau muat data
DATA_FILE = "data.csv"
MODEL_FILE = "model.pkl"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["angka", "tanggal", "jam"])
    df.to_csv(DATA_FILE, index=False)

# Fungsi untuk konversi angka 4D ke fitur numerik
def fitur_numerik(angka):
    return [
        int(angka[0]),  # As
        int(angka[1]),  # Kop
        int(angka[2]),  # Kepala
        int(angka[3]),  # Ekor
        int(angka) % 2,  # Genap/Ganjil
        int(angka) >= 5000,  # Besar/Kecil
        math.log10(int(angka) + 1),  # logaritma
    ]

# Fungsi untuk memuat dan melatih model
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

# Fungsi untuk memuat model
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

# Fungsi untuk hitung Shio
def hitung_shio(tahun):
    daftar_shio = ["Kambing", "Monyet", "Ayam", "Anjing", "Babi", "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular", "Kuda"]
    return daftar_shio[tahun % 12]

# UI Streamlit
st.title("🔢 Prediksi Angka 4D AI")
st.write("Gunakan pembelajaran logaritma dan AI untuk prediksi angka 4 digit.")

angka_input = st.text_input("Masukkan Angka 4D Terakhir", max_chars=4)
tanggal_input = st.date_input("Tanggal", datetime.today())
jam_input = st.time_input("Jam", datetime.now().time())

if st.button("📈 Prediksi Angka 4D Berikutnya"):
    if angka_input and len(angka_input) == 4 and angka_input.isdigit():
        prediksi = prediksi_angka(angka_input)
        st.success(f"Prediksi Angka 4D Berikutnya: {prediksi}")
        
        # Simpan ke data.csv
        df = pd.read_csv(DATA_FILE)
        df.loc[len(df.index)] = [angka_input, tanggal_input, jam_input.strftime("%H:%M")]
        df.to_csv(DATA_FILE, index=False)
    else:
        st.error("Masukkan angka 4 digit yang valid")

if st.button("🔁 Latih Ulang Model (Jika Salah)"):
    model = latih_model()
    if model:
        st.success("Model berhasil dilatih ulang!")
    else:
        st.warning("Belum cukup data untuk melatih model.")

# Tombol tambahan untuk Shio
tahun_shio = st.number_input("Masukkan Tahun untuk hitung Shio", min_value=1900, max_value=2100, value=2025)
if st.button("🔮 Hitung Shio Tahunan"):
    st.info(f"Shio Tahun {tahun_shio}: {hitung_shio(tahun_shio)}") import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os
import math
from datetime import datetime

# Inisialisasi atau muat data
DATA_FILE = "data.csv"
MODEL_FILE = "model.pkl"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["angka", "tanggal", "jam"])
    df.to_csv(DATA_FILE, index=False)

# Fungsi untuk konversi angka 4D ke fitur numerik
def fitur_numerik(angka):
    return [
        int(angka[0]),  # As
        int(angka[1]),  # Kop
        int(angka[2]),  # Kepala
        int(angka[3]),  # Ekor
        int(angka) % 2,  # Genap/Ganjil
        int(angka) >= 5000,  # Besar/Kecil
        math.log10(int(angka) + 1),  # logaritma
    ]

# Fungsi untuk memuat dan melatih model
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

# Fungsi untuk memuat model
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

# Fungsi untuk hitung Shio
def hitung_shio(tahun):
    daftar_shio = ["Kambing", "Monyet", "Ayam", "Anjing", "Babi", "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular", "Kuda"]
    return daftar_shio[tahun % 12]

# UI Streamlit
st.title("🔢 Prediksi Angka 4D AI")
st.write("Gunakan pembelajaran logaritma dan AI untuk prediksi angka 4 digit.")

angka_input = st.text_input("Masukkan Angka 4D Terakhir", max_chars=4)
tanggal_input = st.date_input("Tanggal", datetime.today())
jam_input = st.time_input("Jam", datetime.now().time())

if st.button("📈 Prediksi Angka 4D Berikutnya"):
    if angka_input and len(angka_input) == 4 and angka_input.isdigit():
        prediksi = prediksi_angka(angka_input)
        st.success(f"Prediksi Angka 4D Berikutnya: {prediksi}")
        
        # Simpan ke data.csv
        df = pd.read_csv(DATA_FILE)
        df.loc[len(df.index)] = [angka_input, tanggal_input, jam_input.strftime("%H:%M")]
        df.to_csv(DATA_FILE, index=False)
    else:
        st.error("Masukkan angka 4 digit yang valid")

if st.button("🔁 Latih Ulang Model (Jika Salah)"):
    model = latih_model()
    if model:
        st.success("Model berhasil dilatih ulang!")
    else:
        st.warning("Belum cukup data untuk melatih model.")

# Tombol tambahan untuk Shio
tahun_shio = st.number_input("Masukkan Tahun untuk hitung Shio", min_value=1900, max_value=2100, value=2025)

if st.button("🔮 Hitung Shio Tahunan"):
    st.info("Shio Tahun {}: {}".format(tahun_shio, hitung_shio(tahun_shio)))
