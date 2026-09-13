"""
Administracao de usuarios pelo painel do admin: listar, criar, editar,
apagar. Cadastro publico (self-service) continua em services/auth.py —
este arquivo e so para quem administra OUTROS usuarios.
"""

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import User


class UserError(Exception):
    """Erro de negocio que o blueprint traduz em status HTTP."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status


def list_users():
    return User.query.order_by(User.username.asc()).all()


def get_user_by_id(user_id: int):
    return User.query.get(user_id)


def _check_unique(username: str, email: str, *, ignore_user_id: int = None) -> None:
    existing_email = db.session.query(User).filter_by(email=email).first()
    if existing_email and existing_email.id != ignore_user_id:
        raise UserError("Este e-mail ja esta cadastrado.", 409)

    existing_username = db.session.query(User).filter_by(username=username).first()
    if existing_username and existing_username.id != ignore_user_id:
        raise UserError("Este nome de usuario ja esta em uso.", 409)


def create_user(data: dict) -> User:
    _check_unique(data["username"], data["email"])

    user = User(
        username=data["username"],
        email=data["email"],
        display_name=data.get("display_name"),
        role=data.get("role", "user"),
        password_hash=generate_password_hash(data["password"]),
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise UserError("Este e-mail ou nome de usuario ja esta em uso.", 409)
    return user


def update_user(user_id: int, data: dict, *, requested_by: int) -> User:
    """`data` so contem os campos que vieram no corpo da requisicao (ver
    `validate_user_update`) — os demais ficam como estavam."""
    user = get_user_by_id(user_id)
    if user is None:
        raise UserError("Usuario nao encontrado.", 404)

    if user_id == requested_by:
        if data.get("role") == "user":
            raise UserError("Nao e possivel remover o proprio nivel de admin.", 400)
        if data.get("is_active") is False:
            raise UserError("Nao e possivel desativar a propria conta.", 400)

    if "username" in data or "email" in data:
        _check_unique(
            data.get("username", user.username),
            data.get("email", user.email),
            ignore_user_id=user.id,
        )

    password = data.pop("password", None)
    for field, value in data.items():
        setattr(user, field, value)
    if password:
        user.password_hash = generate_password_hash(password)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise UserError("Este e-mail ou nome de usuario ja esta em uso.", 409)
    return user


def delete_user(user_id: int, *, requested_by: int) -> None:
    if user_id == requested_by:
        raise UserError("Nao e possivel excluir a propria conta.", 400)

    user = get_user_by_id(user_id)
    if user is None:
        raise UserError("Usuario nao encontrado.", 404)

    db.session.delete(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise UserError(
            "Nao e possivel excluir um usuario que cadastrou livros.", 409
        )
