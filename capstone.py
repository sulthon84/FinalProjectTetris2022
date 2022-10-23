import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
from pandasql import sqldf
mysql = lambda q: sqldf(q, globals())

bio_prod = pd.read_csv('biofuel-production.csv')
wind_cap = pd.read_csv('cumulative-installed-wind-energy-capacity-gigawatts.csv')
hydro_share_nrg = pd.read_csv('hydro-share-energy.csv')
hydro_cons = pd.read_csv('hydropower-consumption.csv')
geo_cap = pd.read_csv('installed-geothermal-capacity.csv')
pv_cap = pd.read_csv('installed-solar-PV-capacity.csv')
renew_cons = pd.read_csv('modern-renewable-energy-consumption.csv')
renew_prod = pd.read_csv('modern-renewable-prod.csv')
renew_share_nrg = pd.read_csv('renewable-share-energy.csv')
hydro_share = pd.read_csv('share-electricity-hydro.csv')
renew_share = pd.read_csv('share-electricity-renewables.csv')
solar_share = pd.read_csv('share-electricity-solar.csv')
wind_share = pd.read_csv('share-electricity-wind.csv')
solar_cons = pd.read_csv('solar-energy-consumption.csv')
solar_share_nrg = pd.read_csv('solar-share-energy.csv')
wind_gen = pd.read_csv('wind-generation.csv')
wind_share = pd.read_csv('wind-share-energy.csv')

renew_2020 = mysql("""
SELECT 
    Entity,
    Code,
    "Renewables (% electricity)" AS Share
FROM renew_share
WHERE
    Year = 2020
AND
    Code IS NOT NULL
AND
    Code <> 'OWID_WRL'
""")

st.title('Analisis Konsumsi Energi Listrik vs Produksi Listrik dari Energi Terbarukan Skala Mikro')
st.header('Pendahuluan')
st.caption('Tren kebutuhan energi setiap tahunnya menunjukkan peningkatan seiring dengan meningkatnya laju pertumbuhan ekonomi dan bertambahnya jumlah penduduk. Dewasa ini, pemanfaatan energi akan terus berkembang mengingat inovasi teknologi berbasis listrik terus tumbuh pesat dan digunakan hampir di semua sektor, terutama di sektor rumah tangga dan komersial. Dampak krisis energi yang terjadi sejak beberapa waktu lalu tersebut kemudian mendorong perkembangan konsep Energi Terbarukan (ET). Konsep ini dikenalkan sebagai upaya mengatasi cadangan sumber energi yang selama ini diketahui kian menipis. ')

plt.style.use('fivethirtyeight')
plt.figure(figsize = (14,7))
plt.title("Kapasitas Energi Terbarukan pada 2020")
plt.xlabel("% Share", fontsize = 14)
plt.ylabel("# Countries", fontsize = 14)

plt.hist(renew_2020['Share'], 10, edgecolor = 'black')

st.pyplot(plt)

st.caption(' Histogram diatas menunjukkan bahwa ada banyak negara dengan pembangkit listrik terbarukan yang sangat sedikit. Ketika energy mix dari energi terbarukan meningkat, jumlah negara cenderung menurun, kecuali pada bin 90-100% dimana grafiknya mengalami peningkatan')

st.header('Bauran Energi beberapa negara')

world = renew_cons[(renew_cons.Year == 2020) & (renew_cons.Entity == 'World')]
# Drop all columns not containing consumption data so we can create a pie chart
world.drop(['Entity', 'Code', 'Year'], axis=1, inplace=True)

plt.style.use("seaborn-pastel")
plt.figure(figsize = (7,7))
plt.title('Bauran Konsumsi Energi di beberapa Negara pada 2020')

plt.pie(world.iloc[0], labels = ['Wind', 'Solar', 'Geo/Bio/Other', 'Hydro'], autopct='%1.1f%%', wedgeprops = {'edgecolor':'black'})

st.pyplot(plt)

st.caption('Di sini kita dapat melihat bahwa PLTA merupakan sumber energi terbarukan terbesar di dunia, diikuti oleh Angin kemudian Surya. Panas bumi, Biomassa, dan energi terbarukan lainnya merupakan kategori terakhir.')

st.header('Konsumsi Energi Listrik Skala Rumah Tangga/Mikro')
st.caption('Pada bulan April 2022, Tropical Renewable Energy Center melakukan penelitian terhadap profil beban listrik untuk kelas rumah tangga, dari peneltian tersebut didapatkan data berikut:')

data_rooftop_des = pd.read_excel('Data Rooftop.xlsx', 'Desember 2021')
data_rooftop_jan = pd.read_excel('Data Rooftop.xlsx', 'Januari 2022')
data_rooftop_feb = pd.read_excel('Data Rooftop.xlsx', 'Februari 2022')
data_rooftop_mar = pd.read_excel('Data Rooftop.xlsx', 'Maret 2022')
power_rooftop_des = data_rooftop_des['POWER_TOT']

data_beban_9_april = pd.read_excel('Data logging_5_Sabtu 9 April.xlsx')
data_beban_10_april = pd.read_excel('Data logging_6_Minggu 10 April.xlsx')
data_beban_11_april = pd.read_excel('Data logging 7__Senin 11 April.xlsx')

power_9_april = data_beban_9_april['CH27(W)']
print(power_9_april)


plt.title('Profil Beban Listrik Kelas Rumah Tangga 13 kVA')
st.line_chart(data=power_9_april)

st.header('Produksi Listrik dari Solar Panel 10 kWp')
plt.title('Produksi Listrik dari Solar Panel 10 kWp')
st.line_chart(data=power_rooftop_des)
mean_power = power_rooftop_des.mean()


st.header('Kesimpulan')
st.caption('Produksi solar panel 10 kWp dapat menghemat hampir kurang lebih 7% dari tagihan listrik rumah tangga 13 kVA')



