import streamlit as st
from GoogleNews import GoogleNews
import wikipedia
from google_suggest import get_suggestions  # supongamos que tenés esta función

st.title("Keyword Research con Autosuggest y Categorías Wikipedia")

# Inputs
keyword = st.text_input("Ingresa tu keyword")
pais = st.selectbox("Selecciona el país", ["ar", "cl", "es", "mx"])
idioma = st.selectbox("Selecciona el idioma", ["es", "en"])

def obtener_categoria_wikipedia(sugerencia, lang="es"):
    if len(sugerencia.split()) > 4:
        return "No disponible"
    try:
        resultados = wikipedia.search(sugerencia, results=1, lang=lang)
        if resultados:
            titulo = resultados[0]
            primera_palabra = sugerencia.split()[0].lower()
            if primera_palabra in titulo.lower():
                pagina = wikipedia.page(titulo, auto_suggest=False, lang=lang)
                if pagina.categories:
                    return pagina.categories[0]
        return "No disponible"
    except:
        return "No disponible"

if keyword:
    st.info("Consultando sugerencias...")
    sugerencias = get_suggestions(keyword, country=pais, language=idioma)
    
    resultados = []
    for s in sugerencias:
        categoria = obtener_categoria_wikipedia(s, lang=idioma)
        resultados.append({"Keyword": s, "Categoría de referencia": categoria})
    
    st.table(resultados)
