"""
Testes das rotas de /api/users — painel de administracao.
"""

import uuid

import pytest
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.book import Book
from app.models.user import User

# Credenciais criadas por `flask seed`. Ver app/cli.py.
ADMIN = {"email": "admin@bookshelf.local", "password": "admin123"}
REGULAR = {"email": "ana@bookshelf.local", "password": "user123"}
_SEEDED_EMAILS = {ADMIN["email"], REGULAR["email"], "bruno@bookshelf.local"}


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
    """Apaga so o que os testes deste arquivo criaram (livro de teste
    do caso RESTRICT, usuarios), sem tocar no catalogo seedado nem nos
    usuarios do `flask seed` que o resto do grupo tambem usa."""
    with app.app_context():
        last_book_id = db.session.query(func.max(Book.id)).scalar() or 0

    yield

    with app.app_context():
        db.session.query(Book).filter(Book.id > last_book_id).delete()
        db.session.query(User).filter(User.email.notin_(_SEEDED_EMAILS)).delete(
            synchronize_session=False
        )
        db.session.commit()


def _login(client, credentials) -> str:
    response = client.post("/api/auth/login", json=credentials)
    assert response.status_code == 200, response.get_json()
    return response.get_json()["token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _make_user(**overrides) -> User:
    suffix = uuid.uuid4().hex[:6]
    data = {
        "username": f"user{suffix}",
        "email": f"user{suffix}@bookshelf.local",
        "password_hash": generate_password_hash("senha12345"),
        "role": "user",
    }
    data.update(overrides)
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user


# --- listar (GET) ---------------------------------------------------------


def test_list_users_requires_admin(client):
    token = _login(client, REGULAR)
    response = client.get("/api/users/", headers=_auth(token))

    assert response.status_code == 403


def test_list_users_without_token_returns_401(client):
    response = client.get("/api/users/")

    assert response.status_code == 401


def test_list_users_as_admin(client):
    token = _login(client, ADMIN)
    response = client.get("/api/users/", headers=_auth(token))

    assert response.status_code == 200
    emails = [user["email"] for user in response.get_json()]
    assert ADMIN["email"] in emails


# --- criar (POST) -----------------------------------------------------------


def test_create_user_requires_admin(client):
    token = _login(client, REGULAR)
    response = client.post(
        "/api/users/",
        json={"username": "x", "email": "x@bookshelf.local", "password": "senha12345"},
        headers=_auth(token),
    )

    assert response.status_code == 403


def test_create_user_as_admin(client):
    token = _login(client, ADMIN)
    suffix = uuid.uuid4().hex[:6]
    response = client.post(
        "/api/users/",
        json={
            "username": f"novo{suffix}",
            "email": f"novo{suffix}@bookshelf.local",
            "password": "senha12345",
            "role": "admin",
        },
        headers=_auth(token),
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["role"] == "admin"
    assert data["isActive"] is True
    assert "password" not in data
    assert "password_hash" not in data


def test_create_user_rejects_duplicate_email(client):
    token = _login(client, ADMIN)
    response = client.post(
        "/api/users/",
        json={"username": "outro", "email": ADMIN["email"], "password": "senha12345"},
        headers=_auth(token),
    )

    assert response.status_code == 409


def test_create_user_validates_password_length(client):
    token = _login(client, ADMIN)
    suffix = uuid.uuid4().hex[:6]
    response = client.post(
        "/api/users/",
        json={
            "username": f"fraco{suffix}",
            "email": f"fraco{suffix}@bookshelf.local",
            "password": "123",
        },
        headers=_auth(token),
    )

    assert response.status_code == 400
    assert "password" in response.get_json()["fields"]


# --- editar (PUT) ------------------------------------------------------------


def test_update_user_as_admin(client):
    user = _make_user()
    token = _login(client, ADMIN)

    response = client.put(
        f"/api/users/{user.id}",
        json={"displayName": "Novo Nome"},
        headers=_auth(token),
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["displayName"] == "Novo Nome"
    assert data["username"] == user.username  # campo nao enviado, intacto


def test_update_user_can_deactivate(client):
    user = _make_user()
    token = _login(client, ADMIN)

    response = client.put(
        f"/api/users/{user.id}", json={"isActive": False}, headers=_auth(token),
    )

    assert response.status_code == 200
    assert response.get_json()["isActive"] is False


def test_update_user_requires_admin(client):
    user = _make_user()
    token = _login(client, REGULAR)

    response = client.put(
        f"/api/users/{user.id}", json={"displayName": "X"}, headers=_auth(token),
    )

    assert response.status_code == 403


def test_update_user_not_found(client):
    token = _login(client, ADMIN)
    response = client.put(
        "/api/users/9999", json={"displayName": "X"}, headers=_auth(token),
    )

    assert response.status_code == 404


def test_update_user_rejects_duplicate_email(client):
    other = _make_user()
    user = _make_user()
    token = _login(client, ADMIN)

    response = client.put(
        f"/api/users/{user.id}", json={"email": other.email}, headers=_auth(token),
    )

    assert response.status_code == 409


def test_update_user_rejects_invalid_role_type(client):
    # role=123 (nao-string) nao pode virar "user" silenciosamente: tem
    # que gerar erro de validacao, igual role="qualquer-coisa" ja gera.
    user = _make_user()
    token = _login(client, ADMIN)

    response = client.put(
        f"/api/users/{user.id}", json={"role": 123}, headers=_auth(token),
    )

    assert response.status_code == 400
    assert "role" in response.get_json()["fields"]


def test_admin_cannot_demote_own_account(client):
    token = _login(client, ADMIN)
    admin_user = db.session.query(User).filter_by(email=ADMIN["email"]).one()

    response = client.put(
        f"/api/users/{admin_user.id}", json={"role": "user"}, headers=_auth(token),
    )

    assert response.status_code == 400


def test_admin_cannot_deactivate_own_account(client):
    token = _login(client, ADMIN)
    admin_user = db.session.query(User).filter_by(email=ADMIN["email"]).one()

    response = client.put(
        f"/api/users/{admin_user.id}", json={"isActive": False}, headers=_auth(token),
    )

    assert response.status_code == 400


# --- apagar (DELETE) ----------------------------------------------------------


def test_delete_user_as_admin(client):
    user = _make_user()
    token = _login(client, ADMIN)

    response = client.delete(f"/api/users/{user.id}", headers=_auth(token))

    assert response.status_code == 204


def test_delete_user_requires_admin(client):
    user = _make_user()
    token = _login(client, REGULAR)

    response = client.delete(f"/api/users/{user.id}", headers=_auth(token))

    assert response.status_code == 403


def test_admin_cannot_delete_own_account(client):
    token = _login(client, ADMIN)
    admin_user = db.session.query(User).filter_by(email=ADMIN["email"]).one()

    response = client.delete(f"/api/users/{admin_user.id}", headers=_auth(token))

    assert response.status_code == 400


def test_cannot_delete_user_who_created_books(client):
    # books.created_by e ON DELETE RESTRICT — o banco recusa, e o
    # service precisa traduzir isso num erro legivel, nao num 500.
    user = _make_user()
    book = Book(
        title="Livro de Teste",
        slug=f"livro-teste-{uuid.uuid4().hex[:6]}",
        created_by=user.id,
    )
    db.session.add(book)
    db.session.commit()

    token = _login(client, ADMIN)
    response = client.delete(f"/api/users/{user.id}", headers=_auth(token))

    assert response.status_code == 409
