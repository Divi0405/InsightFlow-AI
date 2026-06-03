import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="InsightFlow AI",
    layout="wide"
)

# ---------------- TITLE ---------------- #

st.title("InsightFlow AI")
st.subheader(
    "AI-Powered Business Intelligence Dashboard"
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# ---------------- MAIN APP ---------------- #

if uploaded_file:

    # READ CSV

    df = pd.read_csv(uploaded_file)

    st.success(
        "Dataset Uploaded Successfully"
    )

    # ---------------- COLUMN TYPES ---------------- #

    categorical_cols = df.select_dtypes(
        include=['object']
    ).columns

    numeric_cols = df.select_dtypes(
        include=['int64', 'float64']
    ).columns

    # ---------------- SIDEBAR FILTERS ---------------- #

    st.sidebar.header("Filters")

    filtered_df = df.copy()

    if len(categorical_cols) > 0:

        st.sidebar.subheader(
            "Dynamic Filters"
        )

        for column in categorical_cols:

            unique_values = df[
                column
            ].dropna().unique()

            selected_values = st.sidebar.multiselect(
                f"Select {column}",
                unique_values,
                default=unique_values
            )

            filtered_df = filtered_df[
                filtered_df[column].isin(
                    selected_values
                )
            ]

    # ---------------- DOWNLOAD FILTERED CSV ---------------- #

    csv = filtered_df.to_csv(
        index=False
    )

    st.sidebar.download_button(
        label="Download Filtered CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

    # ---------------- DATASET PREVIEW ---------------- #

    st.write("## Dataset Preview")

    st.dataframe(filtered_df.head())

    # ---------------- KPI DASHBOARD ---------------- #

    st.write("## KPI Dashboard")

    if len(numeric_cols) > 0:

        selected_metric = st.selectbox(
            "Select Metric",
            numeric_cols
        )

        total_value = round(
            filtered_df[
                selected_metric
            ].sum(),
            2
        )

        average_value = round(
            filtered_df[
                selected_metric
            ].mean(),
            2
        )

        max_value = round(
            filtered_df[
                selected_metric
            ].max(),
            2
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Value",
                total_value
            )

        with col2:

            st.metric(
                "Average Value",
                average_value
            )

        with col3:

            st.metric(
                "Maximum Value",
                max_value
            )

    # ---------------- DATA SUMMARY ---------------- #

    st.write("## Dataset Summary")

    rows, cols = filtered_df.shape

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", rows)

    with col2:
        st.metric("Columns", cols)

    st.write("### Missing Values")

    st.dataframe(
        filtered_df.isnull().sum()
    )

    st.write("### Data Types")

    st.dataframe(
        filtered_df.dtypes.astype(str)
    )

    # ---------------- SMART INSIGHTS ---------------- #

    st.write("## Smart Insights")

    if len(numeric_cols) > 0:

        top_value = filtered_df[
            selected_metric
        ].max()

        avg_value = round(
            filtered_df[
                selected_metric
            ].mean(),
            2
        )

        st.info(
            f"Highest {selected_metric} value is {top_value}"
        )

        st.info(
            f"Average {selected_metric} value is {avg_value}"
        )

    if len(categorical_cols) > 0:

        for column in categorical_cols:

            if not filtered_df[
                column
            ].mode().empty:

                top_category = filtered_df[
                    column
                ].mode()[0]

                st.info(
                    f"Most frequent value in {column} is {top_category}"
                )

    # ---------------- CORRELATION HEATMAP ---------------- #

    st.write("## Correlation Heatmap")

    if len(numeric_cols) > 1:

        correlation = filtered_df[
            numeric_cols
        ].corr()

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        sns.heatmap(
            correlation,
            annot=True,
            cmap="Blues",
            ax=ax
        )

        st.pyplot(fig)

    # ---------------- CHART GENERATOR ---------------- #

    st.write("## Dynamic Chart Generator")

    if (
        len(categorical_cols) > 0
        and len(numeric_cols) > 0
    ):

        x_axis = st.selectbox(
            "Select X-Axis",
            categorical_cols
        )

        y_axis = st.selectbox(
            "Select Y-Axis",
            numeric_cols
        )

        # AUTO CHART RECOMMENDATION

        recommended_chart = "Bar"

        if "date" in x_axis.lower():

            recommended_chart = "Line"

        elif filtered_df[
            y_axis
        ].dtype in ['int64', 'float64']:

            recommended_chart = "Bar"

        st.success(
            f"Recommended Chart: {recommended_chart}"
        )

        chart_type = st.selectbox(
            "Select Chart Type",
            ["Bar", "Line", "Pie", "Scatter"],
            index=[
                "Bar",
                "Line",
                "Pie",
                "Scatter"
            ].index(recommended_chart)
        )

        # BAR CHART

        if chart_type == "Bar":

            fig = px.bar(
                filtered_df,
                x=x_axis,
                y=y_axis,
                color=x_axis
            )

        # LINE CHART

        elif chart_type == "Line":

            fig = px.line(
                filtered_df,
                x=x_axis,
                y=y_axis
            )

        # PIE CHART

        elif chart_type == "Pie":

            fig = px.pie(
                filtered_df,
                names=x_axis,
                values=y_axis
            )

        # SCATTER PLOT

        elif chart_type == "Scatter":

            fig = px.scatter(
                filtered_df,
                x=x_axis,
                y=y_axis,
                color=x_axis
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ---------------- AI ANALYTICS ---------------- #

    st.write("## Ask Your Data")

    user_query = st.text_input(
        "Ask a question about your dataset"
    )

    if user_query:

        query = user_query.lower()

        ai_response = ""

        # HIGHEST VALUE

        if "highest" in query or "maximum" in query:

            metric = selected_metric

            max_value = filtered_df[
                metric
            ].max()

            ai_response = (
                f"The highest {metric} value is {max_value}."
            )

        # AVERAGE VALUE

        elif "average" in query or "mean" in query:

            metric = selected_metric

            avg_value = round(
                filtered_df[
                    metric
                ].mean(),
                2
            )

            ai_response = (
                f"The average {metric} value is {avg_value}."
            )

        # TOTAL VALUE

        elif "total" in query or "sum" in query:

            metric = selected_metric

            total_value = round(
                filtered_df[
                    metric
                ].sum(),
                2
            )

            ai_response = (
                f"The total {metric} value is {total_value}."
            )

        # MOST FREQUENT CATEGORY

        elif "most" in query or "frequent" in query:

            category = categorical_cols[0]

            top_category = filtered_df[
                category
            ].mode()[0]

            ai_response = (
                f"The most frequent value in {category} is {top_category}."
            )

        # DEFAULT RESPONSE

        else:

            ai_response = (
                "Try asking about highest values, averages, totals, or frequent categories."
            )

        st.success(ai_response)