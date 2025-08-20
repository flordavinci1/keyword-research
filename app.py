import streamlit as st
import requests
import urllib.parse
import re
from collections import defaultdict

st.set_page_config(page_title="Keyword Explorer Educativo (completo)", layout="centered")
st.title("🔍 Flor de Research - Un Keyword Explorer Educativo")
st.write("Explorá ideas de palabras clave, descubrí intención de búsqueda y agrupá por tema para crear mejores contenidos.")

# --- Selección de país e idioma ---
st.sidebar.header("🌎 Configuración de búsqueda")
pais = st.sidebar.selectbox("Seleccioná un país:", ["Argentina", "España", "México", "Chile", "Colombia", "Estados Unidos"])
idioma = st.sidebar.selectbox("Seleccioná un idioma:", ["es", "en", "pt"])

# Mapeo simple para códigos de país que usa Google
pais_cod = {
    "Argentina": "AR",
    "España": "ES",
    "México": "MX",
    "Chile": "CL",
    "Colombia": "CO",
    "Estados Unidos": "US"
}
gl = pais_cod.get(pais, "AR")
hl = idioma

query = st.text_input("🔡 Ingresá una palabra clave o tema:", placeholder="Ej: compostaje urbano")

# Función: Clasificación de intención
def clasificar_intencion(palabra):
    palabra = palabra.lower()
    if re.match(r"^(qué|como|por qué|para qué|quién|cuándo|dónde|tipos de|beneficios de)", palabra):
        return "📘 Informacional"
    elif any(p in palabra for p in ["comprar", "mejor", "precio", "opiniones", "barato", "oferta", "envío", "promoción"]):
        return "🛒 Comercial / Transaccional"
    elif any(p in palabra for p in ["facebook", "instagram", "youtube", "mercadolibre", "wikipedia", ".com", ".ar"]):
        return "🧭 Navegacional"
    else:
        return "📘 Informacional"

# Función: Agrupamiento temático simple
def agrupar_keywords(sugerencias):
    grupos = defaultdict(list)
    for kw in sugerencias:
        tokens = [t for t in kw.lower().split() if t not in ("de", "para", "con", "el", "la", "los", "en", "y", "por")]
        clave = tokens[0] if tokens else "Otros"
        grupos[clave].append(kw)
    return grupos

if query:
    st.markdown(f"## Resultados para: **{query}**")
    sugerencias_totales = []

    # Sección 1: Sugerencias de Google
    st.subheader("📚 Sugerencias desde Google")
    try:
        google_url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(query)}&hl={hl}&gl={gl}"
        r = requests.get(google_url)
        google_suggestions = r.json()[1]
        sugerencias_totales.extend(google_suggestions)
        if google_suggestions:
            for s in google_suggestions:
                st.markdown(f"- {s}")
        else:
            st.info("No se encontraron sugerencias.")
    except Exception as e:
        st.error(f"Error al obtener sugerencias de Google: {e}")

    # Sección 2: Sugerencias de YouTube
    st.subheader("🎥 Sugerencias desde YouTube")
    try:
        yt_url = f"https://suggestqueries.google.com/complete/search?clie_
