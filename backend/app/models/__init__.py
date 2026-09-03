"""
Models SQLAlchemy — a fonte da verdade do banco.

IMPORTANTE: todo model novo precisa ser importado aqui. O Alembic so
enxerga o que estiver registrado no metadata, e se voce esquecer, o
`flask db migrate` gera uma migration sem a sua tabela e nao reclama.
"""

from app.models.base import TimestampMixin
from app.models.user import User
from app.models.book import Author, Book, Genre
from app.models.review import Comment, Review, ReviewLike
from app.models.favorite import Favorite

__all__ = [
    "TimestampMixin",
    "User",
    "Book",
    "Author",
    "Genre",
    "Review",
    "Comment",
    "ReviewLike",
    "Favorite",
]
