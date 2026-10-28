# tests/test_review.py
from decimal import Decimal

from app.schemas.review_schema import validate_review_payload


def test_rating_valido_passa():
    errors, data = validate_review_payload({"rating": 4.5})

    assert errors == {}
    assert data["rating"] == Decimal("4.5")


def test_rating_fora_do_passo_de_meio_falha():
    errors, _ = validate_review_payload({"rating": 4.3})

    assert "rating" in errors


def test_sem_rating_e_sem_body_falha():
    errors, _ = validate_review_payload({})

    assert "_geral" in errors


def test_so_body_passa():
    errors, data = validate_review_payload({"body": "Muito bom!"})

    assert errors == {}
    assert data["rating"] is None
    assert data["body"] == "Muito bom!"
    
def test_rating_zero_falha():
    errors, _ = validate_review_payload({"rating": 0})

    assert "rating" in errors


def test_rating_negativo_falha():
    errors, _ = validate_review_payload({"rating": -1.5})

    assert "rating" in errors


def test_rating_texto_invalido_falha():
    errors, _ = validate_review_payload({"rating": "abc"})

    assert "rating" in errors


def test_rating_acima_do_maximo_falha():
    errors, _ = validate_review_payload({"rating": 5.5})

    assert "rating" in errors


def test_rating_e_body_juntos_passa():
    errors, data = validate_review_payload({"rating": 3.0, "body": "Ok"})

    assert errors == {}
    assert data["rating"] == Decimal("3.0")
    assert data["body"] == "Ok"