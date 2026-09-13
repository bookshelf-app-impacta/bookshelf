"""
Testes das rotas de /api/books — listar, buscar, criar, editar, apagar.
"""

import uuid

import pytest
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.book import Author, Book, Genre
from app.models.user import User

# Credenciais criadas por `flask seed`. Ver app/cli.py.
ADMIN = {"email": "admin@bookshelf.local", "password": "admin123"}
REGULAR = {"email": "ana@bookshelf.local", "password": "user123"}


@pytest.fixture(scope="session")
def app():
    flask_app = create_app()
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


def _login(client, credentials) -> str:
    response = client.post("/api/auth/login", json=credentials)
    assert response.status_code == 200, response.get_json()
    return response.get_json()["token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


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
    Roda depois de CADA teste e apaga so o que aquele teste criou
    (livros, autores, generos, usuario de teste) — nunca a tabela
    inteira. Guarda o maior id de cada tabela antes do teste rodar e,
    depois, apaga so quem ficou acima disso.

    Um delete sem filtro aqui apagaria o catalogo seedado (`flask
    seed`) toda vez que a suite rodasse, e cascatearia pra
    reviews/favorites via `ondelete="CASCADE"` em book_id.
    """
    with app.app_context():
        last_book_id = db.session.query(func.max(Book.id)).scalar() or 0
        last_author_id = db.session.query(func.max(Author.id)).scalar() or 0
        last_genre_id = db.session.query(func.max(Genre.id)).scalar() or 0

    yield

    with app.app_context():
        db.session.query(Book).filter(Book.id > last_book_id).delete()
        db.session.query(Author).filter(Author.id > last_author_id).delete()
        db.session.query(Genre).filter(Genre.id > last_genre_id).delete()
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


def test_list_books_returns_a_list(client):
    # Nao assume tabela vazia: o "como testar" deste modulo manda rodar
    # `flask seed` antes (que ja cria 3 livros), entao um teste que
    # exigisse `== []` seria flakey dependendo de quando rodar.
    response = client.get("/api/books/")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_list_books_returns_created_book(client):
    _make_book()

    response = client.get("/api/books/")
    data = response.get_json()
    titles = [book["title"] for book in data]

    assert response.status_code == 200
    assert "Livro Teste" in titles
    created = next(book for book in data if book["title"] == "Livro Teste")
    assert created["author"]["name"] == "Autor Teste"
    assert created["genre"]["name"] == "Ficcao"
    assert "created_by" not in created


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


# --- criar livro (POST) ------------------------------------------------


def test_create_book_without_token_returns_401(client):
    response = client.post("/api/books/", json={"title": "Sem Token"})

    assert response.status_code == 401


def test_create_book_requires_admin(client):
    token = _login(client, REGULAR)
    response = client.post(
        "/api/books/", json={"title": "Livro Comum"}, headers=_auth(token),
    )

    # 403 e nao 401: sabemos quem e, so nao pode.
    assert response.status_code == 403


def test_create_book_as_admin(client):
    token = _login(client, ADMIN)
    response = client.post(
        "/api/books/",
        json={"title": "Livro Novo", "release_year": 2020},
        headers=_auth(token),
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["title"] == "Livro Novo"
    assert data["release_year"] == 2020
    assert data["slug"]  # gerado pelo service a partir do titulo


def test_create_book_validates_required_title(client):
    token = _login(client, ADMIN)
    response = client.post("/api/books/", json={}, headers=_auth(token))

    assert response.status_code == 400
    assert "title" in response.get_json()["fields"]


def test_create_book_rejects_invalid_year(client):
    token = _login(client, ADMIN)
    response = client.post(
        "/api/books/",
        json={"title": "Ano Invalido", "release_year": 3000},
        headers=_auth(token),
    )

    assert response.status_code == 400
    assert "release_year" in response.get_json()["fields"]


def test_create_book_rejects_duplicate_isbn(client):
    token = _login(client, ADMIN)
    headers = _auth(token)
    isbn = "9780000000001"

    first = client.post(
        "/api/books/", json={"title": "Primeiro", "isbn13": isbn}, headers=headers,
    )
    assert first.status_code == 201

    second = client.post(
        "/api/books/", json={"title": "Segundo", "isbn13": isbn}, headers=headers,
    )
    assert second.status_code == 409


# --- editar livro (PUT) ------------------------------------------------


def test_update_book_as_admin(client):
    book = _make_book()
    token = _login(client, ADMIN)

    response = client.put(
        f"/api/books/{book.id}",
        json={"title": "Titulo Editado"},
        headers=_auth(token),
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["title"] == "Titulo Editado"
    # Campo nao enviado no PUT continua intacto — e a edicao e parcial.
    assert data["author"]["name"] == "Autor Teste"
    assert data["slug"] == book.slug


def test_update_book_requires_admin(client):
    book = _make_book()
    token = _login(client, REGULAR)

    response = client.put(
        f"/api/books/{book.id}", json={"title": "Tentativa"}, headers=_auth(token),
    )

    assert response.status_code == 403


def test_update_book_not_found(client):
    token = _login(client, ADMIN)
    response = client.put(
        "/api/books/9999", json={"title": "X"}, headers=_auth(token),
    )

    assert response.status_code == 404


# --- apagar livro (DELETE) ---------------------------------------------


def test_delete_book_as_admin(client):
    book = _make_book()
    token = _login(client, ADMIN)

    response = client.delete(f"/api/books/{book.id}", headers=_auth(token))
    assert response.status_code == 204

    follow_up = client.get(f"/api/books/{book.id}")
    assert follow_up.status_code == 404


def test_delete_book_requires_admin(client):
    book = _make_book()
    token = _login(client, REGULAR)

    response = client.delete(f"/api/books/{book.id}", headers=_auth(token))
    assert response.status_code == 403
