"""
Schema de entrada da Review. Valida o body da requisicao ANTES de
tentar gravar no banco, espelhando as regras que ja existem como
CheckConstraint em app/models/review.py:

  - ck_reviews_rating:         nota entre 0.5 e 5.0, em passos de 0.5
  - ck_reviews_nota_ou_texto:  rating OU body precisa vir preenchido

A unicidade (1 review por usuario por livro) NAO e checada aqui --
isso exige consultar o banco, entao fica por conta do service.
"""

from decimal import Decimal, InvalidOperation

NOTAS_VALIDAS = {Decimal(str(n / 2)) for n in range(1, 11)}  # 0.5 .. 5.0


def validate_review_payload(payload: dict) -> tuple[dict, dict]:
    """
    Recebe o JSON cru da requisicao. Devolve (errors, data).

    - Se errors estiver vazio, data tem os campos ja limpos e prontos
      pra virar um Review(**data).
    - Se errors tiver algo, data deve ser ignorado.
    """
    errors: dict[str, str] = {}
    data: dict = {}

    # --- rating ------------------------------------------------------
    rating_raw = payload.get("rating")

    if rating_raw is not None:
        try:
            rating = Decimal(str(rating_raw))
        except (InvalidOperation, ValueError):
            errors["rating"] = "Nota invalida."
        else:
            if rating not in NOTAS_VALIDAS:
                errors["rating"] = "Nota deve ser entre 0.5 e 5.0, em passos de 0.5."
            else:
                data["rating"] = rating
    else:
        data["rating"] = None

    # --- body (texto da avaliacao) -----------------------------------
    body_raw = payload.get("body")

    if body_raw is not None:
        body = str(body_raw).strip()
        data["body"] = body if body else None
    else:
        data["body"] = None

    # --- regra cruzada: precisa de pelo menos um dos dois ------------
    if not errors.get("rating") and data.get("rating") is None and not data.get("body"):
        errors["_geral"] = "Envie uma nota, um comentario, ou os dois."

    # --- has_spoilers (opcional, default False) -----------------------
    has_spoilers = payload.get("has_spoilers", False)
    if not isinstance(has_spoilers, bool):
        errors["has_spoilers"] = "has_spoilers deve ser true ou false."
    else:
        data["has_spoilers"] = has_spoilers

    # --- consumed_on (opcional) ----------------------------------------
    consumed_on_raw = payload.get("consumed_on")
    if consumed_on_raw is not None:
        from datetime import date
        try:
            data["consumed_on"] = date.fromisoformat(consumed_on_raw)
        except (TypeError, ValueError):
            errors["consumed_on"] = "Data invalida, use o formato AAAA-MM-DD."
    else:
        data["consumed_on"] = None

    return errors, data