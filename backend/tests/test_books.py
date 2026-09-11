"""
Testes da rota GET /api/books.
"""

from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.book import Author, Book, Genre
from app.models.user import User


def _make_user(**overrides):
    data = {
        "username": "tester",
        "email": "tester@bookshelf.local",
        "password_hash": generate_password_hash("senha12345"),
        "role": "user",
    }
    data.update(overrides)

    user = User(**data)
    db.session.add(user)
    db.session.flush()
    return user


def _make_book(**overrides):
    author = Author(name="Autor Teste", slug="autor-teste")
    genre = Genre(name="Ficcao", slug="ficcao")
    db.session.add_all([author, genre])
    db.session.flush()

    user = overrides.pop("user", None) or _make_user()

    data = {
        "title": "Livro Teste",
        "slug": "livro-teste",
        "author_id": author.id,
        "genre_id": genre.id,
        "created_by": user.id,
    }
    data.update(overrides)

    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return book


def test_list_books_empty(client):
    response = client.get("/api/books/")

    assert response.status_code == 200
    assert response.get_json() == []


def test_list_books_returns_created_book(client):
    _make_book()

    response = client.get("/api/books/")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Livro Teste"
    assert data[0]["author"]["name"] == "Autor Teste"
    assert data[0]["genre"]["name"] == "Ficcao"
    assert "created_by" not in data[0]


def test_get_book_by_id(client):
    book = _make_book()

    response = client.get(f"/api/books/{book.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == book.id


def test_get_book_not_found(client):
    response = client.get("/api/books/9999")

    assert response.status_code == 404
    assert "error" in response.get_json()