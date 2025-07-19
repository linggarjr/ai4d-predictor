import streamlit as st
import pandas as pd
import math
import random
import datetime
import itertools
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Konfigurasi halaman
st.set_page_config(page_title="Prediksi Angka 4D AI", layout="centered")
st.title("🔢 Prediksi Angka 4D AI Lengkap")
st.caption("Logika Logaritma + Kombinasi + Shio + ML + 2D/3D/4D")

# === Fungsi bantu ===
def hitung_shio(tahun):
    daftar_shio = ['Tikus', 'Kerbau', 'Macan', 'Kelinci', 'Naga', 'Ular',
                   'Kuda', 'Kambing', 'Monyet', 'Ayam', 'Anjing', 'Babi']
    return daftar_shio[(tahun - 4) % 12]

def prediksi_logika(angka):
    try:
        n = int(angka)
        log_value = math.log(n + random.uniform(0.1, 0.9))
        log_str = str(log_value).replace('.', '')[-6:]
        return {
            '2D': log_str[-2:],
            '3D': log_str[-3:],
            '4D': log_str[-4:]
        }
    except:
        return {'2D': '00', '3D': '000', '4D': '0000'}

def generate_predictions(base_numbers, target=None, n=5):
    freq = Counter(''.join(base_numbers))
    all_digits = set('0123456789')
    sering = {d for d, f in freq.items() if f >= 2}
    jarang = all_digits - set(freq.keys())
    preds = []

    for _ in range(n):
        if target and len(target) == 4:
            prefix = target[:2]
            combo = ''.join(random.choices(list(sering or all_digits), k=1) +
                            random.choices(list(jarang or all_digits), k=1))
            num = prefix + combo
        else:
            num = ''.join(random.choices(list(jarang or all_digits), k=2) +
                          random.choices(list(sering or all_digits), k=2))
        preds.append(num)
    return preds, sering, jarang

def train_ml_model(data):
    clean_data = [x.strip() for x in data.split(',') if len(x.strip()) == 4 and x.strip().isdigit()]
    if len(clean_data) < 5:
        return None
    X = [[int(ch) for ch in num] for num in clean_data]
    y = [1 if int(num[-1]) % 2 == 0 else 0 for num in clean_data]  # dummy label
    model = LogisticRegression()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model.fit(X_train, y_train)
    return model

# === Input User ===
input_angka_terakhir = st.text_input("Masukkan 3 angka 4D terakhir (pisahkan koma)", "8865,7065,1775")
input_target = st.text_input("Target angka (opsional)", "")
angka_real = st.text_area("Masukkan angka real untuk model ML (pisahkan koma)", "2438,9258,4500")
jumlah_prediksi = st.slider("Jumlah prediksi acak awal", 1, 10, 5)

# Informasi shio hari ini
tanggal_hari_ini = datetime.date.today()
shio = hitung_shio(tanggal_hari_ini.year)
st.text(f"Tanggal: {tanggal_hari_ini} | Shio Hari Ini: {shio}")

if st.button("🔮 Prediksi Sekarang"):
    try:
        angka_list = [x.strip() for x in input_angka_terakhir.split(',') if len(x.strip()) == 4]
        if len(angka_list) < 3:
            st.error("Masukkan minimal 3 angka 4D valid.")
        else:
            df_prediksi = pd.DataFrame(columns=['Asal', '2D', '3D', '4D', 'Sumber'])

            # === Prediksi awal (logika log) ===
            for angka in angka_list:
                hasil = prediksi_logika(angka)
                df_prediksi.loc[len(df_prediksi)] = [angka, hasil['2D'], hasil['3D'], hasil['4D'], 'Logika']

            # === Kombinasi 2 angka ===
            kombinasi = list(itertools.combinations(angka_list, 2))
            for a1, a2 in kombinasi:
                gabungan = a1[:2] + a2[-2:]
                hasil = prediksi_logika(gabungan)
                df_prediksi.loc[len(df_prediksi)] = [f"{a1}+{a2}", hasil['2D'], hasil['3D'], hasil['4D'], 'Kombinasi']

            # === Prediksi acak berbasis frekuensi ===
            pred_acak, sering, jarang = generate_predictions(angka_list, input_target or None, jumlah_prediksi)
            for num in pred_acak:
                hasil = prediksi_logika(num)
                df_prediksi.loc[len(df_prediksi)] = [f"Acak:{num}", hasil['2D'], hasil['3D'], hasil['4D'], 'Frekuensi']

            # === Prediksi ulang dari hasil acak ===
            for num in pred_acak:
                hasil = prediksi_logika(num)
                df_prediksi.loc[len(df_prediksi)] = [f"Ulang:{num}", hasil['2D'], hasil['3D'], hasil['4D'], 'Rekursif']

            # === Machine Learning ===
            model = train_ml_model(angka_real)
            if model:
                st.success("Model ML berhasil dilatih.")
                last_data = [int(d) for d in angka_list[-1]]
                pred = model.predict([last_data])[0]
                st.write(f"Prediksi Machine Learning (Genap=1 / Ganjil=0): **{pred}**")
            else:
                st.warning("Model ML gagal dilatih (butuh minimal 5 angka).")

            # === Gabungkan semua prediksi untuk kombinasi akhir ===
            kombinasi_final = set(df_prediksi['4D'].tolist())
            st.subheader("🎯 Kombinasi Angka 4D Potensial")
            for angka in sorted(kombinasi_final):
                st.write(f"• {angka}")

            # === Tampilkan hasil lengkap ===
            st.subheader("📊 Hasil Prediksi Lengkap")
            st.dataframe(df_prediksi)

            # === Unduh CSV ===
            nama_file = f"hasil_prediksi_{tanggal_hari_ini}.csv"
            st.download_button("📥 Unduh CSV", data=df_prediksi.to_csv(index=False), file_name=nama_file, mime='text/csv')

    except Exception as e:
        st.error(f"Terjadi kesalahan saat proses prediksi: {e}")
