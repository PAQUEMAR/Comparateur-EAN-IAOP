
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

PHARMACIES = {
    "https://www.easypara.com": "https://www.easypara.com/search?query={}",
    "https://www.newpharma.fr": "https://www.newpharma.fr/search?q={}",
    "https://www.cocooncenter.com": "https://www.cocooncenter.com/search/{}",
    "https://www.pharma-gdd.com": "https://www.pharma-gdd.com/recherche?controller=search&s={}",
    "https://www.pharmashopdiscount.com": "https://www.pharmashopdiscount.com/modules/gsnsearch/gsnsearch.php?search_query={}",
    "https://www.pharmacie-prado-mermoz.com": "https://www.pharmacie-prado-mermoz.com/recherche?controller=search&s={}",
    "https://www.parapharmazen.com": "https://www.parapharmazen.com/recherche?search_query={}",
    "https://www.pharmashopi.com": "https://www.pharmashopi.com/recherche?search_query={}",
    "https://www.santediscount.com": "https://www.santediscount.com/recherche?search_query={}",
    "https://www.atida.fr": "https://www.atida.fr/search?q={}",
    "https://www.pharmaciechampvert.fr": "https://www.pharmaciechampvert.fr/recherche?controller=search&s={}"
}

def scrape_site(base_url, search_url, query):
    try:
        response = requests.get(search_url.format(query), headers=HEADERS, timeout=10)
        response.raise_for_status()
        return f"✓ {base_url} fonctionne (HTTP {response.status_code})"
    except requests.exceptions.HTTPError as http_err:
        return f"Erreur lors du scraping de {base_url} : {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Erreur lors du scraping de {base_url} : {req_err}"

def run_scrapers(query):
    results = {}
    for site, search_url in PHARMACIES.items():
        result = scrape_site(site, search_url, query)
        results[site] = result
    return results
