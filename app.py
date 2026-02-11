import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="NFHS-4 Dashboard", layout="wide")

st.title("NFHS-4 India Health Dashboard")

# Load data
@st.cache_data
def load_data():
    file_path = "All India National Family Health Survey4.xlsx"
    df = pd.read_excel(file_path, sheet_name="in")
    df = df.dropna(how="all")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# First column assumed as State/UT
area_col = df.columns[0]

# Sidebar filters
st.sidebar.header("Filters")

areas = df[area_col].dropna().unique()
selected_areas = st.sidebar.multiselect(
    "Select State/UT",
    areas,
    default=areas[:5]
)

filtered_df = df[df[area_col].isin(selected_areas)]

# Indicator selection
numeric_cols = filtered_df.select_dtypes(include="number").columns
indicator = st.sidebar.selectbox("Select Indicator", numeric_cols)

# Chart
st.subheader(f"{indicator} by State/UT")

plot_df = filtered_df[[area_col, indicator]].dropna()

fig, ax = plt.subplots()
ax.bar(plot_df[area_col], plot_df[indicator])
plt.xticks(rotation=90)
ax.set_ylabel(indicator)
st.pyplot(fig)

# Summary
col1, col2, col3 = st.columns(3)

if not plot_df.empty:
    col1.metric("Average", round(plot_df[indicator].mean(), 2))
    col2.metric("Max", round(plot_df[indicator].max(), 2))
    col3.metric("Min", round(plot_df[indicator].min(), 2))

# Top/Bottom
st.subheader("Top & Bottom States")

top_n = st.slider("Select Top/Bottom N", 3, 10, 5)
rank_df = plot_df.sort_values(by=indicator, ascending=False)

col4, col5 = st.columns(2)

with col4:
    st.write("Top States")
    st.dataframe(rank_df.head(top_n))

with col5:
    st.write("Bottom States")
    st.dataframe(rank_df.tail(top_n))

# Raw data
st.subheader("Raw Data")
st.dataframe(filtered_df)
