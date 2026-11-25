"""Validacao de entrada e serializacao das avaliacoes de livros."""
from decimal import Decimal

from marshmallow import Schema, ValidationError, fields, pre_load, validate, validates_schema


MAX_REVIEW_BODY_LENGTH = 5000


def _half_star_steps(value):
    """Aceita notas em incrementos de 0,5 (ex.: 3.5)."""
    if value is None:
        return
    if (value * 2) != (value * 2).to_integral_value():
        raise ValidationError("A nota deve usar incrementos de 0,5 estrela.")


class _ReviewBaseSchema(Schema):
    body = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=MAX_REVIEW_BODY_LENGTH),
    )
    rating = fields.Decimal(
        required=False,
        allow_none=True,
        as_string=False,
        places=1,
        validate=[
            validate.Range(
                min=Decimal("0.5"),
                max=Decimal("5.0"),
                error="A nota deve estar entre 0,5 e 5,0.",
            ),
            _half_star_steps,
        ],
    )
    has_spoilers = fields.Boolean(data_key="hasSpoilers", required=False)
    consumed_on = fields.Date(data_key="consumedOn", required=False, allow_none=True)

    @pre_load
    def normalize_body(self, payload, **kwargs):
        # Texto em branco é normalizado para null. A regra de negócio
        # depois garante que exista texto ou nota na avaliação final.
        if not isinstance(payload, dict):
            return payload
        data = dict(payload)
        if isinstance(data.get("body"), str):
            data["body"] = data["body"].strip() or None
        return data


class ReviewCreateSchema(_ReviewBaseSchema):
    """Valida um novo comentário/avaliação."""
    has_spoilers = fields.Boolean(data_key="hasSpoilers", required=False, load_default=False)

    @validates_schema
    def require_body_or_rating(self, data, **kwargs):
        if not data.get("body") and data.get("rating") is None:
            raise ValidationError(
                "Informe um comentário (body), uma nota (rating) ou ambos.",
                field_name="body",
            )


class ReviewUpdateSchema(_ReviewBaseSchema):
    """Valida os campos que o autor pode atualizar na sua avaliação."""

    @validates_schema
    def require_at_least_one_field(self, data, **kwargs):
        if not data:
            raise ValidationError("Informe pelo menos um campo para atualizar.")


def review_to_dict(review):
    """Converte a entidade Review para JSON sem expor dados privados do usuário."""
    user = review.user
    return {
        "id": review.id,
        "bookId": review.book_id,
        "userId": review.user_id,
        "body": review.body,
        "rating": float(review.rating) if review.rating is not None else None,
        "hasSpoilers": bool(review.has_spoilers),
        "consumedOn": review.consumed_on.isoformat() if review.consumed_on else None,
        "createdAt": review.created_at.isoformat() if review.created_at else None,
        "updatedAt": review.updated_at.isoformat() if review.updated_at else None,
        "user": {
            "id": user.id,
            "username": user.username,
            "displayName": user.display_name,
            "avatarUrl": user.avatar_url,
        } if user else None,
    }
