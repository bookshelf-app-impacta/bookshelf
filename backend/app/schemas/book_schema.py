"""
Validacao de entrada e serializacao de saida do Book.

As chaves aqui sao snake_case de proposito, espelhando exatamente os
nomes de coluna do model e o que `book_to_dict` ja devolve — criar uma
segunda convencao (camelCase) so pra entrada confundiria mais do que
ajudaria, já que front e back leem o mesmo nome dos dois lados.
"""

TITLE_MAX = 255
ORIGINAL_TITLE_MAX = 255
COVER_URL_MAX = 500
PUBLISHER_MAX = 150
LANGUAGE_MAX = 40
ISBN13_LEN = 13
YEAR_MIN = 1400  # mesmo intervalo do ck_books_year no banco
YEAR_MAX = 2200


def _text(payload: dict, key: str) -> str:
    value = payload.get(key)
    return value.strip() if isinstance(value, str) else ""


def _optional_int(payload: dict, key: str) -> tuple:
    """Retorna (valor, valido). Ausente ou string vazia conta como
    None valido — sao os dois jeitos de "nao informei esse campo"."""
    if payload.get(key) in (None, ""):
        return None, True
    try:
        return int(payload[key]), True
    except (TypeError, ValueError):
        return None, False


def _validate(payload: dict, *, partial: bool) -> tuple:
    """Motor unico para criar e editar.

    Em criacao (partial=False) todo campo e validado, mesmo ausente.
    Em edicao (partial=True) so entra no `data` (e so e validado) o
    campo que vier no corpo da requisicao — os demais nao sao tocados
    pelo service, em vez de serem sobrescritos com None.
    """
    errors = {}
    data = {}

    if "title" in payload or not partial:
        title = _text(payload, "title")
        if not title or len(title) > TITLE_MAX:
            errors["title"] = f"Obrigatorio, no maximo {TITLE_MAX} caracteres."
        data["title"] = title

    if "original_title" in payload or not partial:
        original_title = _text(payload, "original_title") or None
        if original_title and len(original_title) > ORIGINAL_TITLE_MAX:
            errors["original_title"] = f"No maximo {ORIGINAL_TITLE_MAX} caracteres."
        data["original_title"] = original_title

    if "synopsis" in payload or not partial:
        data["synopsis"] = _text(payload, "synopsis") or None

    if "cover_url" in payload or not partial:
        cover_url = _text(payload, "cover_url") or None
        if cover_url and len(cover_url) > COVER_URL_MAX:
            errors["cover_url"] = f"No maximo {COVER_URL_MAX} caracteres."
        data["cover_url"] = cover_url

    if "isbn13" in payload or not partial:
        isbn13 = _text(payload, "isbn13") or None
        if isbn13 and (not isbn13.isdigit() or len(isbn13) != ISBN13_LEN):
            errors["isbn13"] = f"Deve ter {ISBN13_LEN} digitos numericos."
        data["isbn13"] = isbn13

    if "publisher" in payload or not partial:
        publisher = _text(payload, "publisher") or None
        if publisher and len(publisher) > PUBLISHER_MAX:
            errors["publisher"] = f"No maximo {PUBLISHER_MAX} caracteres."
        data["publisher"] = publisher

    if "language" in payload or not partial:
        language = _text(payload, "language") or None
        if language and len(language) > LANGUAGE_MAX:
            errors["language"] = f"No maximo {LANGUAGE_MAX} caracteres."
        data["language"] = language

    if "release_year" in payload or not partial:
        release_year, ok = _optional_int(payload, "release_year")
        if not ok:
            errors["release_year"] = "Deve ser um numero."
        elif release_year is not None and not (YEAR_MIN <= release_year <= YEAR_MAX):
            errors["release_year"] = f"Deve estar entre {YEAR_MIN} e {YEAR_MAX}."
        data["release_year"] = release_year

    if "page_count" in payload or not partial:
        page_count, ok = _optional_int(payload, "page_count")
        if not ok:
            errors["page_count"] = "Deve ser um numero."
        elif page_count is not None and page_count < 0:
            errors["page_count"] = "Nao pode ser negativo."
        data["page_count"] = page_count

    if "author_id" in payload or not partial:
        author_id, ok = _optional_int(payload, "author_id")
        if not ok:
            errors["author_id"] = "Deve ser um numero."
        data["author_id"] = author_id

    if "genre_id" in payload or not partial:
        genre_id, ok = _optional_int(payload, "genre_id")
        if not ok:
            errors["genre_id"] = "Deve ser um numero."
        data["genre_id"] = genre_id

    return data, errors


def validate_book_create(payload) -> tuple:
    return _validate(payload or {}, partial=False)


def validate_book_update(payload) -> tuple:
    return _validate(payload or {}, partial=True)


def book_to_dict(book) -> dict:
    return {
        "id": book.id,
        "title": book.title,
        "original_title": book.original_title,
        "slug": book.slug,
        "release_year": book.release_year,
        "synopsis": book.synopsis,
        "cover_url": book.cover_url,
        "isbn13": book.isbn13,
        "publisher": book.publisher,
        "page_count": book.page_count,
        "language": book.language,
        "author": {
            "id": book.author.id,
            "name": book.author.name,
            "slug": book.author.slug,
        }
        if book.author
        else None,
        "genre": {
            "id": book.genre.id,
            "name": book.genre.name,
            "slug": book.genre.slug,
        }
        if book.genre
        else None,
    }


def books_to_dict_list(books) -> list[dict]:
    return [book_to_dict(book) for book in books]
