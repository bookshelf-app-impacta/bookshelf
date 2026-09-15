# Book Shelf

Rede social de livros desenvolvida na disciplina de **Projeto de Software**.

O administrador cadastra os livros. Usuários avaliam com nota e comentário e montam sua lista de favoritos.

## Stack

| Camada | Tecnologia |
|---|---|
| Front-end | Next.js (App Router, TypeScript) |
| Back-end | Python + Flask |
| Banco de dados | MySQL 8 (via Docker) |

## Status

- [x] Estrutura de diretórios
- [x] MySQL via Docker Compose
- [x] Backend Flask
- [x] Frontend Next.js
- [x] Modelagem do banco

## Como rodar o projeto

### 1. Banco de dados

Requer Docker instalado.

Na primeira vez, crie o arquivo de ambiente a partir do exemplo:

```bash
cp .env.example .env
```

O `.env` guarda as credenciais do banco e não é versionado. Depois:

```bash
docker compose up -d
```

Isso sobe dois serviços:

- **MySQL** em `localhost:3306` — banco, usuário e senha são os definidos no seu `.env`
- **Adminer** em http://localhost:8080 — interface web para inspecionar o banco

Para parar:

```bash
docker compose down          # mantém os dados
docker compose down -v       # apaga os dados também
```

### 2. Backend (Flask)

```bash
cd backend
cp .env.example .env   # preencher SECRET_KEY (veja o comentário no próprio arquivo)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask seed              # opcional: cria dados de exemplo, incluindo um admin
flask run                # API em http://localhost:5000
```

O `flask seed` cria, entre outros, o usuário administrador `admin@bookshelf.local` / `admin123` — é com essa conta que se cadastra livro, já que **cadastrar livro exige login como admin** (listar e ver detalhes continua público, sem login).

Rodar os testes:

```bash
pytest -v
```

### 3. Frontend (Next.js)

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev              # app em http://localhost:3000
```

## Estrutura

```
backend/    aplicação Flask       (ver backend/README.md)
frontend/   aplicação Next.js     (ver frontend/README.md)
infra/      configuração do Docker
docs/       documentação do projeto
```

## Documentação

- [Entregas e cronograma](docs/ENTREGAS.md)
- [Fluxo de trabalho no Git](docs/GIT-WORKFLOW.md)
- [Banco de dados](docs/BANCO-DE-DADOS.md)

## Equipe

Sete integrantes. Como o repositório é público, aqui ficam só os usuários do GitHub — a lista com os nomes completos vai na entrega do Classroom.

<!-- Preencher com os usuários do GitHub dos 7 integrantes -->

- [@gustavofds](https://github.com/gustavofds)
- [@anaferreg](https://github.com/anaferreg)
- [@BManaf](https://github.com/BManaf)
- [@HGCAVALCANTE](https://github.com/HGCAVALCANTE)
- [@lelevaa](https://github.com/lelevaa)
- [@TabathaPaola](https://github.com/TabathaPaola)
- Carlos Rodrigo
- 
## Board

Trello: <!-- colar o link do board aqui -->
