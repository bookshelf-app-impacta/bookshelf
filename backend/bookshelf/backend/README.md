# Backend — Flask

API REST do Book Shelf.

## Windows / VS Code

Na raiz do projeto:

```powershell
copy .env.example .env
docker compose up -d
```

Depois:

```powershell
cd backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:FLASK_APP="wsgi.py"
flask run --debug --port 5000
```

Teste:

```text
http://localhost:5000/api/health
```

### Autenticação

Cadastre/login em:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

O usuário `admin` é necessário para cadastro/alteração/exclusão de livros.

### Livros

- `GET /api/books`
- `GET /api/books/<id>`
- `POST /api/books`
- `PUT /api/books/<id>`
- `DELETE /api/books/<id>`

O PUT usa o modelo oficial de `app.models.book` da main e não cria um segundo modelo paralelo.
