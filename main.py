import asyncio
import streamlit as st
from sqlalchemy import create_engine


def connect_db():
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'WmEo.1739'
    db_database = 'chicagocrimes'
    db_port = 3306

    # Create connection string using pymysql
    connection_string = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}'
    return create_engine(connection_string)


async def main():
    if 'db' not in st.session_state:
        print("Initializing database connection...")
        st.session_state.db = connect_db()

    # Crear una barra de navegación
    pages = [
        st.Page("views/about.py", title="About"),
        st.Page("views/dashboard.py", title="Dashboard"),
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