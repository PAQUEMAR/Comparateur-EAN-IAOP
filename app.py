import streamlit as st
from scraper import run_scrapers

st.title("Comparateur de prix par EAN ou mot-clé")
query = st.text_input("Entrez un EAN ou un mot-clé :")

if query:
    st.write(f"Résultats pour : {query}")
    results = run_scrapers(query)
    for site, result in results.items():
        st.write(f"**{site}**")
        st.write(result)
