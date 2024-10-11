import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_get_all_logs():
    response = httpx.get(f"{BASE_URL}/logs?page=1&page_size=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Make sure that list returns

def test_get_logs_for_user():
    user_id = "user_id" 
    response = httpx.get(f"{BASE_URL}/logs/{user_id}?page=1&page_size=5")
    assert response.status_code == 422 # Empty list if user not exists

def test_pagination():
    response = httpx.get(f"{BASE_URL}/logs?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5  # Make sure there are no more than 5 entries

def test_time_filtering():
    response = httpx.get(f"{BASE_URL}/logs?page=1&page_size=5&start_time=2024-10-10T00:00:00&end_time=2024-10-11T23:59:59")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_invalid_user_id():
    response = httpx.get(f"{BASE_URL}/logs/999999?page=1&page_size=5")
    assert response.status_code == 404  # Incorrect user
