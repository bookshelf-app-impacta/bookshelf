from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.extensions import db
from app.models.base import PK, TimestampMixin


class Review(TimestampMixin, db.Model):
    __tablename__ = "reviews"
    id = db.Column(PK, primary_key=True, autoincrement=True)
    user_id = db.Column(PK, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = db.Column(PK, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    body = db.Column(Text)
    rating = db.Column(Numeric(2, 1))
    has_spoilers = db.Column(Boolean, nullable=False, default=False, server_default="0")
    consumed_on = db.Column(Date)
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
    comments = relationship("Comment", back_populates="review", cascade="all, delete-orphan")
    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="uq_reviews_user_book"),
        Index("idx_reviews_book_created", "book_id", "created_at"),
        CheckConstraint(
            "rating IS NULL OR (rating >= 0.5 AND rating <= 5.0 AND MOD(rating * 10, 5) = 0)",
            name="ck_reviews_rating",
        ),
        CheckConstraint(
            "rating IS NOT NULL OR body IS NOT NULL",
            name="ck_reviews_nota_ou_texto",
        ),
    )


class Comment(TimestampMixin, db.Model):
    __tablename__ = "comments"
    id = db.Column(PK, primary_key=True, autoincrement=True)
    review_id = db.Column(PK, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(PK, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent_comment_id = db.Column(PK, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    body = db.Column(String(2000), nullable=False)
    is_deleted = db.Column(Boolean, nullable=False, default=False, server_default="0")
    review = relationship("Review", back_populates="comments")
    user = relationship("User", back_populates="comments")
    replies = relationship("Comment", cascade="all, delete-orphan")


class ReviewLike(db.Model):
    __tablename__ = "review_likes"
    user_id = db.Column(PK, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    review_id = db.Column(PK, ForeignKey("reviews.id", ondelete="CASCADE"), primary_key=True)
    created_at = db.Column(DateTime, nullable=False, server_default=func.now())
