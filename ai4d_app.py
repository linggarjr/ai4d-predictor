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

# Load data ke session_state
if 'data_latih' not in st.session_state:
    st.session_state.data_latih, st.session_state.angka_buruk = muat_data()

if 'hasil_rng' not in st.session_state:
    st.session_state.hasil_rng = rng_murni()

# ===============================
# === Input Manual dari User ===
# ===============================

st.subheader("✍️ Masukkan Angka Manual (4 Digit)")
input_manual = st.text_input("Angka 4D (contoh: 1234)", max_chars=4)

col_manual_1, col_manual_2 = st.columns(2)
with col_manual_1:
    if st.button("✅ Tandai Benar (Manual)"):
        if input_manual and input_manual.isdigit() and len(input_manual) == 4:
            if input_manual not in st.session_state.data_latih:
                st.session_state.data_latih.append(input_manual)
                simpan_data(st.session_state.data_latih, st.session_state.angka_buruk)
                st.success(f"{input_manual} ditandai sebagai BENAR (manual)")
        else:
            st.warning("Masukkan angka 4 digit valid.")

with col_manual_2:
    if st.button("❌ Tandai Salah (Manual)"):
        if input_manual and input_manual.isdigit() and len(input_manual) == 4:
            if input_manual not in st.session_state.angka_buruk:
                st.session_state.angka_buruk.append(input_manual)
                simpan_data(st.session_state.data_latih, st.session_state.angka_buruk)
                st.error(f"{input_manual} ditandai sebagai SALAH (manual)")
        else:
            st.warning("Masukkan angka 4 digit valid.")

st.markdown("---")

# =============================
# === RNG Otomatis + Belajar ==
# =============================

if st.button("🔁 Generate Angka Baru"):
    st.session_state.hasil_rng = rng_murni()

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

# ========================
# === Tampilkan Data ===
# ========================

with st.expander("📊 Lihat Data Pembelajaran"):
    st.write("✅ Data Latih (Benar):", st.session_state.data_latih)
    st.write("❌ Angka Buruk (Salah):", st.session_state.angka_buruk)
