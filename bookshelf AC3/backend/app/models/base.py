"""Tipos e mixins compartilhados."""
from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT
from app.extensions import db

PK = BIGINT(unsigned=True)
SMALL_U = SMALLINT(unsigned=True)


class TimestampMixin:
    created_at = db.Column(DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
