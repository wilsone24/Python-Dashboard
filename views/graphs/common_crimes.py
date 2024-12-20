import plotly.express as px


async def graph(data):
    fig = px.bar(
        data,
        x='crime_count',
        y='PrimaryType',
        labels={'crime_count': 'Crime Count'},
        orientation='h',
        color='crime_count',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black',
        xaxis_title="Crime Count",
        yaxis_title="Crime Type",
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )
    return fig