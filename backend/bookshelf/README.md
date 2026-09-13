# Book Shelf — PR #4 corrigido

Projeto de rede social de livros da disciplina de Projeto de Software.

## O que esta versão corrige

Esta versão parte do código enviado no PR #4 e incorpora as correções solicitadas na revisão:

- `backend/app/__init__.py` com o nome correto;
- integração com o `create_app()` existente;
- configuração de banco por `DATABASE_URL`, sem SQLite fixo;
- blueprints/services/schemas dentro de `app/`;
- uso do model `Book` oficial;
- `schema.load()` para validar e converter dados;
- implementação de `get_book_by_isbn()`;
- dependências da main preservadas (`Flask-Migrate`, `Flask-Cors`, `cryptography` etc.);
- remoção do script `backend/test_api.py` do padrão de coleta do pytest;
- remoção da pasta acidental `backend/test.py`;
- PUT integrado em `/api/books/<id>`;
- PUT protegido para administrador, conforme a regra atual do projeto.

## Executar

```powershell
copy .env.example .env
docker compose up -d
cd backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python init_db.py
$env:FLASK_APP="wsgi.py"
flask run --debug --port 5000
```

Health check:

`http://localhost:5000/api/health`

## PUT de livros

Endpoint:

`PUT http://localhost:5000/api/books/<id>`

Exemplo:

```json
{
  "title": "Duna - edição atualizada",
  "releaseYear": 1965,
  "publisher": "Aleph",
  "isbn13": "9788576570000"
}
```

O endpoint trabalha com os nomes do modelo atual (`isbn13`, `releaseYear`, `synopsis`, `authorId`, `genreId etc.), e não com o model simplificado que havia sido criado no PR.

## Estrutura

```text
backend/
└── app/
    ├── blueprints/
    ├── models/
    ├── schemas/
    ├── services/
    ├── config.py
    ├── extensions.py
    ├── security.py
    └── __init__.py
frontend/
docs/
docker-compose.yml
.env.example
```
