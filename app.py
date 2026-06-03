import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="InsightFlow AI",
    layout="wide"
)

st.title("InsightFlow AI")
st.subheader("AI-Powered Analytics Platform")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.success("File Uploaded Successfully")

    # Dataset Preview
    st.write("## Dataset Preview")
    st.dataframe(df.head())

    # Dataset Summary
    st.write("## Dataset Summary")

    rows, cols = df.shape

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", rows)

    with col2:
        st.metric("Columns", cols)

    # Missing Values
    st.write("### Missing Values")
    st.dataframe(df.isnull().sum())

    # Data Types
    st.write("### Data Types")
    st.dataframe(df.dtypes.astype(str))

    # Insights
    st.write("## Smart Insights")

    numeric_cols = df.select_dtypes(
        include=['int64', 'float64']
    ).columns

    if len(numeric_cols) > 0:

        for col in numeric_cols:

            avg = round(df[col].mean(), 2)
            maximum = df[col].max()

            st.info(
                f"{col} average is {avg} and maximum is {maximum}"
            )

    # Charts
    st.write("## Dynamic Chart Generator")

    categorical_cols = df.select_dtypes(
        include=['object']
    ).columns

    if len(categorical_cols) > 0 and len(numeric_cols) > 0:

        x_axis = st.selectbox(
            "Select Category Column",
            categorical_cols
        )

        y_axis = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        chart_type = st.selectbox(
            "Select Chart Type",
            ["Bar", "Line", "Pie", "Scatter"]
        )

        # Bar Chart
        if chart_type == "Bar":

            fig = px.bar(
                df,
                x=x_axis,
                y=y_axis
            )

        # Line Chart
        elif chart_type == "Line":

            fig = px.line(
                df,
                x=x_axis,
                y=y_axis
            )

        # Pie Chart
        elif chart_type == "Pie":

            fig = px.pie(
                df,
                names=x_axis,
                values=y_axis
            )

        # Scatter Plot
        elif chart_type == "Scatter":

            fig = px.scatter(
                df,
                x=x_axis,
                y=y_axis
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )