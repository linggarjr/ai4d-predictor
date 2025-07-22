import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="🎰 RNG 4D Belajar", layout="centered")
st.title("🧠 Sistem RNG 4D + Manipulasi Peluang")

# Inisialisasi session
if "angka_terakhir" not in st.session_state:
    st.session_state.angka_terakhir = ""
if "riwayat_rng" not in st.session_state:
    st.session_state.riwayat_rng = []
if "angka_bagus" not in st.session_state:
    st.session_state.angka_bagus = []
if "angka_buruk" not in st.session_state:
    st.session_state.angka_buruk = []

# Fungsi generate angka 4D standar
def generate_angka():
    angka = str(random.randint(0, 9999)).zfill(4)
    st.session_state.angka_terakhir = angka
    st.session_state.riwayat_rng.append(angka)

# Fungsi manipulasi berdasarkan angka manual
def belajar_dari_input(angka):
    # Simulasi manipulasi berdasarkan angka manual
    digit_mutasi = ''.join(random.sample(angka, 4))  # acak posisi digit
    mutasi_angka = digit_mutasi

    # Kombinasi dengan angka bagus/buruk (jika ada)
    if st.session_state.angka_bagus and st.session_state.angka_buruk:
        bagus = random.choice(st.session_state.angka_bagus)
        buruk = random.choice(st.session_state.angka_buruk)
        kombinasi = random.choice([
            bagus[:2] + buruk[-2:],  # BG depan + BR belakang
            buruk[:2] + bagus[-2:],  # BR depan + BG belakang
            ''.join(random.sample(bagus + buruk, 4))  # acak campur
        ])
        hasil = random.choice([mutasi_angka, kombinasi])
    else:
        hasil = mutasi_angka

    st.session_state.angka_terakhir = hasil
    st.session_state.riwayat_rng.append(hasil)
    return hasil

# Fungsi input angka manual + hasilkan angka baru
def proses_input_manual(angka):
    if len(angka) == 4 and angka.isdigit():
        hasil = belajar_dari_input(angka)
        st.success(f"🎯 Hasil dari input {angka} → {hasil}")
    else:
        st.warning("⚠️ Masukkan 4 digit angka valid.")

# Fungsi kombinasi acak dari angka bagus + buruk
def kombinasi_bagus_buruk():
    if st.session_state.angka_bagus and st.session_state.angka_buruk:
        bagus = random.choice(st.session_state.angka_bagus)
        buruk = random.choice(st.session_state.angka_buruk)
        kombinasi = random.choice([
            bagus[:2] + buruk[-2:], 
            buruk[:2] + bagus[-2:], 
            ''.join(random.sample(bagus + buruk, 4))
        ])
        st.session_state.angka_terakhir = kombinasi
        st.session_state.riwayat_rng.append(kombinasi)
        st.success(f"🔀 Kombinasi Acak: {kombinasi}")
    else:
        st.warning("Minimal 1 angka bagus & buruk diperlukan.")

# Tombol generate biasa
st.button("🎲 Generate Angka Acak", on_click=generate_angka)

# Input manual angka (memicu RNG baru)
with st.expander("✍️ Masukkan Angka Manual (4D) → Hasilkan RNG"):
    angka_input = st.text_input("Masukkan angka 4 digit:")
    if st.button("🔁 Proses Angka Manual"):
        proses_input_manual(angka_input)

# Tampilkan angka terakhir
if st.session_state.angka_terakhir:
    st.markdown("### 🎯 Angka Terakhir:")
    st.code(st.session_state.angka_terakhir)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Tandai Sebagai Bagus"):
            if st.session_state.angka_terakhir not in st.session_state.angka_bagus:
                st.session_state.angka_bagus.append(st.session_state.angka_terakhir)
    with col2:
        if st.button("❌ Tandai Sebagai Buruk"):
            if st.session_state.angka_terakhir not in st.session_state.angka_buruk:
                st.session_state.angka_buruk.append(st.session_state.angka_terakhir)

# Kombinasi angka bagus + buruk
st.subheader("🔀 Kombinasi Acak dari Bagus + Buruk")
st.button("⚡ Buat Kombinasi Acak", on_click=kombinasi_bagus_buruk)

# Riwayat angka RNG
st.subheader("📜 Riwayat RNG (Terakhir 20):")
st.write(", ".join(st.session_state.riwayat_rng[-20:]))

# Statistik angka bagus/buruk
st.subheader("📊 Statistik Manipulasi")
st.write(f"✅ Angka Bagus: {len(st.session_state.angka_bagus)}")
st.write(f"❌ Angka Buruk: {len(st.session_state.angka_buruk)}")

# Tampilkan angka langka (yang sering muncul)
counter = Counter(st.session_state.riwayat_rng)
angka_langka = [a for a, c in counter.items() if c >= 3]
if angka_langka:
    st.write(f"🔥 Angka Langka (Muncul ≥3x): {angka_langka}")
