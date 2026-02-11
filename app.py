import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Data Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Interactive Data Dashboard")

# ---------------------------
# File Upload
# ---------------------------
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File Uploaded Successfully!")

    # Show raw data
    if st.checkbox("Show Raw Data"):
        st.dataframe(df)

    # ---------------------------
    # Sidebar Filters
    # ---------------------------
    st.sidebar.header("🔎 Filter Data")

    # Select column for filtering
    column = st.sidebar.selectbox("Select Column to Filter", df.columns)

    unique_values = df[column].unique()
    selected_values = st.sidebar.multiselect(
        "Select Values",
        unique_values,
        default=unique_values
    )

    filtered_df = df[df[column].isin(selected_values)]

    # ---------------------------
    # KPI Section
    # ---------------------------
    st.subheader("📌 Key Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", len(filtered_df))

    with col2:
        numeric_cols = filtered_df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            st.metric("Average (First Numeric Column)", 
                      round(filtered_df[numeric_cols[0]].mean(), 2))
        else:
            st.metric("No Numeric Data", "-")

    with col3:
        st.metric("Columns", len(filtered_df.columns))

    # ---------------------------
    # Visualization Section
    # ---------------------------
    st.subheader("📈 Data Visualization")

    numeric_columns = filtered_df.select_dtypes(include='number').columns

    if len(numeric_columns) > 0:
        x_axis = st.selectbox("Select X-Axis", filtered_df.columns)
        y_axis = st.selectbox("Select Y-Axis", numeric_columns)

        chart_type = st.radio("Select Chart Type", ["Bar", "Line", "Scatter"])

        if chart_type == "Bar":
            fig = px.bar(filtered_df, x=x_axis, y=y_axis)
        elif chart_type == "Line":
            fig = px.line(filtered_df, x=x_axis, y=y_axis)
        else:
            fig = px.scatter(filtered_df, x=x_axis, y=y_axis)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No numeric columns available for visualization.")

else:
    st.info("Please upload a file to begin.")
