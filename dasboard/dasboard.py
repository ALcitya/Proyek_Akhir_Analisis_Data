import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Load data
@st.cache_data
def load_data_Day():
    dfDay = pd.read_csv("../data/day.csv")
    return dfDay

dfDay = load_data_Day()

@st.cache_data
def load_data_Hour():
    dfHour = pd.read_csv("../data/hour.csv")
    return dfHour

dfHour = load_data_Hour()

# ? - Diagram rata-rata Tahunan
dfDay['yr'] = dfDay['yr'].map({0:2011, 1:2012})
# Dashboard Title
st.title("Dasboard Penyewaan Sepeda")

# Plot: Performa Rental dalam 2 Tahun Terakhir
st.subheader("Performa Rental dalam 2 Tahun Terakhir")
performa_tahunan = dfDay.groupby("yr")["cnt"].sum().astype(int)
fig, ax = plt.subplots(figsize=(4, 3))
ax.bar(["2011", "2012"], performa_tahunan, color=['violet', 'blue'])
ax.set_xlabel("Tahun")
ax.set_ylabel("Total Peminjaman")
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
st.pyplot(fig)
# ? - Diagram Pemakaian per-Musim
# Sidebar untuk memilih musim
musim_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
dfDay["season_label"] = dfDay["season"].map(musim_labels)
st.sidebar.header("Filter Musim")
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim yang Ingin Ditampilkan:",
    options=dfDay["season_label"].unique(),
    default=dfDay["season_label"].unique()  # Defaultnya semua musim ditampilkan
)

# Filter data berdasarkan musim yang dipilih
filtered_df = dfDay[dfDay["season_label"].isin(selected_seasons)]

# Plot: Musim dengan Peminjaman Tertinggi dan Terendah
st.subheader("Musim dengan Peminjaman Tertinggi dan Terendah")
musim_rental = filtered_df.groupby("season_label")["cnt"].mean()

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(musim_rental.index, musim_rental, color=['green', 'red', 'orange', 'blue'])
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Musim dengan Peminjaman Tertinggi dan Terendah")

# Menambahkan label pada batang diagram
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval), ha='center', va='bottom')

st.pyplot(fig)
# ? - Diagram Peminjaman pada Hari Libur
# Filter data: Hari libur yang bukan weekend
libur_non_weekend = dfHour[(dfHour["holiday"] == 1) & (dfHour["workingday"] == 0)]
rata_rata_libur_non_weekend = libur_non_weekend.groupby("hr")["cnt"].mean().round(0).astype(int)

# Dashboard Title
st.title("Analisis Penyewaan Sepeda")

# Subheader untuk plot
st.subheader("Rata-rata Peminjaman di Hari Libur (Bukan Weekend)")

# Membuat plot dengan Matplotlib & Seaborn
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=rata_rata_libur_non_weekend.index, y=rata_rata_libur_non_weekend.values, marker="o", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Rata-rata Peminjaman di Hari Libur (Bukan Weekend)")
ax.set_xticks(range(0, 24))
ax.grid()

# Menampilkan plot di Streamlit
st.pyplot(fig)