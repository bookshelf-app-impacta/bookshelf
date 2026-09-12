"""
Schema de saida do Book. Traduz o model SQLAlchemy pro JSON que o
front recebe — decide explicitamente quais campos vao pra fora.
"""


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