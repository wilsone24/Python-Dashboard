import pandas as pd
import mysql.connector
from mysql.connector import Error

# Leer el archivo CSV
df = pd.read_csv('Crimes2023.csv')
# Asegúrate de que el formato de las fechas sea el correcto
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
df['Updated On'] = pd.to_datetime(df['Updated On'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

# Reemplazar valores NaN por None y verificar si hay columnas que no coinciden
df = df.where(pd.notnull(df), None)
print(df.head())
# Configuración de conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Cambiado a root
    'password': 'WmEo.1739',  # Contraseña actualizada
}

connection = None

try:
    # Conexión a la base de datos
    connection = mysql.connector.connect(**db_config)
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # Crear base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS chicagocrimes")
        cursor.execute("USE chicagocrimes")
        print("Base de datos 'chicagocrimes' lista para usar.")
        
        # Crear tabla
        create_table_query = """
        CREATE TABLE IF NOT EXISTS crimes (
            id INT PRIMARY KEY,
            CaseNumber VARCHAR(255),
            `Date` DATETIME,
            Block VARCHAR(255),
            `PrimaryType` VARCHAR(255),
            `Description` VARCHAR(255),
            LocationDescription VARCHAR(255),
            Arrest VARCHAR(10),
            Domestic VARCHAR(10),
            Beat INT,
            District INT,
            Ward INT,
            CommunityArea INT,
            FbiCode VARCHAR(5),
            xCoordinate INT,
            yCoordinate INT,
            Year INT,
            `UpdatedOn` VARCHAR(255),
            `Latitude` FLOAT,
            `Longitude` FLOAT,
            `Location` VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        
        # Preparar la consulta de inserción
        insert_query = """
        INSERT INTO crimes (id, CaseNumber, `Date`, Block, `PrimaryType`, `Description`, LocationDescription,
          Arrest, Domestic, Beat, District, Ward, CommunityArea, FbiCode, xCoordinate, yCoordinate, Year, `UpdatedOn`, `Latitude`, `Longitude`, `Location`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Insertar datos fila por fila
        for _, row in df.iterrows():
            # Asegurarse de que cada valor en la fila es 'None' si no tiene datos
            values = tuple(None if pd.isna(x) else x for x in [
                row['ID'], row['Case Number'], row['Date'], row['Block'], row['Primary Type'],
                row['Description'], row['Location Description'], row['Arrest'], row['Domestic'],
                row['Beat'], row['District'], row['Ward'], row['Community Area'], row['FBI Code'],
                row['X Coordinate'], row['Y Coordinate'], row['Year'], row['Updated On'],
                row['Latitude'], row['Longitude'], row['Location']
            ])
            cursor.execute(insert_query, values)
        
        # Confirmar los cambios
        connection.commit()
        print("Datos insertados exitosamente")

except Error as e:
    print(f"Error: {e}")

finally:
    # Este bloque se ejecutará sin importar si hubo un error o no
    if connection is not None and connection.is_connected():
        cursor.close()  # Cerrar cursor
        connection.close()  # Cerrar conexión
        print("Conexión MySQL cerrada")