import streamlit as st
import pandas as pd 
import numpy as np 
import joblib import os 
import math from datetime 
import datetime, date, time from sklearn.linear_model 
import LinearRegression

=== Konstanta dan File ===

DATA_FILE = "data.csv" MODEL_FILE = "model.pkl"

=== Inisialisasi File Data ===

if not os.path.exists(DATA_FILE): df = pd.DataFrame(columns=["angka", "tanggal", "jam"]) df.to_csv(DATA_FILE, index=False)

=== Fungsi Ekstraksi Fitur Angka ===

def fitur_numerik(angka): angka_str = str(angka).zfill(4) as_, kop, kepala, ekor = map(int, angka_str) total = int(angka) return [ as_, kop, kepala, ekor, total % 2,                  # Genap/Ganjil total >= 5000,             # Besar/Kecil int(as_ == ekor),          # Silang/Homo int(1 <= kop <= 8),        # Tengah/Tepi int(as_ > kop),            # Kembang/Kempis math.log10(total + 1)      # Logaritma ]

=== Fungsi Pelatihan Model ===

def latih_model(): df = pd.read_csv(DATA_FILE) if len(df) < 10: return None try: X = np.array([fitur_numerik(str(a).zfill(4)) for a in df["angka"]]) y = np.roll(df["angka"].astype(int).values, -1) model = LinearRegression() model.fit(X[:-1], y[:-1]) joblib.dump(model, MODEL_FILE) return model except Exception as e: print(f"Error saat melatih model: {e}") return None

=== Fungsi Load Model ===

def load_model(): if os.path.exists(MODEL_FILE): return joblib.load(MODEL_FILE) else: return latih_model()

=== Fungsi Prediksi ===

def prediksi_angka(angka): model = load_model() if model is None: return "Model belum cukup data" fitur = np.array(fitur_numerik(angka)).reshape(1, -1) hasil = model.predict(fitur)[0] return str(int(hasil)).zfill(4)

=== Fungsi Hitung Shio ===

shio_list = [ "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular", "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi" ]

shio_angka = { "Tikus": [2, 15, 28, 41], "Kerbau": [3, 16, 29, 42], "Macan": [4, 17, 30, 43], "Kelinci": [5, 18, 31, 44], "Naga": [6, 19, 32, 45], "Ular": [7, 20, 33, 46], "Kuda": [8, 21, 34, 47], "Kambing": [9, 22, 35, 48], "Monyet": [10, 23, 36, 49], "Ayam": [11, 24, 37], "Anjing": [12, 25, 38], "Babi": [1, 14, 27, 40] }

def hitung_shio_tahunan(tahun): return shio_list[(tahun - 4) % 12]

def hitung_shio_harian(tanggal): try: tgl = datetime.strptime(tanggal, "%Y/%m/%d").date() return shio_list[tgl.toordinal() % 12] except: return "Format salah"

=== UI STREAMLIT ===

st.set_page_config(page_title="Prediksi AI 4D", layout="centered") st.title("🔢 Prediksi Angka 4D AI Lengkap") st.caption("Dengan AI, Logika Kombinasi, dan Perhitungan Shio")

=== Inputan ===

angka_input = st.text_input("Masukkan Angka 4D Terakhir", max_chars=4) tanggal_input = st.date_input("Tanggal", date.today()) jam_input = st.time_input("Jam", datetime.now().time())

=== Tombol Prediksi ===

if st.button("📈 Prediksi Angka 4D Berikutnya"): if angka_input and len(angka_input) == 4 and angka_input.isdigit(): hasil = prediksi_angka(angka_input) st.success(f"Prediksi AI 4D Berikutnya: {hasil}")

df = pd.read_csv(DATA_FILE)
    new_data = pd.DataFrame([[angka_input, tanggal_input.strftime("%Y-%m-%d"), jam_input.strftime("%H:%M")]],
                            columns=["angka", "tanggal", "jam"])
    df = pd.concat([df, new_data], ignore_index=True)
    df = df.tail(100)  # Simpan hanya 100 data terakhir
    df.to_csv(DATA_FILE, index=False)
else:
    st.error("Masukkan angka 4 digit valid")

=== Tombol Latih Ulang ===

if st.button("🔁 Latih Ulang Model"): model = latih_model() if model: st.success("Model berhasil dilatih ulang!") else: st.warning("Belum cukup data untuk melatih model.")

=== Perhitungan Shio ===

st.subheader("🔮 Perhitungan Shio") tahun_input = st.number_input("Masukkan Tahun", min_value=1900, max_value=2100, value=2025) if st.button("🔮 Hitung Shio Tahunan"): nama_shio = hitung_shio_tahunan(int(tahun_input)) kode_angka = shio_angka.get(nama_shio, []) st.info(f"Shio Tahun {tahun_input}: {nama_shio} ({kode_angka})")

tanggal_sh = st.text_input("Masukkan Tanggal (YYYY/MM/DD)", value="2025/07/17") if st.button("🔮 Hitung Shio Harian"): shio_hari = hitung_shio_harian(tanggal_sh) st.success(f"Shio Harian untuk {tanggal_sh}: {shio_hari} ({shio_angka.get(shio_hari, [])})")

=== Tampilkan Kombinasi Logika Angka ===

if angka_input and len(angka_input) == 4 and angka_input.isdigit(): fitur = fitur_numerik(angka_input) label = ["As", "Kop", "Kepala", "Ekor", "Ganjil/Genap", "Besar/Kecil", "Silang/Homo", "Tengah/Tepi", "Kembang/Kempis", "Log(angka)"] st.subheader("🔍 Logika Kombinasi Angka") for i, val in enumerate(fitur): st.write(f"{label[i]}: {val}")

