import streamlit as st
import random
import datetime
import pandas as pd
import os

# === Data Initialization ===
DATA_FILE = "data.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["angka", "tanggal"]).to_csv(DATA_FILE, index=False)

# === SHIO ===
shio_list = [
    "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular",
    "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"
]
shio_angka = {
    "Tikus": [2, 15, 28, 41],
    "Kerbau": [3, 16, 29, 42],
    "Macan": [4, 17, 30, 43],
    "Kelinci": [5, 18, 31, 44],
    "Naga": [6, 19, 32, 45],
    "Ular": [7, 20, 33, 46],
    "Kuda": [8, 21, 34, 47],
    "Kambing": [9, 22, 35, 48],
    "Monyet": [10, 23, 36, 49],
    "Ayam": [11, 24, 37],
    "Anjing": [12, 25, 38],
    "Babi": [1, 14, 27, 40]
}
def hitung_shio_harian(tanggal):
    try:
        tgl = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
        return shio_list[tgl.toordinal() % 12]
    except:
        return "Format tanggal salah"

# === Kombinasi Angka ===
def logika_kombinasi(angka):
    angka_str = str(angka).zfill(4)
    as_, kop, kepala, ekor = map(int, angka_str)
    total = int(angka)
    return {
        "As": as_,
        "Kop": kop,
        "Kepala": kepala,
        "Ekor": ekor,
        "Ganjil/Genap": "Ganjil" if total % 2 else "Genap",
        "Besar/Kecil": "Besar" if total >= 5000 else "Kecil",
        "Silang/Homo": "Silang" if as_ != ekor else "Homo",
        "Tengah/Tepi": "Tengah" if 1 <= kop <= 8 else "Tepi",
        "Kembang/Kempis": "Kembang" if as_ > kop else "Kempis"
    }

# === Prediksi Otomatis ===
def generate_predictions(last3, target=None, n=5):
    freq = {}
    for num in last3:
        for d in num:
            freq[d] = freq.get(d, 0) + 1

    all_digits = set('0123456789')
    sering = {d for d, f in freq.items() if f >= 2}
    jarang = all_digits - set(freq.keys())

    preds = []
    for _ in range(n):
        if target:
            prefix, _ = target[:2], target[2:]
            combo = ''.join(random.choices(tuple(sering), k=1) +
                            random.choices(tuple(jarang or all_digits), k=1))
            num = prefix + combo
        else:
            num = ''.join(random.choices(tuple(jarang or all_digits), k=2) +
                          random.choices(tuple(sering or all_digits), k=2))

        # Warna
        colored = []
        for ch in num:
            color = '🔵' if ch in jarang else '🔴'
            colored.append(f"{ch}{color}")
        preds.append((''.join(colored), num))
    return preds, sering, jarang

# === Streamlit UI ===
st.set_page_config(page_title="Prediksi AI 4D Lengkap", layout="centered")
st.title("🔢 Prediksi Angka 4D AI")
st.caption("Fitur lengkap: Shio Harian, Kombinasi, 2D/3D/4D Prediksi")

# === Input Angka ===
last_input = st.text_input("Masukkan 3 angka 4D terakhir (pisahkan koma)", value="2438,9258,4500")
target_input = st.text_input("Target angka (opsional, ex: 1784)")
jumlah = st.slider("Jumlah prediksi", 1, 10, 5)

# === Tanggal untuk Shio ===
tanggal = st.date_input("Tanggal untuk Shio Harian", value=datetime.date.today())

# === Prediksi ===
if st.button("🔮 Prediksi Sekarang"):
    last_parts = [x.strip() for x in last_input.split(',') if len(x.strip()) == 4]
    if len(last_parts) != 3 or any(not x.isdigit() for x in last_parts):
        st.error("Masukkan harus 3 angka 4D valid, pisahkan dengan koma.")
    else:
        # Simpan ke data.csv
        df = pd.read_csv(DATA_FILE)
        for angka in last_parts:
            df.loc[len(df)] = [angka, tanggal.strftime("%Y-%m-%d")]
        df.to_csv(DATA_FILE, index=False)

        preds, sering, jarang = generate_predictions(last_parts, target_input or None, jumlah)
        st.write(f"**Angka sering:** {', '.join(sorted(sering))}")
        st.write(f"**Angka jarang:** {', '.join(sorted(jarang))}")
        st.subheader("🎯 Hasil Prediksi:")
        for col, raw in preds:
            st.markdown(f"- {col} ➤ `{raw}`")

        # Prediksi 3D dan 2D dari hasil 4D
        st.subheader("🔢 Prediksi 3D dan 2D:")
        for _, raw in preds:
            st.write(f"- 3D: `{raw[-3:]}`, 2D: `{raw[-2:]}`")

        # Logika Kombinasi dari hasil prediksi pertama
        st.subheader("🔍 Logika Kombinasi Prediksi Pertama:")
        kombinasi = logika_kombinasi(preds[0][1])
        for k, v in kombinasi.items():
            st.write(f"- {k}: {v}")

        # Shio Harian
        st.subheader("🔮 Shio Harian:")
        nama_shio = hitung_shio_harian(tanggal.strftime("%Y-%m-%d"))
        st.success(f"Shio hari ini: **{nama_shio}** ({shio_angka.get(nama_shio, [])})")
