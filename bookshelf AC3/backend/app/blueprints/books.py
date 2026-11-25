from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app.schemas.book import BookCreateSchema, BookUpdateSchema
from app.security import admin_required
from app.services.book_service import BookService

bp = Blueprint("books", __name__)


def _validation_error(error):
    return jsonify(error="Dados invalidos.", fields=error.messages), 400


@bp.get("")
def get_books():
    return jsonify([book.to_dict() for book in BookService.get_all_books()])


@bp.get("/<int:book_id>")
def get_book(book_id):
    book = BookService.get_book_by_id(book_id)
    if not book:
        return jsonify(error="Livro nao encontrado."), 404
    return jsonify(book.to_dict())


@bp.post("")
@admin_required
def create_book():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Corpo JSON obrigatorio."), 400

    try:
        data = BookCreateSchema().load(payload)
    except ValidationError as exc:
        return _validation_error(exc)

    # Slug automatico quando nao informado.
    if not data.get("slug"):
        data["slug"] = BookService.make_unique_slug(data["title"])

    if data.get("isbn13") and BookService.get_book_by_isbn(data["isbn13"]):
        return jsonify(error="ISBN13 ja cadastrado."), 409
    if BookService.get_book_by_slug(data["slug"]):
        return jsonify(error="Slug ja cadastrado."), 409

    try:
        book = BookService.create_book(data, current_user.id)
    except IntegrityError:
        return jsonify(error="Nao foi possivel cadastrar o livro com os dados informados."), 409
    return jsonify(book.to_dict()), 201


@bp.put("/<int:book_id>")
@admin_required
def update_book(book_id):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Corpo JSON obrigatorio."), 400

    try:
        data = BookUpdateSchema().load(payload)
    except ValidationError as exc:
        return _validation_error(exc)

    book = BookService.get_book_by_id(book_id)
    if not book:
        return jsonify(error="Livro nao encontrado."), 404

    if "isbn13" in data and data["isbn13"]:
        existing = BookService.get_book_by_isbn(data["isbn13"])
        if existing and existing.id != book_id:
            return jsonify(error="ISBN13 ja cadastrado."), 409

    if "slug" in data and data["slug"]:
        existing = BookService.get_book_by_slug(data["slug"])
        if existing and existing.id != book_id:
            return jsonify(error="Slug ja cadastrado."), 409

    try:
        updated = BookService.update_book(book_id, data)
    except IntegrityError:
        return jsonify(error="Nao foi possivel atualizar o livro com os dados informados."), 409

    return jsonify(updated.to_dict()), 200


@bp.delete("/<int:book_id>")
@admin_required
def delete_book(book_id):
    if not BookService.delete_book(book_id):
        return jsonify(error="Livro nao encontrado."), 404
    return "", 204
