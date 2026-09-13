"""Cria as tabelas do ambiente local e popula usuarios de desenvolvimento.

Uso:
    python init_db.py
"""
from app import create_app, db
from app.cli import register_cli

app = create_app()

with app.app_context():
    db.create_all()
    print("Tabelas criadas/verificadas.")
    # O comando seed é registrado no factory; execute-o via Flask CLI quando quiser.
