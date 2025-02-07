import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.configs.test_config import TEST_VALID_API_KEY, TEST_NOT_VALID_API_KEY

client = TestClient(app)

# Utilitaire pour gérer les headers
def get_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

# Test pour un token valide
def test_valid_convert_endpoint():
    headers = get_headers(TEST_VALID_API_KEY)
    response = client.get(
        "/convert",
        params={
            "amount": 100,
            "from_currency": "EUR",
            "to_currency": "USD",
            "date": "latest"
        },
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 100
    assert data["from"] == "EUR"
    assert data["to"] == "USD"
    assert data["converted_amount"] > 0

# Test pour un token invalide
def test_invalid_convert_token():
    headers = get_headers(TEST_NOT_VALID_API_KEY)
    response = client.get(
        "/convert",
        params={
            "amount": 100,
            "from_currency": "EUR",
            "to_currency": "USD",
            "date": "latest"
        },
        headers=headers
    )

    assert response.status_code == 403
    assert response.json() == {
        "error": "Erreur",
        "message": "Erreur survenue : Token invalide. Vérifiez que votre clé API est correcte.",
    }

# Test pour une devise de base invalide
def test_convert_invalid_base_currency():
    headers = get_headers(TEST_VALID_API_KEY)
    response = client.get(
        "/convert",
        params={
            "amount": 100,
            "from_currency": "INVALID",
            "to_currency": "USD",
            "date": "latest"
        },
        headers=headers
    )

    assert response.status_code == 404  # 422 = erreur de validation
    assert "error" in response.json()

# ✅ Test pour une devise cible invalide
def test_convert_invalid_target_currency():
    headers = get_headers(TEST_VALID_API_KEY)
    response = client.get(
        "/convert",
        params={
            "amount": 100,
            "from_currency": "EUR",
            "to_currency": "INVALID",
            "date": "latest"
        },
        headers=headers
    )

    assert response.status_code == 402
    assert "error" in response.json()

# ✅ Test pour plusieurs conversions (endpoint /converts)
def test_valid_converts_endpoint():
    headers = get_headers(TEST_VALID_API_KEY)
    response = client.get(
        "/converts",
        params={
            "amounts": [100, 200, 300],
            "from_currency": "EUR",
            "to_currency": "USD",
            "date": "latest"
        },
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    assert data["from"] == "EUR"
    assert data["to"] == "USD"
    assert "exchange_rate" in data
    assert len(data["conversions"]) == 3
    assert data["conversions"][0]["amount"] == 100
    assert "converted_amount" in data["conversions"][0]

# ✅ Test pour un token invalide avec /converts
def test_invalid_converts_token():
    headers = get_headers(TEST_NOT_VALID_API_KEY)
    response = client.get(
        "/converts",
        params={
            "amounts": [100, 200, 300],
            "from_currency": "EUR",
            "to_currency": "USD",
            "date": "latest"
        },
        headers=headers
    )

    assert response.status_code == 422
    assert response.json() == {
        "error": "Erreur",
        "message": "Erreur survenue : Token invalide. Vérifiez que votre clé API est correcte.",
        "path": "/converts"
    }

# ✅ Test pour une devise de base invalide avec /converts
def test_converts_invalid_base_currency():
    headers = get_headers(TEST_VALID_API_KEY)
    response = client.get(
        "/converts",
        params={
            "amounts": [100, 50],
            "from_currency": "INVALID",
            "to_currency": "USD",
            "date": "latest"
        },
        headers=headers
    )

    assert response.status_code == 422
    try:
        data = response.json()
    except ValueError:
        data = None

    assert isinstance(data, dict), f"Réponse attendue sous forme de dictionnaire, mais reçue : {type(data)}"

# ✅ Test pour une devise cible invalide avec /converts
def test_converts_invalid_target_currency():
    headers = get_headers(TEST_VALID_API_KEY)
    response = client.get(
        "/converts",
        params={
            "amounts": [100, 50],
            "from_currency": "EUR",
            "to_currency": "INVALID",
            "date": "latest"
        },
        headers=headers
    )

    assert response.status_code == 422
    try:
        data = response.json()
    except ValueError:
        data = None

    assert isinstance(data, dict), f"Réponse attendue sous forme de dictionnaire, mais reçue : {type(data)}"
