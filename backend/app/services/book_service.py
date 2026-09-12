"""
Logica de busca de livros no banco.
"""

from app.models.book import Book


def get_all_books():
    return Book.query.order_by(Book.title.asc()).all()


def get_book_by_id(book_id: int):
    return Book.query.get(book_id)