from peewee import IntegrityError
from models.currencies import Currency
from services.exchange_api import fetch_all_currencies

def insert_currencies():
    """Récupère les devises et les insère dans la base de données."""
    currencies = fetch_all_currencies()
    if not currencies:
        return

    for code, name in currencies.items():
        try:
            Currency.create(code=code, name=name)
            print(f"Devise insérée : {code} - {name}")
        except IntegrityError:
            print(f"La devise {code} existe déjà.")
