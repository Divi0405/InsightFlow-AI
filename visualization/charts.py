import plotly.express as px

def create_chart(df, x_axis, y_axis, chart_type):

    if chart_type == "Bar":

        fig = px.bar(
            df,
            x=x_axis,
            y=y_axis
        )

    elif chart_type == "Line":

        fig = px.line(
            df,
            x=x_axis,
            y=y_axis
        )

    elif chart_type == "Pie":

        fig = px.pie(
            df,
            names=x_axis,
            values=y_axis
        )

    elif chart_type == "Scatter":

        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis
        )

    return fig