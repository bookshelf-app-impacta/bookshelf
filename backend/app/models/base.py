"""Tipos e mixins compartilhados por todos os models."""

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT

from app.extensions import db

# Tipos UNSIGNED do MySQL.
#
# Uma chave primaria nunca e negativa, entao UNSIGNED dobra o alcance.
# E tem um motivo pratico: no MySQL a FK precisa ter EXATAMENTE o mesmo
# tipo da PK que referencia. Se a PK for UNSIGNED e a FK nao, o MySQL
# recusa a constraint com um erro 3780 que nao explica nada. Por isso
# os aliases abaixo — use sempre eles, nunca BigInteger cru.
PK = BIGINT(unsigned=True)
SMALL_U = SMALLINT(unsigned=True)


class TimestampMixin:
    """created_at / updated_at gerenciados pelo proprio MySQL."""

    created_at = db.Column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
