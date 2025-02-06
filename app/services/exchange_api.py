import requests
import os

API_URL = os.getenv("API_URL", "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1")

def fetch_conversion_rates(currency_code: str):
    """Récupère les taux de conversion pour une devise donnée."""
    url = f"{API_URL}/currencies/{currency_code}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur API pour {currency_code}: {e}")
        return None

def fetch_all_currencies():
    """Récupère la liste de toutes les devises."""
    url = f"{API_URL}/currencies.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur API lors de la récupération des devises: {e}")
        return None
