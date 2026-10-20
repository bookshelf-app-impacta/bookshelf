from functools import wraps
from flask import jsonify
from flask_jwt_extended import current_user, verify_jwt_in_request
from app.extensions import db, jwt
from app.models import User


@jwt.user_identity_loader
def _user_identity(user: User) -> str:
    return str(user.id)


@jwt.user_lookup_loader
def _load_user(_header, jwt_data):
    return db.session.get(User, int(jwt_data["sub"]))


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if not current_user or not current_user.is_admin:
            return jsonify(error="Acesso restrito a administradores."), 403
        return fn(*args, **kwargs)
    return wrapper


@jwt.unauthorized_loader
def _missing_token(_reason):
    return jsonify(error="Token de autenticacao ausente."), 401


@jwt.invalid_token_loader
def _invalid_token(_reason):
    return jsonify(error="Token de autenticacao invalido."), 401


@jwt.expired_token_loader
def _expired_token(_header, _jwt_data):
    return jsonify(error="Sessao expirada. Faca login novamente."), 401


@jwt.user_lookup_error_loader
def _user_not_found(_header, _jwt_data):
    return jsonify(error="Usuario do token nao existe mais."), 401
