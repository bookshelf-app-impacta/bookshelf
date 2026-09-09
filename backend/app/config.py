"""Configuracao da aplicacao, lida do ambiente (.env)."""

import os

from dotenv import load_dotenv

# Ler o .env AQUI, antes do corpo da classe.
#
# Os `os.environ.get` abaixo rodam uma vez so, no momento em que este
# modulo e importado. Enquanto o load_dotenv() ficava dentro do
# create_app, ele acontecia depois — e nenhum valor do .env chegava a
# tempo: a aplicacao subia inteira nos defaults. Passava despercebido
# porque o default da DATABASE_URL e igual ao do arquivo.
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
