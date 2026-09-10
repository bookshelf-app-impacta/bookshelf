"""Favoritos.  [Entrega final — R004, 22/11]"""

from sqlalchemy import DateTime, ForeignKey, func

from app.extensions import db
from app.models.base import PK


class Favorite(db.Model):
    """A PK composta (user_id, book_id) e o que impede favoritar duas
    vezes o mesmo livro. Nao precisa de coluna `id` nem de validacao no
    codigo — o banco ja recusa o INSERT duplicado."""

    __tablename__ = "favorites"

    user_id = db.Column(
        PK, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    book_id = db.Column(
        PK, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    created_at = db.Column(DateTime, nullable=False, server_default=func.now())

    # Consultar "quem favoritou este livro" usa o indice que o MySQL cria
    # sozinho para a FK de book_id. Nao precisa de Index explicito.
