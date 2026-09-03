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

O repositório está na fase de esqueleto. As pastas e o banco estão prontos; o código das aplicações ainda não foi iniciado.

- [x] Estrutura de diretórios
- [x] MySQL via Docker Compose
- [ ] Backend Flask
- [ ] Frontend Next.js
- [x] Modelagem do banco

## Como subir o banco

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

## Board

Trello: <!-- colar o link do board aqui -->
