import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from fastapi import Request, HTTPException
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_valid_convert_endpoint():
    headers = {"Authorization": "Bearer 123"}
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
    assert data["converted_amount"] > 0  # On suppose que le montant converti sera positif

def test_invalid_convert_token():
    headers = {"Authorization": "Bearer 69420"}  # Envoi d'un token invalide
    try:
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
        assert response.json() == {"detail": "Unauthorized access"}
    
    except HTTPException as exc:
        print(f"Test échoué avec le code : {exc.status_code}, {exc.detail}")

def test_convert_invalid_base_currency():
    headers = {"Authorization": "Bearer 123"}
    response = client.get(
        "/convert",
        params={
            "amount": 100,
            "from_currency": "TEST",
            "to_currency": "USD",
            "date": "latest"
        },
        headers=headers
    )

    assert response.status_code == 404

def test_convert_invalid_base_currency():
    headers = {"Authorization": "Bearer 123"}
    response = client.get(
        "/convert",
        params={
            "amount": 100,
            "from_currency": "EUR",
            "to_currency": "TEST",
            "date": "latest"
        },
        headers=headers
    )
    
    assert response.status_code == 400




def test_valid_converts_endpoint():
    headers = {"Authorization": "Bearer 123"}  # Token valide
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

def test_invalid_converts_token():
    headers = {"Authorization": "Bearer INVALID"}  # Token valide
    try:

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

        assert response.status_code == 403
        assert response.json() == {"detail": "Unauthorized access"}

    except HTTPException as exc:
        print(f"Test échoué avec le code : {exc.status_code}, {exc.detail}")

def test_converts_invalid_base_currency():
    headers = {"Authorization": "Bearer 123"}
    response = client.get(
        "/converts",
        params={
            "amounts": [100, 50],
            "from_currency": "INVALID",  # Devise non valide
            "to_currency": "USD",
            "date": "latest"
        },
        headers=headers
    )
    
    assert response.status_code == 404

    try:
        data = response.json()
    except ValueError:
        data = None
    
    assert isinstance(data, dict), f"Réponse attendue sous forme de dictionnaire, mais reçue : {type(data)}"
    
    assert "detail" in data
    assert "La devise de référence n'existe pas" in data["detail"]

def test_converts_invalid_target_currency():
    headers = {"Authorization": "Bearer 123"}
    response = client.get(
        "/converts",
        params={
            "amounts": [100, 50],
            "from_currency": "EUR",  # Devise non valide
            "to_currency": "INVALID",
            "date": "latest"
        },
        headers=headers
    )
    
    assert response.status_code == 400

    try:
        data = response.json()
    except ValueError:
        data = None
    
    assert isinstance(data, dict), f"Réponse attendue sous forme de dictionnaire, mais reçue : {type(data)}"
    
    assert "detail" in data
    assert "La devise de référence n'existe pas" in data["detail"]