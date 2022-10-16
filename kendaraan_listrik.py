import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Kendaraan Bertenaga Listrik,</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Ramah atau Menambah Masalah?</h1>", unsafe_allow_html=True)
st.caption("Oleh : Satrio Sani Sadewo | sani.rio@gmail.com")

st.write("Krisis lingkungan hidup mulai dirasakan di berbagai belahan dunia. Tidak dapat dipungkiri bahwa hasil emisi gas karbon yang bersumber dari fossil termasuk salah satu penyebabnya. Berbagai upaya terus dilakukan untuk melawan permasalahan ini. Salah satunya adalah dengan memanfaatkan listrik sebagai tenaga penggerak kendaraan, yang diklaim sebagai kendaraan ramah lingkungan. Benarkah?")

st.subheader("Data Penjualan Mobil Listrik")
st.caption("sumber : International Energy Agency")
st.write("Dataset dari International Energy Agency memberikan 2 jenis kendaraan bertenaga listrik yaitu kendaraan bertipe PHEV (Plug-in Hybrid Electric Vehicle) dan BEV (Battery Electric Vehicle). Mobil PHEV ini memadukan dua mesin sekaligus yaitu mesin bertenaga konvesional (BBM) dan mesin bertenaga listrik dari battery. Sedangkan mobil BEV benar-benar full mengandalkan tenaga battery / tenaga listrik sebagai penggeraknya. Berikut adalah tampilan grafik penjualan dan stok kedua jenis kendaraan listrik :")

df_ev = pd.read_csv("IEA-EV-data.csv")
df_get_region = df_ev.drop_duplicates("region", keep='first')

col1, col2 = st.columns(2)

with col2:
    daerah_opt = st.selectbox('Negara',(df_get_region["region"]))
    kendaraan_opt = st.selectbox('Tipe Kendaraan',('PHEV','BEV'))
    grafik_opt = st.selectbox('Tipe Grafik',('Based On Data','Relative Percentage'))

with col1:
    df_coba = df_ev[((df_ev["unit"]=='sales') | (df_ev["unit"]=='stock')) & 
    (df_ev["category"]=='Historical') & 
    (df_ev["mode"]=='Cars') ]
    df_coba_opt = df_coba[(df_coba["powertrain"]==kendaraan_opt) & (df_coba["region"]==daerah_opt)]
    df_coba_opt = df_coba_opt[['year','unit','value']]

    if grafik_opt == "Based On Data":

        fig_market_line = px.line(df_coba_opt, x="year",
                            y="value", color="unit",
                            title="Data Penjualan vs Stok "+kendaraan_opt)
        st.plotly_chart(fig_market_line, use_container_width=True)

    if grafik_opt == "Relative Percentage":
        fig_market_bar = px.histogram(df_coba_opt, x="year",
                            y="value", color="unit",
                            barnorm='percent', text_auto='.2f',
                            title="Data Penjualan vs Stok "+kendaraan_opt)
        st.plotly_chart(fig_market_bar, use_container_width=True)

st.write("Mari kita lihat trend data penjualan kendaraan listrik di seluruh dunia yang diperoleh dari hasil riset International Energy Agency. Dari tahun ke tahun mengalami pengingkatan penjualan kendaraan listrik baik berjenis PHEV maupun BEV. Antara supply dengan demand juga menunjukkan kondisi yang sehat jika dilihat dari perbandingan persentase penjualan dan stok. Pada tahun 2010 perbandingan penjualan dan stok sebesar 48.90% : 51.10%. Sedangkan di tahun 2020 mencapai 25.21% : 74.49%. Angka penjualan yang terus naik artinya permintaan juga bertambah. Oleh karena itu produsen terus meningkatkan produksi kendaraan listrik yang dapat dilihat dari kenaikan data stok kendaraan listrik baik tipe PHEV maupun BEV. ")
st.write("Apa yang membuat konsumen tertarik membeli kendaraan listrik? Apakah kendaraan listrik ini memang ramah lingkungan? Mari kita lihat data uji emisi beberapa kendaraan menurut Kementerian ESDM RI berikut ini:")

st.subheader("Data Emisi Kendaraan")
st.caption("sumber : Kementerian ESDM 2017")

df_emisi_ev = pd.read_csv("adu-emisi-mobil-listrik-vs-konvensional.csv")
df_emisi_ev["tenaga"] = df_emisi_ev.loc[:,'nama_data']

col3, col4 = st.columns(2)

with col3:
    bar_chart = (alt.Chart(df_emisi_ev).mark_bar().encode(
        x=alt.X('tenaga', sort=None, title='sumber tenaga'),
        y=alt.Y('value', title='jumlah emisi g/km'),
        color="tenaga:N"
    ))
    
    st.altair_chart(bar_chart, use_container_width=True)

