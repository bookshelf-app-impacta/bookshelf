import requests
import json

BASE_URL = "http://localhost:5000/books"

# 1. POST
resp = requests.post(BASE_URL, json={
    "title": "Livro Teste",
    "author": "Autor",
    "isbn": "1234567890123"
})
print("POST:", resp.status_code, resp.json())

# 2. GET all
resp = requests.get(BASE_URL)
print("GET all:", resp.status_code, resp.json())

# 3. PUT (supondo que o ID seja 1)
resp = requests.put(f"{BASE_URL}/1", json={"title": "Novo Título"})
print("PUT:", resp.status_code, resp.json())

# 4. DELETE
resp = requests.delete(f"{BASE_URL}/1")
print("DELETE:", resp.status_code)