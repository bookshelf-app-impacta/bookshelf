"""
Instancias compartilhadas das extensoes Flask.

Ficam num modulo separado do factory para evitar import circular:
os models importam `db` daqui, e o factory importa os models.
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# compare_type=True: sem isso o Alembic ignora mudanca de TIPO de coluna
# e gera migration vazia sem voce entender o motivo.
migrate = Migrate(compare_type=True)
