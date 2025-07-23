import streamlit as st
import random
import json
import os

# =======================
# === Data & Fungsi ====
# =======================

DATA_FILE = "pembelajaran.json"

def muat_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return data.get("data_latih", []), data.get("angka_buruk", [])
    return [], []

def simpan_data(data_latih, angka_buruk):
    with open(DATA_FILE, "w") as f:
        json.dump({
            "data_latih": data_latih,
            "angka_buruk": angka_buruk
        }, f, indent=4)

def rng_murni(jumlah=10):
    return [''.join(random.choices('0123456789', k=4)) for _ in range(jumlah)]

# =========================
# === Streamlit UI App ===
# =========================

st.set_page_config(page_title="RNG 4D + Pembelajaran", layout="centered")
st.title("🎰 RNG 4D Otomatis + Pembelajaran Manual")

# Load data saat awal
if 'data_latih' not in st.session_state:
    st.session_state.data_latih, st.session_state.angka_buruk = muat_data()

if 'hasil_rng' not in st.session_state:
    st.session_state.hasil_rng = rng_murni()

# Tombol untuk generate ulang angka
if st.button("🔁 Generate Angka Baru"):
    st.session_state.hasil_rng = rng_murni()

# Tampilkan angka hasil RNG
st.subheader("🎲 Hasil RNG 4D:")
for angka in st.session_state.hasil_rng:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**`{angka}`**")
    with col2:
        if st.button("✅ Ini Benar", key=f"benar_{angka}"):
            if angka not in st.session_state.data_latih:
                st.session_state.data_latih.append(angka)
                simpan_data(st.session_state.data_latih, st.session_state.angka_buruk)
                st.success(f"{angka} ditandai BENAR")
    with col3:
        if st.button("❌ Ini Salah", key=f"salah_{angka}"):
            if angka not in st.session_state.angka_buruk:
                st.session_state.angka_buruk.append(angka)
                simpan_data(st.session_state.data_latih, st.session_state.angka_buruk)
                st.error(f"{angka} ditandai SALAH")

# Tampilkan data pembelajaran
with st.expander("📊 Lihat Data Pembelajaran"):
    st.write("✅ Data Latih (Benar):", st.session_state.data_latih)
    st.write("❌ Angka Buruk (Salah):", st.session_state.angka_buruk)
