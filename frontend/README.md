# Frontend — Next.js

Interface web em Next.js (App Router) com TypeScript, consumindo a API do backend (Flask).

Este projeto foi criado com [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

**Importante:** use sempre `pnpm` neste projeto (não misture com `npm`/`yarn`), para evitar lockfiles conflitantes.

## Status

- [x] Projeto Next.js gerado
- [x] Tela de login — integrada ao `POST /api/auth/login` real
- [x] Home (`/`) — catálogo de livros consumindo `GET /api/books`
- [x] Cadastro, edição e exclusão de livro (`/livros/novo` + ações na home), admin-only
- [x] Gerenciamento de usuários pelo admin (`/admin/usuarios`) — listar, adicionar, editar, ativar/desativar, excluir, todos ligados à API real
- [x] Cliente HTTP apontando para a API (`src/lib/api/`) — nada mais usa dados mockados
- [x] Proteção de rotas por `role` no client (`RequireAdmin`) — ver limitação abaixo

## Getting Started

Rode o servidor de desenvolvimento:

```bash
pnpm dev
```

Abra [http://localhost:3000](http://localhost:3000) no navegador para ver o resultado.

Este projeto usa [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) para otimizar e carregar automaticamente a fonte Inter, e um ícone customizado (`src/app/icon.svg`) como favicon da aba.

## Organização das pastas

```
src/
├── app/
│   ├── (auth)/                    # rotas sem header (usuário ainda não autenticado)
│   │   └── login/
│   │       └── page.tsx            # tela de login
│   ├── (main)/                     # rotas com header + navegação
│   │   ├── layout.tsx                # aplica o Header em todas as páginas abaixo
│   │   ├── page.tsx                   # home — catálogo de livros (GET /api/books)
│   │   ├── estante/
│   │   │   └── page.tsx                # redireciona pra "/" (Nav ainda linka aqui)
│   │   ├── admin/
│   │   │   └── usuarios/
│   │   │       └── page.tsx            # gerenciamento de usuários (admin cadastra, não há auto-cadastro)
│   │   ├── livros/
│   │   │   ├── novo/                   # R001 — cadastro de livro (admin-only)
│   │   │   └── [id]/                   # R002/R003 — comentário e nota (ainda nao existe)
│   │   └── favoritos/                  # R004 (ainda nao existe)
│   ├── layout.tsx                       # layout raiz (fonte, <html>/<body>)
│   └── icon.svg                          # favicon
│
├── components/
│   ├── ui/
│   │   └── Table.tsx                # Table, TableHead, TableBody, TableRow, TableHeaderCell, TableCell — genéricos
│   ├── auth/
│   │   └── RequireAdmin.tsx          # bloqueia pagina pra quem nao e admin (ver limitacao abaixo)
│   ├── layout/
│   │   ├── Header.tsx                # logo + Nav + UserBadge (ou link de login, se ninguem logado)
│   │   ├── Nav.tsx                   # links de navegação
│   │   └── UserBadge.tsx             # nome, cargo, avatar e "Sair" do usuário logado
│   └── features/
│       ├── auth/
│       │   └── LoginForm.tsx         # formulário de login
│       ├── book/
│       │   ├── BookForm.tsx          # formulário de cadastro (POST /api/books)
│       │   ├── BookGrid.tsx          # grade de livros + acoes de editar/excluir (admin)
│       │   ├── EditBookModal.tsx     # popup de edição (PUT /api/books/:id)
│       │   └── DeleteBookModal.tsx   # popup de confirmação de exclusão (DELETE /api/books/:id)
│       └── user/
│           ├── UsersToolbar.tsx      # busca (filtra de verdade) + botão "Adicionar Usuário"
│           ├── UserTable.tsx         # tabela de usuários (usa components/ui/Table)
│           ├── AddUserModal.tsx      # popup de cadastro (POST /api/users)
│           ├── EditUserModal.tsx     # popup de edição (PUT /api/users/:id)
│           └── DeleteUserModal.tsx   # popup de confirmação de exclusão (DELETE /api/users/:id)
│
├── lib/
│   ├── api/
│   │   ├── auth.ts                  # login
│   │   ├── books.ts                 # listar/criar/editar/apagar livro
│   │   └── users.ts                 # listar/criar/editar/apagar usuário (admin)
│   ├── auth.ts                      # getCurrentUser()/clearSession() — le o localStorage
│   └── utils/
│
└── types/
    ├── book.ts                       # Book, BookInput (espelha backend/app/schemas/book_schema.py)
    └── user.ts                       # User: id, username, email, displayName?, avatarUrl?, role, isActive
```

### Convenções

- `app/` só cuida de roteamento — a UI em si vive em `components/features/`.
- `components/features/` é dividido por domínio (`auth`, `book`, `user`) para reduzir conflito de merge entre quem está trabalhando em partes diferentes do frontend.
- `components/ui/` guarda componentes genéricos, sem lógica de negócio (ex.: `Table.tsx` não sabe o que é um "usuário", só sabe desenhar linhas e colunas).
- Toda chamada à API passa por `src/lib/api/` — cada arquivo espelha um blueprint do backend Flask (`blueprints/users` ↔ `lib/api/users.ts`). Assim, quando a URL base mudar ou for preciso enviar autenticação, muda em um lugar só.
- `(auth)` é para rotas **sem** o usuário autenticado (login); `(main)` é para rotas **com** o Header.
- Não existe cadastro público de usuário — **o admin cadastra os usuários** pelo painel em `/admin/usuarios`.
- Livros e usuários de `/livros/novo` e `/admin/usuarios` são protegidos pelo `RequireAdmin` — mas é uma proteção **só de client**: o login aqui é token em `localStorage`, sem cookie de sessão, então o middleware do Next (que roda no servidor) não tem como ler isso antes de mandar o HTML. A segurança de fato está no backend (`@admin_required` em toda rota de escrita); o guard do frontend é só pra não deixar a tela de alguém sem permissão aberta por engano.
- Upload de avatar (nos modais de usuário) é só preview local (`blob:` do navegador) — não existe endpoint de upload de arquivo no backend ainda, então isso não é enviado pra API.

## Learn More

Para aprender mais sobre Next.js, veja:

- [Next.js Documentation](https://nextjs.org/docs) — recursos e API do Next.js.
- [Learn Next.js](https://nextjs.org/learn) — tutorial interativo.

O [repositório do Next.js no GitHub](https://github.com/vercel/next.js) está aberto a feedback e contribuições.

## Deploy on Vercel

A forma mais simples de fazer deploy de um app Next.js é usando a [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme), dos criadores do Next.js.

Veja nossa [documentação de deploy do Next.js](https://nextjs.org/docs/app/building-your-application/deploying) para mais detalhes.