import streamlit as st
import requests
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from pytrends.request import TrendReq

st.title("Keyword Research con Google Autosuggest + Estimado de Búsqueda")

# --- Selección de país ---
pais = st.selectbox("Seleccioná el país", ["Argentina", "España", "Chile", "México", "US"])
geo_dict = {"Argentina": "AR", "España": "ES", "Chile": "CL", "México": "MX", "US": "US"}
geo = geo_dict[pais]

# Pytrends country mapping
pytrends_country = {"Argentina": "AR", "España": "ES", "Chile": "CL", "México": "MX", "US": "US"}

# --- Input de keyword ---
keyword = st.text_input("Ingresá la palabra clave principal:")

def get_google_suggestions(query, country_code):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl=es&gl={country_code}&q={query}"
    resp = requests.get(url)
    if resp.status_code == 200:
        suggestions = resp.json()[1]
        return suggestions
    return []

def get_interest_trends(keywords, geo):
    pytrends = TrendReq(hl='es', tz=360)
    pytrends.build_payload(keywords, geo=geo)
    data = pytrends.interest_over_time()
    if not data.empty:
        return data[keywords].mean().sort_values(ascending=False)
    else:
        return pd.Series([0]*len(keywords), index=keywords)

if keyword:
    try:
        sugerencias = get_google_suggestions(keyword, geo)
        if not sugerencias:
            st.warning("No se encontraron sugerencias para esta palabra clave.")
        else:
            # --- Estimado de interés con Pytrends ---
            keywords_for_trends = [keyword] + sugerencias
            st.info("Consultando interés de búsqueda en Google Trends (puede tardar unos segundos)...")
            trends = get_interest_trends(keywords_for_trends, geo)
            df = pd.DataFrame({"Keyword": trends.index, "Interés Relativo": trends.values})
            st.subheader("Sugerencias de Keywords con Interés Estimado")
            st.dataframe(df)

            # --- Gráfico de relaciones ---
            st.subheader("Relaciones entre Keywords")
            G = nx.Graph()
            for k in trends.index:
                G.add_node(k, size=int(trends[k]))
            for item in sugerencias:
                G.add_edge(keyword, item)

            pos = nx.spring_layout(G, seed=42)
            edge_x, edge_y = [], []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=1, color='#888'),
                hoverinfo='none',
                mode='lines'
            )

            node_x, node_y, node_text, node_size = [], [], [], []
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)
                node_size.append(G.nodes[node]['size']*0.5 + 10)  # Ajuste de tamaño

            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                text=node_text,
                textposition="bottom center",
                marker=dict(size=node_size, color='skyblue', line_width=2)
            )

            fig = go.Figure(data=[edge_trace, node_trace])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
