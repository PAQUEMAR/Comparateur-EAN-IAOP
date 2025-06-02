import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def extract_price(text):
    """Extrait un prix à partir d'une chaîne de texte."""
    match = re.search(r"(\d+[\.,]?\d*) ?€", text)
    if match:
        return float(match.group(1).replace(',', '.'))
    return None

# Configuration de la page
st.set_page_config(page_title="Comparateur International AOP", page_icon="🌍")

st.title("🔎 Comparateur International AOP - Recherche par EAN")
st.markdown("---")

# Champs de saisie
ean = st.text_input("📦 Entrez un code EAN :")
target_price = st.number_input("🎯 Prix cible HT (€)", min_value=0.0, format="%.2f")
tva_rate = st.number_input("💶 Taux de TVA (%)", min_value=0.0, max_value=30.0, value=20.0)

# Recherche
if ean and target_price > 0:
    with st.spinner("🔍 Recherche en cours, merci de patienter..."):
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
                link = result.get("link", "")
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                price_ttc = extract_price(title) or extract_price(snippet)

                if price_ttc:
                    price_ht = price_ttc / (1 + tva_rate / 100)
                    economy = max(0, target_price - price_ht)
                    economy_pct = (economy / target_price * 100) if target_price else 0

                    results.append({
                        "Site": f"[Lien]({link})",
                        "Nom du produit": title,
                        "Prix TTC (€)": round(price_ttc, 2),
                        "Prix HT (€)": round(price_ht, 2),
                        "Prix cible HT (€)": round(target_price, 2),
                        "Économie (€)": round(economy, 2),
                        "Économie (%)": round(economy_pct, 1)
                    })

            if results:
                df = pd.DataFrame(results)
                df = df.sort_values(by="Prix HT (€)")
                st.success(f"✅ {len(results)} résultats trouvés.")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Aucun résultat trouvé ou aucune correspondance de prix.")

        except Exception as e:
            st.error(f"Erreur : {e}")
