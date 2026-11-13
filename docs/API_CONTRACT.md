# Contrato da API — LuzVital (rascunho)

**Status:** rascunho. Vai para a documentação de DDD como "tabela de endpoints".

Base: `/api`

| Recurso | GET | POST | PUT | DELETE |
|---|---|---|---|---|
| `/pacientes` | listar / `/{id}` | criar | `/{id}` atualizar | `/{id}` remover |
| `/pacientes/{id}/equipamentos` | listar | criar | `/equipamentos/{id}` | `/equipamentos/{id}` |
| `/contatos` | listar / `/{id}` | criar | `/{id}` | `/{id}` |
| `/interrupcoes` | listar / `/{id}` | registrar (gera alertas) | `/{id}` (encerrar) | `/{id}` |
| `/alertas` | listar / `/{id}` | — | `/{id}/confirmar` | — |

## Convenções

- JSON em `camelCase`.
- Erros no formato `{ "status": 404, "erro": "Paciente não encontrado", "timestamp": "..." }`.
- Códigos: 200, 201, 204, 400 (validação), 404, 409 (conflito), 500.
- Respostas nunca expõem dados além do necessário (ver `SECURITY_AND_PRIVACY.md`).
