import streamlit as st import pandas as pd import numpy as np import joblib import os import math from sklearn.linear_model import LinearRegression from datetime import datetime

========== Konfigurasi ==========

DATA_FILE = "data.csv" MODEL_FILE = "model.pkl"

Buat file data jika belum ada

if not os.path.exists(DATA_FILE): df = pd.DataFrame(columns=["angka", "tanggal", "jam"]) df.to_csv(DATA_FILE, index=False)

========== Fungsi Ekstraksi Fitur ==========

def fitur_kombinasi(angka): angka = str(angka).zfill(4) as_, kop, kepala, ekor = map(int, angka) total = sum([as_, kop, kepala, ekor])

return [
    as_, kop, kepala, ekor,
    int(angka) % 2,                # Ganjil/Genap
    int(angka) >= 5000,            # Besar/Kecil
    math.log10(int(angka) + 1),    # Logaritma
    int(as_ % 2 == kop % 2),       # Silang/Homo
    int(kepala % 2 == ekor % 2),
    int(1 <= as_ <= 4),            # Tengah/Tepi
    int(1 <= ekor <= 4),
    int(total % 2 == 0),           # Kembang/Kempis
]

========== Fungsi Model AI ==========

def latih_model(): df = pd.read_csv(DATA_FILE) if len(df) < 10: return None X = np.array([fitur_kombinasi(str(a).zfill(4)) for a in df["angka"]]) y = np.roll(df["angka"].values, -1) model = LinearRegression() model.fit(X[:-1], y[:-1]) joblib.dump(model, MODEL_FILE) return model

def load_model(): if os.path.exists(MODEL_FILE): return joblib.load(MODEL_FILE) return latih_model()

def prediksi_angka(angka): model = load_model() if model is None: return "Model belum cukup data" fitur = np.array(fitur_kombinasi(angka)).reshape(1, -1) hasil = model.predict(fitur)[0] return str(int(hasil)).zfill(4)

========== Fungsi Shio ==========

def hitung_shio_tahunan(tahun): daftar_shio = ["Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular", "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"] return daftar_shio[(tahun - 4) % 12]

def hitung_shio_harian(tanggal): try: tanggal_obj = datetime.strptime(tanggal, "%Y/%m/%d").date() except: return "Format tanggal salah. Gunakan format: YYYY/MM/DD" daftar_shio = ["Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular", "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"] return daftar_shio[tanggal_obj.toordinal() % 12]

========== Antarmuka Streamlit ==========

st.title("🔢 Prediksi Angka 4D AI") st.write("Menggunakan AI + logika kombinasi angka + perhitungan Shio")

Input utama

angka_input = st.text_input("Masukkan Angka 4D Terakhir", max_chars=4) tanggal_input = st.date_input("Tanggal", datetime.today()) jam_input = st.time_input("Jam", datetime.now().time())

if st.button("📈 Prediksi Angka 4D Berikutnya"): if angka_input and len(angka_input) == 4 and angka_input.isdigit(): prediksi = prediksi_angka(angka_input) st.success(f"Prediksi Angka 4D Berikutnya: {prediksi}")

# Simpan ke file
    df = pd.read_csv(DATA_FILE)
    df.loc[len(df.index)] = [angka_input, tanggal_input, jam_input.strftime("%H:%M")]
    df.to_csv(DATA_FILE, index=False)
else:
    st.error("Masukkan angka 4 digit yang valid.")

Latih ulang model

if st.button("🔁 Latih Ulang Model (Jika Salah)"): model = latih_model() if model: st.success("Model berhasil dilatih ulang!") else: st.warning("Belum cukup data untuk melatih model.")

Shio

st.subheader("🔮 Perhitungan Shio") tahun_input = st.number_input("Masukkan Tahun untuk Shio Tahunan", min_value=1900, max_value=2100, value=2025) if st.button("🔮 Hitung Shio Tahunan"): shio = hitung_shio_tahunan(int(tahun_input)) st.info(f"Shio Tahun {tahun_input}: {shio}")

tanggal_shio_input = st.text_input("Masukkan Tanggal untuk Shio Harian (format: YYYY/MM/DD)", value="2025/07/17") if st.button("🔮 Hitung Shio Harian"): shio_hari = hitung_shio_harian(tanggal_shio_input) st.success(f"Shio Harian untuk {tanggal_shio_input}: {shio_hari}")

