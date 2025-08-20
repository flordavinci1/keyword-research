import streamlit as st
import requests
from pyvis.network import Network
import networkx as nx
import wikipedia
import urllib.parse
import time

st.set_page_config(page_title="Keyword Research Tool", layout="wide")
st.title("Herramienta de Keyword Research y Relaciones Semánticas")

# --- Selección de país e idioma ---
country = st.selectbox("Elegí el país para tus sugerencias:", 
                       ["Argentina", "España", "México", "Chile", "Colombia", "Estados Unidos"])
lang = st.selectbox("Elegí el idioma:", ["es", "en", "pt"])

country_codes = {
    "Argentina": "ar",
    "España": "es",
    "México": "mx",
    "Chile": "cl",
    "Colombia": "co",
    "Estados Unidos": "us"
}
cc = country_codes[country]

# --- Input de keyword ---
keyword = st.text_input("Ingresá la palabra clave principal:")

# Función de autosuggest de Google
def get_google_suggestions(q, cc="us"):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl={cc}&q={urllib.parse.quote(q)}"
    try:
        resp = requests.get(url, timeout=5)
        suggestions = resp.json()[1]
    except:
        suggestions = []
    return suggestions

# Función de extracción de categorías y extracto de Wikipedia
def get_wikipedia_info(term, lang="es"):
    wikipedia.set_lang(lang)
    data = {"categories": [], "summary": ""}
    try:
        page_title = wikipedia.search(term)[0]
        page = wikipedia.page(page_title)
        cats = page.categories
        data["categories"] = [c.replace("Categoría:", "") for c in cats if c][:3]  # máximo 3 categorías
        data["summary"] = page.summary[:300] + "..." if page.summary else ""
    except:
        data = {"categories": [], "summary": ""}
    return data

if keyword:
    st.info("Consultando sugerencias de Google...")
    suggestions = get_google_suggestions(keyword, cc)
    st.success(f"Se encontraron {len(suggestions)} sugerencias.")
    
    entities = {}
    for sug in suggestions:
        info = get_wikipedia_info(sug, lang)
        entities[sug] = info
        time.sleep(0.3)  # Para no saturar Wikipedia
    
    st.subheader("Sugerencias, categorías y extractos de Wikipedia")
    for sug, info in entities.items():
        cats = info["categories"]
        summary = info["summary"]
        st.write(f"- **{sug}**")
        st.write(f"  - Categorías: {', '.join(cats) if cats else 'Sin categorías encontradas'}")
        if summary:
            st.write(f"  - Extracto: {summary}")
    
    # --- Grafo interactivo ---
    st.info("Generando grafo interactivo...")
    G = nx.Graph()
    G.add_node(keyword, color="red", size=20)
    for sug, info in entities.items():
        G.add_node(sug, color="orange", size=15)
        G.add_edge(keyword, sug)
        for cat in info["categories"]:
            G.add_node(cat, color="lightblue", size=10)
            G.add_edge(sug, cat)
    
    net = Network(height="600px", width="100%")
    net.from_nx(G)
    net.show_buttons(filter_=['physics'])
    
    html_file = "graph.html"
    net.write_html(html_file)
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=650, scrolling=True)
