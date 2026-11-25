# Fluxo de trabalho no Git

A `main` é protegida. Alterações entram por Pull Request.

Antes de abrir um PR:

```bash
git checkout main
git pull
git checkout sua-branch
git rebase main
```

Commits seguem Conventional Commits:

```text
feat:
fix:
test:
refactor:
docs:
chore:
```
