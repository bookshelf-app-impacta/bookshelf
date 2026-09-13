"""
Rotas de administracao de usuarios — painel em /admin/usuarios no
frontend. Todas exigem admin, inclusive listar: diferente de livros,
aqui nao tem leitura publica (e-mail de outra pessoa e dado sensivel).

Cadastro publico (self-service) continua em blueprints/auth.py — este
arquivo e so para quem administra OUTROS usuarios.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user

from app.schemas.user import (
    user_to_json,
    users_to_json_list,
    validate_user_create,
    validate_user_update,
)
from app.security import admin_required
from app.services.user_service import (
    UserError,
    create_user,
    delete_user,
    list_users,
    update_user,
)

bp = Blueprint("users", __name__)


@bp.errorhandler(UserError)
def _handle_user_error(error: UserError):
    return jsonify(error=error.message), error.status


def _invalid_data(errors: dict):
    return jsonify(error="Dados invalidos.", fields=errors), 400


@bp.get("/")
@admin_required
def list_users_route():
    return jsonify(users_to_json_list(list_users())), 200


@bp.post("/")
@admin_required
def create_user_route():
    data, errors = validate_user_create(request.get_json(silent=True))
    if errors:
        return _invalid_data(errors)

    user = create_user(data)
    return jsonify(user_to_json(user)), 201


@bp.put("/<int:user_id>")
@admin_required
def update_user_route(user_id: int):
    data, errors = validate_user_update(request.get_json(silent=True))
    if errors:
        return _invalid_data(errors)

    user = update_user(user_id, data, requested_by=current_user.id)
    return jsonify(user_to_json(user)), 200


@bp.delete("/<int:user_id>")
@admin_required
def delete_user_route(user_id: int):
    delete_user(user_id, requested_by=current_user.id)
    return "", 204
