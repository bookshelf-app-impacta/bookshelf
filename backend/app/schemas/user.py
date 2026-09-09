"""
Serializacao de usuario para JSON.

As chaves deste dicionario sao o CONTRATO com o frontend: batem uma a uma
com o `type User` de frontend/src/types/user.ts, que ja existe. Por isso
sao camelCase aqui, mesmo as colunas sendo snake_case no banco.

Nunca montar o JSON de um usuario a mao dentro de um blueprint. Se o
formato mudar, muda aqui, num lugar so, e o front nao descobre por
acidente que um campo sumiu.

Repare no que NAO esta aqui: `password_hash`. Hash tambem nao sai da API.
"""

from app.models import User


def user_to_json(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "displayName": user.display_name,
        "avatarUrl": user.avatar_url,
        "role": user.role,
        "isActive": user.is_active,
    }
