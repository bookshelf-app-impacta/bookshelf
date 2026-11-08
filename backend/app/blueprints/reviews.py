"""
Rotas de avaliacoes (comentarios) de livros. So orquestra: chama o
service, formata com o schema, devolve a resposta HTTP.

Listar e publico (qualquer um le os comentarios de um livro). Criar
exige login — qualquer usuario, nao so admin.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required

from app.schemas.review_schema import (
    review_to_json,
    reviews_to_json_list,
    validate_review_payload,
)
from app.services.review_service import ReviewError, create_review, list_reviews

bp = Blueprint("reviews", __name__)


@bp.errorhandler(ReviewError)
def _handle_review_error(error: ReviewError):
    return jsonify(error=error.message), error.status


def _invalid_data(errors: dict):
    return jsonify(error="Dados invalidos.", fields=errors), 400


@bp.get("/books/<int:book_id>/reviews/")
def list_reviews_route(book_id: int):
    return jsonify(reviews_to_json_list(list_reviews(book_id))), 200


@bp.post("/books/<int:book_id>/reviews/")
@jwt_required()
def create_review_route(book_id: int):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}

    errors, data = validate_review_payload(payload)
    if errors:
        return _invalid_data(errors)

    review = create_review(book_id, user_id=current_user.id, data=data)
    return jsonify(review_to_json(review)), 201
