"""adiciona view de media de notas por livro

Revision ID: ac49234fdd1c
Revises: 78393eb49277

"""
from alembic import op
import sqlalchemy as sa

revision = 'ac49234fdd1c'
down_revision = '78393eb49277'
branch_labels = None
depends_on = None

VIEW_MEDIA = """
CREATE OR REPLACE VIEW vw_book_ratings AS
SELECT
    b.id                    AS book_id,
    b.slug                  AS slug,
    b.title                 AS title,
    COUNT(r.id)             AS total_avaliacoes,
    COUNT(r.rating)         AS total_notas,
    ROUND(AVG(r.rating), 2) AS media,
    MAX(r.created_at)       AS ultima_avaliacao
FROM books b
LEFT JOIN reviews r ON r.book_id = b.id
GROUP BY b.id, b.slug, b.title
"""


def upgrade():
    # Views NAO sao detectadas pelo `flask db migrate` - o autogenerate so
    # compara tabelas, colunas e indices. Por isso esta migration foi criada
    # vazia com `flask db revision` e escrita a mao.
    #
    # Por que view e nao coluna `media` em `books`: media guardada desatualiza
    # toda vez que alguem edita ou apaga uma avaliacao, e o erro e silencioso.
    #
    # Atencao as duas contagens:
    #   total_avaliacoes = COUNT(r.id)     -> todas, com ou sem nota
    #   total_notas      = COUNT(r.rating) -> so as que tem nota
    # Livro so com comentario tem total_notas = 0 e media = NULL. O front
    # precisa mostrar "sem notas ainda", nao "0.0".
    op.execute(VIEW_MEDIA)


def downgrade():
    op.execute("DROP VIEW IF EXISTS vw_book_ratings")
