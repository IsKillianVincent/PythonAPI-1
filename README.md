# API de Conversion de Devises (Exchange-rate)

Ce projet implémente une API de conversion de devises, en utilisant des taux de change extraits de l'API exchange-api. L'API permet de convertir un montant d'une devise à une autre, y compris EUR et toutes les autres monnaies du monde.

## Fonctionnalités
 -Conversion de devises : Convertir un montant entre différentes devises.
 - Gestion des taux de change : Les taux de change sont mis à jour à partir de l'API externe.
 - Filtrage des données : Utilisation de paramètres de requête pour filtrer les résultats des conversions.
 - Gestion des clés API : Protection des endpoints avec une clé API via un middleware.
 - Gestion des erreurs : Gestion avancée des erreurs pour les connexions Redis, les erreurs API, et les erreurs de validation des données.
 - Variables d'environnement : Configuration flexible via un fichier .env.

## Installation
### Prérequis
- Python 3.8+
- Redis (pour la gestion du cache)
- Fichier .env pour configurer les variables d'environnement (clés API, hôte Redis, etc.)

### Étapes d'installation
1. Clonez ce repository :

```
git clone https://github.com/IsKillianVincent/PythonAPI-1.git
```
2. Accédez au dossier du projet :
```
cd PythonAPI-1
```
3. Créez un environnement virtuel :
```
python3 -m venv venv
```
4. Activez l'environnement virtuel :
```
source venv/bin/activate
```
5. Installez les dépendances :
```
pip install -r requirements.txt
```
6. Créez un fichier .env à la racine du projet et ajoutez-y les variables suivantes :
```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_CACHE_EXPIRATION_TIME=60  # en secondes
API_KEY=ton_api_key
API_BASE_URL=https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@
API_FALLBACK_URL=https://currency-api.pages.dev/
API_VERSION=v1
```
7. Lancez l'application :
```
uvicorn app.main:app --reload
```

### Variables d'environnement
Voici les variables que vous pouvez configurer dans votre fichier .env :
- REDIS_HOST : Hôte du serveur Redis.
- REDIS_PORT : Port du serveur Redis.
- REDIS_CACHE_EXPIRATION_TIME : Durée de vie du cache en secondes.
- API_KEY : Clé API utilisée pour protéger les endpoints.
- API_BASE_URL : URL de base de l'API pour récupérer les taux de change.
- API_FALLBACK_URL : URL de secours si l'API principale échoue.
- API_VERSION : Version de l'API à utiliser.

### Endpoints
#### 1. GET /convert
Cet endpoint permet de convertir un montant d'une devise vers une autre.

Paramètres de requête :
- amount (obligatoire) : Montant à convertir.
- from_currency (facultatif) : Devise source (par défaut "EUR").
- to_currency (facultatif) : Devise cible (par défaut "USD").
- date (facultatif) : Date du taux de conversion à utiliser, au format YYYY-MM-DD. Par défaut, utilise le taux "latest".

Exemple de requête :
```
GET /convert?amount=100&from_currency=EUR&to_currency=USD
```

Exemple de réponse :
```
{
    "amount": 100,
    "from": "EUR",
    "to": "USD",
    "date": "latest",
    "exchange_rate": 1.12,
    "converted_amount": 112.0
}
```

#### 2. GET /converts
Cet endpoint permet de convertir une liste de montants d'une devise vers une autre.

Paramètres de requête :
- amounts (obligatoire) : Liste des montants à convertir.
- from_currency (facultatif) : Devise source (par défaut "EUR").
- to_currency (facultatif) : Devise cible (par défaut "USD").
- date (facultatif) : Date du taux de conversion à utiliser, au format YYYY-MM-DD. Par défaut, utilise le taux "latest".

Exemple de requête :
```
GET /converts?amounts=100,200&from_currency=EUR&to_currency=USD
```
Exemple de réponse :
```
{
    "from": "EUR",
    "to": "USD",
    "date": "latest",
    "exchange_rate": 1.12,
    "conversions": [
        {
            "amount": 100,
            "converted_amount": 112.0
        },
        {
            "amount": 200,
            "converted_amount": 224.0
        }
    ]
}
```
#### 3. GET /config
Cet endpoint permet d'obtenir des informations sur la configuration de l'application, y compris les paramètres de l'API externe et la connexion Redis.

Exemple de requête :
```
GET /config
```
Exemple de réponse :
```
{
    "external_api_info": {
        "API_VERSION": "v1",
        "API_BASE_URL": "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@"
    },
    "internal_api_info": {
        "APP_VERSION": "1.0",
        "ENVIRONMENT": "development",
        "PROJECT_PATH": "",
        "DEBUG_MODE": "True",
        "API_KEY_PRESENT": true,
        "DATABASE_CONNECTION": "Inactive",
        "UPTIME": 42.5
    },
    "redis_info": {
        "REDIS_CONNECTION": "Active",
        "REDIS_HOST": "",
        "REDIS_PORT": 
    }
}
```
#### 4. Gestion du cache
Tu peux également gérer le cache avec les endpoints suivants :
- **GET** _/cache/stats_ : Obtenir des statistiques sur le cache Redis.
- **GET** _/cache/keys_ : Lister toutes les clés stockées dans Redis.
- **DELETE** _/cache/{key}_ : Supprimer une clé spécifique du cache Redis.

### Middleware
L'API utilise un middleware pour vérifier la clé API. Pour accéder aux endpoints, vous devez inclure la clé API dans l'en-tête **Authorization** de vos requêtes HTTP.

Exemple d'en-tête :
```
Authorization: Bearer 'API_KEY'
```

## Gestion des données avec Redis
**Pourquoi Redis ?**

Redis est utilisé dans ce projet comme cache pour stocker temporairement les taux de change. Cela permet de :
- Accélérer les performances : En stockant les taux de change en cache, on évite de refaire des appels API à chaque requête, rendant l'API beaucoup plus rapide.
- Réduire les coûts d'API : Moins d'appels à l'API externe, ce qui limite les coûts et dépendances externes.
- Améliorer la scalabilité : Redis est extrêmement rapide et peut gérer un grand nombre de requêtes simultanées.

**Pourquoi pas de base de données pour l'instant ?**

Nous n'utilisons pas de base de données pour ce projet car :
- Pas de besoin de persistance : Les taux de change sont temporaires et changent fréquemment.  Redis suffit pour stocker ces données en cache. Et l'API exchange utilisé nous permet d'être dynamique en date pour les récuperations de donnés.
- Performance : Redis permet d'accéder rapidement aux données en mémoire, contrairement à une base de données qui serait plus lente.

**Pourquoi une base de données pourrait être nécessaire plus tard ?**
À l'avenir, une base de données pourrait être utile pour :
- Stocker l'historique des taux de change : Si nous voulons permettre aux utilisateurs de consulter des taux passés.
- Gérer des utilisateurs : Si on décide d'ajouter des fonctionnalités liées aux utilisateurs (comptes, historiques, etc.).