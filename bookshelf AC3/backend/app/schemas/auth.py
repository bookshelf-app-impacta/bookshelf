USERNAME_MIN, USERNAME_MAX = 3, 30
EMAIL_MAX = 255
DISPLAY_NAME_MAX = 80
PASSWORD_MIN = 8


def _text(payload, key):
    value = payload.get(key)
    return value.strip() if isinstance(value, str) else ""


def validate_register(payload):
    payload = payload or {}
    errors = {}
    username = _text(payload, "username")
    email = _text(payload, "email").lower()
    password = payload.get("password")
    password = password if isinstance(password, str) else ""
    display_name = _text(payload, "displayName")

    if not USERNAME_MIN <= len(username) <= USERNAME_MAX:
        errors["username"] = f"Deve ter entre {USERNAME_MIN} e {USERNAME_MAX} caracteres."
    if not email or "@" not in email or len(email) > EMAIL_MAX:
        errors["email"] = "E-mail invalido."
    if len(password) < PASSWORD_MIN:
        errors["password"] = f"Deve ter no minimo {PASSWORD_MIN} caracteres."
    if len(display_name) > DISPLAY_NAME_MAX:
        errors["displayName"] = f"Deve ter no maximo {DISPLAY_NAME_MAX} caracteres."

    return {
        "username": username,
        "email": email,
        "password": password,
        "display_name": display_name or None,
    }, errors


def validate_login(payload):
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
