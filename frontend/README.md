# Frontend — Next.js

Interface web em Next.js (App Router) com TypeScript, consumindo a API do backend (Flask).

Este projeto foi criado com [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

**Importante:** use sempre `pnpm` neste projeto (não misture com `npm`/`yarn`), para evitar lockfiles conflitantes.

## Status

- [x] Projeto Next.js gerado
- [x] Tela de login
- [x] Gerenciamento de usuários pelo admin (listar, adicionar, editar, ativar/desativar, excluir)
- [ ] Cliente HTTP apontando para a API (ainda usando dados mockados)
- [ ] Autenticação real / proteção de rotas por `role` (a ideia de impedir que um usuário comum acesse páginas que só deveriam ser vistas por admin)

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
│   │   ├── page.tsx                   # home
│   │   ├── admin/
│   │   │   └── usuarios/
│   │   │       └── page.tsx            # gerenciamento de usuários (admin cadastra, não há auto-cadastro)
│   │   ├── livros/
│   │   │   ├── novo/                   # R001 — cadastro de livro
│   │   │   └── [id]/                   # R002/R003 — comentário e nota
│   │   └── favoritos/                  # R004
│   ├── layout.tsx                       # layout raiz (fonte, <html>/<body>)
│   └── icon.svg                          # favicon
│
├── components/
│   ├── ui/
│   │   └── table.tsx                # Table, TableHead, TableBody, TableRow, TableHeaderCell, TableCell — genéricos
│   ├── layout/
│   │   ├── Header.tsx                # logo + Nav + UserBadge
│   │   ├── Nav.tsx                   # links de navegação
│   │   └── UserBadge.tsx             # nome, cargo e avatar do usuário logado
│   └── features/
│       ├── auth/
│       │   └── LoginForm.tsx         # formulário de login
│       └── user/
│           ├── UsersToolbar.tsx      # busca + botão "Adicionar Usuário"
│           ├── UserTable.tsx         # tabela de usuários (usa components/ui/table)
│           ├── AddUserModal.tsx      # popup de cadastro de usuário
│           ├── EditUserModal.tsx     # popup de edição
│           └── DeleteUserModal.tsx   # popup de confirmação de exclusão
│
├── lib/
│   ├── api/
│   │   └── auth.ts                  # chamada de login (ainda não integrada de fato ao backend)
│   └── utils/
│
└── types/
    └── user.ts                       # User: id, username, email, displayName?, avatarUrl?, role, isActive
```

### Convenções

- `app/` só cuida de roteamento — a UI em si vive em `components/features/`.
- `components/features/` é dividido por domínio (`auth`, `user`, e futuramente `book`, `favorites`) para reduzir conflito de merge entre quem está trabalhando em partes diferentes do frontend.
- `components/ui/` guarda componentes genéricos, sem lógica de negócio (ex.: `table.tsx` não sabe o que é um "usuário", só sabe desenhar linhas e colunas).
- Toda chamada à API deve passar por `src/lib/api/` — cada arquivo espelha um blueprint do backend Flask (`blueprints/users` ↔ `lib/api/users.ts`, por exemplo). Assim, quando a URL base mudar ou for preciso enviar autenticação, muda em um lugar só.
- `(auth)` é para rotas **sem** o usuário autenticado (login); `(main)` é para rotas **com** o Header, que exige (futuramente) estar logado.
- Não existe cadastro público de usuário — ficou definido que **o admin cadastra os usuários** pelo painel em `/admin/usuarios`.
- Todos os dados exibidos hoje (usuário do Header, listagem de `/admin/usuarios`) são **mockados**. A integração real com a API do Flask ainda está pendente.

## Learn More

Para aprender mais sobre Next.js, veja:

- [Next.js Documentation](https://nextjs.org/docs) — recursos e API do Next.js.
- [Learn Next.js](https://nextjs.org/learn) — tutorial interativo.

O [repositório do Next.js no GitHub](https://github.com/vercel/next.js) está aberto a feedback e contribuições.

## Deploy on Vercel

A forma mais simples de fazer deploy de um app Next.js é usando a [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme), dos criadores do Next.js.

Veja nossa [documentação de deploy do Next.js](https://nextjs.org/docs/app/building-your-application/deploying) para mais detalhes.