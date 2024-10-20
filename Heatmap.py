import pandas as pd
from sqlalchemy import create_engine
import pydeck as pdk

# Datos de conexión a la base de datos
host = "localhost"  
user = "user"
password = "contrasena"  
database = "chicagocrimes" 

# Crear la cadena de conexión usando pymysql
connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(connection_string)

query = """
SELECT 
    latitude,
    longitude
FROM 
    crimes
WHERE 
    latitude IS NOT NULL AND longitude IS NOT NULL
"""

# Leer los datos directamente con pandas
df = pd.read_sql(query, con=engine)

# Filtrar las coordenadas de latitud y longitud (eliminar valores nulos)
df = df[['latitude', 'longitude']].dropna()

# Configurar el layer del mapa de calor en 3D
layer = pdk.Layer(
    'HexagonLayer',  # Usamos HexagonLayer para el mapa de calor 3D
    df,
    get_position='[longitude, latitude]',
    radius=200,  # Ajusta el radio de los hexágonos
    elevation_scale=4,  # Escala para la altura de los hexágonos
    elevation_range=[0, 1000],  # Altura mínima y máxima de los hexágonos
    extruded=True,  
    pickable=True,  
    coverage=1
)

# Configurar la vista inicial centrada en Chicago
view_state = pdk.ViewState(
    latitude=41.8781,  
    longitude=-87.6298,  
    zoom=11,
    pitch=50 
)

# Crear el deck.gl con el layer
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Crimes Count: {elevationValue}"}  # Mostrar un tooltip con la cuenta de crímenes
)

# Guardar el mapa en un archivo HTML
r.to_html('crime_heatmap.html', notebook_display=False)

engine.dispose()





