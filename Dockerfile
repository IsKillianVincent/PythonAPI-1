# Étape 1 : Utiliser l'image de base Python
FROM python:3.9-slim AS base

# Étape 2 : Définir les variables d'environnement pour éviter les interactivités pendant l'installation
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off

# Étape 3 : Créer un répertoire pour l'application
WORKDIR /app

# Étape 4 : Copier le fichier de dépendances
COPY requirements.txt /app/

# Étape 5 : Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Étape 6 : Copier le reste de l'application
COPY . /app/

# Étape 7 : Exposer le port de l'application FastAPI (8000)
EXPOSE 8000

# Étape 8 : Définir la commande pour lancer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
