"""Rotas REST para as avaliações de livros."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError

from app.schemas.review_schema import (
    ReviewCreateSchema,
    ReviewUpdateSchema,
    review_to_dict,
)
from app.services.review_service import (
    DuplicateReviewError,
    ReviewContentError,
    ReviewNotFoundError,
    ReviewPermissionError,
    ReviewService,
)

# Registrado com prefixo /api em create_app(). Isso gera:
# /api/books/<book_id>/reviews e /api/reviews/<review_id>.
bp = Blueprint("reviews", __name__)


def _invalid_body(message, fields=None):
    response = {"error": message}
    if fields:
        response["fields"] = fields
    return jsonify(response), 400


def _service_error(error):
    return jsonify(error=error.message), error.status_code


@bp.post("/books/<int:book_id>/reviews")
@jwt_required()
def create_review(book_id):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _invalid_body("Corpo JSON obrigatorio.")

    try:
        data = ReviewCreateSchema().load(payload)
    except ValidationError as error:
        return _invalid_body("Dados invalidos.", error.messages)

    try:
        review = ReviewService.create_review(book_id, current_user.id, data)
    except (ReviewNotFoundError, DuplicateReviewError, ReviewContentError) as error:
        return _service_error(error)

    return jsonify(review_to_dict(review)), 201


@bp.get("/books/<int:book_id>/reviews")
def list_reviews(book_id):
    try:
        reviews = ReviewService.list_reviews(book_id)
    except ReviewNotFoundError as error:
        return _service_error(error)

    return jsonify([review_to_dict(review) for review in reviews]), 200


@bp.put("/reviews/<int:review_id>")
@jwt_required()
def update_review(review_id):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _invalid_body("Corpo JSON obrigatorio.")

    try:
        data = ReviewUpdateSchema().load(payload)
    except ValidationError as error:
        return _invalid_body("Dados invalidos.", error.messages)

    try:
        review = ReviewService.update_review(review_id, current_user.id, data)
    except (ReviewNotFoundError, ReviewPermissionError, ReviewContentError) as error:
        return _service_error(error)

    return jsonify(review_to_dict(review)), 200


@bp.delete("/reviews/<int:review_id>")
@jwt_required()
def delete_review(review_id):
    try:
        ReviewService.delete_review(review_id, current_user.id)
    except (ReviewNotFoundError, ReviewPermissionError) as error:
        return _service_error(error)

    return "", 204
