import streamlit as st
import requests
import urllib.parse
import re
from collections import defaultdict

st.set_page_config(page_title="Keyword Explorer Educativo (completo)", layout="centered")
st.title("🔍 Flor de Research - U Keyword Explorer Educativo")
st.write("Explorá ideas de palabras clave, descubrí intención de búsqueda y agrupá por tema para crear mejores contenidos.")

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
        google_url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(query)}"
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
        yt_url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={urllib.parse.quote(query)}"
        r = requests.get(yt_url)
        yt_suggestions = r.json()[1]
        sugerencias_totales.extend(yt_suggestions)
        if yt_suggestions:
            for s in yt_suggestions:
                st.markdown(f"- {s}")
        else:
            st.info("No se encontraron sugerencias en YouTube.")
    except Exception as e:
        st.error(f"Error al obtener sugerencias de YouTube: {e}")

    # Sección 3: Wikipedia
    st.subheader("📖 Temas y entidades desde Wikipedia")
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
        results = r.json()["query"]["search"]
        if results:
            for result in results:
                title = result["title"]
                snippet = result["snippet"].replace("<span class=\"searchmatch\">", "**").replace("</span>", "**")
                url = f"https://es.wikipedia.org/wiki/{title.replace(' ', '_')}"
                st.markdown(f"🔗 [{title}]({url})")
                st.markdown(f"_{snippet}_\n")
        else:
            st.info("No se encontraron temas en Wikipedia.")
    except Exception as e:
        st.error(f"Error al consultar Wikipedia: {e}")

    # Sección 4: Clasificación por intención
    st.subheader("🔎 Clasificación por intención de búsqueda")
    if sugerencias_totales:
        for s in sorted(set(sugerencias_totales)):
            tipo = clasificar_intencion(s)
            st.markdown(f"- {tipo} → **{s}**")

    # Sección 5: Agrupamiento temático
    st.subheader("🧩 Agrupamiento temático")
    grupos = agrupar_keywords(sorted(set(sugerencias_totales)))
    for grupo, items in grupos.items():
        st.markdown(f"**Grupo `{grupo}`** ({len(items)}):")
        for item in items:
            st.markdown(f"- {item}")
        st.markdown("---")

# CTA final
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>✨ Esta herramienta fue creada con fines educativos y de asistencia a profesionales que están comenzando en SEO.</p>
        <p>💌 ¿Te sirvió? ¿Tenés alguna sugerencia? ¿Querés charlar sobre SEO, comunicación digital o IA aplicada? Escribime a <a href="mailto:florencia@crawla.agency">florencia@crawla.agency</a></p>
        <br>
        <a href="https://www.linkedin.com/in/festevez3005/" target="_blank">
            <button style="background-color:#4B8BBE; color:white; padding:10px 20px; font-size:16px; border:none; border-radius:6px; cursor:pointer;">
                🌐 Conectá conmigo en LinkedIn
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
