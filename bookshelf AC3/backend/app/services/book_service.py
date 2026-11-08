from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Book


class BookService:
    @staticmethod
    def get_all_books():
        return Book.query.order_by(Book.title.asc()).all()

    @staticmethod
    def get_book_by_id(book_id):
        return db.session.get(Book, book_id)

    @staticmethod
    def get_book_by_isbn(isbn13):
        if not isbn13:
            return None
        return Book.query.filter_by(isbn13=isbn13).first()

    @staticmethod
    def get_book_by_slug(slug):
        if not slug:
            return None
        return Book.query.filter_by(slug=slug).first()

    @staticmethod
    def make_unique_slug(title):
        import re
        base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "livro"
        slug = base
        counter = 2
        while BookService.get_book_by_slug(slug):
            slug = f"{base}-{counter}"
            counter += 1
        return slug

    @staticmethod
    def create_book(data, created_by):
        book = Book(**data, created_by=created_by)
        db.session.add(book)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
        return book

    @staticmethod
    def update_book(book_id, data):
        book = db.session.get(Book, book_id)
        if not book:
            return None
        for key, value in data.items():
            setattr(book, key, value)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
        return book

    @staticmethod
    def delete_book(book_id):
        book = db.session.get(Book, book_id)
        if not book:
            return False
        db.session.delete(book)
        db.session.commit()
        return True
