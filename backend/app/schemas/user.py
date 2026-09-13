from app.models import User

USERNAME_MIN = 3
USERNAME_MAX = 30
EMAIL_MAX = 255
DISPLAY_NAME_MAX = 80
PASSWORD_MIN = 8
ROLES = ("user", "admin")


def _text(payload: dict, key: str) -> str:
    value = payload.get(key)
    return value.strip() if isinstance(value, str) else ""


def _validate_shared(payload: dict, data: dict, errors: dict, *, partial: bool) -> None:
    """Campos em comum entre criar e editar usuario (painel do admin).

    Chaves de entrada em camelCase, igual ao `validate_register` de
    schemas/auth.py — o `data` de saida usa snake_case porque e isso
    que vira `setattr`/kwarg do model em services/user_service.py.
    """
    if "username" in payload or not partial:
        username = _text(payload, "username")
        if not USERNAME_MIN <= len(username) <= USERNAME_MAX:
            errors["username"] = f"Deve ter entre {USERNAME_MIN} e {USERNAME_MAX} caracteres."
        data["username"] = username

    if "email" in payload or not partial:
        email = _text(payload, "email").lower()
        if not email or "@" not in email or len(email) > EMAIL_MAX:
            errors["email"] = "E-mail invalido."
        data["email"] = email

    if "displayName" in payload or not partial:
        display_name = _text(payload, "displayName") or None
        if display_name and len(display_name) > DISPLAY_NAME_MAX:
            errors["displayName"] = f"Deve ter no maximo {DISPLAY_NAME_MAX} caracteres."
        data["display_name"] = display_name

    if "role" in payload or not partial:
        if "role" in payload and not isinstance(payload.get("role"), str):
            # _text() so distingue "ausente" de "tipo errado" devolvendo
            # "" pros dois casos — sem checar o tipo aqui, role=123 caia
            # no fallback "user" sem erro nenhum.
            errors["role"] = "Deve ser 'user' ou 'admin'."
            role = "user"
        else:
            role = _text(payload, "role") or "user"
            if role not in ROLES:
                errors["role"] = "Deve ser 'user' ou 'admin'."
        data["role"] = role

    if "isActive" in payload:
        is_active = payload.get("isActive")
        if not isinstance(is_active, bool):
            errors["isActive"] = "Deve ser verdadeiro ou falso."
        data["is_active"] = is_active


def validate_user_create(payload) -> tuple:
    payload = payload or {}
    errors = {}
    data = {}

    _validate_shared(payload, data, errors, partial=False)

    password = payload.get("password")
    password = password if isinstance(password, str) else ""
    if len(password) < PASSWORD_MIN:
        errors["password"] = f"Deve ter no minimo {PASSWORD_MIN} caracteres."
    data["password"] = password

    return data, errors


def validate_user_update(payload) -> tuple:
    payload = payload or {}
    errors = {}
    data = {}

    _validate_shared(payload, data, errors, partial=True)

    if "password" in payload:
        password = payload.get("password")
        password = password if isinstance(password, str) else ""
        # Vazio em edicao significa "nao alterar" — diferente da criacao,
        # onde a senha e obrigatoria. So entra no `data` (e so e validado
        # o tamanho) se vier algo de fato.
        if password:
            if len(password) < PASSWORD_MIN:
                errors["password"] = f"Deve ter no minimo {PASSWORD_MIN} caracteres."
            data["password"] = password

    return data, errors


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


def users_to_json_list(users) -> list[dict]:
    return [user_to_json(user) for user in users]
