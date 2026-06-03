def generate_insights(df):

    insights = []

    rows, cols = df.shape

    insights.append(
        f"The dataset contains {rows} rows and {cols} columns."
    )

    missing = df.isnull().sum().sum()

    insights.append(
        f"The dataset has {missing} missing values."
    )

    numeric_cols = df.select_dtypes(
        include=['int64', 'float64']
    ).columns

    for col in numeric_cols:

        avg = round(df[col].mean(), 2)

        insights.append(
            f"Average value of {col} is {avg}."
        )

    return insights