with col4:
    st.write("Berdasarkan data dari kementerian ESDM tahun 2017 disamping, emisi yang dihasilkan oleh kendaraan berbahan bakar konvensional (BBM) lebih besar daripada kendaraan listrik. Tentunya dengan kehadiran mobil bertenaga listrik ini sangat berkontribusi terhadap meningkatnya konsumsi listrik di seluruh dunia.")

st.subheader("Data Konsumsi Listrik Dunia")
st.caption("sumber : ourworldindata.org")

df_cons_el = pd.read_csv("electricity-generation.csv")
df_get_region_cons_el = df_cons_el.drop_duplicates("Entity", keep='first')

col5, col6 = st.columns(2)

with col6:
    daerah_opt_1 = st.selectbox('Negara',(df_get_region_cons_el["Entity"]))
    st.write("Berdasarkan data dari ourworldindata.org, konsumsi listrik di dunia makin meningkat dari tahun ke tahun.")

with col5:
    df_cons_el_opt = df_cons_el[df_cons_el["Entity"]==daerah_opt_1]
    st.line_chart(df_cons_el_opt, x='Year', y= 'Electricity generation (TWh)')

st.write("Setelah mendapatkan fakta bahwa konsumsi listrik di dunia semakin meningkat dimana kendaraan listrik turut berkontribusi akan hal ini, apakah dari data uji emisi kendaraan cukup untuk membuktikan bahwa kendaraan listrik ramah lingkungan? Apakah energi listrik dihasilkan secara alami? Perlu diperdalam lagi, darimana sumber energi yang dipakai untuk menghasilkan listrik?")

st.subheader("Data Sumber Produksi Listrik")
st.caption("sumber : ourworldindata.org")
grafik_opt2 = st.selectbox('Tipe Grafik',('Bar Chart','Line Chart'))

df_source_el = pd.read_csv("electricity-prod-source-stacked.csv")
df_source_el = df_source_el.drop(df_source_el[df_source_el.Year < 1985].index)
df_source_el = df_source_el[df_source_el["Entity"]=='World']
df_source_el = df_source_el.drop(['Entity', 'Code'], axis=1)
df_source_el = df_source_el.melt('Year', var_name='energy', value_name='value')

if grafik_opt2 == "Bar Chart":
    fig_el = px.bar(df_source_el, y="value",
                    x="Year", color="energy",
                    title="Sumber Produksi Listrik (TWh)")

    st.plotly_chart(fig_el, use_container_width=True)

if grafik_opt2 == "Line Chart":
    fig_el_line = px.line(df_source_el, y="value",
                    x="Year", color="energy",
                    title="Sumber Produksi Listrik (TWh)")

    st.plotly_chart(fig_el_line, use_container_width=True)

st.write("Dari data di atas menunjukkan bahwa batubara masih menjadi tumpuan sumber produksi listrik. Batubara yang berasal dari karbon ini sangat berkontribrusi terhadap produksi emisi CO2. Seberapa besar emisi CO2 yang dihasilkan di dunia?")

st.subheader("Data Emisi Gas CO2 Dunia")
st.caption("sumber : ourworldindata.org")

df_emission = pd.read_csv("annual-co2-emissions-per-country.csv")
df_emission = df_emission.drop(df_emission[df_emission.Year < 1985].index)
df_get_region_emission = df_emission.drop_duplicates("Entity", keep='first')

col7, col8 = st.columns(2)

with col8:
    daerah_opt_2 = st.selectbox('Negara',(df_get_region_emission["Entity"]))
    st.write("Emisi gas CO2 yang dihasilkan terus melonjak naik. Akan tetapi menarik dilihat bahwa emisi gas CO2 di Dunia pada tahun 2020 mengalami penurunan dibandingkan 2019. Apakah ada kaitannya dengan konsumsi listrik dan sumber produksinya?")

with col7:
    df_emission_opt = df_emission[df_emission["Entity"]==daerah_opt_2]
    st.line_chart(df_emission_opt, x='Year', y= 'Annual CO2 emissions')

st.subheader("Data Sumber Produksi Listrik Per Kapita dari Fossil vs Nuklir vs Renewables")
st.caption("sumber : ourworldindata.org")
st.write("Dataset berupa produksi listrik 'per kapita' dalam satuan kWh, dimana sumber energy dikelompokkan lagi menjadi 3 jenis yaitu energy fossil (berasal dari batubara, gas, dan minyak), energy nuklir, dan renewable energy (hydro, wind, solar, bioenergy, wave & tidal).")
grafik_opt3 = st.selectbox('Tipe Grafik',('Based On Data','Relative Percent'))

df_source_kp = pd.read_csv("per-capita-electricity-fossil-nuclear-renewables.csv")
df_source_kp = df_source_kp[df_source_kp["Entity"]=='World']
df_source_kp = df_source_kp.drop(['Entity', 'Code'], axis=1)
df_source_kp = df_source_kp.melt('Year', var_name='energy', value_name='value')

