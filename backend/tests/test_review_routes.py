"""
Testes das rotas de comentarios — /api/books/<id>/reviews/ (listar e
criar). As regras do corpo da requisicao ja estao em test_review.py;
aqui o foco e o HTTP: auth, status e formato do JSON.
"""

import uuid

import pytest
from sqlalchemy import func

from app import create_app
from app.extensions import db
from app.models.book import Author, Book
from app.models.user import User

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


@pytest.fixture(autouse=True)
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture(autouse=True)
def _cleanup(app):
    """
    Apaga so os livros e autores que o teste criou (maior id antes do
    teste). As reviews vao junto pelo `ondelete="CASCADE"` em book_id —
    nunca apagar a tabela de reviews inteira, senao some o que o
    `flask seed` criou.
    """
    with app.app_context():
        last_book_id = db.session.query(func.max(Book.id)).scalar() or 0
        last_author_id = db.session.query(func.max(Author.id)).scalar() or 0

    yield

    with app.app_context():
        db.session.query(Book).filter(Book.id > last_book_id).delete()
        db.session.query(Author).filter(Author.id > last_author_id).delete()
        db.session.commit()


def _login(client, credentials) -> str:
    response = client.post("/api/auth/login", json=credentials)
    assert response.status_code == 200, response.get_json()
    return response.get_json()["token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _make_book() -> Book:
    suffix = uuid.uuid4().hex[:6]
    author = Author(name="Autor Teste", slug=f"autor-teste-{suffix}")
    db.session.add(author)
    db.session.flush()

    admin = db.session.query(User).filter_by(email=ADMIN["email"]).one()
    book = Book(
        title="Livro Teste",
        slug=f"livro-teste-{suffix}",
        author_id=author.id,
        created_by=admin.id,
    )
    db.session.add(book)
    db.session.commit()
    return book


def _missing_book_id() -> int:
    return (db.session.query(func.max(Book.id)).scalar() or 0) + 1000


def test_create_review_logged_user(client):
    book = _make_book()
    token = _login(client, REGULAR)

    response = client.post(
        f"/api/books/{book.id}/reviews/",
        json={"body": "  Gostei muito!  "},
        headers=_auth(token),
    )

    assert response.status_code == 201, response.get_json()
    data = response.get_json()
    assert data["bookId"] == book.id
    assert data["body"] == "Gostei muito!"
    assert data["rating"] is None
    assert data["user"]["username"]
    assert set(data["user"]) == {"id", "username", "displayName", "avatarUrl"}
    assert data["createdAt"] and data["updatedAt"]


def test_create_review_requires_login(client):
    book = _make_book()

    response = client.post(f"/api/books/{book.id}/reviews/", json={"body": "Oi"})

    assert response.status_code == 401


def test_create_review_empty_body_returns_400(client):
    book = _make_book()
    token = _login(client, REGULAR)

    response = client.post(
        f"/api/books/{book.id}/reviews/", json={"body": "   "}, headers=_auth(token)
    )

    assert response.status_code == 400
    assert "_geral" in response.get_json()["fields"]


def test_create_review_twice_returns_409(client):
    book = _make_book()
    token = _login(client, REGULAR)
    url = f"/api/books/{book.id}/reviews/"

    first = client.post(url, json={"body": "Primeiro"}, headers=_auth(token))
    second = client.post(url, json={"body": "Segundo"}, headers=_auth(token))

    assert first.status_code == 201
    assert second.status_code == 409


def test_create_review_missing_book_returns_404(client):
    token = _login(client, REGULAR)

    response = client.post(
        f"/api/books/{_missing_book_id()}/reviews/",
        json={"body": "Oi"},
        headers=_auth(token),
    )

    assert response.status_code == 404


def test_list_reviews_is_public_and_newest_first(client):
    book = _make_book()
    url = f"/api/books/{book.id}/reviews/"
    client.post(url, json={"body": "Da Ana"}, headers=_auth(_login(client, REGULAR)))
    client.post(url, json={"body": "Do admin"}, headers=_auth(_login(client, ADMIN)))

    response = client.get(url)

    assert response.status_code == 200
    bodies = [review["body"] for review in response.get_json()]
    assert bodies == ["Do admin", "Da Ana"]


def test_list_reviews_empty(client):
    book = _make_book()

    response = client.get(f"/api/books/{book.id}/reviews/")

    assert response.status_code == 200
    assert response.get_json() == []


def test_list_reviews_missing_book_returns_404(client):
    response = client.get(f"/api/books/{_missing_book_id()}/reviews/")

    assert response.status_code == 404
