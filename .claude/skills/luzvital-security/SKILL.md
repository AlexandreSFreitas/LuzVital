---
name: luzvital-security
description: Use ao revisar segurança e privacidade da LuzVital — autenticação, autorização, controle de acesso, exposição de dados pessoais ou de saúde, credenciais no código ou no Git, validação de entrada, vulnerabilidades e configuração de deploy.
---

# luzvital-security

Revisão de segurança e privacidade. Política do projeto: `docs/SECURITY_AND_PRIVACY.md`.

## Quando usar
- Antes de concluir mudanças em: endpoints, entidades com dados de paciente/contato, configuração (`application*.properties`/`yml`), deploy, scripts SQL com dados.
- Antes de cada commit que toca `backend/`, `database/` ou arquivos de configuração.

## Roteiro de revisão

1. **Segredos**
   - Procure senhas, tokens, URLs com credenciais, strings JDBC com usuário/senha em código, configs, notebooks e histórico do diff.
   - Não abra `.env`, wallets ou chaves para "conferir". Verifique só se estão no `.gitignore` e fora do `git status`.
2. **Dados pessoais e de saúde**
   - Dados de exemplo são fictícios?
   - Respostas da API expõem mais do que a tela precisa?
   - Logs imprimem dados de paciente?
3. **Entrada**
   - Validação (Bean Validation) em todos os DTOs de entrada.
   - SQL sempre parametrizado (`PreparedStatement`/parâmetros nomeados). Nunca concatenação.
4. **Erros**
   - Handler global devolve mensagem genérica; sem stack trace nem SQL para o cliente.
5. **Acesso**
   - Se houver autenticação: quem pode confirmar um alerta? Quem vê dados de saúde? Proponha papéis mínimos (paciente/familiar, cuidador, equipe).
6. **Dependências**
   - Versões atuais das dependências do Spring Boot; nada adicionado sem necessidade.

## Saída
Uma tabela: `Severidade (alta/média/baixa) | Arquivo:linha | Problema | Correção proposta`. Não aplique correções que mudem comportamento sem aprovação.

## Validação
- [ ] `git status` e `git diff --cached` sem arquivos de segredo.
- [ ] Nenhum achado de severidade alta em aberto antes do commit.
