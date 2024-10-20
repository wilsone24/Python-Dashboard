import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Datos de conexión a la base de datos
host = "localhost"
user = "user"
password = "contrasena"  # Reemplaza con tu contraseña
database = "chicagocrimes"  # Reemplaza con el nombre de tu base de datos

# Crear la cadena de conexión usando pymysql
connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(connection_string)

# Query para obtener la cantidad de crímenes por tipo
query = """
SELECT 
    PrimaryType,
    COUNT(*) AS crime_count
FROM 
    crimes
GROUP BY 
    PrimaryType
ORDER BY 
    crime_count DESC
"""

# Leer los datos directamente con pandas
df = pd.read_sql(query, con=engine)

# Cerrar la conexión
engine.dispose()

# Crear el gráfico de pirámide
fig = px.bar(
    df,
    x='crime_count',
    y='PrimaryType',
    title='Tipo de Crímenes Más Cometidos en Chicago',
    labels={
        'crime_count': 'Cantidad de Crímenes',
    },
    orientation='h',  # Orientación horizontal para crear la pirámide
    color='crime_count',
    color_continuous_scale=px.colors.sequential.Plasma  
)

fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    xaxis_title="Cantidad de Crímenes",
    yaxis_title="Tipo de Crimen",
    margin={"r":0,"t":40,"l":0,"b":0},
)

# Mostrar el gráfico
fig.write_html('crime_pyramid.html')
