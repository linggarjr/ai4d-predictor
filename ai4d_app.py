import streamlit as st
import pandas as pd
import random
import datetime

# --- Data Shio ---
shio_list = [
    "Tikus", "Kerbau", "Macan", "Kelinci", "Naga", "Ular",
    "Kuda", "Kambing", "Monyet", "Ayam", "Anjing", "Babi"
]
shio_numbers = {
    "Tikus": [12, 24, 36, 48],
    "Kerbau": [11, 23, 35, 47],
    "Macan": [10, 22, 34, 46],
    "Kelinci": [9, 21, 33, 45],
    "Naga": [8, 20, 32, 44],
    "Ular": [7, 19, 31, 43],
    "Kuda": [6, 18, 30, 42],
    "Kambing": [5, 17, 29, 41],
    "Monyet": [4, 16, 28, 40],
    "Ayam": [3, 15, 27, 39],
    "Anjing": [2, 14, 26, 38],
    "Babi": [1, 13, 25, 37]
}

# --- Fungsi Hitung Shio ---
def get_shio_name(tahun):
    return shio_list[(tahun - 4) % 12]

# --- Fungsi Prediksi ---
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
        if target and len(target) == 4:
            prefix = target[:2]
            combo = ''.join(random.choices(tuple(sering), k=1) + random.choices(tuple(jarang), k=1))
            num = prefix + combo
        else:
            part = ''.join(random.choices(tuple(jarang), k=2) + random.choices(tuple(sering), k=2))
            num = part

        colored = [f"{ch}{'🔵' if ch in jarang else '🔴'}" for ch in num]
        preds.append((''.join(colored), num))

    return preds, sering, jarang

# --- Analisis Kombinasi ---
def analisis_logika(angka):
    return {
        "Ganjil/Genap": {
            "As": "Ganjil" if int(angka[0]) % 2 else "Genap",
            "Kop": "Ganjil" if int(angka[1]) % 2 else "Genap",
            "Kepala": "Ganjil" if int(angka[2]) % 2 else "Genap",
            "Ekor": "Ganjil" if int(angka[3]) % 2 else "Genap",
        },
        "Besar/Kecil": {
            "As": "Besar" if int(angka[0]) >= 5 else "Kecil",
            "Kop": "Besar" if int(angka[1]) >= 5 else "Kecil",
            "Kepala": "Besar" if int(angka[2]) >= 5 else "Kecil",
            "Ekor": "Besar" if int(angka[3]) >= 5 else "Kecil",
        }
    }

# --- Streamlit UI ---
st.title("🔮 Prediksi Angka 4D + Shio Harian + Kombinasi")

# Input
tanggal = st.date_input("Tanggal untuk Shio Harian", datetime.date.today())
tahun_lahir = st.number_input("Tahun Lahir Anda", min_value=1900, max_value=2100, value=1991)
angka_real = st.text_input("Masukkan Angka Real (opsional, pisahkan koma)")
last3 = st.text_input("Masukkan 3 Angka 4D Terakhir (pisahkan koma)", "2438,9258,4500")
target = st.text_input("Target Angka 4D (opsional)")
n = st.slider("Jumlah Prediksi", 1, 10, 5)

if st.button("🔮 Prediksi Sekarang"):
    parts = [s.strip() for s in last3.split(',') if len(s.strip()) == 4 and s.strip().isdigit()]
    if len(parts) != 3:
        st.error("Masukkan harus 3 angka 4D valid dipisah koma.")
    else:
        preds, sering, jarang = generate_predictions(parts, target or None, n)

        shio = get_shio_name(tahun_lahir)
        angka_shio = shio_numbers.get(shio, [])
        st.success(f"Shio Anda: {shio} - Angka Shio: {angka_shio}")

        st.write(f"**Angka Sering Muncul:** {', '.join(sorted(sering))}")
        st.write(f"**Angka Jarang Muncul:** {', '.join(sorted(jarang))}")
        st.markdown("---")
        st.write("### Hasil Prediksi:")

        for colored, raw in preds:
            st.markdown(f"- {colored} ➤  4D: `{raw}` / 3D: `{raw[-3:]}` / 2D: `{raw[-2:]}`")
            st.json(analisis_logika(raw))

        # Simpan data jika angka_real diisi
        if angka_real:
            try:
                df = pd.read_csv('data.csv')
            except FileNotFoundError:
                df = pd.DataFrame(columns=['angka', 'tanggal', 'tahun', 'shio'])

            for angka in angka_real.split(','):
                angka = angka.strip()
                if len(angka) == 4 and angka.isdigit():
                    new_row = pd.DataFrame([[angka, tanggal.strftime('%Y-%m-%d'), tahun_lahir, shio]], columns=df.columns)
                    df = pd.concat([df, new_row], ignore_index=True)

            df.to_csv('data.csv', index=False)
            st.success("Data angka real berhasil disimpan!")
