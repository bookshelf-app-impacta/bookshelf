"""
Regra de negocio da autenticacao.

Nada aqui conhece `request` ou `jsonify`. Quem traduz para HTTP e o
blueprint. Isso deixa a regra testavel sem subir servidor e reaproveitavel
por um comando de CLI, se um dia precisar criar usuario pelo terminal.
"""

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import User

# Hash de uma senha que ninguem usa. Serve so para gastar o mesmo tempo de
# CPU quando o e-mail nao existe. Ver o comentario em `authenticate`.
_HASH_DESCARTAVEL = generate_password_hash("nao-e-a-senha-de-ninguem")


class AuthError(Exception):
    """Erro de negocio que o blueprint traduz em status HTTP."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status


def register_user(username: str, email: str, password: str,
                  display_name: str = None) -> User:
    """Cria uma conta comum.

    Repare que nao existe parametro `role`. Quem se cadastra e sempre
    'user', e a assinatura da funcao e o que garante isso: nao ha por
    onde um {"role": "admin"} vindo do corpo da requisicao chegar aqui.
    Se houvesse, qualquer pessoa se promoveria a administradora e ganharia
    o direito de cadastrar livros. Promover alguem e outro fluxo.
    """
    # Checar antes de inserir para o erro virar 409 com mensagem legivel
    # em vez de um IntegrityError cru do MySQL na cara do usuario.
    if db.session.query(User).filter_by(email=email).first():
        raise AuthError("Este e-mail ja esta cadastrado.", 409)
    if db.session.query(User).filter_by(username=username).first():
        raise AuthError("Este nome de usuario ja esta em uso.", 409)

    user = User(
        username=username,
        email=email,
        # A senha em texto morre aqui. O banco so ve o hash.
        password_hash=generate_password_hash(password),
        display_name=display_name,
        role="user",
    )
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(email: str, password: str) -> User:
    """Devolve o usuario das credenciais, ou levanta AuthError."""
    user = db.session.query(User).filter_by(email=email).first()

    # Quando o e-mail nao existe, conferir contra um hash descartavel em
    # vez de sair direto. Verificar hash e lento de proposito; sair antes
    # deixaria a resposta visivelmente mais rapida para e-mail inexistente
    # e daria para descobrir quem tem conta so cronometrando as chamadas.
    hash_alvo = user.password_hash if user else _HASH_DESCARTAVEL
    senha_confere = check_password_hash(hash_alvo, password)

    # Mensagem unica para e-mail errado e senha errada, pelo mesmo motivo:
    # "esse e-mail nao existe" confirma quais e-mails existem.
    if not user or not senha_confere:
        raise AuthError("E-mail ou senha invalidos.", 401)

    if not user.is_active:
        # Regra de negocio, nao de rota: a tela de admin do front tem um
        # botao de ativar/desativar conta, e desativar precisa impedir o
        # login em qualquer caminho que passe por aqui.
        raise AuthError("Esta conta esta desativada.", 403)

    return user
