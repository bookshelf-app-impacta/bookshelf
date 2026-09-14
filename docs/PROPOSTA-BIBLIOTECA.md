# Proposta: virar sistema de biblioteca

**Status: proposta em aberto, decisão do grupo.** Este documento não muda nada
sozinho — é a base pra discussão no PR. Se aprovado, daí sim atualiza
`README.md`, `ENTREGAS.md` e o board.

## Por que mexer agora

A AC1 (cadastro/listagem de livro) está pronta e mergeada. As próximas três
entregas (R002, R003, R004) ainda são só ideia no `ENTREGAS.md` — nenhuma
tabela, endpoint ou tela delas existe no código. Trocar o rumo agora não
desperdiça nada que já foi feito; trocar depois de começar R002 já seria mais
caro.

O plano atual (R002 comentários, R003 notas, R004 favoritos) monta uma rede
social de avaliação de livro. A alternativa aqui é um sistema de biblioteca
escolar: administrador cadastra livro e aluno, aluno pega livro emprestado e
devolve. É um fluxo de negócio com estado (emprestado → devolvido, com prazo),
o que rende uma demonstração em vídeo mais rica que três telas de CRUD
parecidas entre si.

## O que já existe e é reaproveitado sem mudar nada

- **Cadastro de livro, listagem pública, admin-only** (`/api/books`) — igual,
  não muda.
- **Autenticação e papéis** (`/api/auth`, `role` em `users`) — o "aluno" da
  proposta é o `role = user` que já existe. Não precisa de papel novo nem de
  tabela nova pra representar aluno.
- **Cadastro self-service** (`POST /api/auth/register`) — já é exatamente o
  fluxo "aluno se cadastra sozinho" que R002 propõe. Falta só um campo. Ver
  detalhe abaixo.
- **CRUD de usuário pelo admin** (`/api/users`, tela `/admin/usuarios`) —
  continua existindo pra gerenciar aluno depois de cadastrado (editar,
  desativar, excluir).

## Cronograma proposto

| Entrega | Data | Cartão | Funcionalidade proposta | Custo |
|---|---|---|---|---|
| AC2 | 13/10 | R002 | Cadastro de alunos | Baixo — reaproveita `/api/auth/register` existente, self-service |
| AC3 | 08/11 | R003 | Empréstimo de livro | Médio — tabela e endpoints novos |
| Final | 22/11 | R004 | Devolução de livro + histórico de empréstimos | Baixo — fecha o ciclo do R003, sem tabela nova |

Comparado ao cronograma atual (R002 comentários, R003 notas, R004 favoritos):
mesmo número de entregas, mesma cadência. O que muda é o domínio.

## R002 — Cadastro de alunos

**Self-service, não pelo admin.** Já existe `POST /api/auth/register`
(`backend/app/blueprints/auth.py`), público, sem exigir login nem admin —
qualquer um se cadastra sozinho e já nasce com `role = user`. É exatamente o
fluxo "aluno se cadastra". Fica mais barato que a alternativa de admin
cadastrar cada aluno pelo painel `/api/users`: essa rota já existe, só falta
um campo.

- **Adicionar `registration_number`** (RA/matrícula) em `users`: coluna nova
  (`VARCHAR`, `UNIQUE`, nullable — admin criado por `flask seed` não tem
  RA), migration pequena. Entra em `validate_register`
  (`backend/app/schemas/auth.py`) como campo obrigatório só nesse formulário
  — login continua só com e-mail/senha.
- O painel admin (`/api/users`, tela `/admin/usuarios`) continua existindo
  pra listar/editar/desativar aluno depois de cadastrado — só a **criação**
  deixa de ser feita por lá.
- Sem verificação do RA contra uma lista de matrículas válidas da escola
  (não tem essa base pra consultar). Aceita qualquer valor informado,
  único no banco — suficiente pro escopo da disciplina.
- Endpoint e tabela continuam em inglês (`/api/auth/register`, coluna
  `registration_number` em `users`) — não muda nada nesse quesito.

## R003 — Empréstimo de livro

