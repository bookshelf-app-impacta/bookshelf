"""
Testes da rota GET /api/books.
"""

import uuid

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.book import Author, Book, Genre
from app.models.user import User


@pytest.fixture(scope="session")
def app():
    flask_app = create_app()
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def app_context(app):
    """
    Abre o contexto de aplicacao para todo teste deste arquivo.

    client.get(...) ja entra em contexto sozinho por baixo dos panos,
    mas _make_book/_make_user chamam db.session diretamente, fora de uma
    requisicao real — sem isso da "Working outside of application
    context".
    """
    with app.app_context():
        yield


@pytest.fixture(autouse=True)
def _cleanup_books(app):
    """
    Roda depois de CADA teste e apaga o que os testes deste arquivo
    criaram (livros, autores, generos, usuario de teste).

    Sem isso, o banco fica sujo entre os testes: test_list_books_empty
    so passa se rodar num banco vazio, mas test_list_books_returns_created_book
    cria um livro. Como o pytest nao garante a ordem, cada teste precisa
    comecar do zero.
    """
    yield
    with app.app_context():
        db.session.query(Book).delete()
        db.session.query(Author).delete()
        db.session.query(Genre).delete()
        db.session.query(User).filter_by(email="tester@bookshelf.local").delete()
        db.session.commit()


def _make_user(**overrides):
    # E-mail fixo de proposito: o cleanup acima sabe exatamente qual
    # linha apagar depois. Pra criar mais de um usuario no mesmo teste,
    # passe email=... diferente pelos overrides.
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
    # Sufixo aleatorio no slug: Author/Genre/Book devem ter slug UNIQUE
    # no banco. Sem isso, duas execucoes seguidas do mesmo teste dariam
    # erro de duplicidade em vez do erro que o teste realmente quer
    # verificar.
    suffix = uuid.uuid4().hex[:6]
    author = Author(name="Autor Teste", slug=f"autor-teste-{suffix}")
    genre = Genre(name="Ficcao", slug=f"ficcao-{suffix}")
    db.session.add_all([author, genre])
    db.session.flush()

    user = overrides.pop("user", None) or _make_user()

    data = {
        "title": "Livro Teste",
        "slug": f"livro-teste-{suffix}",
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