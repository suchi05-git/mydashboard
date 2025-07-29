import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Set page configuration
st.set_page_config(page_title="Data Dashboard", layout="wide")

# Title of the dashboard
st.title("📊 Interactive Data Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Determine file type and read accordingly
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

    st.success("File uploaded successfully!")

    # Show raw data
    st.subheader("Raw Data")
    st.dataframe(df)

    # Summary statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # Column selection for filtering
    st.subheader("Filter Data by Column")
    selected_column = st.selectbox("Select a column to filter", df.columns)
    unique_values = df[selected_column].dropna().unique()
    selected_value = st.selectbox("Select a value", unique_values)
    filtered_df = df[df[selected_column] == selected_value]
    st.write(f"Filtered Data ({selected_column} = {selected_value})")
    st.dataframe(filtered_df)

    # Visualization options
    st.subheader("Generate Visualizations")
    chart_type = st.selectbox("Choose chart type", ["Bar Chart", "Line Chart", "Pie Chart"])
    chart_column = st.selectbox("Select column for visualization", df.select_dtypes(include='number').columns)

    fig, ax = plt.subplots()
    if chart_type == "Bar Chart":
        df[chart_column].value_counts().plot(kind='bar', ax=ax)
    elif chart_type == "Line Chart":
        df[chart_column].plot(kind='line', ax=ax)
    elif chart_type == "Pie Chart":
        df[chart_column].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
    st.pyplot(fig)

    # Download processed data
    st.subheader("Download Processed Data")
    buffer = io.BytesIO()
    filtered_df.to_csv(buffer, index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=buffer.getvalue(),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV or Excel file to begin.")