if grafik_opt3 == "Based On Data":
    fig_kp_line = px.line(df_source_kp, y="value",
                    x="Year", color="energy",
                    title="Produksi Listrik Per Kapita Fossil vs Nuklir vs Renewables")                   

    st.plotly_chart(fig_kp_line, use_container_width=True)

if grafik_opt3 == "Relative Percent":
    fig_kp_bar = px.histogram(df_source_kp, y="value",
                    x="Year", color="energy",
                    barnorm='percent', text_auto='.2f',
                    title="Persentase Produksi Listrik Per Kapita Fossil vs Nuklir vs Renewables")                   

    st.plotly_chart(fig_kp_bar, use_container_width=True)

st.write("Dapat dilihat bahwa di tahun 2020 terlihat terdapat penurunan trend konsumsi energy fossil sebagai sumber energi listrik, sedangkan pemanfaatan renewable energy sebagai sumber listrik meningkat. Pemanfaatan energi fossil di tahun 2020 sebesar 61.88% turun jika dibandingkan di tahun sebelumnya sebesar 65%. Sedangkan untuk renewable energy naik dari 24.55% menjadi 28.11% di tahun 2020")

st.subheader("Bagaimana Dengan Sikap Pemerintah Indonesia?")
st.write("Pemerintah Indonesia ternyata mendukung upaya produksi kendaraan bertenaga listrik. Hal ini ditunjukkan dengan diterbitkannya Peraturan Presiden Perpres Nomor 55 Tahun 2019 tanggal 08 Agustus 2019 tentang Percepatan Program Kendaraan Bermotor Listrik Berbasis Baterai (Battery Electric Vehicle/BEV) untuk Transportasi Jalan. Peraturan Presiden tersebut dapat dilihat pada link berikut : https://jdih.esdm.go.id/storage/document/Perpres%20Nomor%2055%20Tahun%202019.pdf")

st.subheader("Kesimpulan")
st.markdown(
"""
1. Penjualan dan Stok Mobil Listrik di dunia terus meningkat.
2. Emisi CO2 kendaraan listrik sebesar 0 g/km lebih kecil dari kendaraan konvensional (BBM) yang sebesar 120 g/km.
3. Energi listrik masih menggunakan energi fosil sebagai sumber produksinya.
4. Terjadi penurunan emisi gas CO2 di dunia dari tahun 2019 ke tahun 2020 dari 36 juta g/km menjadi 34 juta g/km.
5. Masyarakat dunia mulai banyak yang beralih menggunakan renewable energy sebagai sumber produksi listrik dunia di mana penggunaanya meningkat dari sebelumnya 24.55% menjadi 28.11% di tahun 2020.
6. Penggunaan energy fossil sebagai sumber tenaga listrik menurun dari sebelumnya 65% menjadi 61.88% di tahun 2020.
7. Penurunan emisi gas CO2 berbanding lurus dengan penurunan penggunaan energy fossil dan kenaikan penggunaan renewable energy sebagai sumber tenaga listrik.
8. Kendaraan listrik lebih ramah lingkungan jika dilihat dari emisi yang dihasilkan dan upaya peningkatan penggunaan renewable energy sebagai sumber energi listrik.
9. Langkah Pemerintah Indonesia sudah tepat dalam mendukung penggunaan kendaraan listrik sebagai transportasi jalan yang terbuti ramah lingkungan.
"""
)

st.subheader("Daftar Pustaka")
st.markdown(
"""
- Andriarsi, M. K., (2021, June 02). Adu Emisi Mobil Listrik vs Konvensional. https://databoks.katadata.co.id/datapublish/2021/06/02/adu-emisi-mobil-listrik-vs-konvensional
- International Energy Agency. (2022). Global EV Outlook 2022. https://www.iea.org/data-and-statistics/data-product/global-ev-outlook-2022
- Kementerian ESDM RI. (2017, August 11). Mengenal Jenis dan Tingkat Emisi Mobil Listrik. https://www.esdm.go.id/en/media-center/news-archives/mengenal-jenis-dan-tingkat-emisi-mobil-listrik
- Peraturan Presiden Perpres Nomor 55 Tahun 2019 tanggal 08 Agustus 2019 tentang Percepatan Program Kendaraan Bermotor Listrik Berbasis Baterai (Battery Electric Vehicle/BEV) untuk Transportasi Jalan. https://jdih.esdm.go.id/storage/document/Perpres%20Nomor%2055%20Tahun%202019.pdf"
- Rithie, H., & Roser, M. (2022). CO2 Emissions. https://ourworldindata.org/co2-emissions
- Rithie, H., & Roser, M. (2022). Electricity Mix. https://ourworldindata.org/electricity-mix
"""
)

st.markdown("<h1 style='text-align: center;'>TERIMA KASIH !</h1>", unsafe_allow_html=True)

    
