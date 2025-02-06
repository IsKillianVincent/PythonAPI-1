from database import connect_db, close_db
from models.currencies import Currency
from models.rate_conversion import RateConversion
from services.currency_service import insert_currencies
from services.rate_conversion import update_all_conversion_rates

if __name__ == "__main__":
    connect_db()
    print("Database ouvert")

    # Création des tables
    Currency.create_table(safe=True)
    RateConversion.create_table(safe=True)

    # Insérer les devises et les taux de conversion
    insert_currencies()
    update_all_conversion_rates()

    close_db()
    print("Database fermer")