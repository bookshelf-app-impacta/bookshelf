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


### Avaliações (reviews)

- `POST /api/books/<id>/reviews` — cria avaliação do usuário autenticado.
- `GET /api/books/<id>/reviews` — lista avaliações públicas do livro.
- `PUT /api/reviews/<id>` — edita a própria avaliação.
- `DELETE /api/reviews/<id>` — exclui a própria avaliação.

POST, PUT e DELETE exigem JWT. Cada usuário pode ter somente uma avaliação por livro; o model `Review` já possui a restrição única `(user_id, book_id)`. O body pode conter texto, nota ou ambos; a nota deve ser de 0,5 a 5,0 em passos de 0,5.

Veja `../docs/REVIEWS_API.md` para exemplos dos corpos e códigos de resposta.
