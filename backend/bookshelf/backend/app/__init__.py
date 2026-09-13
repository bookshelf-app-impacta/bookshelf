"""Application factory do Book Shelf."""
from flask import Flask

from app.config import Config
from app.extensions import cors, db, jwt, migrate


def create_app(config_object: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
    )

    # Registra todos os models antes do Alembic examinar o metadata.
    from app import models  # noqa: F401
    from app import security  # noqa: F401

    from app.cli import register_cli
    register_cli(app)

    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.blueprints.books import bp as books_bp
    app.register_blueprint(books_bp, url_prefix="/api/books")

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
