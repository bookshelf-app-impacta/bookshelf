# Frontend — Next.js

Interface web em Next.js (App Router) com TypeScript, consumindo a API do backend (Flask).

Este projeto foi criado com [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Status

- [x] Projeto Next.js gerado
- [ ] Cliente HTTP apontando para a API
- [ ] Primeiras telas

## Getting Started

Rode o servidor de desenvolvimento:

```bash
npm run dev
# ou
yarn dev
# ou
pnpm dev
# ou
bun dev
```

Abra [http://localhost:3000](http://localhost:3000) no navegador para ver o resultado.

A página inicial pode ser editada em `src/app/page.tsx`. A página atualiza automaticamente conforme o arquivo é salvo.

Este projeto usa [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) para otimizar e carregar automaticamente a fonte [Geist](https://vercel.com/font).

## Organização das pastas

```
src/
├── app/
│   ├── (auth)/               # rotas sem navbar/sidebar
│   │   ├── login/
│   │   └── cadastro/          # R001 — cadastro de usuário
│   ├── (main)/                # rotas com layout principal
│   │   ├── layout.tsx          # navbar + sidebar
│   │   ├── page.tsx             # home
│   │   ├── livros/
│   │   │   ├── novo/            # R001 — cadastro de livro
│   │   │   └── [id]/            # R002/R003 — comentário e nota
│   │   └── favoritos/           # R004
│   └── layout.tsx               # layout raiz
│
├── components/
│   ├── ui/                     # botão, input, card — genéricos
│   ├── layout/                 # Navbar, Sidebar, Footer
│   └── features/
│       ├── book/                # BookForm, BookCard, RatingStars, CommentForm
│       ├── user/                # LoginForm, RegisterForm
│       └── favorites/           # FavoriteButton, FavoritesList
│
├── lib/
│   ├── api/
│   │   ├── client.ts             # fetch configurado, URL base do Flask
│   │   ├── books.ts              # espelha blueprints/books
│   │   ├── users.ts              # espelha blueprints/users
│   │   └── favorites.ts          # espelha blueprints/favorites
│   └── utils/
│
└── types/
    ├── book.ts
    ├── user.ts
    └── review.ts
```

### Convenções

- `app/` só cuida de roteamento — a UI em si vive em `components/features/`.
- `components/features/` é dividido por domínio (`book`, `user`, `favorites`) para reduzir conflito de merge entre quem está trabalhando em partes diferentes do frontend.
- Toda chamada à API deve passar por `src/lib/api/` — cada arquivo espelha um blueprint do backend Flask (`blueprints/books` ↔ `lib/api/books.ts`, e assim por diante). Assim, quando a URL base mudar ou for preciso enviar autenticação, muda em um lugar só.
- Os nomes das pastas em `app/(main)/` seguem os cartões do board (`livros/novo` → R001, `favoritos` → R004), facilitando saber onde mexer em cada branch.

## Learn More

Para aprender mais sobre Next.js, veja:

- [Next.js Documentation](https://nextjs.org/docs) — recursos e API do Next.js.
- [Learn Next.js](https://nextjs.org/learn) — tutorial interativo.

O [repositório do Next.js no GitHub](https://github.com/vercel/next.js) está aberto a feedback e contribuições.

## Deploy on Vercel

A forma mais simples de fazer deploy de um app Next.js é usando a [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme), dos criadores do Next.js.

Veja nossa [documentação de deploy do Next.js](https://nextjs.org/docs/app/building-your-application/deploying) para mais detalhes.