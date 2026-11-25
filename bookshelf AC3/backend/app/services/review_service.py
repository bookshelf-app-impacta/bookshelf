"""Regras de negocio para criar, listar, editar e apagar avaliações."""
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Book, Review


class ReviewServiceError(Exception):
    status_code = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ReviewNotFoundError(ReviewServiceError):
    status_code = 404


class DuplicateReviewError(ReviewServiceError):
    status_code = 409


class ReviewPermissionError(ReviewServiceError):
    status_code = 403


class ReviewContentError(ReviewServiceError):
    status_code = 400


class ReviewService:
    @staticmethod
    def list_reviews(book_id):
        """Lista as avaliações de um livro, da mais recente para a mais antiga."""
        if db.session.get(Book, book_id) is None:
            raise ReviewNotFoundError("Livro não encontrado.")

        return (
            Review.query.filter_by(book_id=book_id)
            .order_by(Review.created_at.desc(), Review.id.desc())
            .all()
        )

    @staticmethod
    def create_review(book_id, user_id, data):
        """Cria no máximo uma avaliação por usuário para cada livro."""
        if db.session.get(Book, book_id) is None:
            raise ReviewNotFoundError("Livro não encontrado.")

        existing = Review.query.filter_by(book_id=book_id, user_id=user_id).first()
        if existing:
            raise DuplicateReviewError("Você já publicou uma avaliação para este livro.")

        body = data.get("body")
        rating = data.get("rating")
        ReviewService._validate_content(body, rating)

        review = Review(
            book_id=book_id,
            user_id=user_id,
            body=body,
            rating=rating,
            has_spoilers=data.get("has_spoilers", False),
            consumed_on=data.get("consumed_on"),
        )
        db.session.add(review)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # A restrição UNIQUE(user_id, book_id) continua sendo a
            # proteção definitiva contra requisições concorrentes.
            existing = Review.query.filter_by(book_id=book_id, user_id=user_id).first()
            if existing:
                raise DuplicateReviewError("Você já publicou uma avaliação para este livro.")
            raise

        return review

    @staticmethod
    def update_review(review_id, user_id, data):
        """Atualiza uma avaliação apenas se ela pertencer ao usuário autenticado."""
        review = db.session.get(Review, review_id)
        if review is None:
            raise ReviewNotFoundError("Avaliação não encontrada.")
        if review.user_id != user_id:
            raise ReviewPermissionError("Você só pode editar sua própria avaliação.")

        new_body = data.get("body", review.body)
        new_rating = data.get("rating", review.rating)
        ReviewService._validate_content(new_body, new_rating)

        for field in ("body", "rating", "has_spoilers", "consumed_on"):
            if field in data:
                setattr(review, field, data[field])

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise

        return review

    @staticmethod
    def delete_review(review_id, user_id):
        """Exclui uma avaliação apenas se ela pertencer ao usuário autenticado."""
        review = db.session.get(Review, review_id)
        if review is None:
            raise ReviewNotFoundError("Avaliação não encontrada.")
        if review.user_id != user_id:
            raise ReviewPermissionError("Você só pode excluir sua própria avaliação.")

        db.session.delete(review)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise

    @staticmethod
    def _validate_content(body, rating):
        # Compatível com ck_reviews_nota_ou_texto do model: pelo menos
        # um entre body e rating precisa ter valor.
        if (body is None or not str(body).strip()) and rating is None:
            raise ReviewContentError("A avaliação precisa conter texto, nota ou ambos.")
