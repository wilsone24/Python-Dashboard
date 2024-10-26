import os
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# Read the CSV file
df = pd.read_csv('Crimes2023.csv')

# Ensure the date formats are correct
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
df['Updated On'] = pd.to_datetime(df['Updated On'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

# Replace NaN values with None and check for any columns that don't match
df = df.where(pd.notnull(df), None)
print(df.head())

# MySQL connection configuration using pymysql
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': 'chicagocrimes',  # Use this database once it's created
    'port': os.getenv('DB_PORT')
}

connection = None

try:
    # First, create the database
    temp_connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        port=int(db_config['port'])
    )

    with temp_connection.cursor() as cursor:
        # Create the database if it does not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS chicagocrimes")
        print("Database 'chicagocrimes' created if it did not exist.")
    
    temp_connection.close()

    # Connect to the database that has been created
    connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(connection_string)

    with engine.connect() as connection:
        cursor = connection.connection.cursor()

        # Create the table
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

        # Prepare the insertion query
        insert_query = """
        INSERT INTO crimes (id, CaseNumber, `Date`, Block, `PrimaryType`, `Description`, LocationDescription,
          Arrest, Domestic, Beat, District, Ward, CommunityArea, FbiCode, xCoordinate, yCoordinate, Year, `UpdatedOn`, `Latitude`, `Longitude`, `Location`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Insert data row by row
        for _, row in df.iterrows():
            # Ensure each value in the row is 'None' if it has no data
            values = tuple(None if pd.isna(x) else x for x in [
                row['ID'], row['Case Number'], row['Date'], row['Block'], row['Primary Type'],
                row['Description'], row['Location Description'], row['Arrest'], row['Domestic'],
                row['Beat'], row['District'], row['Ward'], row['Community Area'], row['FBI Code'],
                row['X Coordinate'], row['Y Coordinate'], row['Year'], row['Updated On'],
                row['Latitude'], row['Longitude'], row['Location']
            ])
            cursor.execute(insert_query, values)

        # Commit the changes
        connection.commit()
        print("Data inserted successfully")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection if necessary
    if connection is not None:
        connection.close()
        print("MySQL connection closed")