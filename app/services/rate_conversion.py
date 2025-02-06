from models.currencies import Currency
from models.rate_conversion import RateConversion
from services.exchange_api import fetch_conversion_rates

def insert_conversion_rates(source_currency_code: str, rates: dict):
    """Insère les taux de conversion dans la base de données."""
    source_currency = Currency.get_or_none(Currency.code == source_currency_code)
    if not source_currency:
        print(f"La devise {source_currency_code} n'existe pas en base.")
        return

    for target_currency_code, rate in rates.items():
        if source_currency_code != target_currency_code:
            target_currency = Currency.get_or_none(Currency.code == target_currency_code)
            if not target_currency:
                print(f"La devise {target_currency_code} n'existe pas en base, sautée.")
                continue

            # Vérifier si le taux existe déjà
            rate_exists = RateConversion.get_or_none(
                (RateConversion.source_currency == source_currency) &
                (RateConversion.target_currency == target_currency)
            )
            if not rate_exists:
                RateConversion.create(
                    source_currency=source_currency,
                    target_currency=target_currency,
                    rate=rate
                )
                print(f"Taux inséré : {source_currency_code} -> {target_currency_code} = {rate}")
            else:
                print(f"Taux déjà existant : {source_currency_code} -> {target_currency_code}")

def update_all_conversion_rates():
    """Met à jour les taux de conversion pour toutes les devises."""
    currencies = Currency.select()
    for currency in currencies:
        print(f"Récupération des taux pour {currency.code}")
        conversion_data = fetch_conversion_rates(currency.code)
        if conversion_data:
            insert_conversion_rates(currency.code, conversion_data.get(currency.code, {}))
