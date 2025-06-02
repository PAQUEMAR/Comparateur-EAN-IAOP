
import requests

API_KEY = "9b4f626e03f2c28cc2fdedccc4a483e4a0626055363820c01e7fb5cc35ce1baa"
SEARCH_ENGINE_ID = "google"

def search_google_results(query):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": API_KEY,
        "hl": "fr",
        "gl": "fr",
        "num": 20
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = []
        for result in data.get("organic_results", []):
            results.append({
                "Titre": result.get("title"),
                "Lien": result.get("link"),
                "Extrait": result.get("snippet", "")
            })
        return results
    except Exception as e:
        print(f"Erreur SerpAPI: {e}")
        return []
