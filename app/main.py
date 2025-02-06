from app.database import connect_db, close_db 

# Test de la connexion à la bd
if __name__ == "__main__":
    connect_db()
    close_db()