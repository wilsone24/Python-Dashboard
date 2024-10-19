import pandas as pd
import mysql.connector
from mysql.connector import Error

# Read the CSV file
df = pd.read_csv('ruta')

# Asegúrate de que el formato de las fechas sea el correcto
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
df['Updated On'] = pd.to_datetime(df['Updated On'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

# MySQL database connection details
db_config = {
    'host': 'localhost',
    'database': 'chicagocrimes',
    'user': 'user',
    'password': 'Contrasena'
}

connection = None

try:
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(**db_config)
    
    if connection.is_connected():
        cursor = connection.cursor()
        
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
        
        # Prepare the INSERT query
        insert_query = """
        INSERT INTO crimes (id, CaseNumber, `Date`, Block, `PrimaryType`, `Description`, LocationDescription,
          Arrest, Domestic, Beat, District, Ward, CommunityArea, FbiCode, xCoordinate, yCoordinate, Year, `UpdatedOn`, `Latitude`, `Longitude`, `Location`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Insert data row by row
        for _, row in df.iterrows():
            values = (row['ID'], row['Case Number'], row['Date'], row['Block'], row['Primary Type'],
                      row['Description'], row['Location Description'], row['Arrest'], row['Domestic'],
                      row['Beat'], row['District'], row['Ward'], row['Community Area'], row['FBI Code'],
                      row['X Coordinate'], row['Y Coordinate'], row['Year'], row['Updated On'],
                      row['Latitude'], row['Longitude'], row['Location'])
            cursor.execute(insert_query, values)
        
        # Commit the changes
        connection.commit()
        print("Data inserted successfully")

except Error as e:
    print(f"Error: {e}")

finally:
    # Este bloque se ejecutará sin importar si hubo un error o no
    if connection is not None and connection.is_connected():
        cursor.close()  # Cerrar cursor
        connection.close()  # Cerrar conexión
        print("Conexión MySQL cerrada")