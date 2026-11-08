from sqlalchemy import DateTime, ForeignKey, func
from app.extensions import db
from app.models.base import PK


class Favorite(db.Model):
    __tablename__ = "favorites"
    user_id = db.Column(PK, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    book_id = db.Column(PK, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    created_at = db.Column(DateTime, nullable=False, server_default=func.now())
