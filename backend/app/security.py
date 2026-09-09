"""
Autenticacao: quem esta logado e quem pode o que.

Fica na raiz de `app/` porque um decorador de permissao nao e rota, nem
regra de negocio, nem model, nem schema. E o que as outras frentes
importam:

    from flask_jwt_extended import current_user
    from app.security import admin_required

    @bp.post("")
    @admin_required
    def criar_livro():
        livro = Book(..., created_by=current_user.id)
"""

from functools import wraps

from flask import jsonify
from flask_jwt_extended import current_user, verify_jwt_in_request

from app.extensions import db, jwt
from app.models import User


@jwt.user_identity_loader
def _identidade(user: User) -> str:
    # String, nao int: a RFC 7519 define `sub` como string e o
    # Flask-JWT-Extended 4.7 passou a recusar o token quando nao e.
    return str(user.id)


@jwt.user_lookup_loader
def _carrega_usuario(_cabecalho, dados_do_token):
    """Roda a cada requisicao autenticada e alimenta o `current_user`."""
    return db.session.get(User, int(dados_do_token["sub"]))


def admin_required(fn):
    """Exige token valido E papel de admin."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if not current_user.is_admin:
            # 403 e nao 401: sabemos quem e, so nao pode. O front manda
            # para a tela de login no 401 e nao deve mandar aqui.
            return jsonify(error="Acesso restrito a administradores."), 403
        return fn(*args, **kwargs)

    return wrapper


# Sem estes handlers o Flask-JWT-Extended responde em ingles e, as vezes,
# em HTML — e o response.json() do front estoura.


@jwt.unauthorized_loader
def _sem_token(_motivo):
    return jsonify(error="Token de autenticacao ausente."), 401


@jwt.invalid_token_loader
def _token_invalido(_motivo):
    return jsonify(error="Token de autenticacao invalido."), 401


@jwt.expired_token_loader
def _token_expirado(_cabecalho, _dados_do_token):
    return jsonify(error="Sessao expirada. Faca login novamente."), 401


@jwt.user_lookup_error_loader
def _usuario_sumiu(_cabecalho, _dados_do_token):
    return jsonify(error="Usuario do token nao existe mais."), 401
