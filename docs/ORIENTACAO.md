# Orientação do projeto

Documento de entrada do Book Shelf. Serve para os 7 integrantes — inclusive quem
não vai mexer no backend. Leia uma vez no começo e volte quando precisar.

Os detalhes de cada assunto estão nos documentos próprios; aqui fica o mapa e o
que foi combinado entre todos.

| Assunto | Documento |
|---|---|
| Datas, cartões e o que enviar em cada entrega | [ENTREGAS.md](ENTREGAS.md) |
| Branch, commit, PR e tags | [GIT-WORKFLOW.md](GIT-WORKFLOW.md) |
| Modelo de dados e migrations | [BANCO-DE-DADOS.md](BANCO-DE-DADOS.md) |
| Como rodar o backend | [../backend/README.md](../backend/README.md) |
| Como rodar o frontend | [../frontend/README.md](../frontend/README.md) |

---

## 1. O que estamos construindo

Uma aplicação onde a pessoa cria conta, vê um catálogo de livros, avalia com nota
e comentário, e monta uma lista de favoritos.

O repositório é um **monorepo**: as três partes vivem juntas.

```
backend/    API em Python + Flask, devolve JSON
frontend/   Interface em Next.js + TypeScript, consome a API
infra/      Configuração do Docker
docs/       Documentação (você está aqui)
```

**Consequência prática do monorepo:** um Pull Request pode tocar backend e
frontend ao mesmo tempo, e todo mundo puxa as mudanças de todo mundo no mesmo
`git pull`. É bom para manter as partes em sincronia, e exige atenção a uma
coisa: quando alguém mexe no banco, todos precisam rodar `flask db upgrade`
depois de puxar. Ver seção 6.

---

## 2. Três decisões que o grupo precisa fechar

Não são detalhes de implementação — mudam o que a AC1 entrega. **Fechar antes de
14/09.**

### 2.1 Quem cadastra livro?

O `README.md` diz que *usuários* cadastram livros. Foi comentado no grupo que
seria *só o administrador*. É a funcionalidade da AC1, então precisa estar
decidido.

O banco suporta as duas: `users` tem a coluna `role` (`user` / `admin`). O que
muda é a rota. Enquanto ninguém decide, o modelo assume **só admin**, que é o
mais restritivo — soltar depois é fácil, apertar depois quebra dados já
cadastrados.

### 2.2 É só livro, ou livro e filme?

O nome do repositório, o README e as quatro entregas falam só de **livro**. Em
conversa apareceu "livros e filmes". Como não custa nada agora, a tabela se chama
`works` e tem uma coluna `type`, hoje sempre `'book'` — se filme entrar depois,
não quebra nada.

Se a decisão for "só livro, para sempre", vale renomear a tabela para `books`
antes da AC1.

### 2.3 "Comentários" da AC2 é o quê?

O cronograma tem AC2 = *avaliação: comentários* e AC3 = *avaliação: notas*. Duas
leituras: **(a)** o comentário é o texto da própria avaliação, ou **(b)** é uma
resposta de outra pessoa à avaliação alheia.

Estamos assumindo **(a)**, porque em (b) a AC2 dependeria de já existir avaliação
— que só chega na AC3 — e a ordem do cronograma não fecharia.

> Se houver dúvida, é pergunta para a live de orientação de sábado. Melhor
> perguntar em agosto do que descobrir em setembro.

---

## 3. Quem faz o quê

Sete pessoas no mesmo repositório dão certo se cada uma tiver uma frente clara.
A separação de pastas do backend (`blueprints` → `services` → `models`) existe
justamente para duas pessoas não editarem o mesmo arquivo.

| # | Frente | Responsabilidade |
|---|---|---|
| 1 | Banco e migrations | Modelo, migrations, seed, documentação do banco |
| 2 | Autenticação | Cadastro, login, sessão/token, hash de senha, permissão de admin |
| 3 | Cadastro de livros | Endpoints de criar, editar, listar e apagar livro |
| 4 | Avaliações | Endpoints de criar, editar e listar avaliação; cálculo da média |
| 5 | Favoritos e busca | Favoritar/desfavoritar, listagem filtrada, paginação |
| 6 | Frontend — telas | Catálogo, página do livro, formulários, login |
| 7 | Frontend — base | Cliente HTTP, tipos TypeScript, layout, navegação |

Não é rígido. Quem terminar cedo pega card livre. O que não pode é duas pessoas
mexendo no mesmo cartão sem combinar — por isso mover o cartão para "Doing" no
Trello é a primeira coisa a fazer.

**O banco é o gargalo do início:** frentes 2, 3 e 4 dependem das tabelas
existirem. Por isso a AC1 concentra `users` e `works`.

---

## 4. Preparando a máquina

Todo mundo faz isso uma vez, inclusive quem só vai mexer no frontend — dá para
rodar a interface sem entender o backend, mas não sem o backend de pé.

```bash
git clone <url-do-repo>
cd bookshelf
docker compose up -d          # sobe o MySQL e o Adminer
```

