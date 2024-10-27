import plotly.express as px


async def graph(data):
    fig = px.bar(
        data,
        x='District',
        y='crime_count',
        color='crime_type',
        title='Total Crimes by District and Crime Type',
        labels={'District': 'District', 'crime_count': 'Crime Count', 'crime_type': 'Crime Type'},
        barmode='stack',
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    fig.update_layout(
        template='plotly_dark',
        xaxis_title="District",
        yaxis_title="Crime Count",
        legend_title="Crime Type",
        hovermode='x unified'
    )
    return fig
