"""
Rotas de livros. So orquestra: chama o service, formata com o schema,
devolve a resposta HTTP.

Listar e buscar por id sao publicos (qualquer um navega o catalogo).
Criar, editar e apagar exigem admin — e a decisao 0.1 do grupo
(docs/BANCO-DE-DADOS.md): so o administrador cadastra livro.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user

from app.schemas.book_schema import (
    book_to_dict,
    books_to_dict_list,
    validate_book_create,
    validate_book_update,
)
from app.security import admin_required
from app.services.book_service import (
    BookError,
    create_book,
    delete_book,
    get_all_books,
    get_book_by_id,
    update_book,
)

bp = Blueprint("books", __name__)


@bp.errorhandler(BookError)
def _handle_book_error(error: BookError):
    return jsonify(error=error.message), error.status


def _invalid_data(errors: dict):
    return jsonify(error="Dados invalidos.", fields=errors), 400


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


@bp.post("/")
@admin_required
def create_book_route():
    data, errors = validate_book_create(request.get_json(silent=True))
    if errors:
        return _invalid_data(errors)

    book = create_book(data, created_by=current_user.id)
    return jsonify(book_to_dict(book)), 201


@bp.put("/<int:book_id>")
@admin_required
def update_book_route(book_id: int):
    data, errors = validate_book_update(request.get_json(silent=True))
    if errors:
        return _invalid_data(errors)

    book = update_book(book_id, data)
    return jsonify(book_to_dict(book)), 200


@bp.delete("/<int:book_id>")
@admin_required
def delete_book_route(book_id: int):
    delete_book(book_id)
    return "", 204
