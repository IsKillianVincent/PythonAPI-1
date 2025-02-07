import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.configs.api_config import API_KEY

client = TestClient(app)

VALID_HEADERS = {"Authorization": f"Bearer {API_KEY}"}
INVALID_HEADERS = {"Authorization": "Bearer INVALID_KEY"}
NO_AUTH_HEADERS = {}

@pytest.mark.parametrize("headers, expected_status, expected_message", [
    (VALID_HEADERS, 200, None),
    (INVALID_HEADERS, 403, "Erreur survenue : Token invalide. Vérifiez que votre clé API est correcte."),  # Clé invalide
    (NO_AUTH_HEADERS, 401, "Aucun token fourni. Ajoutez un en-tête Authorization sous la forme 'Bearer <API_KEY>'."),  # Pas de clé
])
def test_api_key_auth(headers, expected_status, expected_message):
    response = client.get("/convert?amount=100&from_currency=EUR&to_currency=USD", headers=headers)
    assert response.status_code == expected_status
    if expected_message:
        assert response.json()["message"] == expected_message


@pytest.mark.parametrize("amount, from_currency, to_currency, date, expected_status", [
    (100, "EUR", "USD", "latest", 200),
    (50, "usd", "eur", "latest", 200),
    ("abc", "EUR", "USD", "latest", 422),
    (100, "XYZ", "USD", "latest", 422),
    (100, "EUR", "XYZ", "latest", 422),
    (100, "EUR", "USD", "2022-01-01", 200),
])
def test_currency_conversion(amount, from_currency, to_currency, date, expected_status):
    response = client.get(
        "/convert",
        params={"amount": amount, "from_currency": from_currency, "to_currency": to_currency, "date": date},
        headers=VALID_HEADERS
    )
    assert response.status_code == expected_status


def test_rate_limit():
    headers = VALID_HEADERS

    for _ in range(2):
        response = client.get("/convert?amount=100&from_currency=EUR&to_currency=USD", headers=headers)
        assert response.status_code == 200

    response = client.get("/convert?amount=100&from_currency=EUR&to_currency=USD", headers=headers)
    assert response.status_code == 429
    assert "Limite de requêtes atteinte" in response.json()["detail"]
