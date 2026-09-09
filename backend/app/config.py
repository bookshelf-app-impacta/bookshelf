"""Configuracao da aplicacao, lida do ambiente (.env)."""

import os
from datetime import timedelta

from dotenv import load_dotenv

# Ler o .env AQUI, antes do corpo da classe.
#
# Os `os.environ.get` abaixo rodam uma vez so, no momento em que este
# modulo e importado. Enquanto o load_dotenv() ficava dentro do
# create_app, ele acontecia depois — e nenhum valor do .env chegava a
# tempo: a aplicacao subia inteira nos defaults. Passava despercebido
# porque o default da DATABASE_URL e igual ao do arquivo; ja o
# SECRET_KEY, que assina o token de login, ficava no valor de exemplo.
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

    # Validade do token de login. Oito horas para a sessao nao expirar no
    # meio da gravacao do video da entrega.
    #
    # Nao existe JWT_SECRET_KEY de proposito: quando ela esta ausente, o
    # Flask-JWT-Extended assina com o SECRET_KEY acima. Um segredo so,
    # num lugar so, e um item a menos para alguem esquecer no .env.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # Quem pode chamar a API pelo navegador. O front Next.js roda em
    # :3000 e a API em :5000 — origens diferentes. Sem isso o navegador
    # bloqueia o login antes da requisicao chegar aqui.
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000")
