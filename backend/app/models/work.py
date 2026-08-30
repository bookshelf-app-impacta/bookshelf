"""
Catalogo: obras, detalhes de livro, generos e creditos.  [AC1]

Sobre o nome `works` em vez de `books`
--------------------------------------
A tabela guarda uma OBRA, com uma coluna `type`. Hoje so existe
type='book'. Se o grupo confirmar que filmes entram no escopo, basta
criar `movie_details` e liberar type='movie' — nenhuma FK muda, nenhuma
query existente quebra.

Se a alternativa fosse ter `books` e `movies` separadas, `reviews`,
`comments` e `favorites` precisariam de dois FKs opcionais cada, com a
regra "exatamente um preenchido" impossivel de garantir no banco, e toda
consulta viraria UNION. O custo de manter `works` agora e uma coluna
ENUM; o custo de migrar depois seria reescrever quatro tabelas.

Se o grupo decidir que e SO livro, para sempre: renomear para `books`,
remover `type` e apagar este comentario. Decisao esta no docs/BANCO-DE-DADOS.md.
"""

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.base import PK, SMALL_U, TimestampMixin


class Work(TimestampMixin, db.Model):
    __tablename__ = "works"

    id = db.Column(PK, primary_key=True, autoincrement=True)
    type = db.Column(
        Enum("book", "movie", name="work_type"),
        nullable=False, default="book", server_default="book",
    )
    title = db.Column(String(255), nullable=False)
    original_title = db.Column(String(255))
    slug = db.Column(String(280), nullable=False, unique=True)
    release_year = db.Column(SMALL_U)
    synopsis = db.Column(Text)
    cover_url = db.Column(String(500))
    # Quem cadastrou. RESTRICT: nao deixa apagar o usuario e orfanar o acervo.
    created_by = db.Column(
        PK, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    book_details = relationship(
        "BookDetails", back_populates="work",
        uselist=False, cascade="all, delete-orphan",
    )
    reviews = relationship(
        "Review", back_populates="work", cascade="all, delete-orphan"
    )
    genres = relationship(
        "Genre", secondary="work_genres", back_populates="works"
    )

    __table_args__ = (
        Index("idx_works_type_year", "type", "release_year"),
        Index("idx_works_title", "title"),
        CheckConstraint(
            "release_year IS NULL OR release_year BETWEEN 1400 AND 2200",
            name="ck_works_year",
        ),
    )

    def __repr__(self) -> str:
        return f"<Work {self.type}:{self.slug}>"


class BookDetails(db.Model):
    """Campos que so existem para livro.  Relacao 1:1 com works."""

    __tablename__ = "book_details"

    work_id = db.Column(
        PK, ForeignKey("works.id", ondelete="CASCADE"), primary_key=True
    )
    isbn13 = db.Column(String(13), unique=True)
    publisher = db.Column(String(150))
    page_count = db.Column(SMALL_U)
    language = db.Column(String(40))

    work = relationship("Work", back_populates="book_details")


class Genre(db.Model):
    """[AC1 — opcional; pode ficar para AC2]"""

    __tablename__ = "genres"

    id = db.Column(SMALL_U, primary_key=True, autoincrement=True)
    name = db.Column(String(60), nullable=False, unique=True)
    slug = db.Column(String(70), nullable=False, unique=True)

    works = relationship(
        "Work", secondary="work_genres", back_populates="genres"
    )


class WorkGenre(db.Model):
    __tablename__ = "work_genres"

    work_id = db.Column(
        PK, ForeignKey("works.id", ondelete="CASCADE"), primary_key=True
    )
    genre_id = db.Column(
        SMALL_U, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True
    )


class Person(db.Model):
    """Autor, tradutor — e diretor/elenco, se filmes entrarem."""

    __tablename__ = "people"

    id = db.Column(PK, primary_key=True, autoincrement=True)
    name = db.Column(String(150), nullable=False)
    slug = db.Column(String(170), nullable=False, unique=True)

    __table_args__ = (Index("idx_people_name", "name"),)


class WorkCredit(db.Model):
    """Quem fez o que numa obra. PK composta inclui `role`, entao a mesma
    pessoa pode ser autora E tradutora da mesma obra."""

    __tablename__ = "work_credits"

    work_id = db.Column(
        PK, ForeignKey("works.id", ondelete="CASCADE"), primary_key=True
    )
    person_id = db.Column(
        PK, ForeignKey("people.id", ondelete="CASCADE"), primary_key=True
    )
    role = db.Column(
        Enum("author", "translator", "director", "screenwriter", "actor",
             name="credit_role"),
        primary_key=True,
    )
    character_name = db.Column(String(150))
