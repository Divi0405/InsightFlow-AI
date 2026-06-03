def clean_column_names(df):

    df.columns = [
        col.strip().lower().replace(" ", "_")
        for col in df.columns
    ]

    return df