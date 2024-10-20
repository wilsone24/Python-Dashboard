import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Datos de conexión a la base de datos
host = "localhost"
user = "user"
password = "contrasena" 
database = "crimes"

# Crear la cadena de conexión usando pymysql
connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(connection_string)

# Consulta SQL ajustada para obtener el número total de crímenes por distrito y tipo de crimen
query = """
SELECT 
    District, 
    PrimaryType AS crime_type, 
    COUNT(*) AS crime_count
FROM 
    crimes
WHERE 
    District IS NOT NULL 
    AND PrimaryType IS NOT NULL
GROUP BY 
    District, crime_type
ORDER BY 
    District
"""


try:
    df = pd.read_sql(query, con=engine)
    print("Consulta ejecutada con éxito.")
except Exception as e:
    print(f"Error al ejecutar la consulta: {e}")

engine.dispose()


if not df.empty:
    fig = px.bar(
        df, 
        x='District', 
        y='crime_count', 
        color='crime_type',
        title='Número Total de Crímenes por Distrito y Tipo de Crimen',
        labels={
            'District': 'Distrito',
            'crime_count': 'Número de Crímenes',
            'crime_type': 'Tipo de Crimen'
        },
        barmode='stack',
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    fig.update_layout(
        template='plotly_dark', 
        xaxis_title="Distrito",
        yaxis_title="Número de Crímenes",
        legend_title="Tipo de Crimen",
        hovermode='x unified' 
    )

    fig.write_html('crime_by_district.html')
    print("Gráfico guardado como crime_by_district_dark.html.")
else:
    print("El DataFrame está vacío")




