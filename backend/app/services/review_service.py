"""
Logica de listagem e criacao de avaliacoes (comentario e/ou nota) de
um livro.
"""

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.book import Book
from app.models.review import Review


class ReviewError(Exception):
    """Erro de negocio que o blueprint traduz em status HTTP."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status


def _get_book_or_404(book_id: int) -> Book:
    book = db.session.get(Book, book_id)
    if book is None:
        raise ReviewError("Livro nao encontrado.", 404)
    return book


def list_reviews(book_id: int):
    _get_book_or_404(book_id)
    return (
        Review.query.filter_by(book_id=book_id)
        .order_by(Review.created_at.desc(), Review.id.desc())
        .all()
    )


def create_review(book_id: int, user_id: int, data: dict) -> Review:
    """1 avaliacao por usuario por livro (uq_reviews_user_book). A
    checagem antes do insert da a mensagem amigavel; o IntegrityError
    cobre duas requisicoes simultaneas passando pela checagem juntas."""
    _get_book_or_404(book_id)

    existing = Review.query.filter_by(book_id=book_id, user_id=user_id).first()
    if existing is not None:
        raise ReviewError("Voce ja avaliou este livro.", 409)

    review = Review(**data, book_id=book_id, user_id=user_id)
    db.session.add(review)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ReviewError("Voce ja avaliou este livro.", 409)
    return review
