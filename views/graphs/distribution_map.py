import pydeck as pdk


async def graph(data):
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=data,
        get_position='[longitude, latitude]',
        get_color='color',
        get_radius=100,
        pickable=True,
    )
    view_state = pdk.ViewState(
        latitude=data['latitude'].mean(),
        longitude=data['longitude'].mean(),
        zoom=10,
        pitch=0,
    )

    return pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v10",
        tooltip={"text": "{PrimaryType}\nYear: {Year}\nArrest: {Arrest}"}
    )
