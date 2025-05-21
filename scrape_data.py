import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}  # Hindari blokir situs
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        texts = [para.get_text() for para in paragraphs if para.get_text()]
        return texts
    except Exception as e:
        return [f"Error saat scraping: {e}"]

def save_to_csv(data, filename="dataset.csv"):
    df = pd.DataFrame({"text": data})
    df.to_csv(filename, index=False)
    print(f"Data disimpan ke {filename}")

# Contoh URL (Wikipedia, gratis dan publik)
url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
data = scrape_website(url)
save_to_csv(data)