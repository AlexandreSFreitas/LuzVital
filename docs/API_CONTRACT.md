# Contrato da API — LuzVital (rascunho)

**Status:** rascunho. Vai para a documentação de DDD como "tabela de endpoints".

Base: `/api`

| Recurso | GET | POST | PUT | DELETE | Implementado |
|---|---|---|---|---|---|
| `/regioes` | listar / `/{id}` | criar | `/{id}` atualizar | `/{id}` remover | ✅ tudo |
| `/pacientes` | listar / `/{id}` | criar | `/{id}` atualizar | `/{id}` remover | ✅ tudo |
| `/pacientes/{id}/equipamentos` | listar | criar | `/equipamentos/{id}` | `/equipamentos/{id}` | — |
| `/equipamentos` (catálogo) | listar / `/{id}` | criar | `/{id}` | `/{id}` | — |
| `/contatos` | listar / `/{id}` | criar | `/{id}` | `/{id}` | — |
| `/interrupcoes` | listar / `/{id}` | registrar (gera alertas) | `/{id}` (encerrar) | `/{id}` | ✅ GET e POST |
| `/alertas` | listar / `/{id}` | — | `/{id}/confirmar` | — | — |

## Exemplos

`POST /api/pacientes`

```json
{
  "nome": "Paciente Fictício",
  "dataNascimento": "1950-03-10",
  "logradouro": "Rua Exemplo",
  "numero": "10",
  "complemento": null,
  "cep": "04101-000",
  "idRegiao": 1,
  "observacaoAtendimento": "acesso por escada",
  "ativo": true
}
```

- `cep` aceita com ou sem hífen e é gravado só com os 8 dígitos.
- `ativo` é opcional: no POST vale `true`; no PUT, se omitido, mantém o valor atual.
- `idPaciente` e `dataCadastro` são gerados pelo banco.

`POST /api/interrupcoes`: corpo `{ "idRegiao": 1, "duracaoEstimadaMin": 120 }` (opcionais: `dataInicio`, `origem` = `SIMULADA` | `MANUAL` | `DISPOSITIVO`). A interrupção é sempre criada `ABERTA`. Resposta 201:

```json
{
  "interrupcao": { "idInterrupcao": 6, "idRegiao": 1, "dataInicio": "2026-11-14T12:00:00", "dataFim": null,
                   "duracaoEstimadaMin": 120, "origem": "SIMULADA", "status": "ABERTA" },
  "pacientesAfetados": 2,
  "alertasGerados": 3,
  "alertasPorPrioridade": { "1": 2, "2": 0, "3": 1 },
  "pacientesSemContato": [],
  "alertas": [ { "idAlerta": 21, "idInterrupcao": 6, "idPaciente": 1, "idContato": 1, "prioridade": 1,
                 "status": "PENDENTE", "dataCriacao": "2026-11-14T12:00:01", "dataConfirmacao": null } ]
}
```

## Convenções

- JSON em `camelCase`.
- Erros no formato `{ "status": 404, "erro": "Paciente não encontrado", "timestamp": "..." }`.
- Códigos: 200, 201 (com `Location`), 204, 400 (validação ou JSON inválido), 404, 409 (duplicidade ou registro com vínculos), 500.
- Respostas nunca expõem dados além do necessário (ver `SECURITY_AND_PRIVACY.md`). No registro de interrupção, pacientes e contatos aparecem só pelo ID.
