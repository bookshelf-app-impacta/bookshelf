"""
Avaliacoes e comentarios.

Alinhamento com o cronograma (docs/ENTREGAS.md):
  AC2 (13/10) — "Avaliacao de livro: comentarios"  -> cria `reviews.body`
  AC3 (08/11) — "Avaliacao de livro: notas"        -> adiciona `reviews.rating`

Por isso `rating` e NULLABLE. Se fosse NOT NULL, a AC2 nao teria como
gravar um comentario sem nota e a AC3 nao teria o que entregar. O CHECK
`ck_reviews_nota_ou_texto` garante que pelo menos um dos dois exista —
avaliacao vazia nao entra no banco.

Na pratica: gere a migration da AC2 com o model SEM o campo `rating`, e
na AC3 adicione o campo e gere a segunda migration. Duas migrations
reais, em sprints diferentes, e exatamente o que se espera do processo.
"""

from sqlalchemy import (
    Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Numeric,
    String, Text, UniqueConstraint, func,
)
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.base import PK, TimestampMixin


class Review(TimestampMixin, db.Model):
    __tablename__ = "reviews"

    id = db.Column(PK, primary_key=True, autoincrement=True)
    user_id = db.Column(
        PK, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    book_id = db.Column(
        PK, ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    # [AC2] o comentario/resenha
    body = db.Column(Text)
    # [AC3] a nota, de 0.5 a 5.0 de meio em meio.
    # DECIMAL, nunca FLOAT: 4.5 em float vira 4.4999999 e a media sai errada.
    rating = db.Column(Numeric(2, 1))
    has_spoilers = db.Column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    consumed_on = db.Column(Date)

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
    comments = relationship(
        "Comment", back_populates="review", cascade="all, delete-orphan"
    )

    __table_args__ = (
        # Regra central do produto: 1 avaliacao por usuario por livro.
        # A segunda tentativa deve virar EDICAO, nao um registro novo.
        UniqueConstraint("user_id", "book_id", name="uq_reviews_user_book"),
        Index("idx_reviews_book_created", "book_id", "created_at"),
        CheckConstraint(
            "rating IS NULL OR "
            "(rating >= 0.5 AND rating <= 5.0 AND MOD(rating * 10, 5) = 0)",
            name="ck_reviews_rating",
        ),
        CheckConstraint(
            "rating IS NOT NULL OR body IS NOT NULL",
            name="ck_reviews_nota_ou_texto",
        ),
    )


class Comment(TimestampMixin, db.Model):
    """Resposta de outro usuario a uma avaliacao (thread).

    NAO faz parte das 4 entregas — e extra. So implementar se o nucleo
    estiver fechado. Se 'comentarios' da AC2 se referir apenas ao texto da
    propria avaliacao, esta tabela pode ser cortada inteira.
    """

    __tablename__ = "comments"

    id = db.Column(PK, primary_key=True, autoincrement=True)
    review_id = db.Column(
        PK, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        PK, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    parent_comment_id = db.Column(
        PK, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )
    body = db.Column(String(2000), nullable=False)
    # Soft delete: apagar de verdade derrubaria as respostas penduradas.
    is_deleted = db.Column(
        Boolean, nullable=False, default=False, server_default="0"
    )

    review = relationship("Review", back_populates="comments")
    user = relationship("User", back_populates="comments")
    replies = relationship("Comment", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_comments_review", "review_id", "created_at"),
        # NAO criar Index("idx_comments_user", "user_id"): o MySQL ja cria
        # um indice automatico para a FK de user_id. Um indice explicito
        # duplicado nao acelera nada e ainda quebra o downgrade da migration
        # com o erro 1553 ("needed in a foreign key constraint").
    )


class ReviewLike(db.Model):
    """Curtida em avaliacao. Extra — nao esta nas 4 entregas."""

    __tablename__ = "review_likes"

    user_id = db.Column(
        PK, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    review_id = db.Column(
        PK, ForeignKey("reviews.id", ondelete="CASCADE"), primary_key=True
    )
    created_at = db.Column(DateTime, nullable=False, server_default=func.now())
