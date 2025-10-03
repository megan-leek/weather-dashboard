import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# Load rain log
df = pd.read_csv("data/rain_log.csv")

# Parse timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sidebar filters
st.sidebar.title("Filters")
selected_crag = st.sidebar.selectbox("Choose a crag", sorted(df["crag"].unique()))
date_range = st.sidebar.date_input("Date range", [df["timestamp"].min(), df["timestamp"].max()])

# Filter data
start_date, end_date = pd.to_datetime(date_range)
filtered = df[(df["crag"] == selected_crag) & (df["timestamp"].between(start_date, end_date))]

# Header
st.title("🧗 Crag Rain Dashboard")
st.markdown(f"Showing rain data for **{selected_crag}** from {start_date.date()} to {end_date.date()}")

# Rain chart
st.line_chart(filtered.set_index("timestamp")["rain_mm"])

# Latest reading
latest = filtered.sort_values("timestamp").iloc[-1]
st.metric(label="Latest Rainfall (mm)", value=f"{latest['rain_mm']:.2f}", delta=None)

# Map
st.subheader("Crag Location")
m = folium.Map(location=[latest["lat"], latest["lon"]], zoom_start=10)
folium.Marker([latest["lat"], latest["lon"]], popup=selected_crag).add_to(m)
st_folium(m, width=700)

st.set_page_config(page_title="Crag Rain Dashboard", layout="wide")
st.title("🧗 Crag Rain Dashboard")

try:
    df = pd.read_csv("data/rain_log.csv")
except FileNotFoundError:
    st.warning("No rain log found. Please run the logger first.")
    st.stop()
    