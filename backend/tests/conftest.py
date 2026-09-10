import pytest
import os
from app import create_app, db
from app.models.book import Book

@pytest.fixture(scope='function')
def app():
    app = create_app()
    test_db_uri = os.getenv('TEST_DATABASE_URL',
                            'mysql+pymysql://user:password@localhost:3306/bookshelf_test')
    app.config['SQLALCHEMY_DATABASE_URI'] = test_db_uri
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_book(app):
    book = Book(
        title='Livro Teste',
        author='Autor Teste',
        isbn='1234567890123',
        publication_year=2020,
        publisher='Editora Teste',
        description='Descrição teste'
    )
    db.session.add(book)
    db.session.commit()
    return book.id