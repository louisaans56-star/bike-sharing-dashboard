import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("main_data.csv")

# pastikan datetime
df["dteday"] = pd.to_datetime(df["dteday"])

# =========================
# FEATURE ENGINEERING (AMAN)
# =========================

# Year & Month (kalau belum ada)
if "year" not in df.columns:
    df["year"] = df["dteday"].dt.year

if "month" not in df.columns:
    df["month"] = df["dteday"].dt.month

# Nama hari
if "day_name" not in df.columns:
    df["day_name"] = df["dteday"].dt.day_name()

# Label season (kalau belum ada)
if "season_label" not in df.columns:
    season_map = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }
    df["season_label"] = df["season"].map(season_map)

# =========================
# HEADER
# =========================
st.title("Bike Sharing Analytics Dashboard")
st.caption("Analisis penyewaan sepeda berdasarkan waktu, musim, dan perilaku user")

st.markdown("---")

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("Filter Data")

year_filter = st.sidebar.selectbox("Year", sorted(df["year"].unique()))
month_filter = st.sidebar.selectbox("Month", sorted(df["month"].unique()))

filtered_df = df[
    (df["year"] == year_filter) &
    (df["month"] == month_filter)
]

# =========================
# KPI
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rental", int(filtered_df["cnt"].sum()))
col2.metric("Casual Users", int(filtered_df["casual"].sum()))
col3.metric("Registered Users", int(filtered_df["registered"].sum()))
col4.metric("Avg Rental", round(filtered_df["cnt"].mean(), 1))

st.markdown("---")

# =========================
# TREND
# =========================
st.subheader("Daily Rental Trend")

daily_trend = filtered_df.groupby("dteday")["cnt"].sum()

fig, ax = plt.subplots(figsize=(14, 5))
daily_trend.plot(ax=ax)

ax.set_ylabel("Total Rental")
ax.set_xlabel("Date")

st.pyplot(fig)

st.markdown("---")

# =========================
# SEASON & WEEKDAY
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Rental per Season")

    season_data = filtered_df.groupby("season_label")["cnt"].mean().sort_values(ascending=False)

    fig1, ax1 = plt.subplots()
    season_data.plot(kind="bar", ax=ax1)

    ax1.set_ylabel("Avg Rental")
    st.pyplot(fig1)

with col2:
    st.subheader("Average Rental per Day")

    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_data = filtered_df.groupby("day_name")["cnt"].mean().reindex(weekday_order)

    fig2, ax2 = plt.subplots()
    weekday_data.plot(kind="bar", ax=ax2)

    ax2.set_ylabel("Avg Rental")
    st.pyplot(fig2)

st.markdown("---")

# =========================
# USER TYPE
# =========================
st.subheader("User Type Comparison")

user_data = pd.DataFrame({
    "User Type": ["Casual", "Registered"],
    "Total": [
        filtered_df["casual"].sum(),
        filtered_df["registered"].sum()
    ]
})

fig3, ax3 = plt.subplots()
ax3.bar(user_data["User Type"], user_data["Total"])

st.pyplot(fig3)

st.markdown("---")

# =========================
# WEATHER ANALYSIS
# =========================
if "weathersit" in df.columns:
    st.subheader("Weather Impact")

    weather_data = filtered_df.groupby("weathersit")["cnt"].mean()

    fig4, ax4 = plt.subplots()
    weather_data.plot(kind="bar", ax=ax4)

    ax4.set_ylabel("Avg Rental")
    st.pyplot(fig4)

    st.markdown("---")

# =========================
# DATA PREVIEW
# =========================
st.subheader("Data Preview")
st.dataframe(filtered_df, use_container_width=True)

st.caption("Bike Sharing Dashboard © 2026 | Louisa Anastasya Hermawan")