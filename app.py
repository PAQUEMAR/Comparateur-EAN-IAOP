import os
import re
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Comparateur IAOP", page_icon="💊", layout="centered")
st.title("🔎 Comparateur de prix (Google Shopping) — International AOP")

SERPAPI_KEY = os.environ.get("SERPAPI_KEY")

def safe_float(x):
    try:
        return float(str(x).replace(",", "."))
    except:
        return None

def extract_price_from_text(text: str):
    # Ex: "12,90 €", "12.90€"
    if not text:
        return None
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*€", text)
    if not m:
        return None
    return safe_float(m.group(1))

def serpapi_google_shopping(query: str, hl="fr", gl="fr", num=20):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_KEY,
        "hl": hl,
        "gl": gl,
        "num": num
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def serpapi_google_organic(query: str, hl="fr", gl="fr", num=10):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "hl": hl,
        "gl": gl,
        "num": num
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

# UI
query = st.text_input("🔎 Entrez un EAN ou un mot-clé :")
target_price_ht = st.number_input("🎯 Prix cible HT (€)", min_value=0.0, format="%.2f")
tva_rate = st.number_input("💶 Taux de TVA (%)", min_value=0.0, max_value=30.0, value=20.0)

mode = st.selectbox("Mode", ["Google Shopping (recommandé)", "Google (fallback snippets)"])

if query:
    if not SERPAPI_KEY:
        st.error("❌ SERPAPI_KEY manquante. Ajoute-la dans Render → Environment Variables.")
        st.stop()

    st.markdown(f"### Résultats pour : `{query}`")

    with st.spinner("Recherche en cours..."):
        results = []

        try:
            if mode.startswith("Google Shopping"):
                data = serpapi_google_shopping(query)
                items = data.get("shopping_results", [])

                for it in items:
                    title = it.get("title", "") or "-"
                    link = it.get("link", "") or it.get("product_link", "") or "-"
                    source = it.get("source", "") or it.get("seller", "") or "-"
                    price_str = it.get("price", "")  # souvent "12,90 €"
                    price_ttc = extract_price_from_text(price_str)

                    # parfois SerpAPI donne extracted_price
                    extracted = it.get("extracted_price")
                    if price_ttc is None and extracted is not None:
                        price_ttc = safe_float(extracted)

                    if price_ttc is not None:
                        price_ht = price_ttc / (1 + tva_rate / 100)
                        economie = target_price_ht - price_ht if target_price_ht else None
                        economie_pct = (economie / target_price_ht * 100) if target_price_ht and economie is not None else None
                    else:
                        price_ht = None
                        economie = None
                        economie_pct = None

                    results.append({
                        "Source": source,
                        "Titre": title,
                        "Prix TTC (€)": round(price_ttc, 2) if price_ttc is not None else "-",
                        "Prix HT (€)": round(price_ht, 2) if price_ht is not None else "-",
                        "Lien": link,
                        "Économie (€)": round(economie, 2) if economie is not None else "-",
                        "Économie (%)": round(economie_pct, 1) if economie_pct is not None else "-"
                    })

            else:
                data = serpapi_google_organic(query)
                items = data.get("organic_results", [])

                for it in items:
                    title = it.get("title", "") or "-"
                    link = it.get("link", "") or "-"
                    snippet = it.get("snippet", "") or ""
                    price_ttc = extract_price_from_text(title) or extract_price_from_text(snippet)

                    if price_ttc is not None:
                        price_ht = price_ttc / (1 + tva_rate / 100)
                        economie = target_price_ht - price_ht if target_price_ht else None
                        economie_pct = (economie / target_price_ht * 100) if target_price_ht and economie is not None else None
                    else:
                        price_ht = None
                        economie = None
                        economie_pct = None

                    results.append({
                        "Source": "Google",
                        "Titre": title,
                        "Prix TTC (€)": round(price_ttc, 2) if price_ttc is not None else "-",
                        "Prix HT (€)": round(price_ht, 2) if price_ht is not None else "-",
                        "Lien": link,
                        "Économie (€)": round(economie, 2) if economie is not None else "-",
                        "Économie (%)": round(economie_pct, 1) if economie_pct is not None else "-"
                    })

        except requests.HTTPError as e:
            st.error(f"Erreur SerpAPI (HTTP). Vérifie ta clé / quota. Détail: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Erreur : {e}")
            st.stop()

    if not results:
        st.warning("Aucun résultat trouvé.")
    else:
        df = pd.DataFrame(results)

        # Tri : d'abord ceux qui ont un prix HT, puis les autres
        df_with = df[df["Prix HT (€)"] != "-"].copy()
        df_without = df[df["Prix HT (€)"] == "-"].copy()

        if not df_with.empty:
            df_with["Prix HT (€)"] = df_with["Prix HT (€)"].astype(float)
            df_with = df_with.sort_values(by="Prix HT (€)", ascending=True)

        df_sorted = pd.concat([df_with, df_without], ignore_index=True)

        st.success(f"✅ {len(df_sorted)} résultats.")
        st.dataframe(df_sorted, use_container_width=True)

        st.caption("Astuce : si tu as 'Aucun résultat', passe en mode Google Shopping (recommandé).")
