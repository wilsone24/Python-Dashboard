import pydeck as pdk


async def graph(data):
    layer = pdk.Layer(
        'HexagonLayer',
        data=data,
        get_position='[longitude, latitude]',
        radius=200,
        elevation_scale=4,
        elevation_range=[0, 1000],
        extruded=True,
        pickable=True,
        coverage=1
    )
    view_state = pdk.ViewState(
        latitude=41.8781,
        longitude=-87.6298,
        zoom=11,
        pitch=50
    )
    return pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Crimes Count: {elevationValue}"}
    )
