"""Usuarios e papeis.  [AC1]"""

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.base import PK, TimestampMixin


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(PK, primary_key=True, autoincrement=True)
    username = db.Column(String(30), nullable=False, unique=True)
    email = db.Column(String(255), nullable=False, unique=True)
    # NUNCA guardar a senha. Sempre o hash (werkzeug / bcrypt / argon2).
    password_hash = db.Column(String(255), nullable=False)
    display_name = db.Column(String(80))
    bio = db.Column(String(500))
    avatar_url = db.Column(String(500))
    role = db.Column(
        Enum("user", "admin", name="user_role"),
        nullable=False, default="user", server_default="user",
    )
    is_active = db.Column(
        Boolean, nullable=False, default=True, server_default="1"
    )

    reviews = relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    def __repr__(self) -> str:
        return f"<User {self.username}>"
