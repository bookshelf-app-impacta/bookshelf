import json

def test_get_books_empty(client):
    response = client.get('/books/')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_book_success(client):
    payload = {
        'title': 'Novo Livro',
        'author': 'João Silva',
        'isbn': '978-3-16-148410-0',
        'publication_year': 2023,
        'publisher': 'Editora X',
        'description': 'Um ótimo livro'
    }
    response = client.post('/books/', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Novo Livro'
    assert data['isbn'] == '978-3-16-148410-0'

def test_create_book_duplicate_isbn(client, sample_book):
    payload = {
        'title': 'Outro Livro',
        'author': 'Maria',
        'isbn': '1234567890123',  # mesmo ISBN do sample_book
        'publication_year': 2021
    }
    response = client.post('/books/', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 409
    assert response.get_json()['error'] == 'ISBN already exists'

def test_create_book_invalid_data(client):
    payload = {'title': 'Título'}  # falta author e isbn
    response = client.post('/books/', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
    errors = response.get_json()['errors']
    assert 'author' in errors
    assert 'isbn' in errors

def test_get_book_by_id(client, sample_book):
    response = client.get(f'/books/{sample_book}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == sample_book
    assert data['title'] == 'Livro Teste'

def test_get_book_not_found(client):
    response = client.get('/books/9999')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Book not found'

def test_update_book_success(client, sample_book):
    payload = {'title': 'Título Atualizado', 'author': 'Novo Autor'}
    response = client.put(f'/books/{sample_book}', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Título Atualizado'
    assert data['author'] == 'Novo Autor'
    assert data['isbn'] == '1234567890123'  # não alterado

def test_update_book_not_found(client):
    response = client.put('/books/9999', data=json.dumps({'title': 'X'}), content_type='application/json')
    assert response.status_code == 404

def test_update_book_invalid_data(client, sample_book):
    payload = {'publication_year': 3000}
    response = client.put(f'/books/{sample_book}', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
    errors = response.get_json()['errors']
    assert 'publication_year' in errors

def test_update_book_duplicate_isbn(client, sample_book):
    # Primeiro cria outro livro
    payload = {'title': 'Outro', 'author': 'Fulano', 'isbn': '9999999999999'}
    client.post('/books/', data=json.dumps(payload), content_type='application/json')
    # Tenta atualizar o sample_book para o ISBN do outro
    update_payload = {'isbn': '9999999999999'}
    response = client.put(f'/books/{sample_book}', data=json.dumps(update_payload), content_type='application/json')
    assert response.status_code == 409
    assert response.get_json()['error'] == 'ISBN already exists'

def test_delete_book_success(client, sample_book):
    response = client.delete(f'/books/{sample_book}')
    assert response.status_code == 204
    # Verifica que foi removido
    get_response = client.get(f'/books/{sample_book}')
    assert get_response.status_code == 404

def test_delete_book_not_found(client):
    response = client.delete('/books/9999')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Book not found'

def test_get_books_after_create(client):
    # Limpa dados (já que cada teste recria o banco)
    response = client.get('/books/')
    assert response.status_code == 200
    # Cria um livro
    client.post('/books/', data=json.dumps({
        'title': 'A',
        'author': 'B',
        'isbn': '1111111111111'
    }), content_type='application/json')
    response = client.get('/books/')
    assert len(response.get_json()) == 1