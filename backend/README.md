# Backend — Flask

API REST em Python + Flask, servindo JSON para o frontend.

## Status

Ainda não iniciado. Só a estrutura de pastas existe.

- [ ] `requirements.txt` e instalação do Flask
- [ ] Application factory (`app/__init__.py`)
- [ ] Modelagem do banco e primeira migration
- [ ] Primeiros endpoints

## Ambiente

O combinado do grupo é rodar o Python **localmente** com `venv` — o Docker é usado só para o MySQL.

Recomendado usar Python 3.12 ou mais recente. No macOS:

```bash
brew install python@3.12
```

Depois, de dentro de `backend/`:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

O banco precisa estar de pé (`docker compose up -d` na raiz do repositório).

## Organização das pastas

```
app/
├── blueprints/   rotas HTTP — recebem a requisição e devolvem a resposta
├── services/     regra de negócio — o que a aplicação faz de fato
├── models/       modelos SQLAlchemy — o mapeamento das tabelas
└── schemas/      validação da entrada e serialização da saída
tests/            testes automatizados (pytest)
```

O fluxo de uma requisição é `blueprints` → `services` → `models`. Manter essa separação evita que duas pessoas mexam no mesmo arquivo ao trabalhar em tarefas diferentes.
