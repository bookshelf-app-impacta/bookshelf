from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required

from app.schemas.auth import validate_login, validate_register
from app.schemas.user import user_to_json
from app.services.auth import AuthError, authenticate, register_user

bp = Blueprint("auth", __name__)


@bp.errorhandler(AuthError)
def _handle_auth_error(error):
    return jsonify(error=error.message), error.status


def _invalid_data(errors):
    return jsonify(error="Dados invalidos.", fields=errors), 400


@bp.post("/register")
def register():
    data, errors = validate_register(request.get_json(silent=True))
    if errors:
        return _invalid_data(errors)
    user = register_user(**data)
    return jsonify(token=create_access_token(identity=user), user=user_to_json(user)), 201


@bp.post("/login")
def login():
    data, errors = validate_login(request.get_json(silent=True))
    if errors:
        return _invalid_data(errors)
    user = authenticate(**data)
    return jsonify(token=create_access_token(identity=user), user=user_to_json(user)), 200


@bp.get("/me")
@jwt_required()
def me():
    return jsonify(user_to_json(current_user)), 200
