USERNAME_MIN = 3
USERNAME_MAX = 30       # users.username = String(30)
EMAIL_MAX = 255         # users.email = String(255)
DISPLAY_NAME_MAX = 80   # users.display_name = String(80)
PASSWORD_MIN = 8


def _text(payload: dict, key: str) -> str:
    value = payload.get(key)
    return value.strip() if isinstance(value, str) else ""


def validate_register(payload) -> tuple:
    payload = payload or {}
    errors = {}

    username = _text(payload, "username")
    email = _text(payload, "email").lower()
    # A senha nao leva strip: espaco no comeco ou no fim faz parte dela.
    password = payload.get("password")
    password = password if isinstance(password, str) else ""
    display_name = _text(payload, "displayName")

    if not USERNAME_MIN <= len(username) <= USERNAME_MAX:
        errors["username"] = (
            f"Deve ter entre {USERNAME_MIN} e {USERNAME_MAX} caracteres."
        )
    if not email or "@" not in email or len(email) > EMAIL_MAX:
        errors["email"] = "E-mail invalido."
    if len(password) < PASSWORD_MIN:
        errors["password"] = f"Deve ter no minimo {PASSWORD_MIN} caracteres."
    if len(display_name) > DISPLAY_NAME_MAX:
        errors["displayName"] = (
            f"Deve ter no maximo {DISPLAY_NAME_MAX} caracteres."
        )

    # Um "role" no corpo da requisicao nao sai daqui: papel nao se
    # escolhe no cadastro. Ver app/services/auth.py.
    data = {
        "username": username,
        "email": email,
        "password": password,
        "display_name": display_name or None,
    }
    return data, errors


def validate_login(payload) -> tuple:
    payload = payload or {}
    errors = {}

    email = _text(payload, "email").lower()
    password = payload.get("password")
    password = password if isinstance(password, str) else ""

    if not email:
        errors["email"] = "Obrigatorio."
    if not password:
        errors["password"] = "Obrigatorio."

    return {"email": email, "password": password}, errors
