"""
Validacao da entrada das rotas de autenticacao.

Feita a mao de proposito. Sao tres campos por rota, e marshmallow ou
pydantic seriam uma dependencia nova que os sete integrantes teriam que
instalar para ganhar pouca coisa.

Cada funcao devolve a dupla `(dados, erros)`. Se `erros` nao estiver
vazio, o blueprint responde 400 e nem chega a chamar o service.

Os limites de tamanho vem das colunas em app/models/user.py. Validar aqui
evita dois problemas: o MySQL truncando a string em silencio, e o usuario
recebendo um erro cru de banco de dados na tela.
"""

USERNAME_MIN = 3
USERNAME_MAX = 30       # users.username = String(30)
EMAIL_MAX = 255         # users.email = String(255)
DISPLAY_NAME_MAX = 80   # users.display_name = String(80)
PASSWORD_MIN = 8


def _texto(payload: dict, chave: str) -> str:
    """Le uma chave como texto limpo. Ausente ou de outro tipo vira ''."""
    valor = payload.get(chave)
    return valor.strip() if isinstance(valor, str) else ""


def validate_register(payload) -> tuple:
    payload = payload or {}
    erros = {}

    username = _texto(payload, "username")
    email = _texto(payload, "email").lower()
    # A senha nao leva strip: espaco no comeco ou no fim faz parte dela.
    senha = payload.get("password")
    senha = senha if isinstance(senha, str) else ""
    display_name = _texto(payload, "displayName")

    if not USERNAME_MIN <= len(username) <= USERNAME_MAX:
        erros["username"] = (
            f"Deve ter entre {USERNAME_MIN} e {USERNAME_MAX} caracteres."
        )
    if not email or "@" not in email or len(email) > EMAIL_MAX:
        erros["email"] = "E-mail invalido."
    if len(senha) < PASSWORD_MIN:
        erros["password"] = f"Deve ter no minimo {PASSWORD_MIN} caracteres."
    if len(display_name) > DISPLAY_NAME_MAX:
        erros["displayName"] = (
            f"Deve ter no maximo {DISPLAY_NAME_MAX} caracteres."
        )

    dados = {
        "username": username,
        "email": email,
        "password": senha,
        # Campo opcional: string vazia vira None, porque a coluna aceita
        # NULL e "" nao e um nome de exibicao.
        "display_name": display_name or None,
    }

    # Um eventual "role" no corpo da requisicao e ignorado aqui e nem
    # chega ao service — papel nao se escolhe no cadastro.
    # Ver app/services/auth.py.
    return dados, erros


def validate_login(payload) -> tuple:
    payload = payload or {}
    erros = {}

    email = _texto(payload, "email").lower()
    senha = payload.get("password")
    senha = senha if isinstance(senha, str) else ""

    if not email:
        erros["email"] = "Obrigatorio."
    if not senha:
        erros["password"] = "Obrigatorio."

    # Nada de validar formato de e-mail ou tamanho de senha no login:
    # so importa se as credenciais conferem, e uma mensagem do tipo
    # "senha curta demais" entrega informacao sobre a conta alheia.
    return {"email": email, "password": senha}, erros