### Tabela nova: `loans`

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | `BIGINT UNSIGNED` PK | padrão do projeto |
| `book_id` | `BIGINT UNSIGNED` FK → `books.id` | `ON DELETE RESTRICT` — não dá pra apagar livro com empréstimo em aberto |
| `user_id` | `BIGINT UNSIGNED` FK → `users.id` | o aluno que pegou emprestado |
| `loaned_at` | `DATETIME` | quando pegou |
| `due_date` | `DATE` | prazo de devolução |
| `returned_at` | `DATETIME`, nullable | `NULL` = ainda emprestado |

Sem coluna de "status" guardada — segue a mesma lição já documentada em
`docs/BANCO-DE-DADOS.md` (seção 4.5, sobre não guardar `avg_rating`
calculável): o status é derivado —

- `returned_at IS NULL` e `due_date >= hoje` → emprestado
- `returned_at IS NULL` e `due_date < hoje` → atrasado
- `returned_at IS NOT NULL` → devolvido

### Disponibilidade do livro — decisão em aberto pro grupo

O model `Book` de hoje não tem noção de "quantos exemplares existem". Duas
opções:

- **Op. A (recomendada pra estas 2 entregas restantes):** 1 exemplar por
  linha de `books`. Um livro com empréstimo em aberto (`loans.returned_at IS
  NULL`) fica indisponível pra outro aluno até devolver. Sem coluna nova em
  `books`; a checagem de disponibilidade é uma consulta (`NOT EXISTS` de
  empréstimo aberto), no mesmo padrão de `_check_isbn_unique` que já existe
  em `book_service.py`.
- **Op. B:** adicionar `books.copies` (quantidade de exemplares) e controlar
  quantos estão emprestados. Mais realista, mais schema, mais regra de
  negócio pra implementar em 2 sprints que também têm R004. Fica como
  evolução futura, não pra essas entregas.

### Endpoints propostos (inglês, mesmo padrão de `/api/books`)

| Rota | Quem pode | O que faz |
|---|---|---|
| `POST /api/loans/` | admin | Registra empréstimo — `{book_id, user_id, due_date}`. 409 se o livro já estiver emprestado (op. A) |
| `GET /api/loans/` | admin | Lista empréstimos, com filtro `?status=active\|overdue\|returned` e `?user_id=` |
| `GET /api/loans/<id>` | admin | Detalhe de um empréstimo |

## R004 — Devolução de livro + histórico

Não precisa de tabela nova, só fecha o ciclo do `loans`:

| Rota | Quem pode | O que faz |
|---|---|---|
| `PUT /api/loans/<id>/return` | admin | Marca `returned_at = agora` |
| `GET /api/loans/?user_id=<id>` | admin | Histórico de empréstimos de um aluno (já coberto pelo `GET /api/loans/` do R003, com filtro) |

Na tela: lista de empréstimos ativos com botão "Devolver" ao lado de cada um
— mesmo padrão dos botões de editar/excluir que já existem em `BookGrid.tsx`.

## Perguntas em aberto pro grupo

1. Aceita a troca de rumo? (é o principal — o resto é detalhe de como)
2. R002: cadastro do aluno fica self-service (`/api/auth/register` + RA) como
   proposto, ou o grupo prefere manter pelo painel do admin?
3. R003: 1 exemplar por livro (op. A) ou quantidade de exemplares (op. B)?
4. Multa/penalidade por atraso entra no escopo, ou fica de fora (só marca
   "atrasado" visualmente, sem consequência)?
5. Quem fica responsável por cada card, igual foi feito nas entregas
   anteriores?

## Se aprovado, o que muda em outros documentos

- `README.md`: parágrafo de abertura ("rede social de livros...") vira
  descrição de sistema de biblioteca.
- `docs/ENTREGAS.md`: tabela de cronograma com as novas funcionalidades.
- `docs/BANCO-DE-DADOS.md`: hoje já descreve um modelo (`works`, `reviews`,
  `comments`, `favorites`...) que nunca chegou a ser implementado como está
  documentado — o código real ficou mais simples (`books`, sem `works`, sem
  `type`). Esse documento precisa de uma revisão separada, maior que esta
  proposta, e fica pra depois da decisão do grupo.
- Board do Trello: mover/renomear os cards R002-R004 — feito manualmente por
  quem tiver acesso, não é algo que o Claude Code mexe.
