import requests
from peewee import IntegrityError
from database import connect_db, close_db
from models.currencies import Currency
from models.rate_conversion import RateConversion

CURRENCY_LIST_API_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
def fetchAndInsertCurrencies():
    """Récupère les données de l'API et insère les devises dans la base de données."""
    try:
        response = requests.get(CURRENCY_LIST_API_URL)
        response.raise_for_status()

        data = response.json()

        for code, name in data.items():
            try:
                Currency.create(code=code, name=name)
                print(f"✅ Insertion effectuée : {code} - {name}")
            except IntegrityError:
                print(f"⚠️ La devise {code} existe déja.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Une erreur est survenue lors de la récupération des devises : {e}")


if __name__ == "__main__":
    connect_db()
    print("Database ouvert")

    Currency.create_table()
    RateConversion.create_table()
    print("Tables crées")

    fetchAndInsertCurrencies()
    
    close_db()
    print("Database fermer")