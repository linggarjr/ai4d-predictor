import streamlit as st
import random
from collections import defaultdict

st.set_page_config(page_title="RNG 4D Manipulatif", layout="centered")
st.title("🎰 Sistem RNG 4D dengan Manipulasi Peluang")

# Inisialisasi session state
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "bagus" not in st.session_state:
    st.session_state.bagus = []
if "buruk" not in st.session_state:
    st.session_state.buruk = []
if "bobot" not in st.session_state:
    st.session_state.bobot = defaultdict(lambda: 1)
if "angka_langka" not in st.session_state:
    st.session_state.angka_langka = defaultdict(int)

# Data awal
angka_awal = [2215, 2039, 9361, 9739, 9467, 3114, 8296, 1034, 1032, 5823,
              3754, 6440, 5891, 7496, 5979, 6948, 7947, 372, 1036, 1666,
              7894, 4846, 9286, 4239, 5384, 516, 7139, 8573, 1032, 881, 1711,
              8208, 8333, 2135, 1565, 3312, 6904, 4299, 557]

# Update bobot awal
for angka in angka_awal:
    angka_str = str(angka).zfill(4)
    st.session_state.bobot[angka_str] += 5

# Fungsi untuk manipulasi RNG

def generate_rng():
    pool = []
    for angka, bbt in st.session_state.bobot.items():
        pool.extend([angka] * bbt)
    return random.choice(pool)

# Fungsi untuk update bobot

def update_bobot(angka, status):
    if status == "bagus":
        st.session_state.bobot[angka] += 50
    elif status == "buruk":
        st.session_state.bobot[angka] = max(1, st.session_state.bobot[angka] // 3)

# Tombol generate
if st.button("🎲 Generate Angka 4D"):
    angka_baru = generate_rng()
    st.session_state.riwayat.insert(0, angka_baru)
    st.session_state.angka_langka[angka_baru] += 1
    if st.session_state.angka_langka[angka_baru] == 3:
        st.session_state.bobot[angka_baru] += 1000
        st.toast(f"Angka langka ditemukan: {angka_baru} — bobot dinaikkan drastis!", icon="🔥")

# Input manual
st.subheader("✍️ Masukkan Angka Manual (4D)")
manual_input = st.text_input("Masukkan angka 4 digit:", max_chars=4)
if st.button("🔍 Cek dan Masukkan"):
    if manual_input.isdigit() and len(manual_input) == 4:
        st.session_state.riwayat.insert(0, manual_input)
        st.session_state.angka_langka[manual_input] += 1
        st.success(f"Angka {manual_input} dimasukkan ke sistem RNG")
    else:
        st.error("Masukkan harus 4 digit angka valid.")

# Kombinasi angka bagus dan buruk
st.subheader("🔀 Kombinasi Angka Bagus + Buruk")
if st.session_state.bagus and st.session_state.buruk:
    hasil_kombinasi = []
    for a in st.session_state.bagus:
        for b in st.session_state.buruk:
            a_str, b_str = str(a).zfill(4), str(b).zfill(4)
            kombinasi1 = a_str[:2] + b_str[2:]
            kombinasi2 = b_str[:2] + a_str[2:]
            hasil_kombinasi.extend([kombinasi1, kombinasi2])

    st.write(f"🔢 Total kombinasi: {len(hasil_kombinasi)}")
    st.write(", ".join(hasil_kombinasi[:20]))

    if st.button("➕ Masukkan Kombinasi ke Sistem"):
        for komb in hasil_kombinasi:
            st.session_state.bobot[komb] += 20
        st.success("Kombinasi dimasukkan dan diberi bobot tinggi!")
else:
    st.info("Tambahkan setidaknya 1 angka bagus dan 1 angka buruk untuk membentuk kombinasi.")

# Tampilkan hasil
st.subheader("🎯 Angka Terakhir: ")
if st.session_state.riwayat:
    angka_terakhir = st.session_state.riwayat[0]
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.metric("🎰 Angka", angka_terakhir)
    with col2:
        if st.button("✅ Bagus", key="good"):
            st.session_state.bagus.append(angka_terakhir)
            update_bobot(angka_terakhir, "bagus")
        if st.button("❌ Buruk", key="bad"):
            st.session_state.buruk.append(angka_terakhir)
            update_bobot(angka_terakhir, "buruk")

# Riwayat
st.subheader("📜 Riwayat Angka RNG")
st.write(", ".join(st.session_state.riwayat[:20]))

# Statistik
st.subheader("📊 Statistik Manipulasi")
st.write(f"✅ Total Angka Bagus: {len(st.session_state.bagus)}")
st.write(f"❌ Total Angka Buruk: {len(st.session_state.buruk)}")
st.write(f"🔥 Angka Langka (Muncul ≥3x): {[k for k,v in st.session_state.angka_langka.items() if v >=3]}")
