from app.models import User


def user_to_json(user: User) -> dict:
    """Contrato com o `type User` de frontend/src/types/user.ts — por isso
    camelCase, e por isso nao se monta esse dicionario a mao no blueprint."""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "displayName": user.display_name,
        "avatarUrl": user.avatar_url,
        "role": user.role,
        "isActive": user.is_active,
    }
