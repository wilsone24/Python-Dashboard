import pandas as pd
from sqlalchemy import create_engine

# Configura tu conexión a la base de datos
db_host = 'localhost'
db_user = 'root'
db_password = 'WmEo.1739'
db_database = 'chicagocrimes'
db_port = 3306

# Crea la cadena de conexión
connection_string = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}'
engine = create_engine(connection_string)

# Define tu consulta SQL
query = """
SELECT 
    DATE_FORMAT(Date, '%Y-%m') AS Month,
    COUNT(*) AS TotalRows
FROM 
    crimes
GROUP BY 
    Month
ORDER BY 
    Month;
"""
df = pd.read_sql(query, engine)
print(df)
