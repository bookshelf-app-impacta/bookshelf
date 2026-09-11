"""
Rotas de livros. So orquestra: chama o service, formata com o schema,
devolve a resposta HTTP.
"""

from flask import Blueprint, jsonify

from app.schemas.book_schema import book_to_dict, books_to_dict_list
from app.services.book_service import get_all_books, get_book_by_id

bp = Blueprint("books", __name__)


@bp.get("/")
def list_books():
    books = get_all_books()
    return jsonify(books_to_dict_list(books)), 200


@bp.get("/<int:book_id>")
def get_book(book_id: int):
    book = get_book_by_id(book_id)
    if book is None:
        return jsonify({"error": "Livro nao encontrado"}), 404
    return jsonify(book_to_dict(book)), 200