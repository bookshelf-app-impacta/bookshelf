"""
Comandos de linha de comando do projeto.

Uso:
    flask seed        # popula dados de desenvolvimento
    flask seed --reset  # apaga os dados antes (NAO apaga as tabelas)
"""

from datetime import date
from decimal import Decimal

import click
from flask import Flask
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import (
    BookDetails, Comment, Favorite, Genre, Person, Review, User, Work,
    WorkCredit, WorkGenre,
)

GENEROS = [
    ("Ficção Científica", "ficcao-cientifica"),
    ("Fantasia", "fantasia"),
    ("Drama", "drama"),
    ("Suspense", "suspense"),
    ("Terror", "terror"),
    ("Romance", "romance"),
    ("Aventura", "aventura"),
    ("Biografia", "biografia"),
    ("História", "historia"),
    ("Técnico", "tecnico"),
]

LIVROS = [
    dict(slug="duna-1965", title="Duna", original_title="Dune",
         release_year=1965, autor="Frank Herbert", genero="ficcao-cientifica",
         isbn13="9788576570000", publisher="Aleph", pages=680,
         synopsis="Em um planeta desértico, uma família nobre disputa o "
                  "controle da especiaria mais valiosa do universo."),
    dict(slug="o-conto-da-aia-1985", title="O Conto da Aia",
         original_title="The Handmaid's Tale", release_year=1985,
         autor="Margaret Atwood", genero="ficcao-cientifica",
         isbn13="9788528618677", publisher="Rocco", pages=368,
         synopsis="Num regime totalitário, mulheres férteis são reduzidas à "
                  "função de gerar filhos para a elite."),
    dict(slug="torto-arado-2019", title="Torto Arado", original_title=None,
         release_year=2019, autor="Itamar Vieira Junior", genero="drama",
         isbn13="9788542215984", publisher="Todavia", pages=264,
         synopsis="Duas irmãs crescem numa comunidade de trabalhadores "
                  "rurais no sertão da Bahia."),
]


def _get_or_create(model, defaults=None, **filtros):
    obj = db.session.query(model).filter_by(**filtros).one_or_none()
    if obj:
        return obj, False
    obj = model(**filtros, **(defaults or {}))
    db.session.add(obj)
    db.session.flush()
    return obj, True


def _seed() -> None:
    for nome, slug in GENEROS:
        _get_or_create(Genre, name=nome, slug=slug)

    admin, _ = _get_or_create(
        User, email="admin@bookshelf.local",
        defaults=dict(
            username="admin", display_name="Administrador",
            password_hash=generate_password_hash("admin123"), role="admin",
        ),
    )
    ana, _ = _get_or_create(
        User, email="ana@bookshelf.local",
        defaults=dict(
            username="ana", display_name="Ana",
            password_hash=generate_password_hash("user123"), role="user",
        ),
    )
    bruno, _ = _get_or_create(
        User, email="bruno@bookshelf.local",
        defaults=dict(
            username="bruno", display_name="Bruno",
            password_hash=generate_password_hash("user123"), role="user",
        ),
    )

    obras = {}
    for item in LIVROS:
        obra, novo = _get_or_create(
            Work, slug=item["slug"],
            defaults=dict(
                type="book", title=item["title"],
                original_title=item["original_title"],
                release_year=item["release_year"],
                synopsis=item["synopsis"], created_by=admin.id,
            ),
        )
        obras[item["slug"]] = obra
        if novo:
            db.session.add(BookDetails(
                work_id=obra.id, isbn13=item["isbn13"],
                publisher=item["publisher"], page_count=item["pages"],
                language="Português",
            ))
            autor_slug = item["autor"].lower().replace(" ", "-")
            pessoa, _ = _get_or_create(
                Person, slug=autor_slug, defaults=dict(name=item["autor"])
            )
            db.session.add(WorkCredit(
                work_id=obra.id, person_id=pessoa.id, role="author"
            ))
            genero = db.session.query(Genre).filter_by(
                slug=item["genero"]
            ).one()
            db.session.add(WorkGenre(work_id=obra.id, genre_id=genero.id))

    db.session.flush()

    r1, novo = _get_or_create(
        Review, user_id=ana.id, work_id=obras["duna-1965"].id,
        defaults=dict(
            rating=Decimal("4.5"),
            body="Começo lento, mas a construção de mundo compensa tudo.",
            consumed_on=date(2026, 3, 12),
        ),
    )
    if novo:
        db.session.add(Comment(
            review_id=r1.id, user_id=bruno.id,
            body="Concordo. Os apêndices no final valem a leitura.",
        ))

    _get_or_create(
        Review, user_id=bruno.id, work_id=obras["torto-arado-2019"].id,
        defaults=dict(
            rating=Decimal("5.0"),
            body="A troca de narradora no meio do livro muda tudo.",
            consumed_on=date(2026, 5, 2),
        ),
    )
    # Avaliacao so com texto, sem nota — o caso que a AC2 precisa suportar.
    _get_or_create(
        Review, user_id=ana.id, work_id=obras["o-conto-da-aia-1985"].id,
        defaults=dict(body="Ainda estou lendo, mas já recomendo."),
    )

    _get_or_create(Favorite, user_id=ana.id, work_id=obras["duna-1965"].id)

    db.session.commit()


def register_cli(app: Flask) -> None:
    @app.cli.command("seed")
    @click.option("--reset", is_flag=True,
                  help="Apaga os dados existentes antes de popular.")
    def seed(reset: bool) -> None:
        """Popula o banco com dados de desenvolvimento."""
        if reset:
            # Ordem inversa das dependencias para os FKs nao reclamarem.
            for model in (Favorite, Comment, Review, WorkGenre, WorkCredit,
                          BookDetails, Work, Genre, Person, User):
                db.session.query(model).delete()
            db.session.commit()
            click.echo("Dados anteriores removidos.")

        _seed()
        click.echo("Seed concluido.")
        click.echo("  admin@bookshelf.local / admin123  (admin)")
        click.echo("  ana@bookshelf.local   / user123")
        click.echo("  bruno@bookshelf.local / user123")
