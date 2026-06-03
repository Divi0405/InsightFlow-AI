import streamlit as st

def dataset_summary(df):

    rows, cols = df.shape

    st.write(f"Rows: {rows}")
    st.write(f"Columns: {cols}")

    st.write("### Missing Values")
    st.dataframe(df.isnull().sum())

    st.write("### Data Types")
    st.dataframe(df.dtypes.astype(str))