from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import User

# Hash de uma senha que ninguem usa. Ver o comentario em `authenticate`.
_DUMMY_HASH = generate_password_hash("nao-e-a-senha-de-ninguem")


class AuthError(Exception):
    """Erro de negocio que o blueprint traduz em status HTTP."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status


def register_user(username: str, email: str, password: str,
                  display_name: str = None) -> User:
    """Cria uma conta comum.

    Nao existe parametro `role`, e e a assinatura da funcao que garante
    isso: nao ha por onde um {"role": "admin"} vindo do corpo da
    requisicao chegar aqui e virar direito de cadastrar livros.
    """
    # Checar antes de inserir para o erro virar 409 legivel em vez de um
    # IntegrityError cru do MySQL.
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


def authenticate(email: str, password: str) -> User:
    user = db.session.query(User).filter_by(email=email).first()

    # Com e-mail inexistente, conferir um hash descartavel em vez de sair
    # direto. Verificar hash e lento de proposito; sair antes deixaria a
    # resposta visivelmente mais rapida e entregaria quem tem conta.
    target_hash = user.password_hash if user else _DUMMY_HASH
    password_matches = check_password_hash(target_hash, password)

    # Mensagem unica para e-mail errado e senha errada, pelo mesmo motivo.
    if not user or not password_matches:
        raise AuthError("E-mail ou senha invalidos.", 401)

    # Regra de negocio, nao de rota: o botao de desativar conta da tela
    # de admin precisa barrar o login por qualquer caminho.
    if not user.is_active:
        raise AuthError("Esta conta esta desativada.", 403)

    return user
