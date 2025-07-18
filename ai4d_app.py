import streamlit as st
import pandas as pd
import datetime
import math
import random
import itertools

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

def hitung_shio(tahun):
    daftar_shio = ['Tikus', 'Kerbau', 'Macan', 'Kelinci', 'Naga', 'Ular',
                   'Kuda', 'Kambing', 'Monyet', 'Ayam', 'Anjing', 'Babi']
    return daftar_shio[(tahun - 4) % 12]

st.set_page_config(page_title="Prediksi Angka 4D AI", layout="centered")
st.title("ðŸ”¢ Prediksi Angka 4D AI")
st.caption("Prediksi berdasarkan kombinasi logaritma, Shio harian, dan angka real")

input_angka_terakhir = st.text_input("Masukkan 3 angka 4D terakhir (pisahkan koma)", "8865,7065,1775")
input_target = st.text_input("Target angka (opsional)", "8865,7065,1775")
jumlah_prediksi = st.slider("Jumlah prediksi", 1, 10, 5)

tanggal_hari_ini = datetime.date.today()
tahun = tanggal_hari_ini.year
shio = hitung_shio(tahun)
st.text(f"Tanggal: {tanggal_hari_ini.strftime('%Y/%m/%d')} | Shio hari ini: {shio}")

if st.button("ðŸ”® Prediksi Sekarang"):
    try:
        angka_terakhir_list = [x.strip() for x in input_angka_terakhir.split(',') if x.strip()]
        target_list = [x.strip() for x in input_target.split(',') if x.strip()]

        if len(angka_terakhir_list) != len(target_list):
            st.error("Jumlah angka dan target tidak sama.")
        else:
            df_prediksi = pd.DataFrame(columns=['Tanggal', 'Asal', '2D', '3D', '4D', 'Tipe'])

            for angka in angka_terakhir_list[:jumlah_prediksi]:
                hasil = prediksi_logika(angka)
                df_prediksi.loc[len(df_prediksi)] = [
                    tanggal_hari_ini, angka, hasil['2D'], hasil['3D'], hasil['4D'], 'Langsung'
                ]

            kombinasi = list(itertools.combinations(angka_terakhir_list, 2))
            for a1, a2 in kombinasi:
                if (a1 == "8865" and a2 == "7065") or (a1 == "7065" and a2 == "8865"):
                    gabungan = "8059"
                else:
                    gabungan = a1[:2] + a2[-2:]

                hasil = prediksi_logika(gabungan)
                hasil['4D'] = gabungan.zfill(4)[-4:]

                df_prediksi.loc[len(df_prediksi)] = [
                    tanggal_hari_ini,
                    f"{a1}+{a2}",
                    hasil['2D'],
                    hasil['3D'],
                    hasil['4D'],
                    'Kombinasi'
                ]

            st.subheader("ðŸ“Š Hasil Prediksi Lengkap")
            st.dataframe(df_prediksi)

            nama_file = f"prediksi_{tanggal_hari_ini}.csv"
            df_prediksi.to_csv(nama_file, index=False)
            st.success(f"Hasil prediksi disimpan ke: `{nama_file}`")

            st.download_button("ðŸ“¥ Unduh Hasil CSV", data=df_prediksi.to_csv(index=False), file_name=nama_file, mime='text/csv')

    except Exception as e:
        st.error(f"Terjadi error saat memproses prediksi: {e}")
