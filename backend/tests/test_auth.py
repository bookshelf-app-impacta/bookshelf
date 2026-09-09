"""
Testes das rotas de autenticacao.

Rodam contra o MySQL de desenvolvimento, o mesmo que sobe no
`docker compose up -d`. Nao ha banco em memoria porque os models usam
tipos do dialeto MySQL (o BIGINT UNSIGNED de app/models/base.py) que o
SQLite nao consegue compilar.

Antes de rodar, com o banco de pe:

    flask db upgrade
    flask seed

E rode de dentro de backend/, com o venv ativo:

    python -m pytest

O `python -m` importa: e ele que coloca o diretorio atual no sys.path.
Um `pytest` solto nao acha o pacote `app`.

O que grava no banco usa e-mail unico e apaga a linha no fim, para nao
sujar a base que o grupo usa para revisar PR e gravar o video.
"""

import uuid

import pytest

from app import create_app
from app.extensions import db
from app.models import User
from app.security import admin_required

# Credenciais criadas por `flask seed`. Ver app/cli.py.
ADMIN = {"email": "admin@bookshelf.local", "password": "admin123"}
COMUM = {"email": "ana@bookshelf.local", "password": "user123"}


@pytest.fixture(scope="session")
def app():
    aplicacao = create_app()
    aplicacao.config.update(TESTING=True)

    # Rota descartavel, registrada so aqui. A primeira rota de admin de
    # verdade e o cadastro de livro, que e card de outra pessoa e ainda
    # nao existe — sem isto nao haveria como provar que o @admin_required
    # funciona antes dela chegar.
    @aplicacao.get("/api/_teste/so-admin")
    @admin_required
    def _so_admin():
        return {"ok": True}

    return aplicacao


@pytest.fixture()
def client(app):
    return app.test_client()


def _login(client, credenciais) -> str:
    resposta = client.post("/api/auth/login", json=credenciais)
    assert resposta.status_code == 200, resposta.get_json()
    return resposta.get_json()["token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def email_descartavel(app):
    """E-mail unico; a linha e removida do banco quando o teste acaba."""
    email = f"pytest-{uuid.uuid4().hex[:8]}@bookshelf.local"
    yield email
    with app.app_context():
        db.session.query(User).filter_by(email=email).delete()
        db.session.commit()


# --- login ---------------------------------------------------------------


def test_login_valido_devolve_token_e_usuario(client):
    resposta = client.post("/api/auth/login", json=ADMIN)
    corpo = resposta.get_json()

    assert resposta.status_code == 200
    assert corpo["token"]
    # As chaves do usuario sao o contrato com o frontend
    # (frontend/src/types/user.ts). Se alguma sumir, a tela quebra.
    assert set(corpo["user"]) == {
        "id", "username", "email", "displayName", "avatarUrl",
        "role", "isActive",
    }
    assert corpo["user"]["role"] == "admin"
    # O hash nunca sai da API.
    assert "password_hash" not in corpo["user"]


def test_login_com_senha_errada_devolve_401(client):
    resposta = client.post(
        "/api/auth/login",
        json={"email": ADMIN["email"], "password": "senha-errada"},
    )

    assert resposta.status_code == 401
    # Mesma mensagem de e-mail inexistente, de proposito: dizer qual dos
    # dois errou confirma quais e-mails tem conta.
    assert resposta.get_json()["error"] == "E-mail ou senha invalidos."


def test_login_com_email_inexistente_devolve_401(client):
    resposta = client.post(
        "/api/auth/login",
        json={"email": "ninguem@bookshelf.local", "password": "senha12345"},
    )

    assert resposta.status_code == 401
    assert resposta.get_json()["error"] == "E-mail ou senha invalidos."


def test_conta_desativada_nao_loga(client, app, email_descartavel):
    client.post("/api/auth/register", json={
        "username": f"des{uuid.uuid4().hex[:6]}",
        "email": email_descartavel,
        "password": "senha12345",
    })

    with app.app_context():
        usuario = db.session.query(User).filter_by(
            email=email_descartavel).one()
        usuario.is_active = False
        db.session.commit()

    resposta = client.post("/api/auth/login", json={
        "email": email_descartavel, "password": "senha12345",
    })

    # 403 e nao 401: as credenciais estao certas, a conta e que esta
    # bloqueada. O front precisa distinguir para mostrar a mensagem certa.
    assert resposta.status_code == 403
    assert resposta.get_json()["error"] == "Esta conta esta desativada."


# --- /me -----------------------------------------------------------------


def test_me_sem_token_devolve_401(client):
    resposta = client.get("/api/auth/me")

    assert resposta.status_code == 401
    # Em JSON, nao em HTML: o response.json() do front estoura com HTML.
    assert "error" in resposta.get_json()


def test_me_com_token_devolve_o_usuario_do_token(client):
    token = _login(client, COMUM)
    resposta = client.get("/api/auth/me", headers=_auth(token))

    assert resposta.status_code == 200
    assert resposta.get_json()["email"] == COMUM["email"]
    assert resposta.get_json()["role"] == "user"


# --- register ------------------------------------------------------------


def test_register_ignora_role_do_corpo_da_requisicao(client,
                                                     email_descartavel):
    """O teste mais importante do arquivo.

    Se o `role` do corpo fosse aceito, qualquer pessoa se cadastraria como
    admin e ganharia o direito de cadastrar livros.
    """
    resposta = client.post("/api/auth/register", json={
        "username": f"esc{uuid.uuid4().hex[:6]}",
        "email": email_descartavel,
        "password": "senha12345",
        "role": "admin",
    })

    assert resposta.status_code == 201
    assert resposta.get_json()["user"]["role"] == "user"


def test_register_recusa_email_ja_cadastrado(client):
    resposta = client.post("/api/auth/register", json={
        "username": f"dup{uuid.uuid4().hex[:6]}",
        "email": ADMIN["email"],
        "password": "senha12345",
    })

    assert resposta.status_code == 409


def test_register_valida_a_entrada(client):
    resposta = client.post("/api/auth/register", json={
        "username": "ab", "email": "sem-arroba", "password": "123",
    })

    assert resposta.status_code == 400
    assert set(resposta.get_json()["fields"]) == {
        "username", "email", "password",
    }


# --- @admin_required -----------------------------------------------------


def test_admin_required_deixa_o_admin_passar(client):
    token = _login(client, ADMIN)
    resposta = client.get("/api/_teste/so-admin", headers=_auth(token))

    assert resposta.status_code == 200


def test_admin_required_bloqueia_usuario_comum(client):
    token = _login(client, COMUM)
    resposta = client.get("/api/_teste/so-admin", headers=_auth(token))

    # 403 e nao 401: sabemos quem e, so nao pode. O front nao deve mandar
    # essa pessoa para a tela de login.
    assert resposta.status_code == 403


def test_admin_required_sem_token_devolve_401(client):
    resposta = client.get("/api/_teste/so-admin")

    assert resposta.status_code == 401
