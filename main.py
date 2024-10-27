import streamlit as st

# Importar las páginas
from page1 import page1
from page2 import page2

def main():
    # Crear una barra de navegación
    pages = {
        "Explaining": page2,
        "Dashboard": page1
    }
    st.set_page_config(
        page_title="Chicago Crimes 2023",
        page_icon="👮🏻",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    with st.sidebar:
        
        
        st.title('👮🏻 Chicago Crimes 2023')
        selected_page = st.sidebar.selectbox("Select a page", options=list(pages.keys()))

    # Ejecutar la función de la página seleccionada
    pages[selected_page]()

if __name__ == "__main__":
    main()