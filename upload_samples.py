import json
import requests

API_URL = "http://127.0.0.1:8000/documents"

with open("sample_documents.json", "r") as f:
    documents = json.load(f)

for doc in documents:
    response = requests.post(API_URL, json=doc)
    print(f"Uploaded {doc['id']} ->", response.json())
