
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Configuration Streamlit
st.set_page_config(page_title="Comparateur de prix - Google EAN", layout="centered")
st.title("Comparateur de prix - Google EAN")

# Entrée utilisateur
ean_code = st.text_input("Entrez un code EAN :")
vat_rate = st.slider("Taux de TVA (%)", 0.0, 30.0, 20.0)

# Clé SerpAPI intégrée directement
api_key = "9b4f626e03f2c28cc2fdedccc4a483e4a0626055363820c01e7fb5cc35ce1baa"

def extract_price(text):
    prices = re.findall(r"\d+[\.,]\d{2}", text)
    return float(prices[0].replace(',', '.')) if prices else None

def search_google_ean(ean, api_key):
    params = {
        "engine": "google",
        "q": ean,
        "api_key": api_key,
        "hl": "fr",
        "gl": "fr"
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("organic_results", [])
        return results
    except Exception as e:
        st.error(f"Erreur lors de la récupération des résultats : {e}")
        return []

if ean_code:
    results = search_google_ean(ean_code, api_key)
    data = []

    for result in results:
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")
        price_ttc = extract_price(snippet)
        if price_ttc:
            price_ht = round(price_ttc / (1 + vat_rate / 100), 2)
            data.append({
                "Titre": title,
                "Lien": link,
                "Prix TTC (€)": price_ttc,
                "Prix HT (€)": price_ht
            })

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.warning("Aucun prix détecté dans les résultats. Essayez un autre EAN.")
