import streamlit as st
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from pyvis.network import Network
import wikipedia
from googlesearch import search
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Keyword Research Tool", layout="wide")
st.title("Herramienta de Keyword Research")

# Inputs
query = st.text_input("Ingresa el término o frase principal:")
country = st.selectbox("Selecciona el país:", ["Argentina", "España", "Chile", "México"])
language = st.selectbox("Selecciona el idioma:", ["es", "en", "pt"])

# Función para autosuggest de Google
def get_google_suggestions(term, lang="es", country="AR"):
    url = f"https://www.google.com/complete/search?client=firefox&hl={lang}&gl={country}&q={term}"
    response = requests.get(url)
    suggestions = []
    if response.status_code == 200:
        suggestions = [item[0] for item in response.json()[1]]
    return suggestions

# Función de obtención de primera categoría de Wikipedia
def get_first_wikipedia_category(term, lang="es"):
    wikipedia.set_lang(lang)
    try:
        search_results = wikipedia.search(term)
        if not search_results:
            return None
        page_title = search_results[0]
        page = wikipedia.page(page_title)
        categories = page.categories
        # Solo devolver si hay categorías válidas
        valid_categories = [c for c in categories if not c.lower().startswith("wikipedia:") and not c.lower().startswith("categoría:") and len(c) > 2]
        if valid_categories:
            return valid_categories[0]
    except:
        return None
    return None

# Mapping país -> código de país Google
country_codes = {
    "Argentina": "AR",
    "España": "ES",
    "Chile": "CL",
    "México": "MX"
}

if query:
    st.write("Buscando sugerencias de Google...")
    suggestions = get_google_suggestions(query, lang=language, country=country_codes[country])
    
    st.subheader("Sugerencias y ejemplo de categoría de Wikipedia")
    entities = {}
    for sug in suggestions:
        cat = get_first_wikipedia_category(sug, lang=language)
        entities[sug] = cat
        st.write(f"- **{sug}**")
        if cat:
            st.write(f"  - Categoría de referencia: {cat}")

    # Grafo de relaciones
    net = Network(height="500px", width="100%", notebook=True)
    net.add_node(query, label=query, color="red")
    for sug, cat in entities.items():
        net.add_node(sug, label=sug, color="blue")
        net.add_edge(query, sug)
    net.show("graph.html")
    st.components.v1.html(open("graph.html", "r", encoding="utf-8").read(), height=500)
