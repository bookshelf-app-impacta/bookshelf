from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required

from app.schemas.auth import validate_login, validate_register
from app.schemas.user import user_to_json
from app.services.auth import AuthError, authenticate, register_user

bp = Blueprint("auth", __name__)


@bp.errorhandler(AuthError)
def _handle_auth_error(error: AuthError):
    return jsonify(error=error.message), error.status


def _invalid_data(errors: dict):
    return jsonify(error="Dados invalidos.", fields=errors), 400


@bp.post("/register")
def register():
    # silent=True: corpo ausente ou JSON quebrado vira None, em vez de um
    # 415 em HTML que o front nao consegue ler.
    data, errors = validate_register(request.get_json(silent=True))
    if errors:
        return _invalid_data(errors)

    user = register_user(**data)
    # Ja devolve o token: quem se cadastrou entra logado, sem digitar a
    # senha de novo na tela seguinte.
    return jsonify(
        token=create_access_token(identity=user),
        user=user_to_json(user),
    ), 201


@bp.post("/login")
def login():
    data, errors = validate_login(request.get_json(silent=True))
    if errors:
        return _invalid_data(errors)

    user = authenticate(**data)
    return jsonify(
        token=create_access_token(identity=user),
        user=user_to_json(user),
    ), 200


@bp.get("/me")
@jwt_required()
def me():
    return jsonify(user_to_json(current_user)), 200
