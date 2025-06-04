
import requests
import streamlit as st
from urllib.parse import quote
import pandas as pd

API_KEY = "9b4f626e03f2c28cc2fdedccc4a483e4a0626055363820c01e7fb5cc35ce1baa"
SEARCH_ENGINE_ID = "google"

def get_search_results(query):
    url = f"https://serpapi.com/search.json?q={quote(query)}&engine={SEARCH_ENGINE_ID}&api_key={API_KEY}&hl=fr&gl=fr"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("organic_results", [])

def main():
    st.title("Comparateur de prix - Recherche Google par EAN")
    ean_input = st.text_input("Entrez un code EAN :")

    if ean_input:
        with st.spinner("Recherche en cours..."):
            try:
                results = get_search_results(ean_input)
                if results:
                    data = [{"Titre": r.get("title"), "Lien": r.get("link")} for r in results]
                    df = pd.DataFrame(data)
                    st.success(f"{len(results)} résultats trouvés.")
                    st.dataframe(df)
                else:
                    st.warning("Aucun résultat trouvé.")
            except Exception as e:
                st.error(f"Erreur lors de la recherche : {e}")

if __name__ == "__main__":
    main()
