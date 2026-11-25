"""Testes unitários do schema; não precisam conectar ao MySQL."""
from decimal import Decimal

import pytest
from marshmallow import ValidationError

from app.schemas.review_schema import ReviewCreateSchema, ReviewUpdateSchema


def test_create_review_with_body_only():
    data = ReviewCreateSchema().load({"body": "  Gostei muito do livro.  "})
    assert data["body"] == "Gostei muito do livro."
    assert data["rating"] is None
    assert data["has_spoilers"] is False


def test_create_review_with_rating_only():
    data = ReviewCreateSchema().load({"rating": 4.5})
    assert data["rating"] == Decimal("4.5")
    assert data["body"] is None


def test_create_review_requires_body_or_rating():
    with pytest.raises(ValidationError):
        ReviewCreateSchema().load({})


def test_rating_must_be_half_star_step():
    with pytest.raises(ValidationError):
        ReviewCreateSchema().load({"rating": 4.2})


@pytest.mark.parametrize("rating", [0, 0.4, 5.1, 6])
def test_rating_must_be_between_half_and_five(rating):
    with pytest.raises(ValidationError):
        ReviewCreateSchema().load({"rating": rating})


def test_update_requires_at_least_one_field():
    with pytest.raises(ValidationError):
        ReviewUpdateSchema().load({})


def test_update_converts_spoiler_and_consumed_date():
    data = ReviewUpdateSchema().load({
        "hasSpoilers": True,
        "consumedOn": "2026-10-12",
    })
    assert data["has_spoilers"] is True
    assert data["consumed_on"].isoformat() == "2026-10-12"
