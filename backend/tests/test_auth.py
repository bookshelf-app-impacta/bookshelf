"""
Testes das rotas de autenticacao.

Rodam contra o MySQL de desenvolvimento, ja migrado e com `flask seed`
aplicado — nao da para usar SQLite porque os models usam o BIGINT
UNSIGNED do dialeto MySQL. De dentro de backend/:

    python -m pytest

O `python -m` importa: e ele que poe o diretorio atual no sys.path.
"""

import uuid

import pytest

from app import create_app
from app.extensions import db
from app.models import User
from app.security import admin_required

# Credenciais criadas por `flask seed`. Ver app/cli.py.
ADMIN = {"email": "admin@bookshelf.local", "password": "admin123"}
REGULAR = {"email": "ana@bookshelf.local", "password": "user123"}


@pytest.fixture(scope="session")
def app():
    flask_app = create_app()
    flask_app.config.update(TESTING=True)

    # A primeira rota de admin de verdade e o cadastro de livro, que e
    # card de outra pessoa. Sem esta rota descartavel nao haveria como
    # provar o @admin_required antes dela chegar.
    @flask_app.get("/api/_test/admin-only")
    @admin_required
    def _admin_only():
        return {"ok": True}

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


@pytest.fixture()
def throwaway_email(app):
    """E-mail unico; a linha sai do banco quando o teste acaba, para nao
    sujar a base que o grupo usa para revisar PR e gravar o video."""
    email = f"pytest-{uuid.uuid4().hex[:8]}@bookshelf.local"
    yield email
    with app.app_context():
        db.session.query(User).filter_by(email=email).delete()
        db.session.commit()


# --- login ---------------------------------------------------------------


def test_valid_login_returns_token_and_user(client):
    response = client.post("/api/auth/login", json=ADMIN)
    body = response.get_json()

    assert response.status_code == 200
    assert body["token"]
    # Contrato com frontend/src/types/user.ts: se uma chave sumir, a tela
    # quebra e o teste tem que acusar.
    assert set(body["user"]) == {
        "id", "username", "email", "displayName", "avatarUrl",
        "role", "isActive",
    }
    assert body["user"]["role"] == "admin"
    # O hash nunca sai da API.
    assert "password_hash" not in body["user"]


def test_login_with_wrong_password_returns_401(client):
    response = client.post(
        "/api/auth/login",
        json={"email": ADMIN["email"], "password": "senha-errada"},
    )

    assert response.status_code == 401
    # Mesma mensagem do e-mail inexistente, de proposito: dizer qual dos
    # dois errou confirma quais e-mails tem conta.
    assert response.get_json()["error"] == "E-mail ou senha invalidos."


def test_login_with_unknown_email_returns_401(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "ninguem@bookshelf.local", "password": "senha12345"},
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "E-mail ou senha invalidos."


def test_deactivated_account_cannot_log_in(client, app, throwaway_email):
    client.post("/api/auth/register", json={
        "username": f"des{uuid.uuid4().hex[:6]}",
        "email": throwaway_email,
        "password": "senha12345",
    })

    with app.app_context():
        user = db.session.query(User).filter_by(email=throwaway_email).one()
        user.is_active = False
        db.session.commit()

    response = client.post("/api/auth/login", json={
        "email": throwaway_email, "password": "senha12345",
    })

    # 403 e nao 401: as credenciais estao certas, a conta e que esta
    # bloqueada.
    assert response.status_code == 403
    assert response.get_json()["error"] == "Esta conta esta desativada."


# --- /me -----------------------------------------------------------------


def test_me_without_token_returns_401(client):
    response = client.get("/api/auth/me")

    # Em JSON, nao em HTML: o response.json() do front estoura com HTML.
    assert response.status_code == 401
    assert "error" in response.get_json()


def test_me_returns_the_token_owner(client):
    token = _login(client, REGULAR)
    response = client.get("/api/auth/me", headers=_auth(token))

    assert response.status_code == 200
    assert response.get_json()["email"] == REGULAR["email"]
    assert response.get_json()["role"] == "user"


# --- register ------------------------------------------------------------


def test_register_ignores_role_from_request_body(client, throwaway_email):
    """Se o `role` do corpo fosse aceito, qualquer pessoa se cadastraria
    como admin e ganharia o direito de cadastrar livros."""
    response = client.post("/api/auth/register", json={
        "username": f"esc{uuid.uuid4().hex[:6]}",
        "email": throwaway_email,
        "password": "senha12345",
        "role": "admin",
    })

    assert response.status_code == 201
    assert response.get_json()["user"]["role"] == "user"


def test_register_rejects_duplicate_email(client):
    response = client.post("/api/auth/register", json={
        "username": f"dup{uuid.uuid4().hex[:6]}",
        "email": ADMIN["email"],
        "password": "senha12345",
    })

    assert response.status_code == 409


def test_register_validates_input(client):
    response = client.post("/api/auth/register", json={
        "username": "ab", "email": "sem-arroba", "password": "123",
    })

    assert response.status_code == 400
    assert set(response.get_json()["fields"]) == {
        "username", "email", "password",
    }


# --- @admin_required -----------------------------------------------------


def test_admin_required_allows_admin(client):
    token = _login(client, ADMIN)
    response = client.get("/api/_test/admin-only", headers=_auth(token))

    assert response.status_code == 200


def test_admin_required_blocks_regular_user(client):
    token = _login(client, REGULAR)
    response = client.get("/api/_test/admin-only", headers=_auth(token))

    # 403 e nao 401: sabemos quem e, so nao pode.
    assert response.status_code == 403


def test_admin_required_without_token_returns_401(client):
    response = client.get("/api/_test/admin-only")

    assert response.status_code == 401
