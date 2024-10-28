import asyncio
import os

import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


def connect_db():
    db_host = os.environ.get("DB_HOST")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_database = os.environ.get("DB_NAME") or "chicagocrimes"
    db_port = os.environ.get("DB_PORT") or 3306

    # Create connection string using pymysql
    connection_string = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}'
    return create_engine(connection_string)


async def main():
    if 'db' not in st.session_state:
        print("Initializing database connection...")
        st.session_state.db = connect_db()

    # Crear una barra de navegación
    pages = [
        st.Page("views/about.py", title="About", icon=":material/info:"),
        st.Page("views/dashboard.py", title="Dashboard", icon=":material/monitoring:"),
    ]

    st.set_page_config(
        page_title="Chicago Crimes 2023",
        page_icon="👮🏻",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    asyncio.run(main())