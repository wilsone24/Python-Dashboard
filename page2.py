import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

def page2():
    st.title("👮🏻 Chicago Crimes 2023")
    
    # Section explaining the dashboard with increased font size
    st.markdown("""
    <p style='font-size: 18px;'>This dashboard is an essential tool for visualizing and analyzing crime data in Chicago. 
    It allows users to understand the distribution and frequency of crimes in different areas, 
    which can aid in decision-making to improve public safety. 
    The creation of this application is based on the need to provide clear and accessible information 
    about crime incidence, thus facilitating the identification of patterns and trends over time.</p>
    """, unsafe_allow_html=True)

    # Create two columns for the images
    col1, col2 = st.columns(2)

    # Center the first image in the first column
    with col1:
        st.image('https://i.ibb.co/SsTw7v4/police-line.gif', caption='Crime Visualization in Chicago', use_column_width=True)

    # Center the second image in the second column
    with col2:
        st.image('https://i.ibb.co/Wsfj35M/siren.gif', caption='Crime Visualization in Chicago', use_column_width=True)
    
    # Table of column descriptions
    st.header("Column Descriptions of the Database")
    column_descriptions = {
        "Column Name": [
            "ID", "Case Number", "Date", "Block", "IUCR", 
            "Primary Type", "Description", "Location Description", 
            "Arrest", "Domestic", "Beat", "District", 
            "Ward", "Community Area", "FBI Code", "X Coordinate", 
            "Y Coordinate", "Year", "Updated On", "Latitude", 
            "Longitude", "Location"
        ],
        "Description": [
            "Unique identifier for the record.",
            "The Chicago Police Department RD Number (Records Division Number), which is unique to the incident.",
            "Date when the incident occurred; this is sometimes a best estimate.",
            "The partially redacted address where the incident occurred, placing it on the same block as the actual address.",
            "The Illinois Uniform Crime Reporting code, directly linked to the Primary Type and Description.",
            "The primary description of the IUCR code.",
            "The secondary description of the IUCR code, a subcategory of the primary description.",
            "Description of the location where the incident occurred.",
            "Indicates whether an arrest was made.",
            "Indicates whether the incident was domestic-related as defined by the Illinois Domestic Violence Act.",
            "Indicates the beat where the incident occurred.",
            "Indicates the police district where the incident occurred.",
            "The ward (City Council district) where the incident occurred.",
            "Indicates the community area where the incident occurred.",
            "Indicates the crime classification as outlined in the FBI's National Incident-Based Reporting System (NIBRS).",
            "The x coordinate of the location where the incident occurred.",
            "The y coordinate of the location where the incident occurred.",
            "Year the incident occurred.",
            "Date and time the record was last updated.",
            "The latitude of the location where the incident occurred.",
            "The longitude of the location where the incident occurred.",
            "The location where the incident occurred in a format that allows for geographic operations."
        ],
        "API Field Name": [
            "id", "case_number", "date", "block", "iucr",
            "primary_type", "description", "location_description",
            "arrest", "domestic", "beat", "district",
            "ward", "community_area", "fbi_code", "x_coordinate",
            "y_coordinate", "year", "updated_on", "latitude",
            "longitude", "location"
        ],
        "Data Type": [
            "Number", "Text", "Floating Timestamp", "Text", "Text",
            "Text", "Text", "Text", "Checkbox", "Checkbox",
            "Text", "Text", "Number", "Text", "Text",
            "Number", "Number", "Number", "Floating Timestamp",
            "Number", "Number", "Location"
        ]
    }
    column_df = pd.DataFrame(column_descriptions)
    st.table(column_df)
    
    # Load and display the data from the database
    st.header("Chicago Crime Data")
    
    # Database connection parameters
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'WmEo.1739'
    db_database = 'chicagocrimes'
    db_port = 3306

    # Create connection string using pymysql
    connection_string = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}'
    engine = create_engine(connection_string)
    
    # Fetch data from the database
    query = "SELECT * FROM crimes"  # Replace 'crimes' with the actual table name
    data = pd.read_sql(query, engine)
    
    st.dataframe(data)

if __name__ == "__main__":
    page2()
