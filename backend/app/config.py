"""Configuracao da aplicacao, lida do ambiente (.env)."""

import os


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
