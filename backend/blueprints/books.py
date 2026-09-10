from flask import Blueprint, request, jsonify
from app.schemas.book import BookCreateSchema, BookUpdateSchema
from app.services.book_service import BookService

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/', methods=['GET'])
def get_books():
    books = BookService.get_all_books()
    return jsonify([book.to_dict() for book in books]), 200

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = BookService.get_book_by_id(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book.to_dict()), 200

@books_bp.route('/', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    schema = BookCreateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    # Verifica se ISBN já existe
    existing = BookService.get_book_by_isbn(data.get('isbn'))
    if existing:
        return jsonify({'error': 'ISBN already exists'}), 409

    book = BookService.create_book(data)
    return jsonify(book.to_dict()), 201

@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    schema = BookUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    # Se ISBN for atualizado, verifica unicidade
    if 'isbn' in data:
        existing = BookService.get_book_by_isbn(data['isbn'])
        if existing and existing.id != book_id:
            return jsonify({'error': 'ISBN already exists'}), 409

    book, error = BookService.update_book(book_id, data)
    if error:
        return jsonify({'error': error}), 404

    return jsonify(book.to_dict()), 200

@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    success, error = BookService.delete_book(book_id)
    if not success:
        return jsonify({'error': error}), 404
    return '', 204