from peewee import MySQLDatabase
from dotenv import load_dotenv
import os

# Charger le fichier .env
load_dotenv()

# Récupérer les info de connexion à la bd
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connexion à MySQL avec Peewee
db = MySQLDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=int(DB_PORT))

def connect_db():
    db.connect()

def close_db():
    db.close()
