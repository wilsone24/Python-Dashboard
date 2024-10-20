import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Datos de conexión a la base de datos
host = "localhost"
user = "user"
password = "contrasena"  
database = "chicagocrimes"  

# Crear la cadena de conexión usando pymysql
connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(connection_string)

# Query para obtener datos de crímenes con coordenadas
query = """
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
"""

# Leer los datos directamente con pandas
df = pd.read_sql(query, con=engine)
engine.dispose()

# Crear el gráfico de dispersión geoespacial
fig = px.scatter_mapbox(
    df,
    lat='Latitude',
    lon='Longitude',
    color='PrimaryType',
    title='Distribución de Crímenes en Chicago',
    hover_data=['PrimaryType', 'Year', 'Arrest'],
    color_discrete_sequence=px.colors.sequential.Plasma,
    zoom=10,
    mapbox_style="carto-positron", 
)


fig.update_layout(
    plot_bgcolor='black', 
    paper_bgcolor='black', 
    font_color='white',     
    margin={"r":0,"t":40,"l":0,"b":0},
    legend_title="Tipo de Crimen",
)

# Mostrar el gráfico
fig.write_html('geospatial_crime.html')

