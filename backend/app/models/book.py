"""
Catalogo: livros, autores e generos.  [AC1]

Escopo definido pelo grupo na revisao do PR: o projeto e SO DE LIVROS.
Por isso nao existe tabela `works` nem `book_details` — tudo que descreve
o livro fica em `books`, como colunas.

Se um dia entrar filme, a conta muda: seria preciso criar `movies` e dar
a `reviews`, `favorites` e `comments` uma forma de apontar para os dois
tipos. Nao e o escopo hoje, e resolver antes da hora custaria mais do que
resolveria.
"""

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.base import PK, SMALL_U, TimestampMixin


class Author(db.Model):
    """Autor. Tabela propria em vez de texto solto em `books` para o nome
    nao ser digitado de tres jeitos diferentes e quebrar a busca."""

    __tablename__ = "authors"

    id = db.Column(PK, primary_key=True, autoincrement=True)
    name = db.Column(String(150), nullable=False)
    slug = db.Column(String(170), nullable=False, unique=True)

    books = relationship("Book", back_populates="author")

    __table_args__ = (Index("idx_authors_name", "name"),)

    def __repr__(self) -> str:
        return f"<Author {self.name}>"


class Genre(db.Model):
    """Lista fixa de generos. Mesma logica do autor: evita 'Ficcao
    Cientifica', 'ficcao cientifica' e 'Sci-Fi' virarem tres generos."""

    __tablename__ = "genres"

    id = db.Column(SMALL_U, primary_key=True, autoincrement=True)
    name = db.Column(String(60), nullable=False, unique=True)
    slug = db.Column(String(70), nullable=False, unique=True)

    books = relationship("Book", back_populates="genre")


class Book(TimestampMixin, db.Model):
    __tablename__ = "books"

    id = db.Column(PK, primary_key=True, autoincrement=True)
    title = db.Column(String(255), nullable=False)
    original_title = db.Column(String(255))
    slug = db.Column(String(280), nullable=False, unique=True)
    release_year = db.Column(SMALL_U)
    synopsis = db.Column(Text)
    cover_url = db.Column(String(500))

    # Detalhes do livro — antes ficavam em `book_details`.
    isbn13 = db.Column(String(13), unique=True)
    publisher = db.Column(String(150))
    page_count = db.Column(SMALL_U)
    language = db.Column(String(40))

    # Um autor e um genero por livro.
    # SET NULL, nao CASCADE: apagar um autor nao pode apagar os livros dele.
    # Sao anulaveis para o cadastro poder ser feito em duas etapas — cria o
    # livro, escolhe o autor depois — sem travar o formulario da AC1.
    author_id = db.Column(
        PK, ForeignKey("authors.id", ondelete="SET NULL"), nullable=True
    )
    genre_id = db.Column(
        SMALL_U, ForeignKey("genres.id", ondelete="SET NULL"), nullable=True
    )

    # Quem cadastrou. RESTRICT: nao deixa apagar o usuario e orfanar o acervo.
    created_by = db.Column(
        PK, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    reviews = relationship(
        "Review", back_populates="book", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_books_title", "title"),
        Index("idx_books_year", "release_year"),
        CheckConstraint(
            "release_year IS NULL OR release_year BETWEEN 1400 AND 2200",
            name="ck_books_year",
        ),
    )

    def __repr__(self) -> str:
        return f"<Book {self.slug}>"
