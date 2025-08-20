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
        sugerencias = get_go_
