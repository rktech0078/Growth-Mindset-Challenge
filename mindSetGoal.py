import streamlit as st
import pandas as pd
import os
from io import BytesIO
import time

# Page Config
st.set_page_config(page_title="GEN AI - Growth Mindset Challenge", layout="centered")

# Title & Intro
st.title("🌱 Growth Mindset Challenge")
st.markdown("""
**I have been given the Growth Mindset Challenge as a project by our mentor, Sir Zia Ullah Khan.**  
This challenge focuses on learning, adapting, and overcoming failures. 🚀  
To make data handling easier, I built this **web app using Streamlit & Python**, featuring:
- ✅ **CSV to Excel & Excel to CSV Conversion**  
- 📊 **Data Visualization with Interactive Graphs**  
- 🛠 **Data Cleaning Tools**  
- 🔍 **Custom Column Selection for Conversion**
""")

# File Upload
upload_files = st.file_uploader("📂 Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # File Details
        st.markdown(f"### 📄 **File: {file.name}**")
        st.info(f"📏 **File Size:** {file.size/1024:.2f} KB")
        st.write("🔍 **Data Preview:**")
        st.dataframe(df.head())

        # Data Cleaning Options
        with st.expander("🛠 **Data Cleaning Options**"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🧹 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✔ Duplicates Removed!")

            with col2:
                if st.button(f"🛠 Fill Missing Values for {file.name}"):
                    numeric_col = df.select_dtypes(include=['number']).columns
                    df[numeric_col] = df[numeric_col].fillna(df[numeric_col].mean())
                    st.success("✔ Missing Values Filled!")

        # Column Selection
        with st.expander("🔍 **Select Columns to Convert**"):
            columns = st.multiselect(f"📌 Choose Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        # Data Visualization
        with st.expander("📊 **Data Visualization**"):
            if st.checkbox(f"📈 Show Graphs for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
        
        # Conversion Options
        with st.expander("🔄 **Convert & Download File**"):
            conversion_type = st.radio(f"🔀 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"💾 Convert & Download {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"⬇ Download {file_name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )

st.success("🎉 All files processed successfully!")
