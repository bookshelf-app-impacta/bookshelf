"""Serializacao de usuario para JSON."""

from app.models import User


def user_to_json(user: User) -> dict:
    """As chaves sao o contrato com o front: batem com o `type User` de
    frontend/src/types/user.ts. Por isso camelCase, e por isso nao se
    monta esse dicionario a mao dentro de um blueprint."""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "displayName": user.display_name,
        "avatarUrl": user.avatar_url,
        "role": user.role,
        "isActive": user.is_active,
    }
