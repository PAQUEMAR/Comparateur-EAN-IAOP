import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def extract_price(text):
    match = re.search(r"(\d+[\.,]?\d*) ?€", text)
    if match:
        return float(match.group(1).replace(',', '.'))
    return None

# Configuration de la page
st.set_page_config(page_title="Comparateur EAN IAOP", page_icon="💊", layout="centered")

# Affichage du logo IAOP (à placer dans le même dossier que ce script)
st.image("logo_IAOP.png", width=200)

# Titre de l'application
st.title("🔎 Comparateur de prix par EAN International AOP")

# Champs utilisateur
ean = st.text_input("🔎 Entrez un EAN ou un mot-clé :")
target_price_ht = st.number_input("🎯 Prix cible HT (€)", min_value=0.0, format="%.2f")
tva_rate = st.number_input("💶 Taux de TVA (%)", min_value=0.0, max_value=30.0, value=20.0)

# Lancement de la recherche
if ean:
    st.markdown(f"#### Résultats pour : `{ean}`")
    with st.spinner("Recherche en cours..."):
        api_key = "9b4f626e03f2c28cc2fdedccc4a483e4a0626055363820c01e7fb5cc35ce1baa"
        params = {
            "q": ean,
            "engine": "google",
            "api_key": api_key,
            "hl": "fr",
            "gl": "fr"
        }

        try:
            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()
            results = []

            for result in data.get("organic_results", []):
                title = result.get("title", "")
                link = result.get("link", "")
                snippet = result.get("snippet", "")
                price_ttc = extract_price(title) or extract_price(snippet)

                if price_ttc:
                    price_ht = price_ttc / (1 + tva_rate / 100)
                    economie = target_price_ht - price_ht
                    economie_pct = (economie / target_price_ht * 100) if target_price_ht else 0

                    results.append({
                        "Titre": title,
                        "Lien": link,
                        "Prix TTC (€)": round(price_ttc, 2),
                        "Prix HT (€)": round(price_ht, 2),
                        "Prix cible HT (€)": round(target_price_ht, 2),
                        "Économie (€)": round(economie, 2),
                        "Économie (%)": round(economie_pct, 1)
                    })

            if results:
                df = pd.DataFrame(results)
                df = df.sort_values(by="Prix HT (€)")
                st.success(f"✅ {len(df)} résultats trouvés.")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Aucun prix trouvé.")

        except Exception as e:
            st.error(f"Erreur lors de la recherche : {e}")
