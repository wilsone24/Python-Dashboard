import plotly.express as px


async def graph(data):
    fig_monthly_crimes = px.bar(
        data,
        x='month',
        y='crime_count',
        title='Total Crimes by Month in Chicago (2023)',
        labels={'month': 'Month', 'crime_count': 'Number of Crimes'},
        color='crime_count',
        color_continuous_scale=px.colors.sequential.Viridis
    )

    # Configurar el diseño de la gráfica
    fig_monthly_crimes.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black',
        xaxis_title="Month",
        yaxis_title="Number of Crimes",
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )
    return fig_monthly_crimes
