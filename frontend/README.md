# Frontend — Next.js

Interface web em Next.js (App Router) com TypeScript, consumindo a API do backend.

## Status

Ainda não iniciado. Só a estrutura de pastas existe.

- [ ] Projeto Next.js gerado
- [ ] Cliente HTTP apontando para a API
- [ ] Primeiras telas

## Como gerar o projeto

De dentro de `frontend/`, com Node 20 ou mais recente:

```bash
pnpm create next-app@latest . --ts --app --tailwind --eslint --src-dir --import-alias "@/*"
```

O gerador roda normalmente numa pasta que contenha apenas `README.md` e os `.gitkeep`.

Depois de gerado:

```bash
pnpm install
pnpm dev          # http://localhost:3000
```

## Organização das pastas

```
src/
├── app/          rotas do App Router (cada pasta vira uma URL)
├── components/   componentes reutilizáveis de interface
├── lib/          cliente HTTP e funções utilitárias
└── types/        tipos TypeScript espelhando o que a API devolve
```

Toda chamada à API deve passar por um único módulo em `src/lib/` — assim, quando mudar a URL base ou for preciso enviar autenticação, muda em um lugar só.
