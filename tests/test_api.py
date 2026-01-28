import requests

BASE_URL = "http://127.0.0.1:8000"


# ------------------ Create Document ------------------

def test_create_document_endpoint():
    doc = {
        "id": 900,
        "title": "API Test Document",
        "content": "This document is created via API test.",
        "category": "api_test"
    }

    response = requests.post(f"{BASE_URL}/documents", json=doc)

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"


# ------------------ Simple Search ------------------

def test_search_endpoint():
    payload = {
        "query": "python framework",
        "limit": 5
    }

    response = requests.post(f"{BASE_URL}/search", json=payload)

    assert response.status_code == 200

    results = response.json()["results"]

    assert isinstance(results, list)
    assert len(results) > 0


# ------------------ Get Document Not Found ------------------

def test_get_document_not_found():
    response = requests.get(f"{BASE_URL}/documents/9999999")

    assert response.status_code == 404


# ------------------ Filtered Search ------------------

def test_search_with_filters():
    payload = {
        "query": "anime adventure",
        "limit": 5,
        "category": "anime"
    }

    response = requests.post(f"{BASE_URL}/search/filter", json=payload)

    assert response.status_code == 200

    results = response.json()["results"]

    assert len(results) > 0

    for r in results:
        assert r["payload"]["category"] == "anime"


# ------------------ Pagination ------------------

def test_pagination():
    response = requests.get(
        f"{BASE_URL}/list_all?limit=3&offset=0"
    )

    assert response.status_code == 200

    data = response.json()

    assert "documents" in data
    assert isinstance(data["documents"], list)


