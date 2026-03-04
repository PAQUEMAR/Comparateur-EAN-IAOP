import streamlit as st
import pandas as pd
import requests
import re

# Placement OBLIGATOIRE en tout premier avant tout widget Streamlit
st.set_page_config(page_title="Comparateur EAN IAOP", page_icon="💊", layout="centered")

st.title("🔎 Comparateur de prix par EAN International AOP")

def extract_price(text):
    match = re.search(r"(\d+[\.,]?\d*) ?€", text)
    if match:
        return float(match.group(1).replace(',', '.'))
    return None

ean = st.text_input("🔎 Entrez un EAN ou un mot-clé :")
target_price_ht = st.number_input("🎯 Prix cible HT (€)", min_value=0.0, format="%.2f")
tva_rate = st.number_input("💶 Taux de TVA (%)", min_value=0.0, max_value=30.0, value=20.0)

if ean:
    st.markdown(f"#### Résultats pour : `{ean}`")
    with st.spinner("Recherche en cours..."):
        api_key = "os.environ.get("SERPAPI_KEY")"
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
                else:
                    price_ht = None
                    economie = None
                    economie_pct = None

                results.append({
                    "Titre": title,
                    "Lien": link,
                    "Prix TTC (€)": round(price_ttc, 2) if price_ttc else "-",
                    "Prix HT (€)": round(price_ht, 2) if price_ht else "-",
                    "Prix cible HT (€)": round(target_price_ht, 2),
                    "Économie (€)": round(economie, 2) if economie is not None else "-",
                    "Économie (%)": round(economie_pct, 1) if economie_pct is not None else "-"
                })

            if results:
                df = pd.DataFrame(results)
                # Trier par prix HT uniquement si prix disponible
                df_with_price = df[df["Prix HT (€)"] != "-"]
                df_without_price = df[df["Prix HT (€)"] == "-"]
                df_sorted = pd.concat([df_with_price.sort_values(by="Prix HT (€)"), df_without_price])
                st.success(f"✅ {len(df)} résultats trouvés.")
                st.dataframe(df_sorted, use_container_width=True)
            else:
                st.warning("Aucun résultat trouvé.")

        except Exception as e:
            st.error(f"Erreur lors de la recherche : {e}")
