from app.models.book import Book
from app import db

class BookService:
    @staticmethod
    def get_all_books():
        return Book.query.all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def create_book(data):
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def update_book(book_id, data):
        book = Book.query.get(book_id)
        if not book:
            return None, "Book not found"

        for key, value in data.items():
            if hasattr(book, key) and value is not None:
                setattr(book, key, value)

        db.session.commit()
        return book, None

    @staticmethod
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return False, "Book not found"
        db.session.delete(book)
        db.session.commit()
        return True, None