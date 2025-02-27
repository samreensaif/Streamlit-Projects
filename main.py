import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="💿Data Sweeper", page_icon=":material/upload:", layout="wide")

st.title("💿Data Sweeper")

st.write("Tranform your files between CSV and Excel formats with built-in data cleaning and visualization tools")

uploaded_file = st.file_uploader("Upload a CSV or Excel file:", type=["csv", "xlsx"],accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext= os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

# display the file information
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024} bytes")

# show 5 rows of the dataframe
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

# options for data cleaning
        st.subheader("✡ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed Successfully")


            with col2:
                if st.button("Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled successfully")

# choose specific columns to convert

        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Select columns for {file.name} ", df.columns,default=df.columns)
        df = df[columns]
                    
        # choose some visualization options
        st.subheader(" Data Visualization Options")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_df = df.select_dtypes(include=['number']).iloc[:, :2]
            st.bar_chart(numeric_df)

            

        # convert the file -> csv to excel

        st.subheader("Convert File")
        conversion_type= st.radio(f" Convert {file.name} to ",("Excel","CSV"), key =file.name)
        if st.button(f"Convert {file.name} to {conversion_type}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext,".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            #  download the file
            st.download_button(label=f"⬇ Download {conversion_type} file", data=buffer, file_name=file_name, mime=mime_type)

            st.success(f"🎉File converted to {conversion_type} successfully")









