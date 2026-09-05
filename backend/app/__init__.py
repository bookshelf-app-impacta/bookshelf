"""
Application factory.

Quem for fazer as rotas registra os blueprints aqui dentro, na secao
marcada. Nao criar `app = Flask(__name__)` solto em outro arquivo.
"""

from dotenv import load_dotenv
from flask import Flask

from app.config import Config
from app.extensions import db, migrate


def create_app(config_object: type = Config) -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    # Importar os models DEPOIS do init_app e ANTES de qualquer comando
    # do Alembic. Se um model nao for importado aqui, o `flask db migrate`
    # nao enxerga a tabela e gera uma migration incompleta em silencio.
    from app import models  # noqa: F401

    from app.cli import register_cli
    register_cli(app)

    # --- blueprints -------------------------------------------------
    # from app.blueprints.books import bp as books_bp
    # app.register_blueprint(books_bp, url_prefix="/api/books")
    # ----------------------------------------------------------------

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
