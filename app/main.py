from database import connect_db, close_db
from models.currencies import Currency
from models.rate_conversion import RateConversion

# Test de la connexion à la bd et creation de table
if __name__ == "__main__":
    connect_db()
    print("Database ouvert")

    Currency.create_table()
    RateConversion.create_table()
    print("Tables crées")

    close_db()
    print("Database fermer")