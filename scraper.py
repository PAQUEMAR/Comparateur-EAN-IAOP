import requests
from bs4 import BeautifulSoup

def run_scrapers(ean):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    urls = [
        'https://www.easypara.com/search?query={ean}', 
        'https://www.newpharma.fr/search?q={ean}', 
        'https://www.cocooncenter.com/search/{ean}', 
        'https://www.pharma-gdd.com/recherche?controller=search&s={ean}', 
        'https://www.pharmashopdiscount.com/modules/gsnsearch/gsnsearch.php?search_query={ean}', 
        'https://www.pharmacie-prado-mermoz.com/recherche?controller=search&s={ean}', 
        'https://www.parapharmazen.com/recherche?controller=search&s={ean}', 
        'https://www.pharmashopi.com/recherche?search_query={ean}', 
        'https://www.santediscount.com/search?search_query={ean}', 
        'https://www.atida.fr/search?q={ean}', 
        'https://www.pharmaciechampvert.fr/recherche?controller=search&s={ean}', 
        'https://www.pharmaclic.be/recherche?controller=search&s={ean}', 
        'https://www.beautysuccess.fr/recherche?controller=search&s={ean}', 
        'https://www.docmorris.fr/search?q={ean}', 
        'https://www.shop-pharmacie.fr/search?q={ean}', 
        'https://www.viata.fr/search?search_query={ean}', 
        'https://www.pharmarket.com/recherche?controller=search&s={ean}', 
        'https://www.1001pharmacies.com/search?query={ean}', 
        'https://www.boticinal.com/search?query={ean}', 
        'https://www.citypharma.com/search?q={ean}'
    ]

    results = []
    for url_template in urls:
        url = url_template.format(ean=ean)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            results.append(f"✅ {url} - OK")
        except Exception as e:
            results.append(f"❌ {url} - Erreur : {e}")
    return results
