"""
Autenticacao: quem esta logado e quem pode o que.

Este modulo fica na raiz de `app/` de proposito. Um decorador de permissao
nao e rota (blueprints/), nem regra de negocio (services/), nem mapeamento
de tabela (models/), nem serializacao (schemas/) — nao caberia bem em
nenhuma das quatro pastas.

E o que as outras frentes do projeto importam:

    from flask_jwt_extended import current_user
    from app.security import admin_required

    @bp.post("")
    @admin_required
    def criar_livro():
        livro = Book(..., created_by=current_user.id)

`current_user` ja e o objeto User do banco, nao o id — quem registra isso
e o `user_lookup_loader` abaixo. Ninguem precisa consultar a tabela de
usuarios na mao.
"""

from functools import wraps

from flask import jsonify
from flask_jwt_extended import current_user, verify_jwt_in_request

from app.extensions import db, jwt
from app.models import User


@jwt.user_identity_loader
def _identidade(user: User) -> str:
    """O que vai dentro do token para identificar o usuario.

    String, nao int: a RFC 7519 define o campo `sub` como string, e o
    Flask-JWT-Extended 4.7 passou a recusar o token quando nao e.
    Converter aqui deixa o codigo pronto para a atualizacao.
    """
    return str(user.id)


@jwt.user_lookup_loader
def _carrega_usuario(_cabecalho, dados_do_token):
    """Roda a cada requisicao autenticada e alimenta o `current_user`."""
    return db.session.get(User, int(dados_do_token["sub"]))


def admin_required(fn):
    """Exige token valido E papel de admin.

    Sem token: 401. Com token de usuario comum: 403. Sao coisas
    diferentes — 401 e "nao sei quem voce e", 403 e "sei quem voce e e
    voce nao pode". O front trata os dois casos de forma diferente:
    o 401 manda para a tela de login, o 403 nao.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if not current_user.is_admin:
            return jsonify(error="Acesso restrito a administradores."), 403
        return fn(*args, **kwargs)

    return wrapper


# --- respostas de erro do JWT -------------------------------------------
#
# Sem estes handlers o Flask-JWT-Extended devolve mensagens em ingles e,
# em alguns casos, HTML. O `response.json()` do frontend estoura quando
# recebe HTML, e o erro que aparece na tela nao tem nada a ver com a causa.
# Aqui todos saem no mesmo formato das rotas: {"error": "mensagem"}.


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
    # Token valido de um usuario que foi apagado do banco depois.
    return jsonify(error="Usuario do token nao existe mais."), 401
