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

# Query para obtener la cantidad de crímenes y arrestos por tipo de crimen
query = """
SELECT 
    PrimaryType,
    COUNT(*) AS crime_count,
    SUM(CASE WHEN Arrest THEN 1 ELSE 0 END) AS arrest_count
FROM 
    crimes
GROUP BY 
    PrimaryType
"""

# Leer los datos directamente con pandas
df = pd.read_sql(query, con=engine)
engine.dispose()

# Crear el gráfico de dispersión
fig = px.scatter(
    df,
    x='crime_count',
    y='arrest_count',
    color='PrimaryType',
    title='Relación entre Crímenes y Arrestos',
    labels={
        'crime_count': 'Cantidad de Crímenes',
        'arrest_count': 'Cantidad de Arrestos',
        'PrimaryType': 'Tipo de Crimen'
    },
    color_discrete_sequence=[
        'rgba(255, 255, 0, 0.8)',  
        'rgba(255, 165, 0, 0.8)',   
        'rgba(255, 0, 255, 0.8)',   
        'rgba(128, 0, 128, 0.8)'    
    ]  # Personalizar colores
)


fig.update_layout(
    plot_bgcolor='black',   
    paper_bgcolor='black',  
    font_color='white',     
    xaxis_title="Cantidad de Crímenes",
    yaxis_title="Cantidad de Arrestos",
    legend_title="Tipo de Crimen",
    xaxis=dict(showgrid=True, gridcolor='gray', gridwidth=0.5),  
    yaxis=dict(showgrid=True, gridcolor='gray', gridwidth=0.5)  
)

# Aumentar el tamaño de los marcadores
fig.update_traces(marker=dict(size=16, opacity=0.8, line=dict(width=0, color='rgba(0,0,0,0)')), selector=dict(mode='markers'))

# Mostrar el gráfico
fig.write_html('crime_arrest_relationship.html')

