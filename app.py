# Modification pour forcer le rebuild sur Render

import streamlit as st
import pandas as pd
from serp_scraper import search_google_results

st.title("Comparateur de prix par EAN via Google")
ean = st.text_input("Entrez un EAN ou un mot-clé :")

if ean:
    st.write(f"Résultats pour : {ean}")
    results = search_google_results(ean)
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df)
    else:
        st.warning("Aucun résultat trouvé ou erreur lors de la recherche.")