Depois siga o README da sua parte:

- **Backend:** [`backend/README.md`](../backend/README.md) — venv, dependências,
  `flask db upgrade`, `flask seed`
- **Frontend:** [`frontend/README.md`](../frontend/README.md) — gerar o projeto
  Next.js, `pnpm dev`

**Como saber que deu certo:**

| Endereço | O que é |
|---|---|
| <http://localhost:8080> | Adminer — inspecionar o banco pelo navegador |
| <http://localhost:5000/api/health> | API respondendo |
| <http://localhost:3000> | Interface |

Todo mundo começa com os mesmos dados de teste (`flask seed`): três usuários,
três livros, algumas avaliações. Isso facilita revisar PR e gravar o vídeo da
entrega — a tela do colega fica igual à sua.

---

## 5. O ciclo de trabalho

O caminho de uma tarefa, do começo ao fim:

1. **Pegar um cartão** no Trello e mover para "Doing".
2. **Criar a branch** no mesmo momento, citando o cartão — evita duas pessoas no
   mesmo trabalho. Padrão em [GIT-WORKFLOW.md](GIT-WORKFLOW.md).
3. **Codar**, com commits pequenos e frequentes.
4. **Testar na própria máquina** antes de mostrar para alguém.
5. **Atualizar a branch com a `main`** e resolver conflitos localmente.
6. **Abrir o PR**, preenchendo o template (cartão, o que foi feito, como testar,
   print).
7. **Pedir revisão** de alguém do grupo. Uma aprovação é o mínimo.
8. **Merge**, apagar a branch, mover o cartão para "Done".

A `main` é protegida — ninguém dá push direto nela. Os comandos exatos estão no
GIT-WORKFLOW.

**Sobre revisar PR dos outros:** não é burocracia nem desconfiança. É a única
etapa em que uma segunda pessoa vê o código antes de ele virar problema de todo
mundo. Revisar leva dez minutos; desfazer um merge ruim leva uma tarde. Se você
não entendeu o que o PR faz, isso já é um comentário válido.

---

## 6. Combinados do grupo

Coisas que economizam horas de retrabalho.

**Mexeu no banco, avise.** Quem subir migration nova manda no grupo: *"subi
migration, dá pull e roda `flask db upgrade`"*. Quem só der `git pull` sem rodar
o upgrade vai ver um erro incompreensível e perder tempo procurando bug no lugar
errado.

**Não altere tabela na mão.** Nem pelo Adminer, nem por `ALTER TABLE`. Toda
mudança de estrutura vira migration. Quem mexe direto fica com um banco diferente
do resto do grupo, e o erro aparece na máquina de outra pessoa.

**Frontend e backend acertam o formato antes.** Quem faz a tela e quem faz o
endpoint combinam o JSON — nomes dos campos, o que vem em cada resposta, o que
acontece no erro — antes de qualquer um dos dois começar. Refazer parser porque o
campo mudou de nome é o desperdício mais comum em projeto de grupo.

**Um detalhe que já pega:** um livro pode ter avaliação sem nota (é o caso da
AC2). A média volta vazia, não zero. A tela precisa mostrar "sem notas ainda", e
não "0.0 estrelas".

**Nunca commitar `.env`, `node_modules/` ou `.venv/`.** Estão no `.gitignore`,
mas vale a atenção.

**Perguntar cedo.** Travou mais de uma hora no mesmo erro, manda no grupo. Sete
pessoas, alguém já passou por isso.

---

## 7. Véspera de entrega

Confira antes de gravar o vídeo — a lista completa está em
[ENTREGAS.md](ENTREGAS.md).

- [ ] A funcionalidade está mergeada na `main`
- [ ] Quem clonar do zero consegue rodar (teste numa pasta limpa, sem o seu
      `.env` e sem o seu banco)
- [ ] A tag da entrega foi criada (`ac1`, `ac2`, `ac3`, `final`)
- [ ] Os cartões estão em "Done" no board
- [ ] O vídeo mostra a funcionalidade **funcionando**, não o código
- [ ] **Todos os 7** postaram no Classroom — cada um individualmente, mesmo que
      alguém já tenha enviado

O item de clonar do zero é o que mais pega. O projeto roda na sua máquina porque
você tem arquivos e um banco que os outros não têm. Vale testar uma vez, de
verdade, antes da primeira entrega.

---

## 8. Vocabulário

Para quem está mais no frontend e vai ouvir isso nas conversas do backend:

- **Migration** — script versionado que altera a estrutura do banco. É o
  "commit" do banco de dados.
- **Schema** — o desenho das tabelas, colunas e relacionamentos.
- **Endpoint** — uma URL da API. Ex.: `GET /api/books`.
- **Seed** — dados iniciais de teste.
- **Blueprint** — no Flask, o agrupamento de rotas de um assunto.
- **ORM** — camada que mapeia classe Python para tabela do banco.
- **PR (Pull Request)** — pedido de incorporar sua branch na `main`, com
  revisão.
