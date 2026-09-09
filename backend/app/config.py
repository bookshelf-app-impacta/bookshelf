"""Configuracao da aplicacao, lida do ambiente (.env)."""

import os
from datetime import timedelta

from dotenv import load_dotenv

# Antes do corpo da classe: os os.environ.get abaixo rodam no import, e
# um load_dotenv() la no create_app chegaria tarde demais.
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-nao-usar-em-producao")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://bookshelf:bookshelf@127.0.0.1:3306/bookshelf"
        "?charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # pool_pre_ping evita o classico "MySQL server has gone away" depois
    # que a conexao fica ociosa durante o desenvolvimento.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    JSON_SORT_KEYS = False

    # Sem JWT_SECRET_KEY o Flask-JWT-Extended assina com o SECRET_KEY
    # acima — um segredo so, num lugar so.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # O front roda em :3000 e a API em :5000. Sem CORS o navegador
    # bloqueia o login antes da requisicao sair.
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000")
