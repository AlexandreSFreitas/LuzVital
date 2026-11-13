# Segurança e privacidade — LuzVital

A LuzVital lida com **dados de saúde**, que a LGPD trata como dados pessoais sensíveis. Mesmo usando só dados simulados, o projeto deve ser desenhado como se fossem reais.

## Regras do repositório

1. **Nenhum dado pessoal real.** Nomes, telefones, endereços e condições de saúde são fictícios ou públicos, com a fonte indicada.
2. **Nenhum segredo no Git.** `.env`, wallets Oracle, chaves e tokens estão no `.gitignore` e bloqueados para leitura pelo Claude Code (`.claude/settings.json`).
3. Credenciais só por variáveis de ambiente (veja `env.example`). No render.com, use as variáveis do painel.
4. Usuário de banco com o mínimo de privilégios necessários.

## Regras da aplicação

- Validar todas as entradas (Bean Validation no backend).
- Não retornar dados de saúde em listagens que não precisam deles.
- Mensagens de erro sem stack trace nem SQL para o cliente.
- Registrar quem confirmou cada alerta e quando (rastreabilidade).
- Rede: Wi-Fi do cidadão isolado da VLAN Equipe por ACL; administração só por SSH.

## Revisão

Use a Skill `luzvital-security` antes de concluir qualquer mudança em autenticação, dados de pacientes, configuração ou deploy.
