# API de avaliações (Reviews)

Todas as rotas ficam sob `/api`. POST, PUT e DELETE exigem token JWT; GET da lista é público.

## `POST /api/books/<book_id>/reviews`

Cria avaliação para o livro, usando o usuário autenticado como autor. O usuário pode criar **uma única avaliação por livro**. A restrição também é garantida pelo `UNIQUE(user_id, book_id)` que já existe no model `Review`.

Exemplo de body:

```json
{
  "body": "A história é envolvente e os personagens são bem construídos.",
  "rating": 4.5,
  "hasSpoilers": false,
  "consumedOn": "2026-10-12"
}
```

`body` e `rating` são opcionais individualmente, mas pelo menos um precisa ser informado. `rating` deve estar entre `0.5` e `5.0`, em incrementos de `0.5`. `body` aceita até 5000 caracteres. `hasSpoilers` é falso por padrão e `consumedOn` aceita uma data ISO `YYYY-MM-DD` ou `null`.

Respostas: `201` criada, `400` body inválido, `401` sem token, `404` livro inexistente, `409` já existe avaliação desse usuário para o livro.

## `GET /api/books/<book_id>/reviews`

Lista as avaliações públicas do livro, ordenadas da mais recente para a mais antiga. Retorna `404` quando o livro não existe.

## `PUT /api/reviews/<review_id>`

Atualiza um ou mais campos da avaliação do próprio usuário. Campos aceitos: `body`, `rating`, `hasSpoilers`, `consumedOn`. Não é possível mudar o livro nem o autor da avaliação.

Exemplo:

```json
{
  "body": "Revendo minha opinião depois de reler.",
  "rating": 5.0
}
```

Respostas: `200` atualizada, `400` body inválido ou avaliação sem texto e sem nota após alteração, `401` sem token, `403` avaliação de outro usuário, `404` avaliação inexistente.

## `DELETE /api/reviews/<review_id>`

Exclui a avaliação do usuário autenticado. Responde `204` sem body em caso de sucesso, `401` sem token, `403` se a avaliação pertencer a outro usuário e `404` se não existir.

## Testes de schema

Na pasta `backend`, com as dependências instaladas:

```bash
python -m pytest tests/test_review_schema.py -q
```

Os testes de schema não acessam o banco de dados.
