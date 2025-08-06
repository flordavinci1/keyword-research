import streamlit as st
import requests
import urllib.parse
import re
from collections import defaultdict

st.set_page_config(page_title="Keyword Explorer Educativo V2", layout="centered")
st.title("🔍 Keyword Explorer Educativo V2")
st.write("Explorá palabras clave relacionadas y aprendé sobre intención de búsqueda y agrupación temática.")

query = st.text_input("Ingresá una palabra clave o tema:", placeholder="Ej: compostaje urbano")

# Clasificación de intención
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

# Agrupamiento temático simple
def agrupar_keywords(sugerencias):
    grupos = defaultdict(list)
    for kw in sugerencias:
        tokens = [t for t in kw.lower().split() if t not in ("de", "para", "con", "el", "la", "los", "en", "y", "por")]
        clave = tokens[0] if tokens else "Otros"
        grupos[clave].append(kw)
    return grupos

if query:
    st.markdown(f"### Resultados para: **{query}**")

    # Obtener sugerencias de Google
    try:
        suggest_url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(query)}"
        r = requests.get(suggest_url)
        sugerencias = r.json()[1]
        st.success(f"Se encontraron {len(sugerencias)} sugerencias.")

        # Clasificar cada una
        st.subheader("🔎 Sugerencias clasificadas por intención de búsqueda")
        for s in sugerencias:
            tipo = clasificar_intencion(s)
            st.markdown(f"- {tipo} → **{s}**")

        # Agrupar
        st.subheader("🧩 Agrupamiento temático")
        grupos = agrupar_keywords(sugerencias)
        for clave, items in grupos.items():
            st.markdown(f"**Grupo `{clave}`** ({len(items)}):")
            for item in items:
                st.markdown(f"- {item}")
            st.markdown("---")

    except Exception as e:
        st.error(f"No se pudo obtener sugerencias: {e}")
