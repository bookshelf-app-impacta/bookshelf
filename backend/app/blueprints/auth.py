"""
Rotas de autenticacao.  [AC1]

O token vai em `Authorization: Bearer <token>`. Formato das respostas,
combinado com o front:

    sucesso  {"token": "...", "user": {...}}   (o /me devolve so o user)
    erro     {"error": "mensagem"}
    400      {"error": "...", "fields": {"campo": "o que esta errado"}}
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required

from app.schemas.auth import validate_login, validate_register
from app.schemas.user import user_to_json
from app.services.auth import AuthError, authenticate, register_user

bp = Blueprint("auth", __name__)


@bp.errorhandler(AuthError)
def _trata_auth_error(erro: AuthError):
    """Existir isto e o que permite ao service so levantar AuthError, sem
    saber o que e um status HTTP."""
    return jsonify(error=erro.message), erro.status


def _dados_invalidos(erros: dict):
    return jsonify(error="Dados invalidos.", fields=erros), 400


@bp.post("/register")
def register():
    # silent=True: corpo ausente ou JSON quebrado vira None, em vez de um
    # 415 em HTML que o front nao consegue ler.
    dados, erros = validate_register(request.get_json(silent=True))
    if erros:
        return _dados_invalidos(erros)

    user = register_user(**dados)
    # Ja devolve o token: quem se cadastrou entra logado, sem digitar a
    # senha de novo na tela seguinte.
    return jsonify(
        token=create_access_token(identity=user),
        user=user_to_json(user),
    ), 201


@bp.post("/login")
def login():
    dados, erros = validate_login(request.get_json(silent=True))
    if erros:
        return _dados_invalidos(erros)

    user = authenticate(**dados)
    return jsonify(
        token=create_access_token(identity=user),
        user=user_to_json(user),
    ), 200


@bp.get("/me")
@jwt_required()
def me():
    return jsonify(user_to_json(current_user)), 200
