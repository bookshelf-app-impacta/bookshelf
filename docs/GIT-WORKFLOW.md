# Fluxo de trabalho no Git

Somos 7 pessoas no mesmo repositório. Estas regras existem para ninguém sobrescrever o trabalho do outro.

## Regra principal

A branch `main` é protegida. Ninguém dá push direto nela — todo código entra por Pull Request com pelo menos 1 aprovação.

## Branches

Uma branch por cartão do board. O nome começa com o tipo e cita o cartão:

```
feat/R001-cadastro-livros
feat/R002-comentarios
fix/R001-validacao-isbn
docs/atualiza-readme
```

Quem pega um cartão move ele para "Doing" no Trello e abre a branch no mesmo momento. Isso evita duas pessoas trabalhando no mesmo cartão sem saber.

```bash
git checkout main
git pull
git checkout -b feat/R001-cadastro-livros
```

## Commits

Padrão Conventional Commits — o tipo vem antes da descrição, em letra minúscula:

```
feat: adiciona endpoint de cadastro de livro
fix: corrige validação de ISBN duplicado
chore: atualiza dependências
docs: documenta como rodar o backend
test: cobre listagem de livros
refactor: extrai regra de negócio para service
```

Commits pequenos e frequentes. É mais fácil revisar e mais fácil desfazer.

## Pull Request

1. `git push -u origin feat/R001-cadastro-livros`
2. Abrir o PR no GitHub apontando para `main`
3. Preencher o template (cartão, o que foi feito, como testar, print)
4. Pedir revisão de alguém do grupo
5. Depois de aprovado, fazer o merge e apagar a branch

## Antes de abrir o PR

Atualize sua branch com o que já entrou na `main`:

```bash
git checkout main
git pull
git checkout feat/R001-cadastro-livros
git rebase main
```

Se der conflito, resolva localmente — nunca na interface do GitHub.

## Tags de entrega

A cada entrega, quem fizer o merge final cria a tag:

```bash
git checkout main
git pull
git tag -a ac1 -m "Entrega da AC1 - cadastro de livros"
git push origin ac1
```

Tags usadas: `ac1`, `ac2`, `ac3`, `final`.

## O que nunca fazer

- `git push --force` em `main` ou em qualquer branch compartilhada
- Commitar arquivo `.env` (está no `.gitignore`, mas vale a atenção)
- Commitar `node_modules/` ou `.venv/`
- Trabalhar direto na `main`
