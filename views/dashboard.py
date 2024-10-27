import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
from views.graphs import heatmap, monthly_crimes, common_crimes, type_by_district, distribution_map, crime_arrest


def page():
    engine = st.session_state.db

    # Page styling
    st.markdown(""" 
    <style>
    [data-testid="block-container"] {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        padding-bottom: 0rem;
        margin-bottom: -7rem;
    }
    [data-testid="stVerticalBlock"] {
        padding-left: 0rem;
        padding-right: 0rem;
    }
    [data-testid="stMetric"] {
        background-color: #393939;
        text-align: center;
        padding: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'filters' not in st.session_state:
        print("Updating filters...")

        query_fbi_codes = "SELECT DISTINCT FbiCode FROM crimes"
        query_locations = "SELECT DISTINCT LocationDescription FROM crimes"
        df_fbi_codes = pd.read_sql(query_fbi_codes, con=engine)
        df_locations = pd.read_sql(query_locations, con=engine)

        st.session_state.filters = {
            'fbi_codes': ['No Selection'] + df_fbi_codes['FbiCode'].tolist(),
            'locations': ['No Selection'] + df_locations['LocationDescription'].tolist()
        }

    colfilter = st.columns((1, 1, 1), gap='medium')
    with colfilter[0]:
        selected_fbi_code = st.selectbox("Select an FBI Code Type", st.session_state.filters['fbi_codes'])
    with colfilter[1]:
        selected_dom_arres = st.multiselect("Select Types of Crimes to Display", ["Arrest", "Domestic", "No Selection"],
                                            default=["No Selection"])
    with colfilter[2]:
        selected_location_description = st.selectbox("Select a Location Type:", st.session_state.filters['locations'])

    filters = []

    # Filtro por FBI Code
    if selected_fbi_code != 'No Selection':
        filters.append(f"FbiCode = '{selected_fbi_code}'")

    # Filtro por Location Description
    if selected_location_description != 'No Selection':
        filters.append(f"LocationDescription = '{selected_location_description}'")

    # Filtro por Arrest y Domestic
    if 'Arrest' in selected_dom_arres and 'Domestic' in selected_dom_arres:
        filters.append("Arrest = 1")
        filters.append("Domestic = 1")
    elif 'Arrest' in selected_dom_arres:
        filters.append("Arrest = 1")
    elif 'Domestic' in selected_dom_arres:
        filters.append("Domestic = 1")
    elif 'No Selection' in selected_dom_arres:
        pass
    else:
        filters.append("Arrest = 0")
        filters.append("Domestic = 0")

    where_clause = " AND ".join(filters)
    if where_clause:
        where_clause = "WHERE " + where_clause

    where_clause_map1 = " AND ".join(filters)
    if where_clause_map1:
        where_clause_map1 = "AND " + where_clause_map1

    query_scatter = f"""
    SELECT 
        PrimaryType,
        COUNT(*) AS crime_count,
        SUM(IF(Arrest, 1, 0)) AS arrest_count
    FROM 
        crimes
    {where_clause}
    GROUP BY 
        PrimaryType
    """

    query_map3d = f"""
    SELECT 
        latitude,
        longitude
    FROM 
        crimes
    {where_clause}
    """

    query_bar1 = f"""
    SELECT 
        District, 
        PrimaryType AS crime_type, 
        COUNT(*) AS crime_count
    FROM 
        crimes
    {where_clause}
    GROUP BY 
        District, crime_type
    ORDER BY 
        District
    """

    query_bar2 = f"""
    SELECT 
        PrimaryType,
        COUNT(*) AS crime_count
    FROM 
        crimes
    {where_clause}
    GROUP BY 
        PrimaryType
    ORDER BY 
        crime_count DESC
    """

    query_count1 = f"""
    SELECT 
        COUNT(*) AS crime_count
    FROM 
        crimes
    {where_clause}
    """

    query_count2 = f"""
    SELECT 
        PrimaryType,
        COUNT(*) AS crime_count
    FROM 
        crimes
    {where_clause}
    GROUP BY 
        PrimaryType
    ORDER BY 
        crime_count DESC
    """

    query_crimes_by_month = f"""
    SELECT 
        DATE_FORMAT(Date, '%Y-%m') AS month,
        COUNT(*) AS crime_count
    FROM 
        crimes
    {where_clause}
    GROUP BY 
        month
    ORDER BY 
        month;
    """

    query_map1 = f"""
    SELECT 
        PrimaryType,
        Latitude,
        Longitude,
        YEAR(Date) AS Year,
        Arrest
    FROM 
        crimes
    WHERE 
        Latitude IS NOT NULL AND Longitude IS NOT NULL
    {where_clause_map1}
    """

    # Dataframes for metrics and visualizations
    df_count1 = pd.read_sql(query_count1, con=engine)
    df_count2 = pd.read_sql(query_count2, con=engine)
    df_bar2 = pd.read_sql(query_bar2, con=engine)
    df_bar1 = pd.read_sql(query_bar1, con=engine)
    df_graph_scatter = pd.read_sql(query_scatter, con=engine)
    df_map1 = pd.read_sql(query_map1, con=engine)
    df_map1 = df_map1.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})
    df_graph_3dmap = pd.read_sql(query_map3d, con=engine).dropna()
    df_crimes_by_month = pd.read_sql(query_crimes_by_month, con=engine)

    if not df_count1.empty:
        count_1 = df_count1['crime_count'].values[0]
    else:
        count_1 = "No Data"

    if not df_count2.empty:
        count_2 = df_count2['PrimaryType'].values[0]
    else:
        count_2 = "0"

    crime_types = df_map1['PrimaryType'].unique()
    color_map = {crime: [i * 25 % 255, i * 50 % 255, i * 75 % 255] for i, crime in enumerate(crime_types)}
    df_map1['color'] = df_map1['PrimaryType'].map(color_map)

    # Metrics Display
    col0 = st.columns((1, 1), gap='medium')
    col0[0].metric(label="Total Crimes", value=count_1, delta="-------")
    col0[1].metric(label="Most Common Crime Type", value=count_2, delta="-------")
    style_metric_cards()

    # Bar Charts
    col1 = st.columns((1, 1), gap='medium')
    with col1[0]:
        common_crimes.graph(df_bar2)

    with col1[1]:
        type_by_district.graph(df_bar1)

    # Scatter Plot and 3D Map
    col2 = st.columns((1, 1), gap='medium')
    with col2[0]:
        crime_arrest.graph(df_graph_scatter)

    with col2[1]:
        st.subheader("Distribution Map")
        distribution_map.graph(df_map1)

    # 3D Hexagon Layer
    col3 = st.columns(1, gap='medium')
    with col3[0]:
        st.subheader("Heatmap")
        heatmap.graph(df_graph_3dmap)

    col4 = st.columns(1, gap='medium')
    with col4[0]:
        st.subheader("Monthly Stats")
        monthly_crimes.graph(df_crimes_by_month)


page()