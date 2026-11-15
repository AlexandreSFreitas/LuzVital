# Backend — Domain Driven Design - Java

API REST da LuzVital: Java 21, Spring Boot 4.1.2, Maven Wrapper e Oracle, com **JDBC puro** (sem JPA).

## Camadas (`src/main/java/br/com/luzvital`)

| Pacote | O que tem |
|---|---|
| `model` | Uma classe por tabela do `database/ddl.sql` (Regiao, Paciente, Equipamento, PacienteEquipamento, PacienteContato, Interrupcao, Alerta) e enums dos `CHECK` |
| `dao` | SQL escrito à mão com `PreparedStatement`. `SqlErrorTranslator` converte códigos ORA em exceções de domínio |
| `bo` | Regras de negócio e validações. `RegraPrioridade` e `GeradorAlertas` implementam a seção 4 do `docs/DATABASE_MODEL.md` |
| `controller` | Endpoints REST em `/api` |
| `exception` | Exceções de domínio e `GlobalExceptionHandler` (formato `{status, erro, timestamp}`) |
| `dto` | Respostas que não são uma tabela (resultado do registro de interrupção) |
| `config` | `ConnectionFactory`: entrega conexões do pool (HikariCP), montado a partir das variáveis de ambiente |

## O que já funciona

| Recurso | Operações |
|---|---|
| `/api/regioes` | GET (lista e `/{id}`), POST, PUT `/{id}`, DELETE `/{id}` |
| `/api/pacientes` | GET (lista e `/{id}`), POST, PUT `/{id}`, DELETE `/{id}` |
| `/api/interrupcoes` | GET (lista e `/{id}`), POST (registra a interrupção **e gera os alertas**) |

Ainda não feitos: CRUD de equipamentos, contatos e vínculos; encerrar interrupção (PUT); `/api/alertas` (listar e confirmar).

### Registro de interrupção e alertas

`POST /api/interrupcoes` com `{"idRegiao": 1, "duracaoEstimadaMin": 120}` (opcionais: `dataInicio`, `origem`; padrão: agora e `SIMULADA`).

1. Busca os pacientes **ativos** da região, os equipamentos e os contatos deles.
2. Calcula a prioridade de cada paciente: **1** se algum equipamento de suporte de vida tiver autonomia menor que a duração (ou duração desconhecida); **2** se algum equipamento qualquer estiver nessa situação; **3** nos demais casos. É uma regra acadêmica para ordenar avisos, não um índice clínico.
3. Cria um alerta `PENDENTE` para cada contato de cada paciente.
4. Grava a interrupção e os alertas numa **única transação** (commit ou rollback de tudo).

A resposta (201) traz a interrupção, `pacientesAfetados`, `alertasGerados`, `alertasPorPrioridade`, os alertas e `pacientesSemContato` (pacientes que não têm a quem avisar). Pacientes e contatos aparecem só pelo ID.

### Decisões

- **DELETE de paciente** é exclusão física. Se ele tiver contatos ou alertas, o banco bloqueia e a API devolve **409**; nesse caso, use `PUT` com `"ativo": false`.
- **Fuso horário:** as regras de data usam `America/Sao_Paulo`, porque o render.com roda em UTC.
- Erros de banco nunca expõem o SQL nem a mensagem do Oracle; o detalhe fica só no log do servidor.

## Como rodar

Pré-requisito: JDK 21 (`JAVA_HOME`). Não precisa de Maven instalado.

1. Defina as variáveis de ambiente no **seu terminal** (valores no `env.example` da raiz; nunca versionar):
   - `DB_URL` (ex.: `jdbc:oracle:thin:@//<host-da-fiap>:1521/<servico>`), `DB_USERNAME`, `DB_PASSWORD`
   - opcionais: `SPRING_PROFILES_ACTIVE` (`dev` ou `prod`, padrão `dev`) e `PORT` (padrão 8080)
2. Rode:

```bash
cd backend
./mvnw spring-boot:run        # Windows: mvnw.cmd spring-boot:run
```

## Como validar

```bash
cd backend
./mvnw test                   # Windows: mvnw.cmd test
```

Os testes **não usam banco**: DAOs falsos em memória e MockMvc. Cobrem a regra de prioridade, o gerador de alertas, as validações das BOs, a tradução de erros ORA e as respostas HTTP.

### Roteiro manual contra o Oracle da FIAP

Com a API rodando e o `dml.sql` carregado:

```bash
curl http://localhost:8080/api/regioes
curl -X POST http://localhost:8080/api/regioes -H "Content-Type: application/json" -d '{"nome":"Bairro Teste","cidade":"São Paulo","uf":"SP"}'
curl -X POST http://localhost:8080/api/pacientes -H "Content-Type: application/json" -d '{"nome":"Paciente Fictício","dataNascimento":"1950-03-10","logradouro":"Rua Exemplo","numero":"10","cep":"04101-000","idRegiao":1}'
curl -X POST http://localhost:8080/api/interrupcoes -H "Content-Type: application/json" -d '{"idRegiao":1,"duracaoEstimadaMin":120}'
```

Confira no SQL Developer que os alertas da nova interrupção foram gravados (`SELECT * FROM alerta WHERE id_interrupcao = <id>`). Repetir o POST de região deve dar 409, e o DELETE de um paciente com contatos também.

**Conferido no Oracle da FIAP em 15/11/2026:** `GET /api/regioes`, `POST /api/regioes` (201), `POST /api/pacientes` (201, CEP normalizado e `dataCadastro` do banco) e `POST /api/interrupcoes` na região 1 (1 paciente afetado, 2 alertas de prioridade 1 gravados na mesma transação).

### Problemas comuns

- **500 com `jdbcUrl, ${DB_URL}` no log:** as variáveis não chegaram à API. No Git Bash use `export DB_URL="..."` (sem espaços em volta do `=`) e suba a API **no mesmo terminal**, depois de definir as variáveis.
- **400 "Corpo da requisição inválido" com acentos no `curl`:** o terminal do Windows não envia os acentos em UTF-8. Teste sem acento ou use Postman/Insomnia.
- Os testes manuais gravam de verdade no banco. Para voltar ao estado do `dml.sql`, rode `ddl.sql` e `dml.sql` de novo.
