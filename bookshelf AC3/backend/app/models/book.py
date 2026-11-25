from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models.base import PK, SMALL_U, TimestampMixin


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(PK, primary_key=True, autoincrement=True)
    name = db.Column(String(150), nullable=False)
    slug = db.Column(String(170), nullable=False, unique=True)
    books = relationship("Book", back_populates="author")
    __table_args__ = (Index("idx_authors_name", "name"),)


class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(SMALL_U, primary_key=True, autoincrement=True)
    name = db.Column(String(60), nullable=False, unique=True)
    slug = db.Column(String(70), nullable=False, unique=True)
    books = relationship("Book", back_populates="genre")


class Book(TimestampMixin, db.Model):
    __tablename__ = "books"

    id = db.Column(PK, primary_key=True, autoincrement=True)
    title = db.Column(String(255), nullable=False)
    original_title = db.Column(String(255))
    slug = db.Column(String(280), nullable=False, unique=True)
    release_year = db.Column(SMALL_U)
    synopsis = db.Column(Text)
    cover_url = db.Column(String(500))
    isbn13 = db.Column(String(13), unique=True)
    publisher = db.Column(String(150))
    page_count = db.Column(SMALL_U)
    language = db.Column(String(40))
    author_id = db.Column(PK, ForeignKey("authors.id", ondelete="SET NULL"), nullable=True)
    genre_id = db.Column(SMALL_U, ForeignKey("genres.id", ondelete="SET NULL"), nullable=True)
    created_by = db.Column(PK, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_books_title", "title"),
        Index("idx_books_year", "release_year"),
        CheckConstraint(
            "release_year IS NULL OR release_year BETWEEN 1400 AND 2200",
            name="ck_books_year",
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "originalTitle": self.original_title,
            "slug": self.slug,
            "releaseYear": self.release_year,
            "synopsis": self.synopsis,
            "coverUrl": self.cover_url,
            "isbn13": self.isbn13,
            "publisher": self.publisher,
            "pageCount": self.page_count,
            "language": self.language,
            "authorId": self.author_id,
            "genreId": self.genre_id,
            "createdBy": self.created_by,
            "author": (
                {"id": self.author.id, "name": self.author.name}
                if self.author else None
            ),
            "genre": (
                {"id": self.genre.id, "name": self.genre.name}
                if self.genre else None
            ),
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
