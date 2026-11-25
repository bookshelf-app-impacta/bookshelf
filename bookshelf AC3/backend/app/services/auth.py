from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db
from app.models import User

_DUMMY_HASH = generate_password_hash("nao-e-a-senha-de-ninguem")


class AuthError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def register_user(username, email, password, display_name=None):
    if db.session.query(User).filter_by(email=email).first():
        raise AuthError("Este e-mail ja esta cadastrado.", 409)
    if db.session.query(User).filter_by(username=username).first():
        raise AuthError("Este nome de usuario ja esta em uso.", 409)
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        display_name=display_name,
        role="user",
    )
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(email, password):
    user = db.session.query(User).filter_by(email=email).first()
    target_hash = user.password_hash if user else _DUMMY_HASH
    password_matches = check_password_hash(target_hash, password)
    if not user or not password_matches:
        raise AuthError("E-mail ou senha invalidos.", 401)
    if not user.is_active:
        raise AuthError("Esta conta esta desativada.", 403)
    return user
