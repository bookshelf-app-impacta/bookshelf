import click
from flask import Flask
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import User


def register_cli(app: Flask):
    @app.cli.command("seed")
    @click.option("--reset", is_flag=True)
    def seed(reset):
        """Cria usuarios administrativos/de desenvolvimento."""
        if reset:
            db.session.query(User).delete()
            db.session.commit()

        users = [
            ("admin", "admin@bookshelf.local", "admin123", "admin"),
            ("ana", "ana@bookshelf.local", "user123", "user"),
            ("bruno", "bruno@bookshelf.local", "user123", "user"),
        ]
        for username, email, password, role in users:
            if not User.query.filter_by(email=email).first():
                db.session.add(User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password),
                    display_name=username.title(),
                    role=role,
                ))
        db.session.commit()
        click.echo("Seed concluido.")
