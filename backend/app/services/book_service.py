"""
Logica de busca, criacao, edicao e remocao de livros.
"""

import re
import unicodedata

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.book import Author, Book, Genre


class BookError(Exception):
    """Erro de negocio que o blueprint traduz em status HTTP."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status


def get_all_books():
    return Book.query.order_by(Book.title.asc()).all()


def get_book_by_id(book_id: int):
    return Book.query.get(book_id)


def _slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "livro"


def _unique_slug(title: str, release_year) -> str:
    base = _slugify(title)
    if release_year:
        base = f"{base}-{release_year}"

    slug = base
    suffix = 2
    while db.session.query(Book).filter_by(slug=slug).first() is not None:
        slug = f"{base}-{suffix}"
        suffix += 1
    return slug


def _check_author_and_genre(data: dict) -> None:
    author_id = data.get("author_id")
    if author_id is not None and db.session.get(Author, author_id) is None:
        raise BookError("Autor nao encontrado.", 404)

    genre_id = data.get("genre_id")
    if genre_id is not None and db.session.get(Genre, genre_id) is None:
        raise BookError("Genero nao encontrado.", 404)


def _check_isbn_unique(isbn13, *, ignore_book_id: int = None) -> None:
    if not isbn13:
        return
    existing = db.session.query(Book).filter_by(isbn13=isbn13).first()
    if existing and existing.id != ignore_book_id:
        raise BookError("Este ISBN ja esta cadastrado.", 409)


def create_book(data: dict, created_by: int) -> Book:
    _check_author_and_genre(data)
    _check_isbn_unique(data.get("isbn13"))

    book = Book(
        **data,
        slug=_unique_slug(data["title"], data.get("release_year")),
        created_by=created_by,
    )
    db.session.add(book)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise BookError("Este ISBN ja esta cadastrado.", 409)
    return book


def update_book(book_id: int, data: dict) -> Book:
    """`data` so contem os campos que vieram no corpo da requisicao
    (ver `validate_book_update`) — os demais ficam como estavam. O
    slug nao e recalculado aqui: mudar o titulo nao deve trocar a URL
    do livro por baixo de quem ja tem o link salvo."""
    book = get_book_by_id(book_id)
    if book is None:
        raise BookError("Livro nao encontrado.", 404)

    _check_author_and_genre(data)
    if "isbn13" in data:
        _check_isbn_unique(data["isbn13"], ignore_book_id=book.id)

    for field, value in data.items():
        setattr(book, field, value)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise BookError("Este ISBN ja esta cadastrado.", 409)
    return book


def delete_book(book_id: int) -> None:
    book = get_book_by_id(book_id)
    if book is None:
        raise BookError("Livro nao encontrado.", 404)

    db.session.delete(book)
    db.session.commit()
