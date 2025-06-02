
import streamlit as st
import requests
import pandas as pd
import re

# Clé API SerpAPI
API_KEY = "9b4f626e03f2c28cc2fdedccc4a483e4a0626055363820c01e7fb5cc35ce1baa"

def extraire_prix(prix_str):
    try:
        prix_str = prix_str.replace(",", ".")
        prix = re.findall(r"\d+\.\d+", prix_str)
        return float(prix[0]) if prix else None
    except:
        return None

def chercher_google_par_ean(ean, tva):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": ean,
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    data = response.json()
    resultats = []

    shopping_results = data.get("shopping_results", [])
    for item in shopping_results:
        titre = item.get("title", "N/A")
        prix_ttc = extraire_prix(item.get("price", ""))
        lien = item.get("link", "")
        if prix_ttc is not None:
            prix_ht = round(prix_ttc / (1 + (tva / 100)), 2)
            resultats.append({
                "Produit": titre,
                "Prix TTC (€)": prix_ttc,
                "Prix HT (€)": prix_ht,
                "Lien": lien
            })

    return resultats

st.title("Comparateur de prix - Google EAN")

ean = st.text_input("Entrez un code EAN :")
tva = st.slider("Taux de TVA (%)", 0.0, 30.0, 20.0)

if ean:
    donnees = chercher_google_par_ean(ean, tva)
    if donnees:
        df = pd.DataFrame(donnees)
        df["Lien"] = df["Lien"].apply(lambda x: f"[Voir]({x})")
        st.markdown("### Résultats de la recherche :")
        st.write(df.to_markdown(index=False), unsafe_allow_html=True)
    else:
        st.warning("Aucun résultat trouvé ou une erreur est survenue.")
