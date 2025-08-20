import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
import networkx as nx
import plotly.graph_objects as go

st.title("Keyword Research Interactivo")

# --- Selección de país ---
pais = st.selectbox("Seleccioná el país", ["Argentina", "España", "Chile", "México", "US"])
geo_dict = {"Argentina": "AR", "España": "ES", "Chile": "CL", "México": "MX", "US": "US"}
geo = geo_dict[pais]

# --- Input de keyword ---
keyword = st.text_input("Ingresá la palabra clave principal:")

if keyword:
    pytrends = TrendReq(hl='es-ES', tz=360)
    try:
        # --- Obtener sugerencias ---
        sugerencias = pytrends.suggestions(keyword)
        if not sugerencias:
            st.warning("No se encontraron sugerencias para esta palabra clave.")
        else:
            df = pd.DataFrame(sugerencias)
            st.subheader("Sugerencias de Keywords")
            st.dataframe(df[['title', 'type']].rename(columns={"title": "Keyword", "type": "Tipo"}))

            # --- Crear gráfico de relaciones ---
            st.subheader("Relaciones entre Keywords")
            G = nx.Graph()
            # nodo principal
            G.add_node(keyword)
            # nodos secundarios y aristas
            for item in sugerencias:
                G.add_node(item['title'])
                G.add_edge(keyword, item['title'])

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

            node_x, node_y, node_text = [], [], []
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)

            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                text=node_text,
                textposition="bottom center",
                marker=dict(size=20, color='skyblue', line_width=2)
            )

            fig = go.Figure(data=[edge_trace, node_trace])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
