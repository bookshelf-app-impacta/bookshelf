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
- **Cadastro self-service no backend** (`POST /api/auth/register`) — já é
  exatamente o fluxo "aluno se cadastra sozinho" que R002 propõe, mas sem
  tela no frontend ainda. Ver detalhe abaixo.
- **CRUD de usuário pelo admin** (`/api/users`, tela `/admin/usuarios`) —
  continua existindo pra gerenciar aluno depois de cadastrado (editar,
  desativar, excluir).

## Cronograma proposto

| Entrega | Data | Cartão | Funcionalidade proposta | Custo |
|---|---|---|---|---|
| AC2 | 13/10 | R002 | Cadastro de alunos | Baixo — backend (`/api/auth/register`) já existe; falta tela nova no frontend + campo de RA |
| AC3 | 08/11 | R003 | Empréstimo de livro | Médio — tabela e endpoints novos |
| Final | 22/11 | R004 | Devolução de livro + histórico de empréstimos | Baixo — fecha o ciclo do R003, sem tabela nova |

Comparado ao cronograma atual (R002 comentários, R003 notas, R004 favoritos):
mesmo número de entregas, mesma cadência. O que muda é o domínio.

## R002 — Cadastro de alunos

**Self-service, não pelo admin.** Já existe `POST /api/auth/register`
(`backend/app/blueprints/auth.py`), público, sem exigir login nem admin —
qualquer um se cadastra sozinho e já nasce com `role = user`. É exatamente o
fluxo "aluno se cadastra".

**Mas só existe no backend.** O frontend hoje não tem tela de cadastro
nenhuma — só `/login` (`frontend/src/app/(auth)/login/`), sem link "criar
conta", sem `register()` em `lib/api/auth.ts`. Testado (`curl`), o endpoint
funciona; ninguém consegue usá-lo pela interface. Então R002, na prática, é:

- **Adicionar `registration_number`** (RA/matrícula) em `users`: coluna nova
  (`VARCHAR`, `UNIQUE`, nullable — admin criado por `flask seed` não tem
  RA), migration pequena. Entra em `validate_register`
  (`backend/app/schemas/auth.py`) como campo obrigatório só nesse formulário
  — login continua só com e-mail/senha.
- **Tabela nova `colleges`** (faculdade): `id`, `name`, `slug` — mesmo padrão
  de `authors`/`genres`. O aluno escolhe uma no cadastro (`college_id` em
  `users`, FK, nullable — usuários existentes/admin não têm). `flask seed`
  cria uma linha inicial: **"Faculdade Impacta"**. Se o grupo quiser cadastrar
  outra faculdade depois, é só adicionar outra linha (via seed ou, se
  precisar, um `POST /api/colleges/` admin-only — não obrigatório pra R002,
  dá pra deixar só leitura por enquanto e crescer depois).
- **`GET /api/colleges/`** — público (a tela de cadastro é pública, roda
  antes de existir login), lista as faculdades pra popular o dropdown. Com
  só "Faculdade Impacta" cadastrada, o dropdown nasce com essa opção
  pré-selecionada; se um dia tiver mais de uma, o aluno escolhe livremente.
- **Criar a tela `/cadastro` no frontend** — não existe, é página nova
  (mesmo padrão de `livros/novo`: form + `lib/api/auth.ts` ganha
  `register()`), com o dropdown de faculdade carregado desse endpoint, e um
  link "Criar conta" na tela de login.
- O painel admin (`/api/users`, tela `/admin/usuarios`) continua existindo
  pra listar/editar/desativar aluno depois de cadastrado — só a **criação**
  deixa de ser feita por lá.
- Sem verificação do RA contra uma lista de matrículas válidas da escola
  (não tem essa base pra consultar). Aceita qualquer valor informado,
  único no banco — suficiente pro escopo da disciplina.
- Endpoints e tabelas continuam em inglês (`/api/auth/register`,
  `/api/colleges/`, tabela `colleges`, coluna `registration_number` em
  `users`) — não muda nada nesse quesito.

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

### Frontend

Só admin acessa (mesmo guard `RequireAdmin` que já protege `/livros/novo`):

- **Tela `/admin/emprestimos`** (nova) — lista os empréstimos (reaproveita o
  `GET /api/loans/` com os filtros de status), com badge visual pro status
  (emprestado / atrasado / devolvido — cor diferente, ex. atrasado em
  vermelho).
- **Botão "Emprestar" no card do livro** (`BookGrid.tsx`) — só aparece pra
  admin e só em livro disponível (o próprio `GET /api/books/` já teria que
  informar se tem empréstimo aberto, ou o front checa contra a lista de
  `loans` ativos). Abre um modal (mesmo padrão de `EditBookModal.tsx`) pra
  escolher o aluno (dropdown, carregado de `GET /api/users/`) e o prazo
  (`due_date`).
- Client novo `lib/api/loans.ts` (mesmo padrão de `lib/api/books.ts`):
  `listLoans`, `createLoan`.

## R004 — Devolução de livro + histórico

Não precisa de tabela nova, só fecha o ciclo do `loans`:

| Rota | Quem pode | O que faz |
|---|---|---|
| `PUT /api/loans/<id>/return` | admin | Marca `returned_at = agora` |
| `GET /api/loans/?user_id=<id>` | admin | Histórico de empréstimos de um aluno (já coberto pelo `GET /api/loans/` do R003, com filtro) |

Não precisa de tela nova — usa a mesma `/admin/emprestimos` do R003: cada
linha de empréstimo ativo ganha um botão "Devolver" (mesmo padrão dos ícones
de editar/excluir que já existem em `BookGrid.tsx`), que chama
`returnLoan(id)` (novo, em `lib/api/loans.ts`). O filtro de status na mesma
tela já cobre o "histórico" (trocar pra `?status=returned` ou por aluno).

## Perguntas em aberto pro grupo

1. Aceita a troca de rumo? (é o principal — o resto é detalhe de como)
2. R002: cadastro do aluno fica self-service (`/api/auth/register` + RA) como
   proposto, ou o grupo prefere manter pelo painel do admin?
3. R002: `colleges` fica só leitura por enquanto (cresce via seed/direto no
   banco), ou já entra um `POST /api/colleges/` admin-only pra cadastrar
   faculdade pela tela?
4. R003: 1 exemplar por livro (op. A) ou quantidade de exemplares (op. B)?
5. Multa/penalidade por atraso entra no escopo, ou fica de fora (só marca
   "atrasado" visualmente, sem consequência)?
6. Quem fica responsável por cada card, igual foi feito nas entregas
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
