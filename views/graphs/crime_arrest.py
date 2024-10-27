import plotly.express as px


async def graph(data):
    fig = px.scatter(
        data,
        x='crime_count',
        y='arrest_count',
        color='PrimaryType',
        labels={'crime_count': 'Crime Count', 'arrest_count': 'Arrest Count', 'PrimaryType': 'Crime Type'},
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black',
        xaxis_title="Crime Count",
        yaxis_title="Arrest Count",
        legend_title="Crime Type",
        xaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=0.5),
        yaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=0.5)
    )
    fig.update_traces(marker=dict(size=10, opacity=0.8, line=dict(width=1, color='lightgray')),
                      selector=dict(mode='markers'))
    return fig
