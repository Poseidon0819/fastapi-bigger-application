from fastapi.testclient import TestClient

from ..database_test import configure_test_database

from ...main import app

configure_test_database(app)

client = TestClient(app)

stocks_route = "/api/v1/stocks"

request_json = {
    "car_id": 1,
    "quantity": 10
}

response_json = {
    "id": 1,
    "car": {
        "id": 1,
        "name": "Ram 3",
        "year": 2020,
        "brand": "Dodge"
    },
    "quantity": 10
}

response_error = {"detail": "Stock not found"}

headers = {"X-token":"fake-super-secret-token"}


def generate_test_mass():
    ## Create a car
    response = client.post("/api/v1/cars/", json={
        "name": "Ram 3",
        "year": 2020,
        "brand": "Dodge"
    })

def test_create_stock():
    ''' Create a stock with success '''
    generate_test_mass()
    
    response = client.post(stocks_route + "/", json=request_json)
    assert response.status_code == 201
    assert response.json() == response_json


def test_read_stock():
    ''' Read a stock with success '''
    request_url = stocks_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == response_json

def test_read_stocks():
    ''' Read all stocks paginated with success '''
    request_url = stocks_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [response_json]


def test_delete_stock():
    ''' Delete a stock with success '''
    request_url = stocks_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_stock_not_found():
    ''' Read a stock when not found '''
    request_url = stocks_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == response_error


def test_read_stocks_not_found():
    ''' Read all stocks paginated when not found '''
    request_url = stocks_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_stock_not_found():
    ''' Delete a stock when not exists '''
    request_url = stocks_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == response_error