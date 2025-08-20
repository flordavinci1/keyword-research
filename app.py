import streamlit as st
import requests
import json
import wikipedia
import networkx as nx
from pyvis.network import Network

# --- Configuración ---
st.set_page_config(page_title="Keyword Research Semántico", layout="wide")
st.title("🔍 Keyword Research Semántico")

# --- Input ---
keyword = st.text_input("Escribí la palabra clave principal")
pais = st.selectbox("Seleccioná el país", ["Argentina", "España", "Chile", "México", "US"])
geo_dict = {"Argentina": "AR", "España": "ES", "Chile": "CL", "México": "MX", "US": "US"}
lang_dict = {"Argentina": "es", "España": "es", "Chile": "es", "México": "es", "US": "en"}
geo_code = geo_dict[pais]
lang = lang_dict[pais]

if keyword:
    st.info("Obteniendo sugerencias de Google...")
    
    # --- Autosuggest ---
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl={lang}&ds=yt&q={keyword}"
    try:
        response = requests.get(url)
        suggestions = response.json()[1][:15]  # máximo 15 sugerencias
    except Exception as e:
        st.error(f"No se pudieron obtener sugerencias: {e}")
        suggestions = []

    if suggestions:
        st.success(f"Se encontraron {len(suggestions)} sugerencias")
        st.write(suggestions)
        
        # --- Relación con Wikipedia ---
        st.info("Buscando relaciones en Wikipedia...")
        entities = {}
        for sug in suggestions:
            try:
                page = wikipedia.page(sug, auto_suggest=True, lang=lang)
                categories = page.categories[:5]  # máximo 5 categorías
                entities[sug] = categories
            except Exception:
                entities[sug] = []

        st.write("Relaciones con Wikipedia (categorías):")
        st.json(entities)

        # --- Grafo de relaciones ---
        st.info("Generando grafo interactivo...")
        G = nx.Graph()
        G.add_node(keyword, color="red", size=20)
        
        for sug, cats in entities.items():
            G.add_node(sug, color="orange", size=15)
            G.add_edge(keyword, sug)
            for cat in cats:
                G.add_node(cat, color="lightblue", size=10)
                G.add_edge(sug, cat)

        net = Network(height="600px", width="100%", notebook=False)
        net.from_nx(G)
        net.show_buttons(filter_=['physics'])
        net.show("graph.html")

        st.components.v1.html(open("graph.html", "r", encoding="utf-8").read(), height=650)

    else:
        st.warning("No se encontraron sugerencias para esta keyword.")
