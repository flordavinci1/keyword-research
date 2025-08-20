# app.py
import streamlit as st
from googlesearch import search_suggestions
import wikipedia

# Configuración de Wikipedia
wikipedia.set_lang("es")  # idioma por defecto, luego se ajusta según input

st.title("Herramienta de Keyword Research")

# Inputs
keyword = st.text_input("Ingresa la palabra clave")
country = st.selectbox("País", ["Argentina", "España", "México", "Chile"])
language = st.selectbox("Idioma", ["es", "en", "pt"])

# Ajustamos Wikipedia al idioma elegido
wikipedia.set_lang(language)

def get_wikipedia_category(term):
    try:
        # Buscar página más relevante
        page = wikipedia.page(term)
        # Comprobamos coincidencia parcial
        if term.lower() in page.title.lower():
            cats = wikipedia.categories(page.title)
            if cats:
                return cats[0]  # primera categoría como ejemplo
        return "No disponible"
    except:
        return "No disponible"

if st.button("Buscar"):
    if keyword:
        st.write("Buscando sugerencias...")
        suggestions = search_suggestions(keyword, language=language, country=country)
        
        results = []
        for sug in suggestions:
            category = get_wikipedia_category(sug)
            results.append({"Keyword": sug, "Categoría de referencia": category})
        
        st.table(results)
    else:
        st.warning("Por favor, ingresa una palabra clave.")
