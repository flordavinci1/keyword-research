import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="Keyword Explorer Educativo", layout="centered")
st.title("🔍 Keyword Explorer Educativo")

st.write("Explorá ideas de palabras clave y temas relacionados para mejorar tu contenido.")

query = st.text_input("Ingresá una palabra clave o tema:", placeholder="Ej: compostaje urbano")

if query:
    st.markdown(f"## Resultados para: **{query}**")

    # Sugerencias de autocompletado (Google)
    st.subheader("📚 Sugerencias de búsqueda relacionadas (Google)")
    try:
        google_suggestions_url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(query)}"
        r = requests.get(google_suggestions_url)
        suggestions = r.json()[1]
        if suggestions:
            for s in suggestions:
                st.markdown(f"- {s}")
        else:
            st.info("No se encontraron sugerencias.")
    except Exception as e:
        st.error(f"Error al obtener sugerencias de Google: {e}")

    # Sugerencias de búsqueda relacionadas (YouTube)
    st.subheader("🎥 Sugerencias de búsqueda en YouTube")
    try:
        yt_url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={urllib.parse.quote(query)}"
        r = requests.get(yt_url)
        suggestions = r.json()[1]
        if suggestions:
            for s in suggestions:
                st.markdown(f"- {s}")
        else:
            st.info("No se encontraron sugerencias en YouTube.")
    except Exception as e:
        st.error(f"Error al obtener sugerencias de YouTube: {e}")

    # Buscar en Wikipedia
    st.subheader("📖 Temas y entidades relacionadas (Wikipedia)")
    try:
        wiki_api = "https://es.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": 5
        }
        r = requests.get(wiki_api, params=params)
        search_results = r.json()["query"]["search"]
        if search_results:
            for result in search_results:
                title = result["title"]
                page_url = f"https://es.wikipedia.org/wiki/{title.replace(' ', '_')}"
                snippet = result["snippet"].replace("<span class=\"searchmatch\">", "**").replace("</span>", "**")
                st.markdown(f"🔗 [{title}]({page_url})")
                st.markdown(f"_{snippet}_\n")
        else:
            st.info("No se encontraron temas en Wikipedia.")
    except Exception as e:
        st.error(f"Error al consultar Wikipedia: {e}")
