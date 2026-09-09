"""
Application factory.

Quem for fazer as rotas registra os blueprints aqui dentro, na secao
marcada. Nao criar `app = Flask(__name__)` solto em outro arquivo.
"""

from flask import Flask

from app.config import Config
from app.extensions import cors, db, jwt, migrate


def create_app(config_object: type = Config) -> Flask:
    # O .env ja foi lido no import de app.config — precisa ser antes
    # do corpo da classe Config, nao aqui.
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    # O front roda em localhost:3000 e a API em localhost:5000 — origens
    # diferentes. Sem CORS o navegador bloqueia o login antes da
    # requisicao sair, e o erro que aparece no console nao diz isso.
    cors.init_app(
        app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}}
    )

    # Importar os models DEPOIS do init_app e ANTES de qualquer comando
    # do Alembic. Se um model nao for importado aqui, o `flask db migrate`
    # nao enxerga a tabela e gera uma migration incompleta em silencio.
    from app import models  # noqa: F401

    # Registra os callbacks do JWT: o que vai dentro do token, como o
    # `current_user` e carregado e o formato dos erros 401.
    from app import security  # noqa: F401

    from app.cli import register_cli
    register_cli(app)

    # --- blueprints -------------------------------------------------
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # from app.blueprints.books import bp as books_bp
    # app.register_blueprint(books_bp, url_prefix="/api/books")
    # ----------------------------------------------------------------

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
