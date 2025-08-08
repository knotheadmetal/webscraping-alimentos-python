import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.15"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def scrape_carrefour(product_name):
    url = f"https://mercado.carrefour.com.br/busca/{product_name}"
    headers = {"User-Agent": get_random_user_agent()}
    products_data = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, "html.parser")

        product_cards = soup.find_all("div", class_="product-card")

        for card in product_cards:
            name_tag = card.find("h3", class_="product-card__name")
            price_tag = card.find("span", class_="product-card__price--current")

            name = name_tag.get_text(strip=True) if name_tag else "N/A"
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            products_data.append({"Supermercado": "Carrefour", "Produto": name, "Preço": price})
        
        time.sleep(random.uniform(2, 5)) # Delay para evitar bloqueio

    except requests.exceptions.RequestException as e:
        print(f"Erro ao raspar Carrefour ({product_name}): {e}")

    return products_data

if __name__ == "__main__":
    alimentos_basicos = ["arroz", "feijao", "leite", "carne", "pao", "oleo", "ovos"]
    all_products = []

    for item in alimentos_basicos:
        print(f"Raspando {item} do Carrefour...")
        all_products.extend(scrape_carrefour(item))

    df_all_products = pd.DataFrame(all_products)
    print("\nDados Coletados:")
    print(df_all_products.head())

    # Salvar em CSV
    df_all_products.to_csv("data/precos_mercados.csv", index=False)
    print("\nDados salvos em data/precos_mercados.csv")


