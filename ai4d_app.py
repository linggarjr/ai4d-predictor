import streamlit as st 
import random
from collections import Counter 
import json 
import os

File penyimpanan pembelajaran

DATA_LATIH_FILE = "data_latih.json" ANGKA_REAL_FILE = "angka_real.json"

Load data pembelajaran

if os.path.exists(DATA_LATIH_FILE): with open(DATA_LATIH_FILE, "r") as f: data_latih = json.load(f) else: data_latih = []

Load angka real untuk pembelajaran

if os.path.exists(ANGKA_REAL_FILE): with open(ANGKA_REAL_FILE, "r") as f: angka_real = json.load(f) else: angka_real = []

Angka dasar pedoman

data_pedoman = [ 667, 2215, 2039, 9361, 9739, 9467, 3114, 8296, 1034, 1032, 5823, 3754, 6440, 5891, 7496, 5979, 6948, 7947, 372, 1036, 1666, 7894, 4846, 9286, 4239, 5384, 516, 7139, 8573, 1032, 881, 1711, 8208, 8333, 2135, 1565, 3312, 6904, 4299, 557 ]

def format_angka(angka): return str(angka).zfill(4)

def analisa_pola(data_latih): awalan = Counter() akhiran = Counter() digit = Counter() for angka in data_latih: s = str(angka).zfill(4) awalan[s[:2]] += 1 akhiran[s[2:]] += 1 for d in s: digit[d] += 1 return awalan, akhiran, digit

def generate_rnd_angka(pedoman, data_latih, jumlah=10): hasil = [] awalan, akhiran, digit = analisa_pola(data_latih)

for _ in range(jumlah):
    if data_latih:
        # Gunakan pola dominan
        awalan_terbaik = awalan.most_common(3)
        akhiran_terbaik = akhiran.most_common(3)
        a = random.choice(awalan_terbaik)[0]
        b = random.choice(akhiran_terbaik)[0]
        hasil.append(a + b)
    else:
        angka = str(random.choice(pedoman)).zfill(4)
        hasil.append(angka)
return hasil

def simpan_latihan(angka): if angka not in data_latih: data_latih.append(int(angka)) with open(DATA_LATIH_FILE, "w") as f: json.dump(data_latih, f)

def simpan_angka_real(angka): if angka not in angka_real: angka_real.append(int(angka)) with open(ANGKA_REAL_FILE, "w") as f: json.dump(angka_real, f)

st.set_page_config(page_title="🧠 RNG 4D", layout="wide") st.title("🧠 Sistem RNG 4D + Pembelajaran Dinamis")

with st.form("input_form"): input_manual = st.text_input("Masukkan 2–5 angka manual (pisahkan dengan koma):", "1234,5678") angka_real_input = st.text_input("Masukkan angka real (pisahkan dengan koma jika lebih dari satu):", "") submit = st.form_submit_button("🎰 Hasilkan RNG")

if submit: try: angka_input = [int(i.strip()) for i in input_manual.split(",") if i.strip().isdigit()] angka_real_baru = [int(i.strip()) for i in angka_real_input.split(",") if i.strip().isdigit()]

for ar in angka_real_baru:
        simpan_angka_real(ar)

    hasil_rng = generate_rnd_angka(data_pedoman + angka_input, data_latih, jumlah=20)

    st.subheader("🔢 Hasil Prediksi RNG:")
    for angka in hasil_rng:
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f"### 🎯 {angka}")
        with col2:
            if st.button("✅ Ini benar", key=f"b_{angka}"):
                simpan_latihan(angka)
                st.success(f"Angka {angka} disimpan sebagai pola bagus.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

st.sidebar.header("📊 Data Latih") if data_latih: st.sidebar.write([format_angka(d) for d in data_latih]) else: st.sidebar.write("Belum ada data latih.")

st.sidebar.header("📌 Angka Real") if angka_real: st.sidebar.write([format_angka(d) for d in angka_real]) else: st.sidebar.write("Belum ada angka real.")

